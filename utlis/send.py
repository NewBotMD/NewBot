from utlis.rank import setrank,isrank,remrank,remsudos,setsudo
from utlis.tg import Bot
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json ,os
import importlib

def send_msg(type,client, message,textM,Lhash,T,redis):
  userID = message.from_user.id
  userFN = message.from_user.first_name
  chatID = message.chat.id
  text = message.text
  if redis.sismember("{}Nbot:lang:ar".format(BOT_ID),chatID):
    lang = "ar"
  elif redis.sismember("{}Nbot:lang:en".format(BOT_ID),chatID):
    lang = "en"
  else :
    lang = "ar"
  moduleCMD = "lang."+lang+"-cmd"
  moduleREPLY = "lang."+lang+"-reply"
  c = importlib.import_module(moduleCMD)
  r = importlib.import_module(moduleREPLY)
  if type == "LU":
    if re.search(c.stL, text):
      Tp = "LtoU"
    if re.search(c.stU, text):
      Tp = "UtoL"
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
    tx = textM.format(BY,T)
    b = json.dumps(["LandU",Lhash,userID,Tp])
    v = InlineKeyboardMarkup([[InlineKeyboardButton(r.Corder, callback_data=b)]])
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":v})
  if type == "LUN":
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userID,userFN)
    tx = textM.format(BY,T)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

  if type == "UD":
    R = text.split(" ")[1]
    userId = T.id
    userFn = Name(T.first_name)
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
    tx = textM.format(BY,R)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

  if type == "BN":
    userId = T.id
    userFn = Name(T.first_name)
    BY = "[{}](tg://user?id={})".format(userFn,userId)
    tx = textM.format(BY)
    if re.search(c.stC, text):
      Tp = "UtoB"
    else:
      Tp = "BtoU"
    b = json.dumps(["Corder",Lhash,userID,userId,Tp])
    v = InlineKeyboardMarkup([[InlineKeyboardButton(r.Corder, callback_data=b)]])
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"markdown","disable_web_page_preview":True,"reply_markup":v})
  
  if type == "BNN":
    userId = T.id
    userFn = Name(T.first_name)
    BY = "<a href=\"tg://user?id={}\">{}</a>".format(userId,userFn)
    tx = textM.format(BY)
    Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
  


def BYusers(arrays,chatID,redis,client):
  users = ""
  i = 0
  if redis.sismember("{}Nbot:lang:ar".format(BOT_ID),chatID):
    lang = "ar"
  elif redis.sismember("{}Nbot:lang:en".format(BOT_ID),chatID):
    lang = "en"
  else :
    lang = "ar"
  moduleCMD = "lang."+lang+"-cmd"
  moduleREPLY = "lang."+lang+"-reply"
  c = importlib.import_module(moduleCMD)
  r = importlib.import_module(moduleREPLY)
  for user in arrays:
    i +=1
    try:
      getUser = client.get_users(user)
      userId = getUser.id
      userFn = getUser.first_name
      users = users+"\n"+str(i)+" - "+"[{}](tg://user?id={})".format(userFn,userId)
      print(userFn)
    except Exception as e:
      users = users+"\n"+str(i)+" - "+"[{}](tg://user?id={})".format(user,user)
      print(e)
      print(user)
  return users

def CKsend(redis,callback_query,type,ck,sID):
  if ck["ok"] == False and not redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),sID):
    redis.sadd("{}Nbot:dontsend".format(BOT_ID),sID)
    if type == "privates":
      redis.srem("{}Nbot:privates".format(BOT_ID),sID)
    else:
      redis.srem("{}Nbot:groups".format(BOT_ID),sID)
  elif ck["ok"]:
    redis.sadd("{}Nbot:donesend".format(BOT_ID),sID)

def Sendto(redis,callback_query,type):
  IDS = redis.smembers("{}Nbot:{}".format(BOT_ID,type))
  print(IDS)

  if callback_query.message.reply_to_message.text:
    for sID in IDS:
     ck = Bot("sendMessage",{"chat_id":sID,"text":callback_query.message.reply_to_message.text,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.photo:
    ID = callback_query.message.reply_to_message.photo.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendphoto",{"chat_id":sID,"photo":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.video:
    ID = callback_query.message.reply_to_message.video.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendvideo",{"chat_id":sID,"video":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.video_note:
    ID = callback_query.message.reply_to_message.video_note.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendVideoNote",{"chat_id":sID,"video_note":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.voice:
    ID = callback_query.message.reply_to_message.voice.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendvoice",{"chat_id":sID,"voice":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.audio:
    ID = callback_query.message.reply_to_message.audio.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendaudio",{"chat_id":sID,"audio":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.sticker:
    ID = callback_query.message.reply_to_message.sticker.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendsticker",{"chat_id":sID,"sticker":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)
     
  if callback_query.message.reply_to_message.document:
    ID = callback_query.message.reply_to_message.document.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("senddocument",{"chat_id":sID,"document":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)

  if callback_query.message.reply_to_message.animation:
    ID = callback_query.message.reply_to_message.animation.file_id
    CP = callback_query.message.reply_to_message.caption
    for sID in IDS:
     ck = Bot("sendanimation",{"chat_id":sID,"animation":ID,"caption":CP,"parse_mode":"html"})
     CKsend(redis,callback_query,type,ck,sID)
     time.sleep(0.3)
  

  return redis.scard("{}Nbot:donesend".format(BOT_ID)),redis.scard("{}Nbot:dontsend".format(BOT_ID))



def fwdto(redis,callback_query,type):
  IDS = redis.smembers("{}Nbot:{}".format(BOT_ID,type))
  if callback_query.message.reply_to_message.message_id:
    for sID in IDS:
      ck = Bot("forwardMessage",{"chat_id":sID,"from_chat_id":callback_query.message.chat.id,"message_id":callback_query.message.reply_to_message.message_id})
      CKsend(redis,callback_query,type,ck,sID)
      time.sleep(0.3)
  return redis.scard("{}Nbot:donesend".format(BOT_ID)),redis.scard("{}Nbot:dontsend".format(BOT_ID))

def sendM(T,msg,message):
  if T == "NO":
    chatID = message.chat.id
    Len = 3000
    msgs = [msg[y-Len:y] for y in range(Len, len(msg)+Len,Len)]
    for tx in msgs:
      Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})
      time.sleep(0.3)

def GetLink(chatID):
  li = Bot("getchat",{"chat_id":chatID})["result"]
  if "invite_link" in li:
    return li["invite_link"]
  else:
    Bot("exportChatInviteLink",{"chat_id":chatID})
    li = Bot("getchat",{"chat_id":chatID})["result"]
    if "invite_link" in li:
      return li["invite_link"]
    else:
      return False
  

def Name(name):
  Len = 10
  names = [name[y-Len:y] for y in range(Len, len(name)+Len,Len)]
  return names[0]


def run(redis,chatID):
  redis.set("{}:Nbot:restart".format(BOT_ID),chatID)
  os.system("pm2 restart {}".format(BOT_ID))
