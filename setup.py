import requests,os
from pyrogram import Client

API_ID = 793178
API_HASH = '9f4461079f30757ca0a4c23e14bd523f'

out ="""
API_ID = 793178
API_HASH = '9f4461079f30757ca0a4c23e14bd523f'
"""
def Bot(TOKEN,method,data):
  url = "https://api.telegram.org/bot{}/{}".format(TOKEN,method)
  post = requests.post(url,data=data)
  return post.json()
ID = ""
go = True
while go:
  token = input("input you're bot TOKEN:")
  get = Bot(token,"getme",{})
  if get["ok"]:
    out = out+"\n"+"TOKEN = '{}'\nBOT_ID = TOKEN.split(':')[0]".format(token)
    go = False
    ID = token.split(':')[0]
    #with Client(":memory:",bot_token=token,api_id = API_ID, api_hash = API_HASH) as app, open("session.txt", "w+") as s_file:
      #session_string = app.export_session_string()
      #s_file.write(session_string)
  else:
    print("TOKEN is invalid, Try again")

sudo = input("input you're ID:")
out = out+"\n"+"SUDO = {}".format(sudo)

f = open("config.py","w+") 
f.write(out)
f.close()
#app = Client("NB"+ID,bot_token=token,api_id = API_ID, api_hash = API_HASH)
#app.start()
#app.get_me()
#app.stop()
os.system('pm2 start bot.py --name {} --interpreter python3.7 --interpreter-args -u'.format(ID))
