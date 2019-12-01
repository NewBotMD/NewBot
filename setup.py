import requests,os

out ="""
API_ID = 770767
API_HASH = '5ce182752b91a16f90e88f96a541f331'
"""
def Bot(TOKEN,method,data):
  url = "https://api.telegram.org/bot{}/{}".format(TOKEN,method)
  post = requests.post(url,data=data)
  #print(post.json())
  return post.json()
ID = ""
go = True
while go:
  token = input("input you're bot TOKEN:")
  get = Bot(token,"getme",{})
  if get["ok"]:
    out = out+"\n"+"TOKEN = '{}'\nBOT_ID = int(TOKEN.split(':')[0])".format(token)
    go = False
    ID = int(token.split(':')[0])
  else:
    print("TOKEN is invalid, Try again")

sudo = input("input you're ID:")
out = out+"\n"+"SUDO = int({})".format(sudo)

f = open("config.py","w+") 
f.write(out)
f.close()

os.system('cd ~/NewBot;pm2 start bot.py --name {} --interpreter python3.7 --interpreter-args -u'.format(ID))
