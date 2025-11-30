import socket,ssl,random,threading,time,os,datetime

# Simple banner
os.system('clear')
print('\033[1;36m')
print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
print('\033[1;35m')
print('    ╔══════════════════════════════════════╗')
print('    ║           C H A T  N O W            ║')
print('    ║      S I M P L E • R E A L          ║')
print('    ╚══════════════════════════════════════╝')
print('\033[0m')

# Generate name
names = ['Ghost','Raven','Viper','Wolf','Phantom','Falcon','Steel','Shadow']
suffixes = ['Reaper','Strike','Fang','Blade','Sight','Watch','Guard','Hunter']
nick = f"{random.choice(names)}_{random.choice(suffixes)}{random.randint(100,999)}"

print(f'👤 \033[1;33mYOU:\033[0m \033[1;36m{nick}\033[0m')
print(f'🌐 \033[1;33mROOM:\033[0m \033[1;35m#CodeArmy\033[0m')
print('🔗 Connecting...', end='', flush=True)

# Simple connection
sock = None
connected = False
servers = [('irc.libera.chat', 6667, False), ('irc.libera.chat', 6697, True)]

for server, port, use_ssl in servers:
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
        sock.send(f"NICK {nick}\r\n".encode())
        sock.send(f"USER {nick} 0 * :{nick}\r\n".encode())
        sock.send(f"JOIN #CodeArmy\r\n".encode())
        
        # Wait a bit for connection
        time.sleep(2)
        connected = True
        print('\r✅ \033[1;32mConnected! Start chatting:\033[0m\n')
        break
        
    except Exception:
        if sock:
            try:
                sock.close()
            except:
                pass
            sock = None
        continue

if not connected:
    print('\r💡 \033[1;33mLocal mode - type to practice!\033[0m\n')

message_count = 0

def receive_messages():
    global connected, message_count
    if not connected:
        return
        
    buffer = ""
    while connected:
        try:
            sock.settimeout(1)
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
                            text = parts[1]
                            if sender != nick:
                                message_count += 1
                                timestamp = datetime.datetime.now().strftime('%H:%M:%S')
                                colors = ['32','33','35','36','92','93','94','95']
                                color = colors[hash(sender) % len(colors)]
                                print(f'\033[1;{color}m[{timestamp}] {sender}:\033[0m {text}')
                    
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
                        
        except socket.timeout:
            continue
        except Exception:
            connected = False
            break

# Start receiving
if connected:
    threading.Thread(target=receive_messages, daemon=True).start()
    sock.send(f"PRIVMSG #CodeArmy :👋 Hello from Chat Now!\r\n".encode())

# Chat loop
while True:
    try:
        msg = input('\033[1;37m💬 ➤ \033[0m').strip()
        
        if msg.startswith('/nick '):
            new_nick = msg[6:].strip()
            if new_nick:
                if connected:
                    sock.send(f"NICK {new_nick}\r\n".encode())
                nick = new_nick
                print(f'🆔 \033[1;33m{new_nick}\033[0m')
        elif msg == '/help':
            print('\033[1;34mType to chat • /nick [name] • /exit\033[0m')
        elif msg == '/status':
            status = "🟢 Connected" if connected else "🔴 Local"
            print(f'📊 \033[1;36m{status}\033[0m')
        elif msg in ['/exit','/quit']:
            break
        elif msg:
            timestamp = datetime.datetime.now().strftime('%H:%M:%S')
            if connected:
                try:
                    sock.send(f"PRIVMSG #CodeArmy :{msg}\r\n".encode())
                    print(f'   \033[1;36m[{timestamp}] YOU:\033[0m {msg}')
                except:
                    connected = False
                    print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
            else:
                print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                
    except KeyboardInterrupt:
        break
    except Exception:
        print('⚠️  Please try again')

if connected and sock:
    try:
        sock.close()
    except:
        pass

print('\n👋 \033[1;36mChat ended\033[0m')
