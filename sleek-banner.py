#!/usr/bin/env python3
import websocket,json,random,threading,time,os

# Sleek ASCII Banner
def show_sleek_banner():
    os.system('clear')
    print('\033[1;36m')  # Cyan color
    print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
    print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
    print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
    print('\033[1;35m')  # Magenta color
    print('    ╔══════════════════════════════════════╗')
    print('    ║    A N O N Y M O U S   C H A T      ║')
    print('    ║      T E R M I N A L   S P A C E    ║')
    print('    ╚══════════════════════════════════════╝')
    print('\033[0m')

# Generate cool nickname
first_names = ['Phantom', 'Raven', 'Viper', 'Wolf', 'Ghost', 'Steel', 'Iron', 'Shadow']
last_names = ['Reaper', 'Strike', 'Fang', 'Blade', 'Sight', 'Watch', 'Guard', 'Wraith']
nickname = f"{random.choice(first_names)}_{random.choice(last_names)}{random.randint(10,99)}"

show_sleek_banner()
print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{nickname}\033[0m')
print(f'📡 \033[1;33mCHANNEL:\033[0m \033[1;35m#CodeArmy\033[0m')
print(f'🌐 \033[1;33mSTATUS:\033[0m Connecting to secure channel...')

# Cool loading animation
for i in range(3):
    for char in ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']:
        print(f'\r🔒 \033[1;33mSECURING CONNECTION {char}\033[0m', end='', flush=True)
        time.sleep(0.1)

print('\r✅ \033[1;32mCONNECTION SECURED\033[0m')
print('─' * 55)
print('💬 \033[1;32mType your message and press ENTER to transmit\033[0m')
print('⚡ \033[1;37mCommands: /nick [name], /exit, Ctrl+C\033[0m')
print('─' * 55)
print()

try:
    # Connect to chat
    ws = websocket.create_connection("wss://hack.chat/chat-ws", timeout=10)
    ws.send(json.dumps({"cmd": "join", "channel": "CodeArmy", "nick": nickname}))
    
    print('🟢 \033[1;32mSECURE CHANNEL ESTABLISHED\033[0m\n')
    
    # Message receiver
    def receive_messages():
        while True:
            try:
                message = ws.recv()
                data = json.loads(message)
                
                if data["cmd"] == "chat":
                    if data["nick"] == nickname:
                        print(f'   🗨️  \033[1;36mYOU:\033[0m {data["text"]}')
                    else:
                        colors = ['32', '33', '35', '36', '91', '92', '93', '94', '95', '96']
                        color = colors[hash(data["nick"]) % len(colors)]
                        print(f'\033[1;{color}m🎯 {data["nick"]}:\033[0m {data["text"]}')
                        
                elif data["cmd"] == "onlineAdd":
                    print(f'🟢 \033[1;32m{data["nick"]} joined the network\033[0m')
                    
                elif data["cmd"] == "onlineRemove":
                    print(f'🔴 \033[1;31m{data["nick"]} left the network\033[0m')
                    
            except:
                break
    
    # Start receiver
    receiver = threading.Thread(target=receive_messages, daemon=True)
    receiver.start()
    
    # Send join message
    join_messages = [
        "🚀 Secure connection established",
        "🔐 Encrypted channel active", 
        "🌐 Network access granted",
        "💫 Secure comms online"
    ]
    ws.send(json.dumps({"cmd": "chat", "text": random.choice(join_messages)}))
    
    # Chat loop
    while True:
        try:
            message = input('\033[1;37m➤ \033[0m').strip()
            
            if not message:
                continue
                
            if message.lower() in ['/exit', '/quit', 'exit', 'quit']:
                break
                
            elif message.startswith('/nick '):
                new_nick = message[6:].strip()
                if new_nick:
                    ws.send(json.dumps({"cmd": "changenick", "nick": new_nick}))
                    nickname = new_nick
                    print(f'🆔 \033[1;33mIDENTITY UPDATED: {nickname}\033[0m')
                    
            else:
                ws.send(json.dumps({"cmd": "chat", "text": message}))
                
        except KeyboardInterrupt:
            print('\n\n🔴 \033[1;31mEMERGENCY DISCONNECT INITIATED\033[0m')
            break
    
    # Clean exit
    print('👋 \033[1;36mSecure connection terminated\033[0m')
    ws.close()
    
except Exception as e:
    print(f'❌ \033[1;31mCONNECTION FAILED: {e}\033[0m')
    print('💡 \033[1;33mEnsure network connectivity and try again\033[0m')
