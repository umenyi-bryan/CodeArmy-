#!/usr/bin/env python3
import socket
import ssl
import random
import threading
import time
import os
import datetime
import sys
import select

class SuperChat:
    def __init__(self):
        self.nickname = self.generate_cool_nickname()
        self.connected = False
        self.socket = None
        self.active = True
        self.current_server = ""
        self.message_count = 0
        self.channel = "#CodeArmy"
        
    def generate_cool_nickname(self):
        """Generate awesome military/agent style nicknames"""
        prefixes = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Phantom', 'Falcon', 'Orion', 'Steel', 'Iron', 'Shadow']
        suffixes = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Wraith', 'Hunter', 'Scout']
        codes = ['Alpha', 'Bravo', 'Charlie', 'Delta', 'Echo', 'Foxtrot', 'Gamma', 'Sigma', 'Omega', 'Zulu']
        
        style = random.choice(['agent', 'military', 'cyber', 'operative'])
        
        if style == 'agent':
            return f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.randint(100,999)}"
        elif style == 'military':
            return f"{random.choice(codes)}-{random.randint(1000,9999)}"
        elif style == 'cyber':
            cyber_names = ['Neo', 'Trinity', 'Morpheus', 'Cypher', 'Tank', 'Switch', 'Apoc', 'Mouse']
            return f"{random.choice(cyber_names)}_{random.randint(10000,99999)}"
        else:
            return f"Op_{random.choice(prefixes)}_{random.randint(10,99)}"
    
    def show_super_banner(self):
        """Show perfect banner without formatting issues"""
        os.system('clear')
        print('\033[1;36m')  # Cyan
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')  # Magenta
        print('    ╔══════════════════════════════════════╗')
        print('    ║         U L T I M A T E             ║')
        print('    ║    A N O N Y M O U S  C H A T       ║')
        print('    ║     R E A L - T I M E • F R E E     ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')  # Reset
    
    def show_connection_sequence(self):
        """Enhanced connection animation"""
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m{self.channel}\033[0m')
        print(f'🛰️  \033[1;34mINITIATING GLOBAL CONNECTION SEQUENCE\033[0m')
        print()
        
        steps = [
            ("🔍 SCANNING NETWORKS", 2),
            ("🔒 ESTABLISHING ENCRYPTION", 2),
            ("🌐 CONNECTING TO IRC NETWORK", 3),
            ("📡 AUTHENTICATING ANONYMOUSLY", 2),
            ("🚀 JOINING SECURE CHANNEL", 1)
        ]
        
        for step, duration in steps:
            print(f'   {step}', end='', flush=True)
            for _ in range(duration * 5):
                print('.', end='', flush=True)
                time.sleep(0.2)
            print(' ✅')
        
        print()
    
    def get_super_servers(self):
        """Enhanced server list with better reliability"""
        return [
            {
                'name': 'LiberaChat Main',
                'host': 'irc.libera.chat',
                'port': 6667,
                'ssl': False,
                'description': 'Primary Open Source Network'
            },
            {
                'name': 'LiberaChat SSL',
                'host': 'irc.libera.chat',
                'port': 6697,
                'ssl': True,
                'description': 'Encrypted Secure Connection'
            },
            {
                'name': 'OFTC Network',
                'host': 'irc.oftc.net',
                'port': 6667,
                'ssl': False,
                'description': 'Free Software Community'
            },
            {
                'name': 'IRCNet Global',
                'host': 'open.ircnet.net',
                'port': 6667,
                'ssl': False,
                'description': 'Oldest IRC Network'
            },
            {
                'name': 'Freenode Legacy',
                'host': 'chat.freenode.net',
                'port': 6667,
                'ssl': False,
                'description': 'Community Network'
            },
            {
                'name': 'HackInt Privacy',
                'host': 'irc.hackint.org',
                'port': 6697,
                'ssl': True,
                'description': 'Privacy-Focused Network'
            }
        ]
    
    def super_connect(self, server_info):
        """Enhanced connection with better timeout handling"""
        try:
            print(f'🎯 \033[1;33mAttempting: {server_info["name"]}\033[0m')
            print(f'   📡 {server_info["description"]}')
            
            # Create socket with timeout
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(15)
            
            if server_info['ssl']:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.socket = context.wrap_socket(sock, server_hostname=server_info['host'])
            else:
                self.socket = sock
            
            # Connect with progress indicator
            print('   🔗 Connecting', end='', flush=True)
            self.socket.connect((server_info['host'], server_info['port']))
            print(' ✅')
            
            # Send registration
            print('   📝 Authenticating', end='', flush=True)
            self.send_irc_command(f"NICK {self.nickname}")
            self.send_irc_command(f"USER {self.nickname} 0 * :Anonymous Chat User")
            print(' ✅')
            
            # Wait for welcome with better handling
            print('   🎯 Joining network', end='', flush=True)
            welcome_received = False
            start_time = time.time()
            
            while time.time() - start_time < 10 and not welcome_received:
                ready = select.select([self.socket], [], [], 1)
                if ready[0]:
                    response = self.socket.recv(4096).decode('utf-8', errors='ignore')
                    if response:
                        if '001' in response or 'Welcome' in response:
                            welcome_received = True
                        # Handle PING immediately
                        if 'PING' in response:
                            self.handle_ping(response)
            
            if welcome_received:
                self.connected = True
                self.current_server = server_info['name']
                print(' ✅')
                return True
            else:
                print(' ❌')
                return False
                
        except Exception as e:
            print(f' ❌ Error: {str(e)[:30]}...')
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            return False
    
    def send_irc_command(self, command):
        """Send command to IRC server"""
        if self.socket:
            try:
                self.socket.send(f"{command}\r\n".encode('utf-8'))
            except:
                self.connected = False
    
    def handle_ping(self, message):
        """Handle PING messages"""
        if 'PING' in message:
            try:
                ping_msg = message.split('PING :')[-1].split('\n')[0]
                self.send_irc_command(f"PONG :{ping_msg}")
            except:
                pass
    
    def join_super_channel(self):
        """Join channel with confirmation"""
        if self.connected:
            self.send_irc_command(f"JOIN {self.channel}")
            time.sleep(1)  # Brief pause for join to process
    
    def super_message_handler(self):
        """Enhanced message handler with non-blocking reads"""
        buffer = ""
        while self.active and self.connected:
            try:
                # Use select for non-blocking read
                ready = select.select([self.socket], [], [], 1)
                if ready[0]:
                    data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                    if data:
                        buffer += data
                        lines = buffer.split('\n')
                        buffer = lines[-1]  # Keep incomplete line
                        
                        for line in lines[:-1]:
                            line = line.strip()
                            if line:
                                self.process_irc_message(line)
                
                # Handle PING in buffer
                if 'PING' in buffer:
                    self.handle_ping(buffer)
                    buffer = ""
                    
            except Exception as e:
                if self.active:
                    print(f'⚠️  \033[1;33mConnection issue: {e}\033[0m')
                    self.connected = False
                break
    
    def process_irc_message(self, message):
        """Process IRC messages with enhanced formatting"""
        # Handle PING immediately
        if message.startswith('PING'):
            self.handle_ping(message)
            return
        
        parts = message.split(' ')
        if len(parts) < 2:
            return
        
        command = parts[1]
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        
        if command == 'PRIVMSG' and len(parts) >= 4:
            # Chat message
            channel = parts[2]
            text = ' '.join(parts[3:])[1:]  # Remove leading colon
            sender = parts[0][1:].split('!')[0]
            
            if channel == self.channel and text and sender != self.nickname:
                self.message_count += 1
                self.display_user_message(sender, text, timestamp)
                
        elif command == 'JOIN':
            # User joined
            sender = parts[0][1:].split('!')[0]
            channel = parts[2]
            if channel == self.channel and sender != self.nickname:
                print(f'🟢 \033[1;32m[{timestamp}] {sender} joined the channel\033[0m')
                
        elif command == 'PART':
            # User left
            sender = parts[0][1:].split('!')[0]
            channel = parts[2]
            if channel == self.channel and sender != self.nickname:
                print(f'🔴 \033[1;31m[{timestamp}] {sender} left the channel\033[0m')
                
        elif command == 'QUIT':
            # User disconnected
            sender = parts[0][1:].split('!')[0]
            if sender != self.nickname:
                print(f'⚡ \033[1;33m[{timestamp}] {sender} disconnected\033[0m')
        
        elif '001' in message or 'Welcome' in message:
            # Server welcome
            print(f'✅ \033[1;32m[{timestamp}] Connected to {self.current_server}\033[0m')
    
    def display_user_message(self, sender, text, timestamp):
        """Display user messages with awesome formatting"""
        # Color based on user hash
        colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
        color = colors[hash(sender) % len(colors)]
        
        # Cool icons that rotate
        icons = ['🎯', '💬', '⚡', '🔥', '🌟', '💫', '🎮', '🚀', '🔊', '📢']
        icon = icons[self.message_count % len(icons)]
        
        # Different formatting styles
        styles = [
            f'\033[1;{color}m[{timestamp}] {icon} {sender}:\033[0m {text}',
            f'\033[1;{color}m[{timestamp}] 🗨️  {sender}:\033[0m {text}',
            f'\033[1;{color}m[{timestamp}] 💻 {sender}:\033[0m {text}'
        ]
        
        print(styles[self.message_count % len(styles)])
    
    def attempt_super_connection(self):
        """Try all servers with better reporting"""
        servers = self.get_super_servers()
        print(f'🔄 Testing {len(servers)} global networks...\n')
        
        for i, server in enumerate(servers, 1):
            print(f'\033[1;36m[{i}/{len(servers)}]\033[0m ', end='')
            if self.super_connect(server):
                self.join_super_channel()
                return True
            print()
            time.sleep(1)  # Brief pause between attempts
        
        return False
    
    def show_super_help(self):
        """Enhanced help system"""
        help_text = """
\033[1;36m
╔══════════════════════════════════╗
║        S U P E R  C H A T       ║
║      C O M M A N D S  L I S T   ║
╚══════════════════════════════════╝

\033[1;35m💬 CHAT COMMANDS:\033[0m
  Just type to send messages to everyone
  /nick [name] - Change your identity
  /status - Show connection information  
  /help - Display this help message
  /exit - Leave the chat safely

\033[1;33m🎨 ENHANCED FEATURES:\033[0m
  🕒 Real-time timestamps on all messages
  🎯 Color-coded usernames for easy reading
  🔄 Automatic reconnection to backup servers
  🌐 Global network with multiple fallbacks
  🔒 100% anonymous - no registration needed
  📱 Works on any device with Python

\033[1;32m📊 STATUS INDICATORS:\033[0m
  🟢 User joined the channel
  🔴 User left the channel  
  ⚡ User disconnected from network
  🎯 New message received

\033[1;31m⚠️  PRESS CTRL+C TO EXIT SAFELY\033[0m
\033[0m
"""
        print(help_text)
    
    def show_enhanced_status(self):
        """Show comprehensive status information"""
        if self.connected:
            status_icon = "🟢"
            status_text = f"CONNECTED to {self.current_server}"
            status_color = "\033[1;32m"
        else:
            status_icon = "🔴" 
            status_text = "LOCAL MODE - No active connection"
            status_color = "\033[1;31m"
        
        print(f'{status_icon} \033[1;36mCHAT STATUS:\033[0m {status_color}{status_text}\033[0m')
        print(f'🎖️  \033[1;36mYOUR IDENTITY:\033[0m \033[1;35m{self.nickname}\033[0m')
        print(f'💬 \033[1;36mMESSAGE COUNT:\033[0m \033[1;33m{self.message_count}\033[0m')
        print(f'🌐 \033[1;36mCHANNEL:\033[0m \033[1;34m{self.channel}\033[0m')
        
        if not self.connected:
            print('💡 \033[1;33mTIP: Invite others to join the same channel on any IRC network!\033[0m')
    
    def send_super_message(self, message):
        """Send message with enhanced feedback"""
        if self.connected:
            try:
                self.send_irc_command(f"PRIVMSG {self.channel} :{message}")
                return True
            except:
                self.connected = False
                return False
        return False
    
    def start_super_chat(self):
        """Main chat interface with all enhancements"""
        self.show_super_banner()
        self.show_connection_sequence()
        
        # Attempt connection to all servers
        connection_success = self.attempt_super_connection()
        
        if connection_success:
            print('\n🎉 \033[1;32mSUCCESS! GLOBAL CHAT CONNECTION ESTABLISHED\033[0m')
            print('💬 \033[1;32mStart chatting in real-time with the world!\033[0m')
            print('🔒 \033[1;32m100% anonymous • No registration required\033[0m')
            print('─' * 65)
            print()
            
            # Start enhanced message handler
            handler = threading.Thread(target=self.super_message_handler, daemon=True)
            handler.start()
            
            # Send welcome message
            welcome_messages = [
                "🚀 Super anonymous chat activated!",
                "🌐 Connected to global real-time network",
                "🔐 Secure anonymous communications online", 
                "💫 Ultimate terminal chat experience engaged",
                "🎯 Ready for global anonymous conversations"
            ]
            self.send_super_message(random.choice(welcome_messages))
            
        else:
            print('\n❌ \033[1;31mUNABLE TO ESTABLISH GLOBAL CONNECTION\033[0m')
            print('💡 \033[1;33mRunning in enhanced local mode\033[0m')
            print('🔶 \033[1;33mYou can still chat and see your messages locally\033[0m')
            print('🌍 \033[1;33mTell friends to join #CodeArmy on any IRC network!\033[0m')
            print('─' * 65)
            print()
        
        # Enhanced input loop
        while self.active:
            try:
                message = input('\033[1;37m💬 ➤ \033[0m').strip()
                
                if not message:
                    continue
                    
                if message.lower() in ['/exit', '/quit']:
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
                    self.show_super_help()
                    
                elif message == '/status':
                    self.show_enhanced_status()
                    
                elif message == '/time':
                    current_time = datetime.datetime.now().strftime('%H:%M:%S %Y-%m-%d')
                    print(f'🕒 \033[1;36mCURRENT TIME: {current_time}\033[0m')
                    
                elif message == '/reconnect':
                    print('🔄 Attempting to reconnect...')
                    if self.attempt_super_connection():
                        print('✅ Reconnected successfully!')
                    else:
                        print('❌ Reconnection failed')
                        
                else:
                    # Handle regular message
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if self.connected:
                        if self.send_super_message(message):
                            print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;31m[{timestamp}] ❌ FAILED TO SEND:\033[0m {message}')
                    else:
                        print(f'   \033[1;90m[{timestamp}] [LOCAL MODE]: {message}\033[0m')
                        
            except KeyboardInterrupt:
                print('\n\n🔴 \033[1;31mINITIATING SAFE SHUTDOWN...\033[0m')
                break
        
        # Clean shutdown
        self.active = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print('\n👋 \033[1;36mSuper chat session ended. Stay anonymous! 🎭\033[0m')

if __name__ == "__main__":
    chat = SuperChat()
    chat.start_super_chat()
