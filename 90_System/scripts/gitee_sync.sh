#!/bin/bash
# ============================================================
# Genspark Gitee ????
# ????: https://gitee.com/iBrainNest/i-nest.git
# ???: "??gitee" / "sync gitee"
# ============================================================

set -e

REPO_URL="https://gitee.com/iBrainNest/i-nest.git"
BRANCH="main"
REPO_DIR="$HOME/i-nest-sync"
LOG_FILE="$REPO_DIR/logs/sync.log"
STATE_FILE="$REPO_DIR/.sync_state"

# ??
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

log() {
    local ts=$(date '+%Y-%m-%d %H:%M:%S')
    echo -e "$ts | $1"
    mkdir -p "$(dirname "$LOG_FILE")"
    echo "$ts | $1" >> "$LOG_FILE"
}

# ---- ??? ----
init_repo() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        log "${YELLOW}?????????...${NC}"
        git clone "$REPO_URL" "$REPO_DIR"
        log "${GREEN}??????${NC}"
    fi
    cd "$REPO_DIR"
    git checkout "$BRANCH" 2>/dev/null || true
}

# ---- Step 1: Fetch ----
fetch_remote() {
    log "${CYAN}Step 1/4: ??????...${NC}"
    git fetch origin "$BRANCH" 2>&1
    local behind=$(git rev-list --count HEAD..origin/$BRANCH 2>/dev/null || echo 0)
    echo "$behind"
}

# ---- Step 2: Pull ----
pull_remote() {
    local behind=$1
    if [ "$behind" -gt 0 ]; then
        log "${YELLOW}Step 2/4: ??? $behind ????????...${NC}"
        git pull origin "$BRANCH" --no-rebase 2>&1
        log "${GREEN}???????${NC}"
    else
        log "Step 2/4: ???????????"
    fi
}

# ---- Step 3: Detect & Categorize ----
detect_changes() {
    log "${CYAN}Step 3/4: ??????...${NC}"
    local status=$(git status --porcelain)
    
    if [ -z "$status" ]; then
        log "${GREEN}??????${NC}"
        return 1
    fi
    
    local added=$(echo "$status" | grep -c "^??\|^A" || echo 0)
    local modified=$(echo "$status" | grep -c "^ M\|^M" || echo 0)
    
    echo ""
    echo -e "${CYAN}========== ???? ==========${NC}"
    echo -e "  ??: $added  ??: $modified"
    
    # ???????
    echo ""
    echo -e "${YELLOW}?????:${NC}"
    echo "$status" | while read line; do
        local op="${line:0:2}"
        local file="${line:3}"
        case "$op" in
            "??") echo -e "  ${GREEN}+${NC} $file" ;;
            "A "|"A"*) echo -e "  ${GREEN}+${NC} $file" ;;
            "M "|" M") echo -e "  ${YELLOW}~${NC} $file" ;;
            "D "|" D") echo -e "  ${RED}-${NC} $file" ;;
        esac
    done
    
    return 0
}

# ---- Step 4: Commit & Push ----
commit_and_push() {
    log "${CYAN}Step 4/4: ?????...${NC}"
    git add -A
    
    local commit_msg="sync: genspark - $(date '+%Y-%m-%d %H:%M')"
    git commit -m "$commit_msg" 2>&1 || log "${YELLOW}???????????${NC}"
    
    git push origin "$BRANCH" 2>&1
    
    if [ $? -eq 0 ]; then
        local hash=$(git rev-parse --short HEAD)
        echo ""
        echo -e "${GREEN}========== ???? ==========${NC}"
        echo -e "  ??: Genspark ? Gitee"
        echo -e "  ??: $commit_msg"
        echo -e "  ??: $hash"
        echo "$(date -Iseconds)|$hash" > "$STATE_FILE"
        log "???? | $commit_msg"
    else
        log "${RED}????${NC}"
        return 1
    fi
}

# ---- ??? ----
main() {
    echo ""
    echo -e "${CYAN}========== Genspark ? Gitee ?? ==========${NC}"
    
    init_repo
    local behind=$(fetch_remote)
    pull_remote "$behind"
    
    if detect_changes; then
        commit_and_push
    else
        log "${GREEN}???????????${NC}"
    fi
    
    echo ""
}

main "$@"