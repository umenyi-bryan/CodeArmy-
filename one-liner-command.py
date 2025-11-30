import websocket,json,random,threading,time,os,datetime,sys,ssl

def get_time(): return datetime.datetime.now().strftime('%H:%M:%S')

# Show banner
os.system('clear')
print('\033[1;36m')
print('    ╔═╗╔╦╗╔╦╗╔═╗  ╔═╗╔╗╔╔═╗╔╦╗╦╔═╗')
print('    ║ ║║║║║║║╠═╝  ║ ║║║║╠═╣║║║║║ ')  
print('    ╚═╝╩ ╩╩ ╩╩    ╚═╝╝╚╝╩ ╩╩ ╩╩╚═╝')
print('\033[1;35m')
print('    ╔══════════════════════════════════════╗')
print('    ║    A N O N Y M O U S   C H A T      ║')
print('    ║      T E R M I N A L   S P A C E    ║')
print('    ╚══════════════════════════════════════╝')
print('\033[0m')

n=f"{random.choice(['Phantom','Raven','Viper','Wolf','Ghost'])}"+f"{random.choice(['Reaper','Strike','Fang','Blade','Sight'])}{random.randint(10,99)}"
print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{n}\033[0m')
print('📡 \033[1;33mCONNECTING...\033[0m',end='')
sys.stdout.flush()

connected = False
ws = None

# Try multiple connection methods
methods = [
    lambda: websocket.create_connection("wss://hack.chat/chat-ws", timeout=15),
    lambda: websocket.create_connection("wss://hack.chat/chat-ws", timeout=15, sslopt={"cert_reqs": ssl.CERT_NONE}),
]

for i, method in enumerate(methods):
    try:
        ws = method()
        ws.send(json.dumps({"cmd":"join","channel":"CodeArmy","nick":n}))
        # Test if we get a response
        response = ws.recv()
        data = json.loads(response)
        connected = True
        print('\r✅ \033[1;32mCONNECTED! TYPE TO CHAT:\033[0m\n')
        break
    except Exception as e:
        if i == len(methods) - 1:
            print(f'\r❌ \033[1;31mCONNECTION FAILED\033[0m')
            print('💡 \033[1;33mServer might be down. Running in local mode.\033[0m\n')
        continue

def receive_messages():
    if not connected: return
    while True:
        try:
            m=ws.recv()
            d=json.loads(m)
            t=get_time()
            if d["cmd"]=="chat":
                if d["nick"]==n:print(f'   \033[1;36m[{t}] YOU:\033[0m {d["text"]}')
                else:print(f'\033[1;32m[{t}] 🎯 {d["nick"]}:\033[0m {d["text"]}')
            elif d["cmd"]=="onlineAdd":print(f'🟢 \033[1;32m[{t}] {d["nick"]} joined\033[0m')
            elif d["cmd"]=="onlineRemove":print(f'🔴 \033[1;31m[{t}] {d["nick"]} left\033[0m')
        except:break

if connected:
    t=threading.Thread(target=receive_messages,daemon=True)
    t.start()
    ws.send(json.dumps({"cmd":"chat","text":"🚀 Secure connection established"}))

while True:
    try:
        m=input('\033[1;37m➤ \033[0m').strip()
        if m.startswith('/nick '):
            new_nick=m[6:].strip()
            if new_nick:
                if connected:
                    ws.send(json.dumps({"cmd":"changenick","nick":new_nick}))
                    n=new_nick
                print(f'🆔 \033[1;33m{new_nick}\033[0m')
        elif m=='/help':
            print('\033[1;34mCommands: /nick, /help, /exit, /status\033[0m')
            status = "🟢 CONNECTED" if connected else "🔴 LOCAL MODE"
            print(f'\033[1;36mStatus: {status}\033[0m')
        elif m=='/status':
            status = "🟢 CONNECTED" if connected else "🔴 LOCAL MODE"
            print(f'📊 \033[1;36mStatus: {status}\033[0m')
        elif m in ['/exit','/quit']:break
        elif m:
            if connected:
                ws.send(json.dumps({"cmd":"chat","text":m}))
                print(f'   \033[1;36m[{get_time()}] YOU:\033[0m {m}')
            else:
                print(f'   \033[1;90m[{get_time()}] [LOCAL]: {m}\033[0m')
    except KeyboardInterrupt:break

if connected and ws: 
    try: ws.close()
    except: pass
print('\n👋 \033[1;36mSession ended\033[0m')
