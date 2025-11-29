#!/usr/bin/env python3
import websocket
import json
import random
import threading
import time
import os
import sys

class CodeArmyChat:
    def __init__(self):
        self.nickname = self.generate_nickname()
        self.connected = False
        self.ws = None
        
    def generate_nickname(self):
        military_names = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Hunter', 'Steel', 'Iron', 'Shadow']
        military_units = ['Reaper', 'Strike', 'Fang', 'Claw', 'Blade', 'Sight', 'Watch', 'Guard']
        return f"{random.choice(military_names)}_{random.choice(military_units)}{random.randint(10,99)}"
    
    def display_banner(self):
        os.system('clear')
        print('\033[1;32m')
        print('  ╔══════════════════════════════════════════════╗')
        print('  ║              🎯 CODE ARMY 🎯                 ║')
        print('  ║           Anonymous Terminal Chat           ║')
        print('  ║                                              ║')
        print('  ║    No Setup • No Registration • Pure Fun    ║')
        print('  ╚══════════════════════════════════════════════╝')
        print('\033[0m')
    
    def show_loading(self):
        frames = ['🔫 Loading Weapons', '📡 Establishing Comms', '🎯 Targeting Chat', '🚀 Launching Sequence']
        for frame in frames:
            print(f'\033[1;36m⏳ {frame}...\033[0m', end='\r')
            time.sleep(0.5)
        print('\033[1;32m✅ Battlefield Ready!          \033[0m')
    
    def connect(self):
        try:
            self.ws = websocket.create_connection("wss://hack.chat/chat-ws", timeout=10)
            self.ws.send(json.dumps({"cmd": "join", "channel": "CodeArmy", "nick": self.nickname}))
            self.connected = True
            return True
        except Exception as e:
            print(f'\033[1;31m❌ Connection failed: {e}\033[0m')
            return False
    
    def receive_messages(self):
        while self.connected:
            try:
                message = self.ws.recv()
                data = json.loads(message)
                
                if data["cmd"] == "chat":
                    if data["nick"] == self.nickname:
                        print(f'   \033[1;36mYOU:\033[0m {data["text"]}')
                    else:
                        colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
                        color = colors[hash(data["nick"]) % len(colors)]
                        print(f'\033[1;{color}m🎯 {data["nick"]}:\033[0m {data["text"]}')
                        
                elif data["cmd"] == "onlineAdd":
                    print(f'\033[1;32m📍 {data["nick"]} joined the squad\033[0m')
                    
                elif data["cmd"] == "onlineRemove":
                    print(f'\033[1;31m🏃 {data["nick"]} left the field\033[0m')
                    
            except:
                break
    
    def start_chat(self):
        self.display_banner()
        print(f'🔫 \033[1;36mCALLSIGN:\033[0m {self.nickname}')
        print(f'📡 \033[1;35mCHANNEL:\033[0m #CodeArmy')
        self.show_loading()
        print('─' * 50)
        print('💬 \033[1;32mType your message and press ENTER to chat!\033[0m')
        print('🎮 \033[1;37mCommands: /nick [name], /help, /exit\033[0m')
        print('─' * 50)
        print()
        
        if not self.connect():
            return
        
        print('\033[1;32m✅ Connected to CodeArmy battlefield!\033[0m\n')
        
        # Send welcome message
        welcome_messages = [
            "🚀 Reporting for duty!",
            "💂 New soldier on the field!",
            "🎯 Locked and loaded!",
            "🔫 Ready for action!"
        ]
        self.ws.send(json.dumps({"cmd": "chat", "text": random.choice(welcome_messages)}))
        
        # Start receiver thread
        receiver = threading.Thread(target=self.receive_messages, daemon=True)
        receiver.start()
        
        # Main chat loop
        try:
            while self.connected:
                message = input('\033[1;37m» \033[0m').strip()
                
                if not message:
                    continue
                    
                if message.lower() in ['/exit', '/quit']:
                    break
                    
                elif message.startswith('/nick '):
                    new_nick = message[6:].strip()
                    if new_nick:
                        self.ws.send(json.dumps({"cmd": "changenick", "nick": new_nick}))
                        self.nickname = new_nick
                        print(f'\033[1;33m🆔 Callsign changed to: {self.nickname}\033[0m')
                        
                elif message == '/help':
                    self.show_help()
                    
                else:
                    self.ws.send(json.dumps({"cmd": "chat", "text": message}))
                    
        except KeyboardInterrupt:
            print('\n\033[1;33m🚁 Emergency extraction initiated...\033[0m')
        
        self.connected = False
        if self.ws:
            self.ws.close()
        print('\033[1;32m👋 Mission complete! Until next time, soldier!\033[0m')
    
    def show_help(self):
        print('\033[1;34m')
        print('🎮 CODE ARMY COMMANDS:')
        print('  Just type to chat with the squad')
        print('  /nick [name] - Change your callsign')
        print('  /help - Show this help message')
        print('  /exit - Leave the battlefield')
        print('  Ctrl+C - Emergency exit')
        print('\033[0m')

if __name__ == "__main__":
    chat = CodeArmyChat()
    chat.start_chat()
