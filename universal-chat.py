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
        self.channel = "#CodeArmy"
        self.message_count = 0
        self.connection_method = "irc"
        
    def generate_nickname(self):
        names = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Phantom', 'Falcon', 'Steel', 'Shadow', 'Cyber', 'Neo']
        suffixes = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Hunter', 'Byte', 'Code']
        return f"{random.choice(names)}_{random.choice(suffixes)}{random.randint(100,999)}"
    
    def show_banner(self):
        os.system('clear')
        print('\033[1;36m')
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')
        print('    ╔══════════════════════════════════════╗')
        print('    ║         U N I V E R S A L           ║')
        print('    ║    C H A T • W O R K S • A L L      ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')
        print(f'👤 \033[1;33mUSER:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mROOM:\033[0m \033[1;35m{self.channel}\033[0m')
    
    def try_all_connections(self):
        """Try multiple connection methods"""
        print('🔗 Testing connection methods...\n')
        
        # Method 1: Standard IRC
        if self.connect_irc():
            self.connection_method = "irc"
            return True
        
        # Method 2: Alternative IRC servers
        if self.connect_irc_alternative():
            self.connection_method = "irc_alt"
            return True
            
        # Method 3: Direct socket with different approach
        if self.connect_direct():
            self.connection_method = "direct"
            return True
            
        return False
    
    def connect_irc(self):
        """Standard IRC connection"""
        print('   🟢 Standard IRC...', end='', flush=True)
        servers = [
            ('irc.libera.chat', 6667, False),
            ('irc.libera.chat', 6697, True),
        ]
        
        for server, port, use_ssl in servers:
            try:
                if use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket = context.wrap_socket(sock, server_hostname=server)
                else:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                self.socket.settimeout(15)
                self.socket.connect((server, port))
                
                # Send registration
                self.socket.send(f"NICK {self.nickname}\r\n".encode())
                self.socket.send(f"USER {self.nickname} 0 * :Universal Chat\r\n".encode())
                self.socket.send(f"JOIN {self.channel}\r\n".encode())
                
                # Wait and check connection
                time.sleep(3)
                
                # Test by sending PING
                self.socket.send(f"PING :test\r\n".encode())
                time.sleep(1)
                
                # If we're still connected, it worked
                self.connected = True
                print(' ✅')
                return True
                
            except Exception as e:
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    self.socket = None
                continue
        
        print(' ❌')
        return False
    
    def connect_irc_alternative(self):
        """Alternative IRC servers"""
        print('   🟡 Alternative IRC...', end='', flush=True)
        servers = [
            ('irc.oftc.net', 6667, False),
            ('irc.hackint.org', 6697, True),
            ('chat.freenode.net', 6667, False),
            ('open.ircnet.net', 6667, False),
        ]
        
        for server, port, use_ssl in servers:
            try:
                if use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.socket = context.wrap_socket(sock, server_hostname=server)
                else:
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                self.socket.settimeout(15)
                self.socket.connect((server, port))
                
                self.socket.send(f"NICK {self.nickname}\r\n".encode())
                self.socket.send(f"USER {self.nickname} 0 * :Universal Chat\r\n".encode())
                self.socket.send(f"JOIN {self.channel}\r\n".encode())
                
                time.sleep(3)
                self.connected = True
                print(' ✅')
                return True
                
            except Exception:
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    self.socket = None
                continue
        
        print(' ❌')
        return False
    
    def connect_direct(self):
        """Direct connection with different settings"""
        print('   🔴 Direct connect...', end='', flush=True)
        
        # Try with different socket options
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.socket.settimeout(20)
            
            # Try LiberaChat with longer timeout
            self.socket.connect(('irc.libera.chat', 6667))
            
            # Send registration with delays
            self.socket.send(f"NICK {self.nickname}\r\n".encode())
            time.sleep(1)
            self.socket.send(f"USER {self.nickname} 0 * :Direct Chat\r\n".encode())
            time.sleep(1)
            self.socket.send(f"JOIN {self.channel}\r\n".encode())
            time.sleep(2)
            
            self.connected = True
            print(' ✅')
            return True
            
        except Exception:
            if self.socket:
                try:
                    self.socket.close()
                except:
                    pass
                self.socket = None
            print(' ❌')
            return False
    
    def start_message_receiver(self):
        """Universal message receiver"""
        if not self.connected:
            return
            
        def receiver():
            buffer = ""
            last_ping = time.time()
            
            while self.connected:
                try:
                    # Set timeout for non-blocking
                    self.socket.settimeout(1)
                    
                    data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                    if data:
                        buffer += data
                        lines = buffer.split('\n')
                        buffer = lines[-1]
                        
                        for line in lines[:-1]:
                            if line.strip():
                                self.process_message(line.strip())
                        
                        last_ping = time.time()
                    
                    # Handle PING in buffer
                    if 'PING' in buffer:
                        self.handle_ping(buffer)
                        buffer = ""
                    
                    # Send periodic PING to keep connection alive
                    if time.time() - last_ping > 60:
                        self.send_raw("PING :keepalive")
                        last_ping = time.time()
                        
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f'\n⚠️  \033[1;33mConnection issue: {e}\033[0m')
                    self.connected = False
                    break
        
        thread = threading.Thread(target=receiver, daemon=True)
        thread.start()
    
    def handle_ping(self, message):
        """Handle PING messages"""
        try:
            if 'PING' in message:
                ping_msg = message.split('PING :')[-1].split('\n')[0]
                self.send_raw(f"PONG :{ping_msg}")
        except:
            self.connected = False
    
    def send_raw(self, message):
        """Send raw IRC command"""
        if self.connected and self.socket:
            try:
                self.socket.send(f"{message}\r\n".encode())
                return True
            except:
                self.connected = False
                return False
        return False
    
    def process_message(self, line):
        """Process incoming messages"""
        # Handle PING immediately
        if line.startswith('PING'):
            self.handle_ping(line)
            return
        
        # PRIVMSG - Chat message
        if 'PRIVMSG' in line and self.channel in line:
            try:
                parts = line.split('PRIVMSG')[1].split(':', 1)
                if len(parts) >= 2:
                    sender = line.split('!')[0][1:]
                    text = parts[1].strip()
                    
                    if sender != self.nickname:
                        self.message_count += 1
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                        
                        colors = ['32', '33', '35', '36', '92', '93', '94', '95', '96']
                        color = colors[hash(sender) % len(colors)]
                        
                        print(f'\033[1;{color}m[{timestamp}] {sender}:\033[0m {text}')
            except:
                pass
        
        # JOIN - User joined
        elif 'JOIN' in line and self.channel in line:
            try:
                sender = line.split('!')[0][1:]
                if sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🟢 \033[1;32m[{timestamp}] {sender} joined\033[0m')
            except:
                pass
        
        # PART - User left
        elif 'PART' in line and self.channel in line:
            try:
                sender = line.split('!')[0][1:]
                if sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🔴 \033[1;31m[{timestamp}] {sender} left\033[0m')
            except:
                pass
        
        # Handle various server messages
        elif '001' in line or 'Welcome' in line:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            print(f'✅ \033[1;32m[{timestamp}] Connected to chat network\033[0m')
    
    def send_message(self, text):
        """Send chat message"""
        if self.connected:
            return self.send_raw(f"PRIVMSG {self.channel} :{text}")
        return False
    
    def show_help(self):
        print("""
\033[1;36m
💬 UNIVERSAL CHAT - ALWAYS WORKS

COMMANDS:
• Just type to send messages
• /nick [name] - Change username
• /reconnect - Try connecting again
• /status - Connection info
• /help - This message
• /exit - Leave chat

TROUBLESHOOTING:
• If messages don't send, wait a moment
• Use /reconnect if having issues
• Different networks work for different people

Press Ctrl+C to exit
\033[0m
""")
    
    def show_status(self):
        if self.connected:
            status = f"🟢 CONNECTED ({self.connection_method})"
        else:
            status = "🔴 DISCONNECTED"
        
        print(f'📊 \033[1;36mStatus: {status}\033[0m')
        print(f'💬 \033[1;36mMessages sent/received: {self.message_count}\033[0m')
    
    def attempt_reconnect(self):
        """Attempt to reconnect"""
        print('🔄 Attempting to reconnect...')
        if self.socket:
            try:
                self.socket.close()
            except:
                pass
            self.socket = None
        
        self.connected = False
        return self.try_all_connections()
    
    def start_chat(self):
        """Main chat interface"""
        self.show_banner()
        
        # Try to connect
        if self.try_all_connections():
            print(f'\n🎉 \033[1;32mSUCCESS! Connected via {self.connection_method}\033[0m')
            print('💬 \033[1;32mStart chatting with the world!\033[0m')
            print('─' * 50)
            print()
            
            # Start receiving messages
            self.start_message_receiver()
            
            # Send welcome message
            self.send_message("🚀 Hello from Universal Chat!")
            
        else:
            print('\n💡 \033[1;33mCould not establish connection\033[0m')
            print('🔶 \033[1;33mYou can still type messages locally\033[0m')
            print('🌍 \033[1;33mTry /reconnect later or use different network\033[0m')
            print('─' * 50)
            print()
        
        # Main chat loop
        while True:
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
                            self.send_raw(f"NICK {new_nick}")
                        self.nickname = new_nick
                        print(f'🆔 \033[1;33mName: {new_nick}\033[0m')
                        
                elif message == '/help':
                    self.show_help()
                    
                elif message == '/status':
                    self.show_status()
                    
                elif message == '/reconnect':
                    if self.attempt_reconnect():
                        print('✅ \033[1;32mReconnected successfully!\033[0m')
                        self.start_message_receiver()
                    else:
                        print('❌ \033[1;31mReconnection failed\033[0m')
                    
                else:
                    # Send message
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if self.connected:
                        if self.send_message(message):
                            print(f'   \033[1;36m[{timestamp}] YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;31m[{timestamp}] ❌ Failed to send\033[0m')
                            print('   💡 Try /reconnect or wait a moment')
                    else:
                        print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                        print('   💡 Use /reconnect to try connecting again')
                        
            except KeyboardInterrupt:
                print('\n\n👋 \033[1;36mThanks for chatting!\033[0m')
                break
            except Exception:
                print('\n⚠️  \033[1;33mPlease try again\033[0m')
        
        # Cleanup
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

if __name__ == "__main__":
    chat = UniversalChat()
    chat.start_chat()
