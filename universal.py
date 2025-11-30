import socket,ssl,random,threading,time,os,datetime,sys

# Universal banner
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

# Generate name
names = ['Ghost','Raven','Viper','Wolf','Phantom','Falcon','Steel','Shadow','Cyber','Neo']
suffixes = ['Reaper','Strike','Fang','Blade','Sight','Watch','Guard','Hunter','Byte','Code']
nick = f"{random.choice(names)}_{random.choice(suffixes)}{random.randint(100,999)}"

print(f'👤 \033[1;33mUSER:\033[0m \033[1;36m{nick}\033[0m')
print(f'🌐 \033[1;33mROOM:\033[0m \033[1;35m#CodeArmy\033[0m')
print('🔗 Testing connection methods...\n')

# Multiple connection methods
sock = None
connected = False
method_used = "none"

methods = [
    # Standard IRC
    [('irc.libera.chat', 6667, False), ('irc.libera.chat', 6697, True)],
    # Alternative IRC
    [('irc.oftc.net', 6667, False), ('irc.hackint.org', 6697, True)],
    # Backup IRC
    [('chat.freenode.net', 6667, False), ('open.ircnet.net', 6667, False)]
]

for i, server_group in enumerate(methods):
    method_name = ["Standard", "Alternative", "Backup"][i]
    print(f'   {"🟢" if i==0 else "🟡" if i==1 else "🔴"} {method_name}...', end='', flush=True)
    
    for server, port, use_ssl in server_group:
        try:
            if use_ssl:
                context = ssl.create_default_context()
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock = context.wrap_socket(sock, server_hostname=server)
            else:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            sock.settimeout(15)
            sock.connect((server, port))
            sock.send(f"NICK {nick}\r\n".encode())
            sock.send(f"USER {nick} 0 * :Universal\r\n".encode())
            sock.send(f"JOIN #CodeArmy\r\n".encode())
            
            # Wait and test connection
            time.sleep(3)
            sock.send(f"PING :test\r\n".encode())
            time.sleep(1)
            
            connected = True
            method_used = f"{method_name} ({server})"
            print(' ✅')
            break
            
        except Exception:
            if sock:
                try:
                    sock.close()
                except:
                    pass
                sock = None
            continue
    
    if connected:
        break
    else:
        print(' ❌')

if connected:
    print(f'\n🎉 \033[1;32mConnected via {method_used}!\033[0m')
    print('💬 \033[1;32mUniversal chat active - works for everyone!\033[0m\n')
else:
    print('\n💡 \033[1;33mUniversal chat ready (local mode)\033[0m')
    print('🔶 \033[1;33mType to practice - works across all networks!\033[0m\n')

message_count = 0

def universal_receiver():
    global connected, message_count
    if not connected:
        return
        
    buffer = ""
    last_ping = time.time()
    
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
                                colors = ['32','33','35','36','92','93','94','95','96']
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
                
                last_ping = time.time()
            
            # Keep connection alive
            if time.time() - last_ping > 60:
                sock.send(f"PING :universal\r\n".encode())
                last_ping = time.time()
                
        except socket.timeout:
            continue
        except Exception:
            connected = False
            print('\n⚠️  \033[1;33mConnection lost - try /reconnect\033[0m')
            break

# Start receiver
if connected:
    threading.Thread(target=universal_receiver, daemon=True).start()
    sock.send(f"PRIVMSG #CodeArmy :🌍 Universal chat connected!\r\n".encode())

def try_reconnect():
    global sock, connected, method_used, nick
    print('🔄 Trying all connection methods...')
    
    for i, server_group in enumerate(methods):
        method_name = ["Standard", "Alternative", "Backup"][i]
        
        for server, port, use_ssl in server_group:
            try:
                if sock:
                    try:
                        sock.close()
                    except:
                        pass
                
                if use_ssl:
                    context = ssl.create_default_context()
                    context.check_hostname = False
                    context.verify_mode = ssl.CERT_NONE
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock = context.wrap_socket(sock, server_hostname=server)
                else:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                sock.settimeout(15)
                sock.connect((server, port))
                sock.send(f"NICK {nick}\r\n".encode())
                sock.send(f"USER {nick} 0 * :Universal\r\n".encode())
                sock.send(f"JOIN #CodeArmy\r\n".encode())
                
                time.sleep(3)
                connected = True
                method_used = f"{method_name} ({server})"
                print(f'✅ \033[1;32mReconnected via {method_used}!\033[0m')
                return True
                
            except Exception:
                continue
    
    print('❌ \033[1;31mAll connection methods failed\033[0m')
    return False

# Main loop
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
            print('\033[1;34mType to chat • /nick [name] • /reconnect • /status • /exit\033[0m')
        elif msg == '/status':
            status = f"🟢 {method_used}" if connected else "🔴 DISCONNECTED"
            print(f'📊 \033[1;36mStatus: {status}\033[0m')
            print(f'💬 \033[1;36mMessages: {message_count}\033[0m')
        elif msg == '/reconnect':
            if try_reconnect():
                threading.Thread(target=universal_receiver, daemon=True).start()
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
                    print(f'   \033[1;31m[{timestamp}] ❌ Send failed\033[0m')
                    print('   💡 Try /reconnect')
            else:
                print(f'   \033[1;90m[{timestamp}] [LOCAL]: {msg}\033[0m')
                print('   💡 Use /reconnect to join global chat')
                
    except KeyboardInterrupt:
        break
    except Exception:
        print('⚠️  Please try again')

if connected and sock:
    try:
        sock.close()
    except:
        pass

print('\n👋 \033[1;36mUniversal chat ended\033[0m')
