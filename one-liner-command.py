import websocket,json,random,threading,time,os,datetime,sys
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

def get_time(): return datetime.datetime.now().strftime('%H:%M:%S')
n=f"{random.choice(['Phantom','Raven','Viper','Wolf','Ghost'])}"+f"{random.choice(['Reaper','Strike','Fang','Blade','Sight'])}{random.randint(10,99)}"
print(f'🎖️  \033[1;33mOPERATIVE:\033[0m \033[1;36m{n}\033[0m')
print('📡 \033[1;33mCONNECTING...\033[0m',end='')

connected = False
try:
 w=websocket.create_connection("wss://hack.chat/chat-ws",timeout=10)
 w.send(json.dumps({"cmd":"join","channel":"CodeArmy","nick":n}))
 connected = True
 print('\r✅ \033[1;32mCONNECTED! TYPE TO CHAT:\033[0m\n')
except Exception as e:
 print(f'\r❌ \033[1;31mCONNECTION FAILED: {e}\033[0m')
 print('💡 \033[1;33mRunning in offline mode - messages won\\'t send\033[0m\n')

def receive_messages():
 if not connected: return
 while True:
  try:
   m=w.recv();d=json.loads(m)
   t=get_time()
   if d["cmd"]=="chat":
    if d["nick"]==n:print(f'   \033[1;36m[{t}] YOU:\033[0m {d["text"]}')
    else:print(f'\033[1;32m[{t}] 🎯 {d["nick"]}:\033[0m {d["text"]}')
   elif d["cmd"]=="onlineAdd":print(f'🟢 \033[1;32m[{t}] {d["nick"]} joined\033[0m')
   elif d["cmd"]=="onlineRemove":print(f'🔴 \033[1;31m[{t}] {d["nick"]} left\033[0m')
  except:break

if connected:
 t=threading.Thread(target=receive_messages,daemon=True);t.start()
 w.send(json.dumps({"cmd":"chat","text":"🚀 Secure connection established"}))

while True:
 try:
  m=input('\033[1;37m➤ \033[0m').strip()
  if m.startswith('/nick '):
   new_nick=m[6:].strip()
   if new_nick:
    if connected:
     w.send(json.dumps({"cmd":"changenick","nick":new_nick}))
     n=new_nick
    print(f'🆔 \033[1;33m{new_nick}\033[0m')
  elif m=='/help':
   print('\033[1;34mCommands: /nick, /help, /exit, /status\033[0m')
   if not connected: print('\033[1;31m⚠️  OFFLINE MODE - messages not sending\033[0m')
  elif m=='/status':
   s='🟢 CONNECTED' if connected else '🔴 OFFLINE'
   print(f'📊 \033[1;36mStatus: {s}\033[0m')
  elif m in ['/exit','/quit']:break
  elif m:
   if connected:
    w.send(json.dumps({"cmd":"chat","text":m}))
    print(f'   \033[1;36m[{get_time()}] YOU:\033[0m {m}')
   else:
    print(f'   \033[1;90m[{get_time()}] [OFFLINE]: {m}\033[0m')
 except KeyboardInterrupt:break

if connected: w.close()
print('\n👋 \033[1;36mConnection closed\033[0m')
