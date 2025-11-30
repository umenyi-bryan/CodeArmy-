#!/usr/bin/env python3
import socket
import ssl
import random
import threading
import time
import os
import datetime
import sys

class UniversalChat:
    def __init__(self):
        self.nickname = self.generate_nickname()
        self.connected = False
        self.socket = None
        self.active = True
        self.current_server = None
        
    def generate_nickname(self):
        names = ['Phantom', 'Raven', 'Viper', 'Wolf', 'Ghost', 'Falcon', 'Orion']
        units = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard']
        return f"{random.choice(names)}_{random.choice(units)}{random.randint(10,99)}"
    
    def show_banner(self):
        os.system('clear')
        print('\033[1;36m')
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')
        print('    ╔══════════════════════════════════════╗')
        print('    ║    U N I V E R S A L   C H A T      ║')
        print('    ║      A N O N Y M O U S • F R E E    ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')
    
    def get_irc_servers(self):
        """Multiple IRC servers as fallbacks"""
        return [
            # LiberaChat (most popular)
            {
                'name': 'LiberaChat',
                'host': 'irc.libera.chat',
                'port': 6667,
                'ssl': False
            },
            {
                'name': 'LiberaChat SSL',
                'host': 'irc.libera.chat', 
                'port': 6697,
                'ssl': True
            },
            # OFTC (open source community)
            {
                'name': 'OFTC',
                'host': 'irc.oftc.net',
                'port': 6667,
                'ssl': False
            },
            # Freenode legacy
            {
                'name': 'Freenode',
                'host': 'chat.freenode.net',
                'port': 6667,
                'ssl': False
            },
            # HackInt
            {
                'name': 'HackInt',
                'host': 'irc.hackint.org',
                'port': 6697,
                'ssl': True
            },
            # IRCNet (one of the oldest)
            {
                'name': 'IRCNet',
                'host': 'open.ircnet.net',
                'port': 6667,
                'ssl': False
            }
        ]
    
    def connect_to_irc(self, server_info):
        """Connect to IRC server"""
        try:
            print(f'🔗 Connecting to {server_info["name"]}...')
            
            if server_info['ssl']:
                # SSL connection
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket = context.wrap_socket(sock, server_hostname=server_info['host'])
                self.socket.settimeout(10)
                self.socket.connect((server_info['host'], server_info['port']))
            else:
                # Plain text connection
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.settimeout(10)
                self.socket.connect((server_info['host'], server_info['port']))
            
            # Send IRC registration
            self.send_irc_command(f"NICK {self.nickname}")
            self.send_irc_command(f"USER {self.nickname} 0 * :{self.nickname}")
            
            # Wait for connection acknowledgement
            response = self.receive_irc_message(timeout=10)
            if response and ('001' in response or 'Welcome' in response):
                self.connected = True
                self.current_server = server_info
                return True
                
        except Exception as e:
            print(f'❌ Failed: {e}')
            if self.socket:
                self.socket.close()
                self.socket = None
            return False
    
    def send_irc_command(self, command):
        """Send command to IRC server"""
        if self.socket:
            self.socket.send(f"{command}\r\n".encode('utf-8'))
    
    def receive_irc_message(self, timeout=5):
        """Receive message from IRC server"""
        if self.socket:
            self.socket.settimeout(timeout)
            try:
                data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                return data
            except socket.timeout:
                return None
            except Exception:
                return None
        return None
    
    def join_channel(self, channel="#CodeArmy"):
        """Join IRC channel"""
        if self.connected:
            self.send_irc_command(f"JOIN {channel}")
            print(f'📡 Joined channel: {channel}')
    
    def send_message(self, message, channel="#CodeArmy"):
        """Send message to IRC channel"""
        if self.connected:
            self.send_irc_command(f"PRIVMSG {channel} :{message}")
    
    def irc_message_loop(self):
        """Main IRC message receiving loop"""
        buffer = ""
        while self.active and self.connected:
            try:
                data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                if data:
                    buffer += data
                    lines = buffer.split('\n')
                    buffer = lines[-1]  # Keep incomplete line in buffer
                    
                    for line in lines[:-1]:
                        line = line.strip()
                        if line:
                            self.handle_irc_message(line)
                            
                # Send PING response
                if "PING" in buffer:
                    ping_msg = buffer.split('PING :')[-1].split('\n')[0]
                    self.send_irc_command(f"PONG :{ping_msg}")
                    buffer = ""
                    
            except socket.timeout:
                continue
            except Exception as e:
                print(f'📡 Connection error: {e}')
                self.connected = False
                break
    
    def handle_irc_message(self, message):
        """Handle incoming IRC messages"""
        # Parse IRC message format: :prefix COMMAND params :trailing
        parts = message.split(' ')
        
        if len(parts) >= 2:
            # PRIVMSG (chat message)
            if parts[1] == 'PRIVMSG':
                channel = parts[2]
                text = ' '.join(parts[3:])[1:]  # Remove leading colon
                sender = parts[0][1:].split('!')[0]  # Extract nickname
                
                if channel == "#CodeArmy":
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    if sender != self.nickname:
                        colors = ['32', '33', '35', '36', '91', '92', '93', '94']
                        color = colors[hash(sender) % len(colors)]
                        print(f'\033[1;{color}m[{timestamp}] 🎯 {sender}:\033[0m {text}')
            
            # JOIN (user joined)
            elif parts[1] == 'JOIN':
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == "#CodeArmy" and sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🟢 \033[1;32m[{timestamp}] {sender} joined\033[0m')
            
            # PART (user left)
            elif parts[1] == 'PART':
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == "#CodeArmy" and sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🔴 \033[1;31m[{timestamp}] {sender} left\033[0m')
            
            # Handle server messages
            elif 'Welcome' in message or '001' in message:
                print(f'✅ Connected to {self.current_server["name"]}')
    
    def try_all_servers(self):
        """Try connecting to all available servers"""
        servers = self.get_irc_servers()
        
        for server in servers:
            if self.connect_to_irc(server):
                self.join_channel()
                return True
            time.sleep(1)  # Brief pause between attempts
        
        return False
    
    def show_help(self):
        help_text = """
\033[1;34m
╔══════════════════════════════╗
║    U N I V E R S A L   🚀   ║
╚══════════════════════════════╝

🌐 CONNECTED TO: IRC NETWORK
💬 Channel: #CodeArmy

COMMANDS:
💬 Just type to send messages
🆔 /nick [name] - Change identity  
📊 /status - Connection status
🔄 /reconnect - Try different server
❓ /help - This message
🚪 /exit - Leave chat

FEATURES:
✅ Works worldwide
🔒 100% anonymous  
🕒 Real-time messaging
🌐 Multiple server fallbacks

Press Ctrl+C to exit
\033[0m
"""
        print(help_text)
    
    def start_chat(self):
        self.show_banner()
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
        print('─' * 55)
        
        # Try to connect to any IRC server
        print('🔄 Connecting to global IRC network...')
        
        if self.try_all_servers():
            print('✅ \033[1;32mCONNECTED TO GLOBAL CHAT NETWORK\033[0m')
            print('💬 \033[1;32mType to chat • /help for commands\033[0m')
            print('─' * 55)
            print()
            
            # Start message receiver
            receiver = threading.Thread(target=self.irc_message_loop, daemon=True)
            receiver.start()
            
            # Send welcome message
            self.send_message("🚀 Universal anonymous chat connected!")
            
        else:
            print('❌ \033[1;31mALL CONNECTION ATTEMPTS FAILED\033[0m')
            print('💡 \033[1;33mNo internet connection or firewall blocking\033[0m')
            print('─' * 55)
            print('🔶 \033[1;33mRunning in local demo mode\033[0m\n')
        
        # Main input loop
        while self.active:
            try:
                message = input('\033[1;37m➤ \033[0m').strip()
                
                if not message:
                    continue
                    
                if message.lower() in ['/exit', '/quit']:
                    break
                    
                elif message.startswith('/nick '):
                    new_nick = message[6:].strip()
                    if new_nick:
                        if self.connected:
                            self.send_irc_command(f"NICK {new_nick}")
                        self.nickname = new_nick
                        print(f'🆔 \033[1;33mIdentity: {self.nickname}\033[0m')
                        
                elif message == '/help':
                    self.show_help()
                    
                elif message == '/status':
                    if self.connected:
                        status = f"🟢 CONNECTED to {self.current_server['name']}"
                    else:
                        status = "🔴 LOCAL MODE"
                    print(f'📊 \033[1;36mStatus: {status}\033[0m')
                    
                elif message == '/reconnect':
                    if self.connected:
                        self.socket.close()
                        self.connected = False
                    print('🔄 Reconnecting...')
                    if self.try_all_servers():
                        print('✅ Reconnected!')
                    else:
                        print('❌ Reconnection failed')
                        
                else:
                    # Regular message
                    if self.connected:
                        self.send_message(message)
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                        print(f'   \033[1;36m[{timestamp}] YOU:\033[0m {message}')
                    else:
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                        print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                        
            except KeyboardInterrupt:
                print('\n\n🔴 Shutting down...')
                break
        
        # Cleanup
        self.active = False
        if self.socket:
            self.socket.close()
        print('👋 \033[1;36mUniversal chat session ended\033[0m')

if __name__ == "__main__":
    chat = UniversalChat()
    chat.start_chat()
