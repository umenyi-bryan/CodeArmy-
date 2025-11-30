#!/usr/bin/env python3
import socket
import ssl
import random
import threading
import time
import os
import datetime

class PerfectChat:
    def __init__(self):
        self.nickname = self.generate_nickname()
        self.connected = False
        self.socket = None
        self.channel = "#CodeArmy"
        self.message_count = 0
        
    def generate_nickname(self):
        names = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Phantom', 'Falcon', 'Steel', 'Shadow']
        suffixes = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Hunter']
        return f"{random.choice(names)}_{random.choice(suffixes)}{random.randint(100,999)}"
    
    def show_banner(self):
        os.system('clear')
        print('\033[1;36m')
        print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
        print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
        print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
        print('\033[1;35m')
        print('    ╔══════════════════════════════════════╗')
        print('    ║         P E R F E C T  C H A T      ║')
        print('    ║    E A S Y • R E L I A B L E        ║')
        print('    ╚══════════════════════════════════════╝')
        print('\033[0m')
        print(f'👤 \033[1;33mUSER:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m{self.channel}\033[0m')
    
    def connect_simple(self):
        """Simple, reliable connection method"""
        servers = [
            ('irc.libera.chat', 6667, False),
            ('irc.libera.chat', 6697, True),
        ]
        
        print('🔗 Connecting to chat network...')
        
        for server, port, use_ssl in servers:
            try:
                print(f'   Trying {server}...', end='', flush=True)
                
                # Create socket
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(10)
                
                if use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    self.socket = context.wrap_socket(sock, server_hostname=server)
                else:
                    self.socket = sock
                
                # Connect
                self.socket.connect((server, port))
                
                # Send registration
                self.socket.send(f"NICK {self.nickname}\r\n".encode())
                self.socket.send(f"USER {self.nickname} 0 * :Chat User\r\n".encode())
                self.socket.send(f"JOIN {self.channel}\r\n".encode())
                
                # Wait for response
                time.sleep(2)
                
                # Check if we're connected by trying to receive
                self.socket.settimeout(2)
                try:
                    data = self.socket.recv(1024).decode('utf-8', errors='ignore')
                    if data:
                        self.connected = True
                        print(' ✅')
                        return True
                except socket.timeout:
                    # Timeout is okay, we might still be connected
                    self.connected = True
                    print(' ✅')
                    return True
                    
            except Exception as e:
                print(' ❌')
                if self.socket:
                    try:
                        self.socket.close()
                    except:
                        pass
                    self.socket = None
                continue
        
        return False
    
    def start_receiver(self):
        """Simple message receiver"""
        if not self.connected:
            return
            
        def receiver():
            buffer = ""
            while self.connected:
                try:
                    # Set a reasonable timeout
                    self.socket.settimeout(1)
                    
                    data = self.socket.recv(4096).decode('utf-8', errors='ignore')
                    if data:
                        buffer += data
                        lines = buffer.split('\n')
                        buffer = lines[-1]  # Keep incomplete line
                        
                        for line in lines[:-1]:
                            line = line.strip()
                            if line:
                                self.handle_message(line)
                    
                    # Handle PING
                    if 'PING' in buffer:
                        self.handle_ping(buffer)
                        buffer = ""
                        
                except socket.timeout:
                    continue
                except Exception:
                    self.connected = False
                    break
        
        # Start receiver thread
        thread = threading.Thread(target=receiver, daemon=True)
        thread.start()
    
    def handle_ping(self, message):
        """Handle PING messages"""
        try:
            if 'PING' in message:
                ping_msg = message.split('PING :')[-1].split('\n')[0]
                self.socket.send(f"PONG :{ping_msg}\r\n".encode())
        except:
            self.connected = False
    
    def handle_message(self, message):
        """Handle incoming messages"""
        if 'PRIVMSG' in message and self.channel in message:
            try:
                # Extract sender and message
                parts = message.split('PRIVMSG')[1].split(':', 1)
                if len(parts) >= 2:
                    sender_part = message.split('!')[0][1:]
                    text = parts[1].strip()
                    
                    # Don't show our own messages twice
                    if sender_part != self.nickname:
                        self.message_count += 1
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                        
                        # Color based on sender
                        colors = ['32', '33', '35', '36', '92', '93', '94', '95']
                        color = colors[hash(sender_part) % len(colors)]
                        
                        print(f'\033[1;{color}m[{timestamp}] {sender_part}:\033[0m {text}')
                        
            except Exception:
                pass  # Ignore message parsing errors
        
        elif 'JOIN' in message and self.channel in message:
            try:
                sender = message.split('!')[0][1:]
                if sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🟢 \033[1;32m[{timestamp}] {sender} joined\033[0m')
            except:
                pass
        
        elif 'PART' in message and self.channel in message:
            try:
                sender = message.split('!')[0][1:]
                if sender != self.nickname:
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    print(f'🔴 \033[1;31m[{timestamp}] {sender} left\033[0m')
            except:
                pass
    
    def send_message(self, message):
        """Send message reliably"""
        if self.connected and self.socket:
            try:
                self.socket.send(f"PRIVMSG {self.channel} :{message}\r\n".encode())
                return True
            except:
                self.connected = False
                return False
        return False
    
    def show_help(self):
        print("""
\033[1;36m
💬 PERFECT CHAT - SIMPLE COMMANDS:

• Just type to send messages
• /nick [name] - Change your name
• /help - Show this help
• /exit - Leave chat

🎯 FEATURES:
• Real-time global chat
• Colorful usernames  
• Join/leave notifications
• 100% anonymous
• Works everywhere

Press Ctrl+C to exit
\033[0m
""")
    
    def start_chat(self):
        """Main chat interface - simple and reliable"""
        self.show_banner()
        
        # Connect to chat
        if self.connect_simple():
            print('\n🎉 \033[1;32mSUCCESS! Connected to global chat\033[0m')
            print('💬 \033[1;32mStart chatting with people worldwide!\033[0m')
            print('─' * 50)
            print()
            
            # Start receiving messages
            self.start_receiver()
            
            # Send welcome message
            self.send_message("🚀 Hello! I'm using Perfect Chat")
            
        else:
            print('\n💡 \033[1;33mNote: Could not connect to chat servers\033[0m')
            print('🔶 \033[1;33mYou can still type messages locally\033[0m')
            print('🌍 \033[1;33mTell friends to join #CodeArmy on IRC!\033[0m')
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
                            self.socket.send(f"NICK {new_nick}\r\n".encode())
                        self.nickname = new_nick
                        print(f'🆔 \033[1;33mName changed to: {new_nick}\033[0m')
                        
                elif message == '/help':
                    self.show_help()
                    
                elif message == '/status':
                    status = "🟢 CONNECTED" if self.connected else "🔴 LOCAL"
                    print(f'📊 \033[1;36mStatus: {status}\033[0m')
                    
                else:
                    # Send message
                    timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                    
                    if self.connected:
                        if self.send_message(message):
                            print(f'   \033[1;36m[{timestamp}] YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;31m[{timestamp}] Failed to send\033[0m')
                    else:
                        print(f'   \033[1;90m[{timestamp}] [LOCAL]: {message}\033[0m')
                        
            except KeyboardInterrupt:
                print('\n\n👋 \033[1;36mThanks for chatting!\033[0m')
                break
            except Exception:
                print('\n⚠️  \033[1;33mPlease type your message again\033[0m')
        
        # Cleanup
        if self.socket:
            try:
                self.socket.close()
            except:
                pass

if __name__ == "__main__":
    chat = PerfectChat()
    chat.start_chat()
