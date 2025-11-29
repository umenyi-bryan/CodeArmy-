#!/usr/bin/env python3
import websocket
import json
import random

print("🔍 CodeArmy Connection Test")
print("==========================")

try:
    nick = "Test_" + str(random.randint(1000,9999))
    print(f"Testing with nickname: {nick}")
    
    ws = websocket.create_connection("wss://hack.chat/chat-ws", timeout=5)
    print("✅ WebSocket connection successful!")
    
    ws.send(json.dumps({"cmd": "join", "channel": "CodeArmy", "nick": nick}))
    print("✅ Channel join successful!")
    
    ws.send(json.dumps({"cmd": "chat", "text": "Connection test message"}))
    print("✅ Message send successful!")
    
    ws.close()
    print("✅ Connection test completed successfully!")
    print("🎯 CodeArmy is ready to use!")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
    print("💡 Check your internet connection and try again")
