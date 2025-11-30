#!/usr/bin/env python3
import websocket
import json
import random
import threading
import time
import os
import datetime
import sys
import ssl

class SuperRobustCodeArmy:
    def __init__(self):
        self.nickname = self.generate_nickname()
        self.ws = None
        self.active = True
        self.connected = False
        self.reconnect_attempts = 0
        self.max_reconnect_attempts = 3
        
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
    
    def try_connect_super_robust(self):
        """Super robust connection with multiple fallbacks"""
        connection_methods = [
            # Primary method with SSL context
            lambda: websocket.create_connection(
                "wss://hack.chat/chat-ws", 
                timeout=15,
                sslopt={"cert_reqs": ssl.CERT_NONE}
            ),
            # Alternative without SSL verification
            lambda: websocket.create_connection(
                "wss://hack.chat/chat-ws",
                timeout=15,
                sslopt={"cert_reqs": ssl.CERT_NONE, "check_hostname": False}
            ),
            # Try with different timeout
            lambda: websocket.create_connection(
                "wss://hack.chat/chat-ws",
                timeout=20
            ),
        ]
        
        for i, connect_method in enumerate(connection_methods):
            try:
                print(f'🔄 \033[1;33mConnection attempt {i+1}/{len(connection_methods)}...\033[0m')
                self.ws = connect_method()
                
                # Test the connection by joining
                self.ws.send(json.dumps({
                    "cmd": "join", 
                    "channel": "CodeArmy", 
                    "nick": self.nickname
                }))
                
                # Wait for response to confirm connection works
                response = self.ws.recv()
                data = json.loads(response)
                
                if data.get("cmd") in ["welcome", "onlineSet", "info"]:
                    self.connected = True
                    self.reconnect_attempts = 0
                    return True
                    
            except Exception as e:
                error_msg = str(e)
                print(f'❌ \033[1;31mAttempt {i+1} failed: {error_msg[:50]}...\033[0m')
                if i < len(connection_methods) - 1:
                    time.sleep(2)  # Wait before retry
        
        return False
    
    def show_connection_flow(self):
        print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{self.nickname}\033[0m')
        print(f'📡 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
        print('─' * 55)
        
        if self.try_connect_super_robust():
            print('✅ \033[1;32mSECURE CONNECTION ESTABLISHED\033[0m')
            print('💬 \033[1;32mType to chat • /help for commands • Ctrl+C to exit\033[0m')
            print('─' * 55)
            print()
            return True
        else:
            print('❌ \033[1;31mUNABLE TO ESTABLISH CONNECTION\033[0m')
            print('💡 \033[1;33mTroubleshooting:')
            print('   • The chat server might be temporarily down')
            print('   • Try again in a few minutes')
            print('   • Check https://hack.chat status')
            print('   • You can still chat locally\033[0m')
            print('─' * 55)
            print('🔶 \033[1;33mRunning in LOCAL MODE - Find friends to join #CodeArmy!\033[0m\n')
            return False
    
    def get_timestamp(self):
        return datetime.datetime.now().strftime('%H:%M:%S')
    
    def receive_messages_safe(self):
        """Safe message receiver with comprehensive error handling"""
        while self.active and self.connected:
            try:
                if self.ws:
                    message = self.ws.recv()
                    if message:
                        data = json.loads(message)
                        self.handle_incoming_message(data)
            except websocket.WebSocketConnectionClosedException:
                self.handle_connection_lost()
                break
            except websocket.WebSocketTimeoutException:
                continue  # Just continue on timeout
            except Exception as e:
                if self.active:
                    print(f'⚠️  \033[1;33mNetwork issue: {e}\033[0m')
                break
    
    def handle_incoming_message(self, data):
        """Process incoming messages safely"""
        timestamp = self.get_timestamp()
        
        try:
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
                
            elif data["cmd"] == "info":
                print(f'ℹ️  \033[1;34m[{timestamp}] {data["text"]}\033[0m')
                
        except KeyError as e:
            print(f'⚠️  \033[1;33mMalformed message received\033[0m')
    
    def handle_connection_lost(self):
        """Handle lost connection gracefully"""
        print('\n🔌 \033[1;31mConnection to server lost\033[0m')
        self.connected = False
        if self.reconnect_attempts < self.max_reconnect_attempts:
            print(f'🔄 \033[1;33mAttempting to reconnect ({self.reconnect_attempts + 1}/{self.max_reconnect_attempts})...\033[0m')
            if self.try_connect_super_robust():
                print('✅ \033[1;32mReconnected successfully!\033[0m')
                # Restart message receiver
                receiver = threading.Thread(target=self.receive_messages_safe, daemon=True)
                receiver.start()
            else:
                self.reconnect_attempts += 1
                print('🔶 \033[1;33mContinuing in local mode\033[0m')
        else:
            print('🔶 \033[1;33mMax reconnection attempts reached. Continuing locally.\033[0m')
    
    def send_message_safe(self, text):
        """Send message with comprehensive error handling"""
        if not self.connected:
            return False
        
        try:
            self.ws.send(json.dumps({"cmd": "chat", "text": text}))
            return True
        except websocket.WebSocketConnectionClosedException:
            self.handle_connection_lost()
            return False
        except Exception as e:
            print(f'❌ \033[1;31mSend failed: {e}\033[0m')
            return False
    
    def show_comprehensive_help(self):
        help_text = """
\033[1;34m
╔══════════════════════════════╗
║        C O M M A N D S       ║
╚══════════════════════════════╝

💬 Just type to send a message
🆔 /nick [name] - Change your identity  
🔄 /reconnect - Reconnect to server
📊 /status - Show connection status
❓ /help - Show this help message
🚪 /exit - Leave the chat
🕒 /time - Show current time

CONNECTION STATUS:
🟢 GREEN - Connected to server
🔴 RED - Local mode only
🟡 YELLOW - Attempting reconnect

Press Ctrl+C to exit safely
\033[0m
"""
        print(help_text)
    
    def attempt_reconnect(self):
        """Manual reconnection attempt"""
        print('🔄 \033[1;33mManual reconnection initiated...\033[0m')
        if self.ws:
            try:
                self.ws.close()
            except:
                pass
        
        self.reconnect_attempts = 0
        if self.try_connect_super_robust():
            print('✅ \033[1;32mReconnected successfully!\033[0m')
            # Restart message receiver
            receiver = threading.Thread(target=self.receive_messages_safe, daemon=True)
            receiver.start()
        else:
            print('❌ \033[1;31mReconnection failed\033[0m')
    
    def show_status(self):
        """Show detailed connection status"""
        status = "🟢 CONNECTED" if self.connected else "🔴 LOCAL MODE"
        print(f'📊 \033[1;36mStatus: {status}\033[0m')
        print(f'🎖️  \033[1;36mOperative: {self.nickname}\033[0m')
        print(f'🔢 \033[1;36mReconnect attempts: {self.reconnect_attempts}/{self.max_reconnect_attempts}\033[0m')
        if not self.connected:
            print('💡 \033[1;33mTip: Use /reconnect to try connecting again\033[0m')
    
    def start_chat(self):
        self.show_banner()
        
        # Establish connection
        connection_success = self.show_connection_flow()
        
        # Start message receiver if connected
        if connection_success:
            receiver = threading.Thread(target=self.receive_messages_safe, daemon=True)
            receiver.start()
            
            # Send welcome message
            welcome_messages = [
                "🚀 Secure terminal connection active",
                "🔐 Encrypted channel established", 
                "🌐 Connected to global chat network",
                "💫 Anonymous communications online"
            ]
            self.send_message_safe(random.choice(welcome_messages))
        
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
                        if self.connected:
                            success = self.send_message_safe(f"/nick {new_nick}")
                            if success:
                                old_nick = self.nickname
                                self.nickname = new_nick
                                print(f'🆔 \033[1;33mIDENTITY: {old_nick} → {self.nickname}\033[0m')
                        else:
                            self.nickname = new_nick
                            print(f'🆔 \033[1;33mIDENTITY: {self.nickname}\033[0m')
                            
                elif message == '/help':
                    self.show_comprehensive_help()
                    
                elif message == '/reconnect':
                    self.attempt_reconnect()
                    
                elif message == '/status':
                    self.show_status()
                    
                elif message == '/time':
                    print(f'🕒 \033[1;36mCurrent time: {self.get_timestamp()}\033[0m')
                    
                else:
                    # Regular message
                    if self.connected:
                        success = self.send_message_safe(message)
                        if success:
                            print(f'   \033[1;36m[{self.get_timestamp()}] YOU:\033[0m {message}')
                        else:
                            print(f'   \033[1;90m[{self.get_timestamp()}] [FAILED TO SEND]: {message}\033[0m')
                    else:
                        print(f'   \033[1;90m[{self.get_timestamp()}] [LOCAL MODE]: {message}\033[0m')
                        
            except KeyboardInterrupt:
                print('\n\n🔴 \033[1;31mSAFE SHUTDOWN INITIATED...\033[0m')
                break
                
        # Clean shutdown
        self.active = False
        if self.ws and self.connected:
            try:
                self.ws.close()
            except:
                pass
        print('👋 \033[1;36mSession terminated. Until next time, operative.\033[0m')

if __name__ == "__main__":
    chat = SuperRobustCodeArmy()
    chat.start_chat()
