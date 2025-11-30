import socket,ssl,random,threading,time,os,datetime,sys

# Ultimate banner
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

# Generate cool nickname
names = ['Phantom','Raven','Viper','Wolf','Ghost','Falcon','Orion','Zenith','Nova','Blaze']
titles = ['Agent','Operative','Soldier','Scout','Sniper','Ranger','Cadet','Major','Captain','Chief']
nick = f"{random.choice(titles)}_{random.choice(names)}{random.randint(10,99)}"

print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{nick}\033[0m')
print('🌐 \033[1;33mINITIATING GLOBAL CONNECTION...\033[0m')

# Connection animation
for i in range(8):
    for char in ['⡿','⣟','⣯','⣷','⣾','⣽','⣻','⢿']:
        print(f'\r🛰️  \033[1;34mCONNECTING {char}\033[0m', end='', flush=True)
        time.sleep(0.1)

# Try multiple IRC servers
servers = [
    ('irc.libera.chat', 6667, False, 'LiberaChat'),
    ('irc.oftc.net', 6667, False, 'OFTC'),
    ('chat.freenode.net', 6667, False, 'Freenode'),
]

sock = None
connected = False
current_server = ""

for server, port, use_ssl, name in servers:
    try:
        print(f'\r🔗 Trying {name}...', end='')
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
            current_server = name
            print('\r✅ \033[1;32mCONNECTED! REAL-TIME CHAT ACTIVE:\033[0m\n')
            break
        else:
            sock.close()
            sock = None
            print('\r❌ Failed', end='')
    except Exception as e:
        if sock: sock.close()
        sock = None
        print('\r❌ Failed', end='')

if not connected:
    print('\r💡 \033[1;33mLOCAL MODE - Find friends to join #CodeArmy!\033[0m\n')

message_count = 0

def receive_messages():
    if not connected: return
    buffer = ""
    global message_count
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
                            message_count += 1
                            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                            
                            if sender != nick:
                                colors = ['32','33','35','36','91','92','93','94','95','96']
                                color = colors[hash(sender) % len(colors)]
                                icons = ['🎯','💬','⚡','🔥','🌟','💫','🎮','🚀']
                                icon = icons[message_count % len(icons)]
                                print(f'\033[1;{color}m[{timestamp}] {icon} {sender}:\033[0m {message}')
                    elif 'JOIN #CodeArmy' in line and nick not in line:
                        sender = line.split('!')[0][1:]
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                        print(f'🟢 \033[1;32m[{timestamp}] {sender} joined\033[0m')
                    elif 'PART #CodeArmy' in line:
                        sender = line.split('!')[0][1:]
                        timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                        print(f'🔴 \033[1;31m[{timestamp}] {sender} left\033[0m')
                    elif 'PING' in line:
                        ping_msg = line.split('PING :')[-1]
                        sock.send(f"PONG :{ping_msg}\r\n".encode())
        except: break

if connected:
    threading.Thread(target=receive_messages, daemon=True).start()
    sock.send(f"PRIVMSG #CodeArmy :🚀 Ultimate chat engaged!\r\n".encode())

while True:
    try:
        msg = input('\033[1;37m➤ \033[0m').strip()
        if msg.startswith('/nick '):
            new_nick = msg[6:].strip()
            if new_nick:
                if connected: sock.send(f"NICK {new_nick}\r\n".encode())
                old_nick = nick
                nick = new_nick
                print(f'🆔 \033[1;33m{old_nick} → {new_nick}\033[0m')
        elif msg == '/help':
            print('\033[1;34mCommands: /nick, /status, /help, /exit\033[0m')
        elif msg == '/status':
            status = f"🟢 {current_server}" if connected else "🔴 LOCAL"
            print(f'📊 \033[1;36mStatus: {status} | Messages: {message_count}\033[0m')
        elif msg in ['/exit','/quit']: break
        elif msg:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            if connected:
                sock.send(f"PRIVMSG #CodeArmy :{msg}\r\n".encode())
                print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {msg}')
            else:
                print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
    except KeyboardInterrupt: break

if connected and sock: sock.close()
print('\n👋 \033[1;36mUltimate chat session ended\033[0m')
