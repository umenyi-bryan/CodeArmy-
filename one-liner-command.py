import websocket,json,random,threading,time,os
os.system('clear')
print('\033[1;32m\n  🎯 CODE ARMY - Anonymous Terminal Chat\n  🔫 No Setup • No Registration • Pure Fun\n\033[0m')
n=f"{random.choice(['Ghost','Raven','Viper','Wolf','Steel'])}"+f"{random.choice(['Reaper','Strike','Fang','Blade','Watch'])}{random.randint(10,99)}"
print(f'🔫 Callsign: \033[1;36m{n}\033[0m')
print('📡 Connecting...',end='')
try:
 w=websocket.create_connection("wss://hack.chat/chat-ws",timeout=10)
 w.send(json.dumps({"cmd":"join","channel":"CodeArmy","nick":n}))
 print('\r✅ Connected! Type to chat:\033[0m\n')
 def r():
  while True:
   try:
    m=w.recv();d=json.loads(m)
    if d["cmd"]=="chat":
     if d["nick"]==n:print(f'   \033[1;36mYOU:\033[0m {d["text"]}')
     else:print(f'\033[1;32m🎯 {d["nick"]}:\033[0m {d["text"]}')
    elif d["cmd"]=="onlineAdd":print(f'\033[1;33m📍 {d["nick"]} joined\033[0m')
    elif d["cmd"]=="onlineRemove":print(f'\033[1;31m🏃 {d["nick"]} left\033[0m')
   except:break
 t=threading.Thread(target=r,daemon=True);t.start()
 w.send(json.dumps({"cmd":"chat","text":"🚀 Joined the battle!"}))
 while True:
  try:
   m=input('\033[1;37m» \033[0m').strip()
   if m.startswith('/nick '):
    new_nick=m[6:].strip()
    if new_nick:w.send(json.dumps({"cmd":"changenick","nick":new_nick}));n=new_nick;print(f'🆔 {new_nick}')
   elif m in ['/exit','/quit']:break
   elif m:w.send(json.dumps({"cmd":"chat","text":m}))
  except KeyboardInterrupt:break
 print('\n👋 Goodbye!');w.close()
except Exception as e:print(f'\r❌ Failed: {e}\033[0m')
