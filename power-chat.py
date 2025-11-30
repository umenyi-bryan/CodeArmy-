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

class PowerChat:
    def __init__(self):
        self.nickname = self.generate_cool_nickname()
        self.connected = False
        self.socket = None
        self.active = True
        self.current_server = ""
        self.message_count = 0
        self.channel = "#CodeArmy"
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 5
        self.last_activity = time.time()
        
    def generate_cool_nickname(self):
        """Generate awesome nicknames"""
        prefixes = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Phantom', 'Falcon', 'Steel', 'Shadow', 'Cyber', 'Neo']
        suffixes = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Hunter', 'Byte', 'Code']
        return f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.randint(100,999)}"
    
    def show_power_banner(self):
        """Show power banner"""
        os.system('clear')
        print('\033[1;36m')
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')
        print('    ╔══════════════════════════════════════╗')
        print('    ║           P O W E R  C H A T        ║')
        print('    ║    G L O B A L • R E A L - T I M E  ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m{self.channel}\033[0m')
        print('🛰️  \033[1;34mINITIALIZING POWER CONNECTION SYSTEM...\033[0m\n')
    
    def get_power_servers(self):
        """Enhanced server list with multiple strategies"""
        return [
            # Primary servers
            {
                'name': 'LiberaChat Main',
                'host': 'irc.libera.chat',
                'port': 6667,
                'ssl': False,
                'priority': 1
            },
            {
                'name': 'LiberaChat SSL', 
                'host': 'irc.libera.chat',
                'port': 6697,
                'ssl': True,
                'priority': 1
            },
            # Secondary servers
            {
                'name': 'OFTC Network',
                'host': 'irc.oftc.net',
                'port': 6667,
                'ssl': False,
                'priority': 2
            },
            {
                'name': 'IRCNet Global',
                'host': 'open.ircnet.net',
                'port': 6667,
                'ssl': False,
                'priority': 2
            },
            # Tertiary servers
            {
                'name': 'HackInt Privacy',
                'host': 'irc.hackint.org',
                'port': 6697,
                'ssl': True,
                'priority': 3
            },
            {
                'name': 'Freenode Legacy',
                'host': 'chat.freenode.net',
                'port': 6667,
                'ssl': False,
                'priority': 3
            }
        ]
    
    def power_connect(self, server_info):
        """Enhanced connection with multiple strategies"""
        try:
            print(f'🔗 \033[1;33m{server_info["name"]}\033[0m', end='', flush=True)
            
            # Create socket with different timeouts based on priority
            timeout = 8 if server_info['priority'] == 1 else 12
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(timeout)
            
            if server_info['ssl']:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.socket = context.wrap_socket(sock, server_hostname=server_info['host'])
            else:
                self.socket = sock
            
            # Connect with progress indicator
            self.socket.connect((server_info['host'], server_info['port']))
            
            # Send registration
            self.send_irc_command(f"NICK {self.nickname}")
            self.send_irc_command(f"USER {self.nickname} 0 * :Power Chat User")
            
            # Enhanced welcome detection
            welcome_received = False
            start_time = time.time()
            dots = 0
            
            while time.time() - start_time < timeout and not welcome_received:
                print('.', end='', flush=True)
                dots += 1
                
                ready = select.select([self.socket], [], [], 0.5)
                if ready[0]:
                    try:
                        response = self.socket.recv(4096).decode('utf-8', errors='ignore')
                        if response:
                            if any(msg in response for msg in ['001', 'Welcome', 'MODE']):
                                welcome_received = True
                            if 'PING' in response:
                                self.handle_ping(response)
                    except socket.timeout:
                        continue
                
                if dots > 6:  # Limit dots to prevent long lines
                    print('\r' + ' ' * 50 + '\r', end='')
                    print(f'🔗 \033[1;33m{server_info["name"]}\033[0m', end='')
                    dots = 0
            
            if welcome_received:
                self.connected = True
                self.current_server = server_info['name']
                self.reconnect_attempts = 0
                self.last_activity = time.time()
                print(' ✅')
                return True
            else:
                print(' ❌')
                return False
                
        except Exception as e:
            error_msg = str(e)
            if 'Connection refused' in error_msg:
                print(' 🔄')  # Server exists but refused
            elif 'Network is unreachable' in error_msg:
                print(' 🌐')  # Network issue
            elif 'timed out' in error_msg:
                print(' ⏰')  # Timeout
            else:
                print(' ❌')  # Other error
            
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            
            return False
    
    def send_irc_command(self, command):
        """Send command with enhanced error handling"""
        if self.socket and self.connected:
            try:
                self.socket.send(f"{command}\r\n".encode('utf-8'))
                self.last_activity = time.time()
                return True
            except (BrokenPipeError, ConnectionResetError, OSError, socket.timeout):
                self.handle_connection_lost("Send failed")
                return False
            except Exception:
                return False
        return False
    
    def handle_ping(self, message):
        """Handle PING messages"""
        try:
            if 'PING' in message:
                ping_msg = message.split('PING :')[-1].split('\n')[0]
                self.send_irc_command(f"PONG :{ping_msg}")
        except:
            pass
    
    def handle_connection_lost(self, reason="Connection lost"):
        """Enhanced connection loss handling"""
        if self.connected:
            print(f'\n🔌 \033[1;31m{reason} - {self.current_server}\033[0m')
            self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        # Auto-reconnect with backoff
        if self.active and self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            delay = min(2 ** self.reconnect_attempts, 10)  # Exponential backoff
            print(f'🔄 \033[1;33mAuto-reconnect in {delay}s ({self.reconnect_attempts}/{self.max_reconnect_attempts})...\033[0m')
            time.sleep(delay)
            self.attempt_power_reconnection()
    
    def join_channel(self):
        """Join channel with retry logic"""
        if self.connected:
            for attempt in range(3):
                if self.send_irc_command(f"JOIN {self.channel}"):
                    time.sleep(0.5)
                    return True
                time.sleep(1)
        return False
    
    def power_message_handler(self):
        """Powerful message handler with keep-alive"""
        buffer = ""
        last_keepalive = time.time()
        
        while self.active:
            try:
                if not self.connected:
                    time.sleep(1)
                    continue
                
                # Check if connection is stale
                if time.time() - self.last_activity > 180:  # 3 minutes no activity
                    print('⚠️  \033[1;33mConnection seems stale, sending keep-alive\033[0m')
                    self.send_irc_command(f"PING :{int(time.time())}")
                    self.last_activity = time.time()
                
                # Non-blocking read
                ready = select.select([self.socket], [], [], 1)
                
                if ready[0]:
                    try:
                        data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                        if data:
                            buffer += data
                            lines = buffer.split('\n')
                            buffer = lines[-1]
                            
                            for line in lines[:-1]:
                                line = line.strip()
                                if line:
                                    self.process_irc_message(line)
                            
                            self.last_activity = time.time()
                        else:
                            self.handle_connection_lost("Server closed connection")
                            continue
                            
                    except (ConnectionResetError, BrokenPipeError, OSError, socket.timeout):
                        self.handle_connection_lost("Network error")
                        continue
                    except Exception as e:
                        if self.active:
                            print(f'⚠️  \033[1;33mRead error: {e}\033[0m')
                        continue
                
                # Send periodic PING to prevent timeout
                if self.connected and time.time() - last_keepalive > 120:
                    self.send_irc_command(f"PING :keepalive_{int(time.time())}")
                    last_keepalive = time.time()
                    
            except Exception as e:
                if self.active:
                    print(f'⚠️  \033[1;33mHandler error: {e}\033[0m')
                time.sleep(1)
    
    def process_irc_message(self, message):
        """Process messages with enhanced parsing"""
        if message.startswith('PING'):
            self.handle_ping(message)
            return
        
        parts = message.split(' ')
        if len(parts) < 2:
            return
        
        command = parts[1]
        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
        
        try:
            if command == 'PRIVMSG' and len(parts) >= 4:
                channel = parts[2]
                text = ' '.join(parts[3:])[1:]
                sender = parts[0][1:].split('!')[0]
                
                if channel == self.channel and text and sender != self.nickname:
                    self.message_count += 1
                    self.display_user_message(sender, text, timestamp)
                    
            elif command == 'JOIN':
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == self.channel and sender != self.nickname:
                    print(f'🟢 \033[1;32m[{timestamp}] {sender} joined\033[0m')
                    
            elif command == 'PART':
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == self.channel and sender != self.nickname:
                    print(f'🔴 \033[1;31m[{timestamp}] {sender} left\033[0m')
                    
            elif command == 'QUIT':
                sender = parts[0][1:].split('!')[0]
                if sender != self.nickname:
                    print(f'⚡ \033[1;33m[{timestamp}] {sender} disconnected\033[0m')
            
            elif '001' in message or 'Welcome' in message:
                print(f'✅ \033[1;32m[{timestamp}] Connected to {self.current_server}\033[0m')
                
        except Exception as e:
            print(f'⚠️  \033[1;33mMessage error: {e}\033[0m')
    
    def display_user_message(self, sender, text, timestamp):
        """Enhanced message display"""
        try:
            colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
            color = colors[hash(sender) % len(colors)]
            
            icons = ['🎯', '💬', '⚡', '🔥', '🌟', '💫', '🎮', '🚀', '🔊', '📢']
            icon = icons[self.message_count % len(icons)]
            
            print(f'\033[1;{color}m[{timestamp}] {icon} {sender}:\033[0m {text}')
        except:
            print(f'[{timestamp}] {sender}: {text}')
    
    def attempt_power_connection(self):
        """Enhanced connection attempt with priority"""
        servers = self.get_power_servers()
        
        # Sort by priority
        servers.sort(key=lambda x: x['priority'])
        
        print('🌐 \033[1;34mScanning global networks...\033[0m')
        print('   (Primary → Secondary → Tertiary)\n')
        
        for server in servers:
            if self.power_connect(server):
                if self.join_channel():
                    return True
                else:
                    self.connected = False
                    if self.socket:
                        self.socket.close()
                        self.socket = None
            time.sleep(1)
        
        return False
    
    def attempt_power_reconnection(self):
        """Enhanced reconnection"""
        if self.attempt_power_connection():
            print('✅ \033[1;32mAuto-reconnect successful!\033[0m')
            # Resend last few messages if needed
            return True
        else:
            print('❌ \033[1;31mAuto-reconnect failed\033[0m')
            return False
    
    def send_chat_message(self, message):
        """Send message with reconnection attempt"""
        if self.connected:
            return self.send_irc_command(f"PRIVMSG {self.channel} :{message}")
        return False
    
    def show_power_help(self):
        """Enhanced help"""
        help_text = """
\033[1;36m
╔══════════════════════════════╗
║        P O W E R  C H A T   ║
╚══════════════════════════════╝

\033[1;35m💬 CHAT COMMANDS:\033[0m
  Just type to send messages
  /nick [name] - Change identity
  /status - Detailed status
  /reconnect - Force reconnect
  /servers - List available servers
  /help - This message
  /exit - Leave chat

\033[1;33m🚀 POWER FEATURES:\033[0m
  🔄 Auto-reconnect with backoff
  🌐 Multi-priority server list
  🛡️  Connection keep-alive
  📡 Real-time global chat
  🔒 100% anonymous

\033[1;32mPress Ctrl+C to exit\033[0m
\033[0m
"""
        print(help_text)
    
    def show_power_status(self):
        """Enhanced status display"""
        if self.connected:
            status = f"🟢 CONNECTED to {self.current_server}"
            status_color = "\033[1;32m"
        else:
            status = "🔴 DISCONNECTED"
            status_color = "\033[1;31m"
        
        print(f'📊 \033[1;36mPOWER STATUS:\033[0m {status_color}{status}\033[0m')
        print(f'🎖️  \033[1;36mIdentity:\033[0m \033[1;35m{self.nickname}\033[0m')
        print(f'💬 \033[1;36mMessages:\033[0m \033[1;33m{self.message_count}\033[0m')
        print(f'🔁 \033[1;36mReconnects:\033[0m \033[1;33m{self.reconnect_attempts}/{self.max_reconnect_attempts}\033[0m')
        print(f'⏰ \033[1;36mLast activity:\033[0m \033[1;33m{int(time.time() - self.last_activity)}s ago\033[0m')
        
        if not self.connected:
            print('💡 \033[1;33mAuto-reconnect will attempt on next message\033[0m')
    
    def list_servers(self):
        """List available servers"""
        servers = self.get_power_servers()
        print('\n🌐 \033[1;36mAVAILABLE SERVERS:\033[0m')
        for server in servers:
            status = "🟢 Primary" if server['priority'] == 1 else "🟡 Secondary" if server['priority'] == 2 else "🔴 Tertiary"
            ssl_info = " (SSL)" if server['ssl'] else ""
            print(f'   {status} - {server["name"]}{ssl_info}')
    
    def start_power_chat(self):
        """Main power chat interface"""
        self.show_power_banner()
        
        # Initial connection attempt
        if self.attempt_power_connection():
            print('\n🎉 \033[1;32mPOWER CHAT CONNECTED!\033[0m')
            print('💬 \033[1;32mGlobal real-time chat active\033[0m')
            print('🛡️  \033[1;32mAuto-reconnect & keep-alive enabled\033[0m')
            print('─' * 60)
            print()
            
            # Send welcome
            self.send_chat_message("🚀 Power chat connected! Type /help for commands")
        else:
            print('\n💡 \033[1;33mPOWER CHAT READY (Local Mode)\033[0m')
            print('🔶 \033[1;33mAuto-reconnect will attempt when needed\033[0m')
            print('🌍 \033[1;33mInvite others to #CodeArmy on any IRC network!\033[0m')
            print('─' * 60)
            print()
        
        # Start power message handler
        handler = threading.Thread(target=self.power_message_handler, daemon=True)
        handler.start()
        
        # Main input loop
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
                        self.nickname = new_nick
                        print(f'🆔 \033[1;33mIdentity: {self.nickname}\033[0m')
                        
                elif message == '/help':
                    self.show_power_help()
                    
                elif message == '/status':
                    self.show_power_status()
                    
                elif message == '/servers':
                    self.list_servers()
                    
                elif message == '/reconnect':
                    print('🔄 Force reconnecting...')
                    self.attempt_power_reconnection()
                    
                else:
                    # Handle message with enhanced reconnection
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if self.connected:
                        if self.send_chat_message(message):
                            print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;31m[{timestamp}] ❌ Send failed\033[0m')
                    else:
                        # Enhanced reconnection on message send
                        print('🔄 Connection needed, attempting...')
                        if self.attempt_power_reconnection():
                            if self.send_chat_message(message):
                                print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {message}')
                            else:
                                print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                        else:
                            print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                            
            except KeyboardInterrupt:
                print('\n\n🔴 \033[1;31mPOWERING DOWN...\033[0m')
                break
            except Exception as e:
                print(f'\n⚠️  \033[1;33mInput error: {e}\033[0m')
                continue
        
        # Clean shutdown
        self.active = False
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
        print('\n👋 \033[1;36mPower chat session ended\033[0m')

if __name__ == "__main__":
    chat = PowerChat()
    chat.start_power_chat()
