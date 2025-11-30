#!/usr/bin/env python3
import socket,ssl,random,threading,time,os,datetime,sys

# Banner
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

nick = f"User_{random.randint(1000,9999)}"
print(f'👤 \033[1;33mUSER:\033[0m \033[1;36m{nick}\033[0m')
print('🌐 \033[1;33mConnecting to global network...\033[0m')

# Try multiple IRC servers
servers = [
    ('irc.libera.chat', 6667, False),
    ('irc.oftc.net', 6667, False),
    ('chat.freenode.net', 6667, False),
]

sock = None
connected = False
current_server = ""

for server, port, use_ssl in servers:
    try:
        print(f'🔗 Trying {server}...', end='')
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = context.wrap_socket(sock, server_hostname=server)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        sock.settimeout(10)
        sock.connect((server, port))
        sock.send(f"NICK {nick}\r\n".encode())
        sock.send(f"USER {nick} 0 * :{nick}\r\n".encode())
        sock.send(f"JOIN #CodeArmy\r\n".encode())
        
        # Check connection
        response = sock.recv(1024).decode('utf-8', errors='ignore')
        if '001' in response or 'Welcome' in response:
            connected = True
            current_server = server
            print('\r✅ \033[1;32mCONNECTED! Type to chat:\033[0m\n')
            break
        else:
            sock.close()
            sock = None
            print('\r❌ Failed')
    except Exception as e:
        if sock: sock.close()
        sock = None
        print('\r❌ Failed')

if not connected:
    print('💡 \033[1;33mRunning in local mode - Find friends to join!\033[0m\n')

def receive_messages():
    if not connected: return
    buffer = ""
    while True:
        try:
            data = sock.recv(4096).decode('utf-8', errors='ignore')
            if data:
                buffer += data
                lines = buffer.split('\n')
                buffer = lines[-1]
                
                for line in lines[:-1]:
                    line = line.strip()
                    if 'PRIVMSG #CodeArmy :' in line:
                        parts = line.split('PRIVMSG #CodeArmy :')
                        if len(parts) > 1:
                            sender = parts[0].split('!')[0][1:]
                            message = parts[1]
                            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                            if sender != nick:
                                print(f'\033[1;32m[{timestamp}] {sender}:\033[0m {message}')
                    elif 'PING' in line:
                        ping_msg = line.split('PING :')[-1]
                        sock.send(f"PONG :{ping_msg}\r\n".encode())
        except: break

if connected:
    threading.Thread(target=receive_messages, daemon=True).start()
    sock.send(f"PRIVMSG #CodeArmy :🚀 Joined universal chat!\r\n".encode())

while True:
    try:
        msg = input('\033[1;37m➤ \033[0m').strip()
        if msg.startswith('/nick '):
            new_nick = msg[6:].strip()
            if new_nick:
                if connected: sock.send(f"NICK {new_nick}\r\n".encode())
                nick = new_nick
                print(f'🆔 {new_nick}')
        elif msg in ['/exit', '/quit']: break
        elif msg == '/status':
            status = f"🟢 {current_server}" if connected else "🔴 LOCAL"
            print(f'📊 {status}')
        elif msg:
            if connected:
                sock.send(f"PRIVMSG #CodeArmy :{msg}\r\n".encode())
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                print(f'   \033[1;36m[{timestamp}] YOU:\033[0m {msg}')
            else:
                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
    except KeyboardInterrupt: break

if connected and sock: sock.close()
print('\n👋 \033[1;36mChat ended\033[0m')
