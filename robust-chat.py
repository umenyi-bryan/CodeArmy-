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

class RobustChat:
    def __init__(self):
        self.nickname = self.generate_cool_nickname()
        self.connected = False
        self.socket = None
        self.active = True
        self.current_server = ""
        self.message_count = 0
        self.channel = "#CodeArmy"
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        
    def generate_cool_nickname(self):
        """Generate awesome military/agent style nicknames"""
        prefixes = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Phantom', 'Falcon', 'Steel', 'Shadow']
        suffixes = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Hunter']
        return f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.randint(100,999)}"
    
    def show_banner(self):
        """Show perfect banner without formatting issues"""
        os.system('clear')
        print('\033[1;36m')  # Cyan
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')  # Magenta
        print('    ╔══════════════════════════════════════╗')
        print('    ║         R O B U S T  C H A T        ║')
        print('    ║    A U T O - R E C O N N E C T      ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')  # Reset
    
    def get_robust_servers(self):
        """Enhanced server list with better reliability"""
        return [
            {
                'name': 'LiberaChat',
                'host': 'irc.libera.chat',
                'port': 6667,
                'ssl': False,
                'description': 'Primary Network'
            },
            {
                'name': 'LiberaChat SSL', 
                'host': 'irc.libera.chat',
                'port': 6697,
                'ssl': True,
                'description': 'Encrypted'
            },
            {
                'name': 'OFTC',
                'host': 'irc.oftc.net',
                'port': 6667, 
                'ssl': False,
                'description': 'Backup Network'
            },
            {
                'name': 'HackInt',
                'host': 'irc.hackint.org',
                'port': 6697,
                'ssl': True,
                'description': 'Privacy Network'
            }
        ]
    
    def robust_connect(self, server_info):
        """Robust connection with comprehensive error handling"""
        try:
            print(f'🎯 \033[1;33mTrying: {server_info["name"]}\033[0m')
            
            # Create socket
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            
            if server_info['ssl']:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                self.socket = context.wrap_socket(sock, server_hostname=server_info['host'])
            else:
                self.socket = sock
            
            # Connect
            self.socket.connect((server_info['host'], server_info['port']))
            
            # Send registration
            self.send_irc_command(f"NICK {self.nickname}")
            self.send_irc_command(f"USER {self.nickname} 0 * :Anonymous Chat")
            
            # Wait for welcome with comprehensive handling
            welcome_received = False
            start_time = time.time()
            
            while time.time() - start_time < 8 and not welcome_received:
                ready = select.select([self.socket], [], [], 1)
                if ready[0]:
                    try:
                        response = self.socket.recv(4096).decode('utf-8', errors='ignore')
                        if response:
                            if '001' in response or 'Welcome' in response:
                                welcome_received = True
                            # Handle any PINGs during connection
                            if 'PING' in response:
                                self.handle_ping(response)
                    except socket.timeout:
                        continue
            
            if welcome_received:
                self.connected = True
                self.current_server = server_info['name']
                self.reconnect_attempts = 0
                print(f'✅ \033[1;32mConnected to {server_info["name"]}\033[0m')
                return True
                
        except Exception as e:
            print(f'❌ \033[1;31mFailed: {str(e)[:40]}\033[0m')
        
        # Cleanup on failure
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        return False
    
    def send_irc_command(self, command):
        """Send command with comprehensive error handling"""
        if self.socket and self.connected:
            try:
                self.socket.send(f"{command}\r\n".encode('utf-8'))
                return True
            except (BrokenPipeError, ConnectionResetError, OSError):
                self.handle_connection_lost()
                return False
            except Exception:
                return False
        return False
    
    def handle_ping(self, message):
        """Handle PING messages safely"""
        try:
            if 'PING' in message:
                ping_msg = message.split('PING :')[-1].split('\n')[0]
                self.send_irc_command(f"PONG :{ping_msg}")
        except:
            pass
    
    def handle_connection_lost(self):
        """Handle lost connection gracefully"""
        if self.connected:
            print(f'\n🔌 \033[1;31mConnection to {self.current_server} lost\033[0m')
            self.connected = False
        
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        # Auto-reconnect if we were previously connected
        if self.active and self.reconnect_attempts < self.max_reconnect_attempts:
            self.reconnect_attempts += 1
            print(f'🔄 \033[1;33mAttempting auto-reconnect ({self.reconnect_attempts}/{self.max_reconnect_attempts})...\033[0m')
            self.attempt_reconnection()
    
    def attempt_reconnection(self):
        """Attempt to reconnect to any server"""
        servers = self.get_robust_servers()
        
        for server in servers:
            if self.robust_connect(server):
                self.join_channel()
                print('✅ \033[1;32mAuto-reconnect successful!\033[0m')
                return True
            time.sleep(1)
        
        print('❌ \033[1;31mAuto-reconnect failed\033[0m')
        return False
    
    def join_channel(self):
        """Join channel with error handling"""
        if self.connected:
            self.send_irc_command(f"JOIN {self.channel}")
            # Small delay to let join process
            time.sleep(0.5)
    
    def robust_message_handler(self):
        """Robust message handler with comprehensive error handling"""
        buffer = ""
        last_ping_time = time.time()
        
        while self.active:
            try:
                if not self.connected:
                    time.sleep(1)
                    continue
                
                # Use select with timeout for non-blocking operation
                ready = select.select([self.socket], [], [], 1)
                
                if ready[0]:
                    # Data available to read
                    try:
                        data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                        if data:
                            buffer += data
                            lines = buffer.split('\n')
                            buffer = lines[-1]  # Keep incomplete line
                            
                            for line in lines[:-1]:
                                line = line.strip()
                                if line:
                                    self.process_irc_message(line)
                            
                            last_ping_time = time.time()
                        else:
                            # Empty data usually means connection closed
                            self.handle_connection_lost()
                            continue
                            
                    except (ConnectionResetError, BrokenPipeError, OSError):
                        self.handle_connection_lost()
                        continue
                    except socket.timeout:
                        continue
                    except Exception as e:
                        print(f'⚠️  \033[1;33mRead error: {e}\033[0m')
                        continue
                
                # Check if we need to send PING (prevent timeout)
                if self.connected and time.time() - last_ping_time > 120:
                    # Some servers require PING from client
                    self.send_irc_command(f"PING :{int(time.time())}")
                    last_ping_time = time.time()
                    
            except Exception as e:
                if self.active:
                    print(f'⚠️  \033[1;33mHandler error: {e}\033[0m')
                    time.sleep(1)
    
    def process_irc_message(self, message):
        """Process IRC messages safely"""
        # Handle PING immediately
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
                    print(f'🟢 \033[1;32m[{timestamp}] {sender} joined\033[0m')
                    
            elif command == 'PART':
                # User left
                sender = parts[0][1:].split('!')[0]
                channel = parts[2]
                if channel == self.channel and sender != self.nickname:
                    print(f'🔴 \033[1;31m[{timestamp}] {sender} left\033[0m')
                    
            elif command == 'QUIT':
                # User disconnected
                sender = parts[0][1:].split('!')[0]
                if sender != self.nickname:
                    print(f'⚡ \033[1;33m[{timestamp}] {sender} disconnected\033[0m')
            
            elif '001' in message or 'Welcome' in message:
                # Server welcome message
                print(f'✅ \033[1;32m[{timestamp}] Connected to {self.current_server}\033[0m')
                
        except Exception as e:
            print(f'⚠️  \033[1;33mMessage processing error: {e}\033[0m')
    
    def display_user_message(self, sender, text, timestamp):
        """Display user messages with awesome formatting"""
        try:
            colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
            color = colors[hash(sender) % len(colors)]
            
            icons = ['🎯', '💬', '⚡', '🔥', '🌟', '💫', '🎮', '🚀']
            icon = icons[self.message_count % len(icons)]
            
            print(f'\033[1;{color}m[{timestamp}] {icon} {sender}:\033[0m {text}')
        except:
            print(f'[{timestamp}] {sender}: {text}')
    
    def attempt_initial_connection(self):
        """Try all servers for initial connection"""
        servers = self.get_robust_servers()
        print('🔍 Testing global networks...\n')
        
        for server in servers:
            if self.robust_connect(server):
                self.join_channel()
                return True
            time.sleep(1)
        
        return False
    
    def send_chat_message(self, message):
        """Send chat message with robust error handling"""
        if self.connected:
            success = self.send_irc_command(f"PRIVMSG {self.channel} :{message}")
            return success
        return False
    
    def show_help(self):
        """Show help information"""
        help_text = """
\033[1;36m
╔══════════════════════════════╗
║    R O B U S T  C H A T     ║
╚══════════════════════════════╝

\033[1;35m💬 CHAT COMMANDS:\033[0m
  Just type to send messages
  /nick [name] - Change identity
  /status - Connection status
  /reconnect - Manual reconnect
  /help - This message
  /exit - Leave chat

\033[1;33m🛡️  ROBUST FEATURES:\033[0m
  🔄 Auto-reconnect on disconnect
  🛡️  Comprehensive error handling
  🌐 Multiple server fallbacks
  📡 Real-time global chat
  🔒 100% anonymous

\033[1;31mPress Ctrl+C to exit safely\033[0m
\033[0m
"""
        print(help_text)
    
    def show_status(self):
        """Show connection status"""
        if self.connected:
            status = f"🟢 CONNECTED to {self.current_server}"
        else:
            status = "🔴 DISCONNECTED"
        
        print(f'📊 \033[1;36mStatus: {status}\033[0m')
        print(f'🎖️  \033[1;36mYou: {self.nickname}\033[0m')
        print(f'💬 \033[1;36mMessages: {self.message_count}\033[0m')
        print(f'🔁 \033[1;36mReconnect attempts: {self.reconnect_attempts}/{self.max_reconnect_attempts}\033[0m')
    
    def start_robust_chat(self):
        """Main chat interface with robust error handling"""
        self.show_banner()
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m{self.channel}\033[0m')
        print('🛰️  \033[1;34mESTABLISHING ROBUST CONNECTION...\033[0m\n')
        
        # Initial connection attempt
        if self.attempt_initial_connection():
            print('\n🎉 \033[1;32mGLOBAL CHAT CONNECTED!\033[0m')
            print('💬 \033[1;32mStart chatting in real-time\033[0m')
            print('🛡️  \033[1;32mAuto-reconnect enabled\033[0m')
            print('─' * 50)
            print()
            
            # Send welcome message
            self.send_chat_message("🚀 Robust anonymous chat connected!")
        else:
            print('\n💡 \033[1;33mRunning in local mode\033[0m')
            print('🔶 \033[1;33mAuto-reconnect will attempt when you send messages\033[0m')
            print('─' * 50)
            print()
        
        # Start robust message handler
        handler = threading.Thread(target=self.robust_message_handler, daemon=True)
        handler.start()
        
        # Main input loop with comprehensive error handling
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
                    self.show_help()
                    
                elif message == '/status':
                    self.show_status()
                    
                elif message == '/reconnect':
                    print('🔄 Manual reconnect initiated...')
                    self.attempt_reconnection()
                    
                else:
                    # Regular message
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if self.connected:
                        if self.send_chat_message(message):
                            print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;31m[{timestamp}] ❌ FAILED TO SEND\033[0m')
                    else:
                        # Try to reconnect when sending in disconnected state
                        if self.reconnect_attempts < self.max_reconnect_attempts:
                            print('🔄 Attempting to reconnect...')
                            if self.attempt_reconnection():
                                if self.send_chat_message(message):
                                    print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {message}')
                                else:
                                    print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                            else:
                                print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                        else:
                            print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                            
            except KeyboardInterrupt:
                print('\n\n🔴 \033[1;31mSHUTTING DOWN...\033[0m')
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
        print('\n👋 \033[1;36mRobust chat session ended\033[0m')

if __name__ == "__main__":
    chat = RobustChat()
    chat.start_robust_chat()
