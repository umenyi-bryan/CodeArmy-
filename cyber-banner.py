#!/usr/bin/env python3
import websocket,json,random,threading,time,os

# Cyberpunk ASCII Banner
def show_cyber_banner():
    os.system('clear')
    print('\033[1;35m')  # Magenta/Purple
    print('    █▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀█')
    print('    █ 🅲 🅾 🅳 🅴 🅰 🆁 🅼 🆈 █')
    print('    █▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄█')
    print('\033[1;36m')
    print('    ═══════════════════════════════')
    print('      A N O N Y M O U S   N E T')
    print('    ═══════════════════════════════')
    print('\033[0m')

# Generate cyber-style nickname
cyber_names = ['Neo', 'Trinity', 'Morpheus', 'Cypher', 'Tank', 'Apoc', 'Switch', 'Mouse']
cyber_tags = ['01', 'X1', 'Z3R0', '4LPH4', 'B3T4', '0M3G4', 'PR0T0', 'SYSTEM']
nickname = f"{random.choice(cyber_names)}_{random.choice(cyber_tags)}"

show_cyber_banner()
print(f'🔷 \033[1;36mUSER:\033[0m \033[1;35m{nickname}\033[0m')
print(f'🔶 \033[1;33mROOM:\033[0m \033[1;32m#CodeArmy\033[0m')
print(f'🛰️  \033[1;34mCONNECTING TO NETWORK\033[0m', end='')

# Matrix-style loading
for i in range(10):
    chars = ['▰▱▱▱', '▰▰▱▱', '▰▰▰▱', '▰▰▰▰', '▰▰▰▱', '▰▰▱▱', '▰▱▱▱']
    print(f'\r🛰️  \033[1;34mCONNECTING TO NETWORK {chars[i % len(chars)]}\033[0m', end='', flush=True)
    time.sleep(0.2)

print('\r✅ \033[1;32mNETWORK CONNECTION ESTABLISHED\033[0m')
print('─' * 50)
print('💠 \033[1;36mTYPE TO COMMUNICATE • CTRL+C TO EXIT\033[0m')
print('─' * 50)
print()

try:
    ws = websocket.create_connection("wss://hack.chat/chat-ws", timeout=10)
    ws.send(json.dumps({"cmd": "join", "channel": "CodeArmy", "nick": nickname}))
    
    print('🟣 \033[1;35mENTERING CYBERSPACE\033[0m\n')
    
    def receive_messages():
        while True:
            try:
                message = ws.recv()
                data = json.loads(message)
                
                if data["cmd"] == "chat":
                    if data["nick"] == nickname:
                        print(f'   💬 \033[1;36mYOU:\033[0m {data["text"]}')
                    else:
                        colors = ['92', '93', '94', '95', '96', '97']
                        color = colors[hash(data["nick"]) % len(colors)]
                        print(f'\033[1;{color}m🔹 {data["nick"]}:\033[0m {data["text"]}')
                        
                elif data["cmd"] == "onlineAdd":
                    print(f'🟢 \033[1;32m{data["nick"]} entered the network\033[0m')
                    
                elif data["cmd"] == "onlineRemove":
                    print(f'🔴 \033[1;31m{data["nick"]} left the network\033[0m')
                    
            except:
                break
    
    receiver = threading.Thread(target=receive_messages, daemon=True)
    receiver.start()
    
    cyber_messages = [
        "⚡ System online",
        "🔓 Access granted", 
        "🌐 Connected to matrix",
        "💾 Session initialized"
    ]
    ws.send(json.dumps({"cmd": "chat", "text": random.choice(cyber_messages)}))
    
    while True:
        try:
            message = input('\033[1;37m⫸ \033[0m').strip()
            
            if not message:
                continue
                
            if message.lower() in ['/exit', '/quit']:
                break
                
            elif message.startswith('/nick '):
                new_nick = message[6:].strip()
                if new_nick:
                    ws.send(json.dumps({"cmd": "changenick", "nick": new_nick}))
                    nickname = new_nick
                    print(f'🆔 \033[1;33mIDENTITY: {nickname}\033[0m')
                    
            else:
                ws.send(json.dumps({"cmd": "chat", "text": message}))
                
        except KeyboardInterrupt:
            print('\n\n🔴 \033[1;31mDISCONNECTING FROM NETWORK\033[0m')
            break
    
    print('👋 \033[1;36mSession terminated\033[0m')
    ws.close()
    
except Exception as e:
    print(f'\r❌ \033[1;31mNETWORK ERROR: {e}\033[0m')
