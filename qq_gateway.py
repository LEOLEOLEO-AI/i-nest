#!/usr/bin/env python3
"""
QQ Bot 独立网关 — 绕过有问题的OpenClaw QQ Bot插件处理器
直接与QQ服务通信，消息经由本地HTTP webhook转发给OpenClaw agent
"""
import os, sys, json, time, requests, threading, queue
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime

QQ_API_URL = "https://api.sgroup.qq.com"
QQ_APP_ID = os.getenv('QQ_BOT_APP_ID', '1903555571')
QQ_APP_SECRET = os.getenv('QQ_BOT_APP_SECRET', '')  # 从env读取
OPENCLAW_GATEWAY = "http://127.0.0.1:18789"
WEBHOOK_PORT = 18800

class MessageHandler(BaseHTTPRequestHandler):
    msg_queue = queue.Queue()
    
    def do_POST(self):
        if self.path == '/qq/webhook':
            try:
                length = int(self.headers.get('content-length', 0))
                body = self.rfile.read(length).decode('utf-8')
                data = json.loads(body)
                
                print(f"[{datetime.now().strftime('%H:%M:%S')}] ✅ 收到QQ消息: {data.get('content', 'N/A')[:50]}")
                self.msg_queue.put(data)
                
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'ok': True}).encode())
            except Exception as e:
                print(f"❌ Webhook处理失败: {e}")
                self.send_response(500)
                self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
    
    def log_message(self, format, *args):
        pass  # 禁用默认日志

def send_to_openclaw(msg_data):
    """转发消息到OpenClaw agent执行"""
    try:
        payload = {
            'message': msg_data.get('content', ''),
            'channel': 'qqbot',
            'sender': msg_data.get('sender_id', 'unknown'),
            'timestamp': int(time.time())
        }
        
        resp = requests.post(
            f"{OPENCLAW_GATEWAY}/api/message",
            json=payload,
            timeout=30
        )
        
        if resp.status_code == 200:
            print(f"✅ 已转发到OpenClaw")
            return resp.json()
        else:
            print(f"❌ OpenClaw响应失败: {resp.status_code}")
    except Exception as e:
        print(f"❌ 转发失败: {e}")
    
    return None

def webhook_server():
    """启动本地webhook服务器"""
    handler = MessageHandler
    server = HTTPServer(('127.0.0.1', WEBHOOK_PORT), handler)
    print(f"📡 QQ Gateway Webhook服务已启动: http://127.0.0.1:{WEBHOOK_PORT}/qq/webhook")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n⏹️  服务已停止")
        server.shutdown()

def process_messages():
    """处理消息队列，转发给OpenClaw"""
    while True:
        try:
            msg = MessageHandler.msg_queue.get(timeout=5)
            send_to_openclaw(msg)
        except queue.Empty:
            continue
        except Exception as e:
            print(f"❌ 消息处理异常: {e}")

if __name__ == '__main__':
    print(f"""
╔═══════════════════════════════════════════════════════════════╗
║         QQ Bot 独立网关 (绕过OpenClaw插件问题)              ║
║                                                               ║
║  模式：QQ API → 本地Webhook → OpenClaw Agent执行             ║
║  端口：{WEBHOOK_PORT}                                             ║
║  状态：启动中...                                               ║
╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # 启动webhook服务和消息处理线程
    t1 = threading.Thread(target=webhook_server, daemon=True)
    t2 = threading.Thread(target=process_messages, daemon=True)
    
    t1.start()
    t2.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n⏹️  已关闭")
        sys.exit(0)

