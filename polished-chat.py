#!/usr/bin/env python3
import websocket, json, random, threading, time, os, datetime

class PolishedCodeArmy:
    def __init__(self):
        self.nickname = self.generate_nickname()
        self.ws = None
        self.active = True
        
    def generate_nickname(self):
        names = ['Phantom', 'Raven', 'Viper', 'Wolf', 'Ghost', 'Falcon', 'Orion', 'Zenith']
        units = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Wraith']
        return f"{random.choice(names)}_{random.choice(units)}{random.randint(10,99)}"
    
    def show_banner(self):
        os.system('clear')
        print('\033[1;36m')
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')
        print('    ╔══════════════════════════════════════╗')
        print('    ║    A N O N Y M O U S   C H A T      ║')
        print('    ║      T E R M I N A L   S P A C E    ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')
    
    def show_connection_animation(self):
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'📡 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
        print(f'🛰️  \033[1;34mESTABLISHING SECURE CONNECTION\033[0m', end='')
        
        dots = ['', '.', '..', '...']
        for i in range(12):
            print(f'\r🛰️  \033[1;34mESTABLISHING SECURE CONNECTION{dots[i % 4]}\033[0m', end='', flush=True)
            time.sleep(0.2)
        
        print('\r✅ \033[1;32mSECURE CONNECTION ESTABLISHED\033[0m')
        print('─' * 55)
        print('💬 \033[1;32mType to chat • /help for commands • Ctrl+C to exit\033[0m')
        print('─' * 55)
        print()
    
    def get_timestamp(self):
        return datetime.datetime.now().strftime('%H:%M')
    
    def typing_animation(self, duration=2):
        """Show typing indicator"""
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        start_time = time.time()
        while time.time() - start_time < duration:
            for frame in frames:
                if time.time() - start_time >= duration:
                    break
                print(f'\r{frame} \033[1;36mTyping...\033[0m', end='', flush=True)
                time.sleep(0.1)
        print('\r' + ' ' * 30 + '\r', end='', flush=True)
    
    def receive_messages(self):
        while self.active:
            try:
                message = self.ws.recv()
                data = json.loads(message)
                
                timestamp = self.get_timestamp()
                
                if data["cmd"] == "chat":
                    if data["nick"] == self.nickname:
                        print(f'   \033[1;36m[{timestamp}] YOU:\033[0m {data["text"]}')
                    else:
                        colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
                        color = colors[hash(data["nick"]) % len(colors)]
                        print(f'\033[1;{color}m[{timestamp}] 🎯 {data["nick"]}:\033[0m {data["text"]}')
                        
                elif data["cmd"] == "onlineAdd":
                    print(f'🟢 \033[1;32m[{timestamp}] {data["nick"]} joined the network\033[0m')
                    
                elif data["cmd"] == "onlineRemove":
                    print(f'🔴 \033[1;31m[{timestamp}] {data["nick"]} left the network\033[0m')
                    
            except:
                break
    
    def show_help(self):
        help_text = """
\033[1;34m
╔══════════════════════════════╗
║        C O M M A N D S       ║
╚══════════════════════════════╝

💬 Just type to send a message
🆔 /nick [name] - Change your identity
❓ /help - Show this help message  
🚪 /exit - Leave the chat
🕒 Messages show timestamps
⚡ Real-time typing indicators
🔒 100% anonymous & secure

Press Ctrl+C for emergency exit
\033[0m
"""
        print(help_text)
    
    def start_chat(self):
        self.show_banner()
        self.show_connection_animation()
        
        try:
            self.ws = websocket.create_connection("wss://hack.chat/chat-ws", timeout=10)
            self.ws.send(json.dumps({"cmd": "join", "channel": "CodeArmy", "nick": self.nickname}))
            
            print('🟢 \033[1;32mCONNECTED TO GLOBAL CHAT NETWORK\033[0m\n')
            
            # Start message receiver
            receiver = threading.Thread(target=self.receive_messages, daemon=True)
            receiver.start()
            
            # Send welcome message with typing effect
            self.typing_animation(1.5)
            welcome_messages = [
                "🚀 Secure terminal connection active",
                "🔐 Encrypted channel established", 
                "🌐 Connected to global chat network",
                "💫 Anonymous communications online"
            ]
            self.ws.send(json.dumps({"cmd": "chat", "text": random.choice(welcome_messages)}))
            
            # Main chat loop
            while self.active:
                try:
                    message = input('\033[1;37m➤ \033[0m').strip()
                    
                    if not message:
                        continue
                        
                    if message.lower() in ['/exit', '/quit', 'exit', 'quit']:
                        break
                        
                    elif message.startswith('/nick '):
                        new_nick = message[6:].strip()
                        if new_nick:
                            self.typing_animation(1)
                            self.ws.send(json.dumps({"cmd": "changenick", "nick": new_nick}))
                            old_nick = self.nickname
                            self.nickname = new_nick
                            print(f'🆔 \033[1;33mIDENTITY CHANGED: {old_nick} → {self.nickname}\033[0m')
                            
                    elif message == '/help':
                        self.show_help()
                        
                    elif message == '/time':
                        print(f'🕒 \033[1;36mCurrent time: {self.get_timestamp()}\033[0m')
                        
                    elif message == '/users':
                        print('👥 \033[1;33mUser list feature coming soon...\033[0m')
                        
                    else:
                        # Show typing indicator before sending
                        self.typing_animation(0.5)
                        self.ws.send(json.dumps({"cmd": "chat", "text": message}))
                        
                except KeyboardInterrupt:
                    print('\n\n🔴 \033[1;31mINITIATING SAFE DISCONNECT...\033[0m')
                    break
                    
        except Exception as e:
            print(f'❌ \033[1;31mCONNECTION FAILED: {e}\033[0m')
            print('💡 \033[1;33mCheck your internet connection and try again\033[0m')
            return
        
        # Clean shutdown
        self.active = False
        if self.ws:
            self.ws.close()
        print('👋 \033[1;36mSecure connection terminated. Until next time, operative.\033[0m')

if __name__ == "__main__":
    chat = PolishedCodeArmy()
    chat.start_chat()
