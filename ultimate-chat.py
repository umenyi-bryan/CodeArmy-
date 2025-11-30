#!/usr/bin/env python3
import socket
import ssl
import random
import threading
import time
import os
import datetime
import sys

class UltimateChat:
    def __init__(self):
        self.nickname = self.generate_cool_nickname()
        self.connected = False
        self.socket = None
        self.active = True
        self.current_server = ""
        self.message_count = 0
        
    def generate_cool_nickname(self):
        """Generate military-style cool nicknames"""
        first_names = ['Phantom', 'Raven', 'Viper', 'Wolf', 'Ghost', 'Falcon', 'Orion', 'Zenith', 'Nova', 'Blaze']
        last_names = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Wraith', 'Shadow', 'Steel']
        titles = ['Agent', 'Operative', 'Soldier', 'Scout', 'Sniper', 'Ranger', 'Cadet', 'Major', 'Captain', 'Chief']
        
        style = random.choice(['military', 'agent', 'cyber'])
        
        if style == 'military':
            return f"{random.choice(titles)}_{random.choice(first_names)}{random.randint(10,99)}"
        elif style == 'agent':
            return f"{random.choice(first_names)}_{random.choice(last_names)}{random.randint(100,999)}"
        else:  # cyber
            cyber_names = ['Neo', 'Trinity', 'Morpheus', 'Cypher', 'Tank', 'Switch', 'Apoc', 'Mouse']
            cyber_codes = ['01', 'X1', 'Z3R0', '4LPH4', 'B3T4', '0M3G4', 'PR0T0', 'SY5T3M']
            return f"{random.choice(cyber_names)}_{random.choice(cyber_codes)}"
    
    def show_ultimate_banner(self):
        """Show the sleek animated banner"""
        os.system('clear')
        print('\033[1;36m')
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')
        print('    ╔══════════════════════════════════════╗')
        print('    ║    U L T I M A T E   C H A T        ║')
        print('    ║   S L E E K • R E A L - T I M E     ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')
    
    def show_connection_animation(self):
        """Cool connection animation"""
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
        print(f'🛰️  \033[1;34mINITIATING GLOBAL CONNECTION\033[0m', end='')
        
        # Matrix-style loading animation
        frames = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        for i in range(15):
            frame = frames[i % len(frames)]
            status = "SECURING" if i < 5 else "ENCRYPTING" if i < 10 else "CONNECTING"
            print(f'\r🛰️  \033[1;34m{status} {frame}\033[0m', end='', flush=True)
            time.sleep(0.1)
        
        print('\r' + ' ' * 50 + '\r', end='', flush=True)
    
    def get_irc_servers(self):
        """Multiple reliable IRC servers"""
        return [
            {
                'name': 'LiberaChat',
                'host': 'irc.libera.chat',
                'port': 6667,
                'ssl': False,
                'description': 'Open Source Community'
            },
            {
                'name': 'LiberaChat SSL', 
                'host': 'irc.libera.chat',
                'port': 6697,
                'ssl': True,
                'description': 'Encrypted Connection'
            },
            {
                'name': 'OFTC',
                'host': 'irc.oftc.net', 
                'port': 6667,
                'ssl': False,
                'description': 'Free Software Network'
            },
            {
                'name': 'IRCNet',
                'host': 'open.ircnet.net',
                'port': 6667, 
                'ssl': False,
                'description': 'Oldest IRC Network'
            }
        ]
    
    def connect_to_server(self, server_info):
        """Connect to IRC server with robust error handling"""
        try:
            print(f'🔗 \033[1;33m{server_info["name"]}\033[0m - {server_info["description"]}')
            
            if server_info['ssl']:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket = context.wrap_socket(sock, server_hostname=server_info['host'])
            else:
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            self.socket.settimeout(10)
            self.socket.connect((server_info['host'], server_info['port']))
            
            # Send registration
            self.send_irc_command(f"NICK {self.nickname}")
            self.send_irc_command(f"USER {self.nickname} 0 * :Ultimate Chat User")
            
            # Wait for welcome
            start_time = time.time()
            while time.time() - start_time < 10:
                response = self.receive_irc_message(2)
                if response and ('001' in response or 'Welcome' in response):
                    self.connected = True
                    self.current_server = server_info['name']
                    return True
                elif response and 'PING' in response:
                    self.handle_ping(response)
            
            return False
            
        except Exception as e:
            if self.socket:
                self.socket.close()
                self.socket = None
            return False
    
    def send_irc_command(self, command):
        """Send command to IRC server"""
        if self.socket:
            self.socket.send(f"{command}\r\n".encode('utf-8'))
    
    def receive_irc_message(self, timeout=2):
        """Receive message with timeout"""
        if self.socket:
            self.socket.settimeout(timeout)
            try:
                return self.socket.recv(4096).decode('utf-8', errors='ignore')
            except:
                return None
        return None
    
    def handle_ping(self, message):
        """Handle PING messages"""
        if 'PING' in message:
            ping_msg = message.split('PING :')[-1].split('\n')[0]
            self.send_irc_command(f"PONG :{ping_msg}")
    
    def join_channel(self, channel="#CodeArmy"):
        """Join the chat channel"""
        if self.connected:
            self.send_irc_command(f"JOIN {channel}")
            time.sleep(1)  # Wait for join to complete
    
    def send_chat_message(self, message, channel="#CodeArmy"):
        """Send message to channel"""
        if self.connected:
            self.send_irc_command(f"PRIVMSG {channel} :{message}")
            return True
        return False
    
    def irc_message_handler(self):
        """Main message handling loop with cool features"""
        buffer = ""
        while self.active and self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                if data:
                    buffer += data
                    lines = buffer.split('\n')
                    buffer = lines[-1]
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        if line:
                            self.handle_irc_message(line)
                            
                # Handle PING in buffer
                if 'PING' in buffer:
                    self.handle_ping(buffer)
                    buffer = ""
                    
            except socket.timeout:
                continue
            except Exception as e:
                if self.active:
                    self.handle_connection_lost()
                break
    
    def handle_irc_message(self, message):
        """Handle incoming IRC messages with cool formatting"""
        # Handle PING immediately
        if message.startswith('PING'):
            self.handle_ping(message)
            return
        
        parts = message.split(' ')
        
        if len(parts) >= 2:
            # PRIVMSG - Chat message
            if parts[1] == 'PRIVMSG':
                channel = parts[2]
                text = ' '.join(parts[3:])[1:]  # Remove leading colon
                sender = parts[0][1:].split('!')[0]
                
                if channel == "#CodeArmy" and text:
                    self.message_count += 1
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if sender == self.nickname:
                        # Your own messages
                        print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {text}')
                    else:
                        # Others' messages with colorful usernames
                        colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
                        color = colors[hash(sender) % len(colors)]
                        
                        # Different icons based on message count
                        icons = ['🎯', '💬', '⚡', '🔥', '🌟', '💫', '🎮', '🚀']
                        icon = icons[self.message_count % len(icons)]
                        
                        print(f'\033[1;{color}m[{timestamp}] {icon} {sender}:\033[0m {text}')
            
            # JOIN - User joined
            elif parts[1] == 'JOIN':
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == "#CodeArmy" and sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🟢 \033[1;32m[{timestamp}] {sender} joined the network\033[0m')
            
            # PART - User left  
            elif parts[1] == 'PART':
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == "#CodeArmy" and sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🔴 \033[1;31m[{timestamp}] {sender} left the network\033[0m')
            
            # QUIT - User disconnected
            elif parts[1] == 'QUIT':
                sender = parts[0][1:].split('!')[0]
                if sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'⚡ \033[1;33m[{timestamp}] {sender} disconnected\033[0m')
    
    def handle_connection_lost(self):
        """Handle lost connection gracefully"""
        print('\n🔌 \033[1;31mConnection to server lost\033[0m')
        self.connected = False
        if self.socket:
            self.socket.close()
            self.socket = None
    
    def try_all_connections(self):
        """Try connecting to all available servers"""
        servers = self.get_irc_servers()
        
        for server in servers:
            if self.connect_to_server(server):
                self.join_channel()
                return True
            time.sleep(1)
        
        return False
    
    def show_ultimate_help(self):
        """Show comprehensive help with cool formatting"""
        help_text = """
\033[1;34m
╔══════════════════════════════╗
║    U L T I M A T E   🚀     ║
║        C O M M A N D S      ║
╚══════════════════════════════╝

\033[1;36m💬 CHAT COMMANDS:\033[0m
  Just type to send messages
  /nick [name] - Change your identity
  /status - Show connection info
  /help - This help message
  /exit - Leave chat

\033[1;35m🎨 COOL FEATURES:\033[0m
  🕒 Timestamps on all messages
  🎯 Colorful user names  
  🔄 Multiple server fallbacks
  🛡️ Auto-reconnection
  🌐 Global real-time chat

\033[1;33m📊 STATUS INDICATORS:\033[0m
  🟢 User joined | 🔴 User left
  ⚡ Disconnected | 🎯 New message

Press \033[1;31mCtrl+C\033[0m to exit safely
\033[0m
"""
        print(help_text)
    
    def show_connection_status(self):
        """Show detailed connection status"""
        if self.connected:
            status = f"🟢 CONNECTED to {self.current_server}"
        else:
            status = "🔴 LOCAL MODE"
        
        print(f'📊 \033[1;36mSTATUS: {status}\033[0m')
        print(f'🎖️  \033[1;36mOPERATIVE: {self.nickname}\033[0m')
        print(f'💬 \033[1;36mMESSAGES: {self.message_count} exchanged\033[0m')
        
        if not self.connected:
            print('💡 \033[1;33mTip: Messages are local until connection is established\033[0m')
    
    def start_ultimate_chat(self):
        """Main chat interface with all cool features"""
        self.show_ultimate_banner()
        self.show_connection_animation()
        
        print('🔄 Establishing secure connection...')
        
        if self.try_all_connections():
            print('✅ \033[1;32mSECURE GLOBAL CONNECTION ESTABLISHED\033[0m')
            print('💬 \033[1;32mType to chat • /help for commands • Real-time active\033[0m')
            print('─' * 60)
            print()
            
            # Start message handler
            handler = threading.Thread(target=self.irc_message_handler, daemon=True)
            handler.start()
            
            # Send welcome message
            welcome_messages = [
                "🚀 Ultimate anonymous chat activated!",
                "🔐 Secure real-time communications online",
                "🌐 Connected to global chat network", 
                "💫 Sleek terminal experience engaged"
            ]
            self.send_chat_message(random.choice(welcome_messages))
            
        else:
            print('❌ \033[1;31mUNABLE TO CONNECT TO CHAT NETWORK\033[0m')
            print('💡 \033[1;33mRunning in local mode - messages will be visible locally\033[0m')
            print('─' * 60)
            print('🔶 \033[1;33mFind friends to join #CodeArmy on any IRC network!\033[0m\n')
        
        # Main input loop with cool features
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
                        if self.connected:
                            self.send_irc_command(f"NICK {new_nick}")
                        old_nick = self.nickname
                        self.nickname = new_nick
                        print(f'🆔 \033[1;33mIDENTITY UPDATED: {old_nick} → {self.nickname}\033[0m')
                        
                elif message == '/help':
                    self.show_ultimate_help()
                    
                elif message == '/status':
                    self.show_connection_status()
                    
                elif message == '/time':
                    current_time = datetime.datetime.now().strftime('%H:%M:%S %Y-%m-%d')
                    print(f'🕒 \033[1;36mCURRENT TIME: {current_time}\033[0m')
                    
                elif message == '/users':
                    print('👥 \033[1;33mUser list feature - tell others to join #CodeArmy!\033[0m')
                    
                else:
                    # Regular message with cool sending effect
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if self.connected:
                        if self.send_chat_message(message):
                            print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;31m[{timestamp}] ❌ FAILED TO SEND:\033[0m {message}')
                    else:
                        print(f'   \033[1;90m[{timestamp}] [LOCAL MODE]:\033[0m {message}')
                        
            except KeyboardInterrupt:
                print('\n\n🔴 \033[1;31mINITIATING SAFE SHUTDOWN SEQUENCE...\033[0m')
                break
        
        # Clean shutdown
        self.active = False
        if self.socket:
            self.socket.close()
        print('👋 \033[1;36mUltimate chat session terminated. Until next time, operative.\033[0m')

if __name__ == "__main__":
    chat = UltimateChat()
    chat.start_ultimate_chat()
