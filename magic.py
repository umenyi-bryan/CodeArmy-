#!/usr/bin/env python3
import websocket, json, random, threading, time, os, sys

def main():
    # Generate cool nickname
    names = ['Ghost', 'Raven', 'Viper', 'Wolf', 'Hunter', 'Steel']
    units = ['Reaper', 'Strike', 'Fang', 'Claw', 'Blade', 'Sight']
    nick = f"{random.choice(names)}_{random.choice(units)}{random.randint(10,99)}"
    
    # Display banner
    os.system('clear')
    print('\033[1;32m')
    print('  🎯 CODE ARMY - Anonymous Terminal Chat')
    print('  🔫 No Setup • No Registration • Pure Fun')
    print('\033[0m')
    print(f'🔫 Callsign: \033[1;36m{nick}\033[0m')
    print('📡 Connecting...', end='')
    
    try:
        # Connect to chat
        ws = websocket.create_connection("wss://hack.chat/chat-ws", timeout=10)
        ws.send(json.dumps({"cmd": "join", "channel": "CodeArmy", "nick": nick}))
        print('\r✅ Connected! Type to chat:\033[0m\n')
        
        # Message receiver
        def receive_messages():
            while True:
                try:
                    msg = ws.recv()
                    data = json.loads(msg)
                    if data["cmd"] == "chat":
                        if data["nick"] == nick:
                            print(f'   \033[1;36mYOU:\033[0m {data["text"]}')
                        else:
                            print(f'\033[1;32m🎯 {data["nick"]}:\033[0m {data["text"]}')
                    elif data["cmd"] == "onlineAdd":
                        print(f'\033[1;33m📍 {data["nick"]} joined\033[0m')
                    elif data["cmd"] == "onlineRemove":
                        print(f'\033[1;31m🏃 {data["nick"]} left\033[0m')
                except:
                    break
        
        # Start receiver thread
        thread = threading.Thread(target=receive_messages, daemon=True)
        thread.start()
        
        # Send join message
        ws.send(json.dumps({"cmd": "chat", "text": "🚀 Joined the battle!"}))
        
        # Chat loop
        while True:
            try:
                message = input('\033[1;37m» \033[0m').strip()
                if message.startswith('/nick '):
                    new_nick = message[6:].strip()
                    if new_nick:
                        ws.send(json.dumps({"cmd": "changenick", "nick": new_nick}))
                        nick = new_nick
                        print(f'🆔 {new_nick}')
                elif message in ['/exit', '/quit']:
                    break
                elif message:
                    ws.send(json.dumps({"cmd": "chat", "text": message}))
            except KeyboardInterrupt:
                break
        
        print('\n👋 Goodbye!')
        ws.close()
        
    except Exception as e:
        print(f'\r❌ Connection failed: {e}\033[0m')

if __name__ == "__main__":
    main()
