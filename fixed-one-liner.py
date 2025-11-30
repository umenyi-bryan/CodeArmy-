import socket,ssl,random,threading,time,os,datetime,sys,select

# Fixed banner that won't get cut off
os.system('clear')
print('\033[1;36m')
print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
print('\033[1;35m')
print('    ╔══════════════════════════════════════╗')
print('    ║         S U P E R  C H A T          ║')
print('    ║    A N O N Y M O U S • G L O B A L  ║')
print('    ╚══════════════════════════════════════╝')
print('\033[0m')

# Generate cool nickname
prefixes = ['Ghost','Raven','Viper','Wolf','Phantom','Falcon','Steel','Shadow']
suffixes = ['Reaper','Strike','Fang','Blade','Sight','Watch','Guard','Hunter']
nick = f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.randint(100,999)}"

print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{nick}\033[0m')
print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
print('🛰️  \033[1;34mINITIATING GLOBAL CONNECTION...\033[0m\n')

# Enhanced connection animation
for i in range(3):
    for status in ['SCANNING', 'ENCRYPTING', 'CONNECTING']:
        for char in ['⡿','⣟','⣯','⣷','⣾','⣽','⣻','⢿']:
            print(f'\r   {status} {char}', end='', flush=True)
            time.sleep(0.1)
print('\r   CONNECTION SEQUENCE COMPLETE ✅')

# Enhanced server list
servers = [
    ('irc.libera.chat', 6667, False, 'LiberaChat'),
    ('irc.libera.chat', 6697, True, 'LiberaChat SSL'),
    ('irc.oftc.net', 6667, False, 'OFTC'),
    ('irc.hackint.org', 6697, True, 'HackInt'),
    ('chat.freenode.net', 6667, False, 'Freenode'),
]

sock = None
connected = False
current_server = ""
message_count = 0

print('\n🔍 Testing global networks...')
for server, port, use_ssl, name in servers:
    try:
        print(f'   🎯 {name}...', end='', flush=True)
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
        
        # Better connection verification
        start_time = time.time()
        while time.time() - start_time < 8:
            ready = select.select([sock], [], [], 1)
            if ready[0]:
                response = sock.recv(1024).decode('utf-8', errors='ignore')
                if '001' in response or 'Welcome' in response:
                    connected = True
                    current_server = name
                    print(' ✅')
                    break
                elif 'PING' in response:
                    ping_msg = response.split('PING :')[-1].split('\n')[0]
                    sock.send(f"PONG :{ping_msg}\r\n".encode())
        
        if connected:
            print(f'\n🎉 \033[1;32mCONNECTED TO {name}!\033[0m')
            print('💬 \033[1;32mREAL-TIME GLOBAL CHAT ACTIVE\033[0m\n')
            break
        else:
            sock.close()
            sock = None
            print(' ❌')
    except Exception as e:
        if sock: 
            sock.close()
            sock = None
        print(' ❌')

if not connected:
    print('\n💡 \033[1;33mENHANCED LOCAL MODE ACTIVATED\033[0m')
    print('🔶 \033[1;33mYou can chat locally - invite others to #CodeArmy!\033[0m\n')

def super_receiver():
    if not connected: return
    buffer = ""
    global message_count
    while True:
        try:
            ready = select.select([sock], [], [], 1)
            if ready[0]:
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
    threading.Thread(target=super_receiver, daemon=True).start()
    sock.send(f"PRIVMSG #CodeArmy :🚀 Super chat connected! Type /help for commands\r\n".encode())

while True:
    try:
        msg = input('\033[1;37m💬 ➤ \033[0m').strip()
        if msg.startswith('/nick '):
            new_nick = msg[6:].strip()
            if new_nick:
                if connected: 
                    sock.send(f"NICK {new_nick}\r\n".encode())
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
print('\n👋 \033[1;36mSuper chat session complete\033[0m')
