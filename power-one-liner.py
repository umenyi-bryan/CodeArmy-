import socket,ssl,random,threading,time,os,datetime,sys,select

# Power banner
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

# Generate nickname
prefixes = ['Ghost','Raven','Viper','Wolf','Phantom','Falcon','Steel','Shadow','Cyber','Neo']
suffixes = ['Reaper','Strike','Fang','Blade','Sight','Watch','Guard','Hunter','Byte','Code']
nick = f"{random.choice(prefixes)}_{random.choice(suffixes)}{random.randint(100,999)}"

print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{nick}\033[0m')
print(f'🌐 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
print('🛰️  \033[1;34mPOWERING UP GLOBAL CONNECTION SYSTEM...\033[0m\n')

# Enhanced server list with priorities
servers = [
    ('irc.libera.chat', 6667, False, 'LiberaChat', 1),
    ('irc.libera.chat', 6697, True, 'LiberaChat SSL', 1),
    ('irc.oftc.net', 6667, False, 'OFTC', 2),
    ('irc.hackint.org', 6697, True, 'HackInt', 2),
    ('open.ircnet.net', 6667, False, 'IRCNet', 3),
    ('chat.freenode.net', 6667, False, 'Freenode', 3),
]

sock = None
connected = False
current_server = ""
message_count = 0
reconnect_attempts = 0
max_reconnect_attempts = 5
active = True
last_activity = time.time()

def handle_connection_lost(reason="Connection lost"):
    global connected, sock, reconnect_attempts
    if connected:
        print(f'\n🔌 \033[1;31m{reason}\033[0m')
        connected = False
    if sock:
        try:
            sock.close()
        except:
            pass
        sock = None

def send_irc_command(command):
    global sock, connected, last_activity
    if sock and connected:
        try:
            sock.send(f"{command}\r\n".encode('utf-8'))
            last_activity = time.time()
            return True
        except (BrokenPipeError, ConnectionResetError, OSError, socket.timeout):
            handle_connection_lost("Send failed")
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

print('🌐 Scanning global networks...\n')
servers.sort(key=lambda x: x[4])  # Sort by priority

for server, port, use_ssl, name, priority in servers:
    try:
        priority_icon = '🟢' if priority == 1 else '🟡' if priority == 2 else '🔴'
        print(f'   {priority_icon} {name}', end='', flush=True)
        
        if use_ssl:
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock = context.wrap_socket(sock, server_hostname=server)
        else:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        timeout = 8 if priority == 1 else 12
        sock.settimeout(timeout)
        sock.connect((server, port))
        send_irc_command(f"NICK {nick}")
        send_irc_command(f"USER {nick} 0 * :{nick}")
        send_irc_command(f"JOIN #CodeArmy")
        
        # Enhanced connection check
        welcome_received = False
        start_time = time.time()
        dots = 0
        
        while time.time() - start_time < timeout and not welcome_received:
            print('.', end='', flush=True)
            dots += 1
            
            ready = select.select([sock], [], [], 0.5)
            if ready[0]:
                try:
                    response = sock.recv(1024).decode('utf-8', errors='ignore')
                    if response:
                        if any(msg in response for msg in ['001', 'Welcome', 'MODE']):
                            welcome_received = True
                        if 'PING' in response:
                            handle_ping(response)
                except socket.timeout:
                    continue
            
            if dots > 6:
                print('\r' + ' ' * 50 + '\r', end='')
                print(f'   {priority_icon} {name}', end='')
                dots = 0
        
        if welcome_received:
            connected = True
            current_server = name
            reconnect_attempts = 0
            last_activity = time.time()
            print(' ✅')
            break
        else:
            sock.close()
            sock = None
            print(' ❌')
    except Exception as e:
        error_msg = str(e)
        if 'Connection refused' in error_msg:
            print(' 🔄')
        elif 'Network is unreachable' in error_msg:
            print(' 🌐')
        elif 'timed out' in error_msg:
            print(' ⏰')
        else:
            print(' ❌')
        
        if sock:
            sock.close()
            sock = None

if connected:
    print(f'\n🎉 \033[1;32mPOWER CHAT CONNECTED TO {current_server}!\033[0m')
    print('💬 \033[1;32mGLOBAL REAL-TIME CHAT ACTIVE\033[0m\n')
else:
    print('\n💡 \033[1;33mPOWER CHAT READY (Local Mode)\033[0m')
    print('🔶 \033[1;33mAuto-reconnect enabled • Type to chat\033[0m\n')

def power_receiver():
    global sock, connected, message_count, active, last_activity
    buffer = ""
    last_keepalive = time.time()
    
    while active:
        try:
            if not connected:
                time.sleep(1)
                continue
            
            # Keep-alive
            if time.time() - last_activity > 180:
                send_irc_command(f"PING :keepalive_{int(time.time())}")
                last_activity = time.time()
            
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
                        
                        last_activity = time.time()
                    else:
                        handle_connection_lost("Server closed")
                except (ConnectionResetError, BrokenPipeError, OSError):
                    handle_connection_lost("Network error")
                except Exception:
                    pass
            
            # Periodic PING
            if connected and time.time() - last_keepalive > 120:
                send_irc_command(f"PING :periodic_{int(time.time())}")
                last_keepalive = time.time()
                
        except Exception:
            pass

def attempt_power_reconnect():
    global sock, connected, current_server, reconnect_attempts, last_activity
    if reconnect_attempts >= max_reconnect_attempts:
        return False
    
    reconnect_attempts += 1
    delay = min(2 ** reconnect_attempts, 10)
    print(f'🔄 Reconnect in {delay}s ({reconnect_attempts}/{max_reconnect_attempts})...')
    time.sleep(delay)
    
    for server, port, use_ssl, name, priority in servers:
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
                        last_activity = time.time()
                        return True
                    elif 'PING' in response:
                        handle_ping(response)
            
        except Exception:
            if sock:
                sock.close()
                sock = None
    
    return False

# Start receiver
if connected:
    threading.Thread(target=power_receiver, daemon=True).start()
    send_irc_command(f"PRIVMSG #CodeArmy :🚀 Power chat connected!")

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
            print('\033[1;34mCommands: /nick, /status, /reconnect, /servers, /help, /exit\033[0m')
        elif msg == '/status':
            status = f"🟢 {current_server}" if connected else "🔴 DISCONNECTED"
            print(f'📊 \033[1;36mStatus: {status} | Messages: {message_count}\033[0m')
            print(f'🔁 \033[1;36mReconnects: {reconnect_attempts}/{max_reconnect_attempts}\033[0m')
        elif msg == '/servers':
            print('\n🌐 Available servers:')
            for server, port, use_ssl, name, priority in servers:
                icon = '🟢' if priority == 1 else '🟡' if priority == 2 else '🔴'
                ssl_info = " (SSL)" if use_ssl else ""
                print(f'   {icon} {name}{ssl_info}')
        elif msg == '/reconnect':
            print('🔄 Force reconnecting...')
            attempt_power_reconnect()
        elif msg in ['/exit','/quit']:
            break
        elif msg:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            if connected:
                if send_irc_command(f"PRIVMSG #CodeArmy :{msg}"):
                    print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {msg}')
                else:
                    print(f'   \033[1;31m[{timestamp}] ❌ Failed\033[0m')
            else:
                print('🔄 Connection needed...')
                if attempt_power_reconnect():
                    if send_irc_command(f"PRIVMSG #CodeArmy :{msg}"):
                        print(f'   \033[1;36m[{timestamp}] 🗨️  YOU:\033[0m {msg}')
                    else:
                        print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                else:
                    print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                    
    except KeyboardInterrupt:
        print('\n\n🔴 POWERING DOWN...')
        break
    except Exception as e:
        print(f'\n⚠️  Error: {e}')
        continue

active = False
if sock: 
    try: sock.close()
    except: pass
print('\n👋 \033[1;36mPower chat ended\033[0m')
