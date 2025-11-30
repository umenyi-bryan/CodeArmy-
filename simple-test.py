#!/usr/bin/env python3
import websocket
import json
import random
import time
import os

def test_connection():
    print("🔍 Testing Hack.Chat Connection...")
    print("=" * 40)
    
    nickname = f"Test_{random.randint(1000,9999)}"
    
    # Test different connection methods
    methods = [
        ("Standard SSL", "wss://hack.chat/chat-ws"),
        ("With Timeout", "wss://hack.chat/chat-ws"),
    ]
    
    for method_name, url in methods:
        print(f"\n🧪 Trying: {method_name}")
        try:
            if "Timeout" in method_name:
                ws = websocket.create_connection(url, timeout=10)
            else:
                ws = websocket.create_connection(url)
            
            # Try to join a channel
            ws.send(json.dumps({"cmd": "join", "channel": "test", "nick": nickname}))
            
            # Wait for response
            response = ws.recv()
            data = json.loads(response)
            
            print(f"✅ SUCCESS: Connected and joined channel")
            print(f"   Response: {data.get('cmd', 'unknown')}")
            
            ws.close()
            return True
            
        except Exception as e:
            print(f"❌ FAILED: {e}")
            continue
    
    print(f"\n💡 Conclusion: Hack.Chat server might be down or having issues.")
    print("   Try: https://hack.chat to check status")
    return False

if __name__ == "__main__":
    test_connection()
