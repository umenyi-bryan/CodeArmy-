import socket,ssl,random,threading,time,os,datetime,sys,select

# Robust banner
os.system('clear')
print('\033[1;36m')
print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
print('\033[1;35m')
print('    ╔══════════════════════════════════════╗')
print('    ║         R O B U S T  C H A T        ║')
print('    ║    A U T O - R E C O N N E C T      ║')
print('    ╚══════════════════════════════════════╝')
print('\033[0m')

# Generate nickname
prefixes = ['Ghost','Raven','Viper','Wolf','Phantom','Falcon','Steel','Shadow']
suffixes = ['Reaper','Strike','Fang','Blade','Sight','Watch','Guard','Hunter']
nick = f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.randint(100,999)}"

print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{nick}\033[0m')
print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
print('🛰️  \033[1;34mESTABLISHING ROBUST CONNECTION...\033[0m\n')

# Server list
servers = [
    ('irc.libera.chat', 6667, False, 'LiberaChat'),
    ('irc.libera.chat', 6697, True, 'LiberaChat SSL'),
    ('irc.oftc.net', 6667, False, 'OFTC'),
    ('irc.hackint.org', 6697, True, 'HackInt'),
]

sock = None
connected = False
current_server = ""
message_count = 0
reconnect_attempts = 0
max_reconnect_attempts = 3
active = True

def handle_connection_lost():
    global connected, sock, reconnect_attempts
    if connected:
        print(f'\n🔌 \033[1;31mConnection to {current_server} lost\033[0m')
        connected = False
    if sock:
        try:
            sock.close()
        except:
            pass
        sock = None

def send_irc_command(command):
    global sock, connected
    if sock and connected:
        try:
            sock.send(f"{command}\r\n".encode('utf-8'))
            return True
        except (BrokenPipeError, ConnectionResetError, OSError):
            handle_connection_lost()
            return False
        except Exception:
            return False
    return False

def handle_ping(message):
    try:
        if 'PING' in message:
            ping_msg = message.split('PING :')[-1].split('\n')[0]
            send_irc_command(f"PONG :{ping_msg}")
    except:
        pass

print('🔍 Testing networks...')
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
        send_irc_command(f"NICK {nick}")
        send_irc_command(f"USER {nick} 0 * :{nick}")
        send_irc_command(f"JOIN #CodeArmy")
        
        # Wait for welcome
        welcome_received = False
        start_time = time.time()
        while time.time() - start_time < 8 and not welcome_received:
            ready = select.select([sock], [], [], 1)
            if ready[0]:
                try:
                    response = sock.recv(1024).decode('utf-8', errors='ignore')
                    if response:
                        if '001' in response or 'Welcome' in response:
                            welcome_received = True
                        if 'PING' in response:
                            handle_ping(response)
                except socket.timeout:
                    continue
        
        if welcome_received:
            connected = True
            current_server = name
            reconnect_attempts = 0
            print(' ✅')
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

if connected:
    print(f'\n🎉 \033[1;32mCONNECTED TO {current_server}!\033[0m')
    print('💬 \033[1;32mROBUST CHAT ACTIVE • AUTO-RECONNECT ENABLED\033[0m\n')
else:
    print('\n💡 \033[1;33mLOCAL MODE • AUTO-RECONNECT WILL ATTEMPT\033[0m\n')

def robust_receiver():
    global sock, connected, message_count, active
    buffer = ""
    last_ping = time.time()
    
    while active:
        try:
            if not connected:
                time.sleep(1)
                continue
            
            ready = select.select([sock], [], [], 1)
            if ready[0]:
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
                                handle_ping(line)
                        
                        last_ping = time.time()
                    else:
                        handle_connection_lost()
                except (ConnectionResetError, BrokenPipeError, OSError):
                    handle_connection_lost()
                except Exception:
                    pass
            
            # Prevent timeout
            if connected and time.time() - last_ping > 120:
                send_irc_command(f"PING :{int(time.time())}")
                last_ping = time.time()
                
        except Exception:
            pass

def attempt_reconnect():
    global sock, connected, current_server, reconnect_attempts
    if reconnect_attempts >= max_reconnect_attempts:
        return False
    
    reconnect_attempts += 1
    print(f'🔄 Reconnect attempt {reconnect_attempts}/{max_reconnect_attempts}...')
    
    for server, port, use_ssl, name in servers:
        try:
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
            send_irc_command(f"NICK {nick}")
            send_irc_command(f"USER {nick} 0 * :{nick}")
            send_irc_command(f"JOIN #CodeArmy")
            
            # Quick welcome check
            start_time = time.time()
            while time.time() - start_time < 5:
                ready = select.select([sock], [], [], 1)
                if ready[0]:
                    response = sock.recv(1024).decode('utf-8', errors='ignore')
                    if '001' in response or 'Welcome' in response:
                        connected = True
                        current_server = name
                        reconnect_attempts = 0
                        return True
                    elif 'PING' in response:
                        handle_ping(response)
            
        except Exception:
            if sock:
                sock.close()
                sock = None
    
    return False

# Start receiver thread
if connected:
    threading.Thread(target=robust_receiver, daemon=True).start()
    send_irc_command(f"PRIVMSG #CodeArmy :🚀 Robust chat connected!")

# Main loop
while active:
    try:
        msg = input('\033[1;37m💬 ➤ \033[0m').strip()
        
        if msg.startswith('/nick '):
            new_nick = msg[6:].strip()
            if new_nick:
                if connected:
                    send_irc_command(f"NICK {new_nick}")
                nick = new_nick
                print(f'🆔 \033[1;33m{nick}\033[0m')
        elif msg == '/help':
            print('\033[1;34mCommands: /nick, /status, /reconnect, /help, /exit\033[0m')
        elif msg == '/status':
            status = f"🟢 {current_server}" if connected else "🔴 DISCONNECTED"
            print(f'📊 \033[1;36mStatus: {status} | Messages: {message_count}\033[0m')
        elif msg == '/reconnect':
            print('🔄 Manual reconnect...')
            attempt_reconnect()
        elif msg in ['/exit','/quit']:
            break
        elif msg:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            if connected:
                if send_irc_command(f"PRIVMSG #CodeArmy :{msg}"):
                    print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {msg}')
                else:
                    print(f'   \033[1;31m[{timestamp}] ❌ FAILED\033[0m')
            else:
                if reconnect_attempts < max_reconnect_attempts:
                    if attempt_reconnect():
                        if send_irc_command(f"PRIVMSG #CodeArmy :{msg}"):
                            print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {msg}')
                        else:
                            print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                    else:
                        print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                else:
                    print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                    
    except KeyboardInterrupt:
        print('\n\n🔴 SHUTTING DOWN...')
        break
    except Exception as e:
        print(f'\n⚠️  Error: {e}')
        continue

active = False
if sock: 
    try: sock.close()
    except: pass
print('\n👋 \033[1;36mChat ended\033[0m')
