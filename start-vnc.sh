#!/bin/bash
# OpenClaw VNC Server — Xvfb + Fluxbox + x11vnc + noVNC
# Deployed to ~/.openclaw/start-vnc.sh by configure script
# Starts automatically at boot; browser (Chromium) is separate and on-demand.
export DISPLAY=:99

# Generate VNC password if not exists
VNC_PASSWD_FILE="$HOME/.openclaw/vnc_password"
if [ ! -f "$VNC_PASSWD_FILE" ]; then
  head -c 16 /dev/urandom | xxd -p | head -c 24 > "$VNC_PASSWD_FILE"
  chmod 600 "$VNC_PASSWD_FILE"
fi
VNC_PASSWORD=$(cat "$VNC_PASSWD_FILE")

# Kill any existing VNC stack (but leave chromium alone)
pkill -f 'Xvfb :99' 2>/dev/null
pkill -f x11vnc 2>/dev/null
pkill -f websockify 2>/dev/null
pkill -f fluxbox 2>/dev/null
sleep 1

# Start virtual display
Xvfb :99 -screen 0 1920x1080x24 -ac &
sleep 2

# Shared Chromium flags (single source of truth)
source "$HOME/.openclaw/chromium-env.sh"

# Fluxbox config: right-click menu + desktop shortcut

mkdir -p ~/.fluxbox ~/Desktop
cat > ~/.fluxbox/menu << MENUEOF
[begin] (Desktop)
  [exec] (Chromium Browser) {$CHROMIUM_CMD}
  [exec] (Terminal) {xterm}
  [restart] (Restart Fluxbox)
[end]
MENUEOF

# Desktop shortcut (rendered by pcmanfm --desktop)
# NOTE: Must use PNG icons, not SVG. The VM image has librsvg2-2 but NOT
# librsvg2-common, so gdk-pixbuf cannot render SVG (no libpixbufloader-svg.so).
# Using SVG paths causes pcmanfm to show a generic fallback icon.
# Icon: prefer google-chrome (apt install), fall back to old Chrome for Testing path.
if [ -f /usr/share/icons/hicolor/48x48/apps/google-chrome.png ]; then
  CHROME_ICON="google-chrome"
else
  CHROME_ICON="/opt/chrome-linux64/product_logo_48.png"
fi
cat > ~/Desktop/chromium.desktop << DESKEOF
[Desktop Entry]
Type=Application
Name=Chromium Browser
Exec=$CHROMIUM_CMD
Icon=$CHROME_ICON
Terminal=false
DESKEOF
chmod +x ~/Desktop/chromium.desktop

cat > ~/Desktop/terminal.desktop << 'TERMEOF'
[Desktop Entry]
Type=Application
Name=Terminal
Exec=xterm -fa "Monospace" -fs 12
Icon=/usr/share/icons/hicolor/48x48/apps/xterm-color.png
Terminal=false
TERMEOF
chmod +x ~/Desktop/terminal.desktop

# Fluxbox apps: auto-maximize chromium windows
cat > ~/.fluxbox/apps << 'APPSEOF'
[app] (name=chrome)
  [Maximized] {yes}
[end]
APPSEOF

# Fluxbox init: show toolbar
cat > ~/.fluxbox/init << 'INITEOF'
session.screen0.toolbar.visible: true
session.screen0.toolbar.placement: BottomCenter
session.screen0.toolbar.widthPercent: 100
session.screen0.toolbar.tools: prevworkspace, workspacename, nextworkspace, iconbar, systemtray, clock
session.screen0.workspaceNames: Desktop
INITEOF

# Override default theme's wallpaper (ubuntu-light sets background.pixmap which
# triggers fbsetbg and shows an xmessage error dialog on failure).
cat > ~/.fluxbox/overlay << 'OVERLAYEOF'
background: none
OVERLAYEOF

# pcmanfm config: skip "execute or open" dialog for .desktop files
mkdir -p ~/.config/libfm ~/.config/pcmanfm/default
cat > ~/.config/libfm/libfm.conf << 'FMEOF'
[config]
quick_exec=1
FMEOF

# pcmanfm desktop wallpaper (use Ubuntu default instead of plain black).
# Wallpaper is set via pcmanfm, NOT Fluxbox's fbsetbg, to avoid xmessage errors.
cat > ~/.config/pcmanfm/default/desktop-items-0.conf << 'WPEOF'
[*]
wallpaper_mode=stretch
wallpaper_common=1
wallpaper=/usr/share/images/fluxbox/ubuntu-light.png
desktop_fg=#ffffff
desktop_shadow=#000000
desktop_font=Sans 12
show_wm_menu=0
show_documents=0
show_trash=1
show_mounts=0
WPEOF

# Fluxbox startup: dark background + pcmanfm desktop icons
# pcmanfm needs the systemd user session dbus address.
cat > ~/.fluxbox/startup << 'STARTUPEOF'
#!/bin/bash
export DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/$(id -u)/bus
xsetroot -solid "#2d2d2d" &
pcmanfm --desktop &
exec fluxbox
STARTUPEOF
chmod +x ~/.fluxbox/startup

# Window manager
DISPLAY=:99 bash ~/.fluxbox/startup &
sleep 1

# VNC server (with password authentication)
x11vnc -display :99 -forever -passwd "$VNC_PASSWORD" -rfbport 5900 -shared -bg -noxdamage

# noVNC websocket proxy (custom UI if available, else system default)
NOVNC_DIR="$HOME/.openclaw/novnc"
if [ ! -d "$NOVNC_DIR" ]; then
  NOVNC_DIR="/usr/share/novnc"
fi
websockify --web="$NOVNC_DIR" 6080 localhost:5900 &

echo "VNC server started (password protected)"

