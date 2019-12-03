from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks,IDrank
from utlis.send import send_msg, BYusers, GetLink,Name
from utlis.locks import st,getOR
from utlis.tg import Bot
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib

from pyrogram.api.types import InputPeerChat
def allGP(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  chatID = message.chat.id
  username = message.from_user.username
  if username is None:
    username = "None"
  userFN = message.from_user.first_name
  title = message.chat.title
  rank = isrank(redis,userID,chatID)
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
  redis.hincrby("{}Nbot:{}:msgs".format(BOT_ID,chatID),userID)
  if text :
    if re.search(c.ShowO,text) and (rank is not False or rank is not  0 or rank != "vip"):
      reply_markup = getOR(rank,r,userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.Showall,"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True,"reply_markup":reply_markup})



    if text == c.ID and not redis.sismember("{}Nbot:IDSend".format(BOT_ID),chatID) and not message.reply_to_message:
      Ch = True
      if redis.sismember("{}Nbot:IDpt".format(BOT_ID),chatID):
        t = IDrank(redis,userID,chatID,r)
        msgs = (redis.hget("{}Nbot:{}:msgs".format(BOT_ID,chatID),userID) or 0)
        edits = (redis.hget("{}Nbot:{}:edits".format(BOT_ID,chatID),userID) or 0)
        rate = int(msgs)*100/20000
        if redis.hget("{}Nbot:SHOWid".format(BOT_ID),chatID):
          tx = redis.hget("{}Nbot:SHOWid".format(BOT_ID),chatID)
        else:
          tx = r.IDnPT
        if not redis.sismember("{}Nbot:IDSendPH".format(BOT_ID),chatID):
          get = Bot("getUserProfilePhotos",{"user_id":userID,"offset":0,"limit":1})
          if get["ok"] == False: 
            Ch = True
          elif get["result"]["total_count"] == 0:
            Ch = True
          else:
            Ch = False
            file_id = get["result"]["photos"][0][0]["file_id"]
            Bot("sendPhoto",{"chat_id":chatID,"photo":file_id,"caption":tx.format(us=("@"+username or "None"),id=userID,rk=t,msgs=msgs,edits=edits,rate=str(rate)+"%"),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        if Ch == True:
          Bot("sendMessage",{"chat_id":chatID,"text":tx.format(us=("@"+username or "None"),id=userID,rk=t,msgs=msgs,edits=edits,rate=str(rate)+"%"),"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if not redis.sismember("{}Nbot:IDSendPH".format(BOT_ID),chatID) and not redis.sismember("{}Nbot:IDpt".format(BOT_ID),chatID):
        get = Bot("getUserProfilePhotos",{"user_id":userID,"offset":0,"limit":1})
        if get["ok"] == False: 
          Ch = True
        elif get["result"]["total_count"] == 0:
          Ch = True
        else:
          Ch = False
          reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(r.RIDPHs,callback_data=json.dumps(["ShowDateUser","",userID]))]])
          file_id = get["result"]["photos"][0][0]["file_id"]
          Bot("sendPhoto",{"chat_id":chatID,"photo":file_id,"caption":r.RID.format(userID),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})
      if Ch == True and not redis.sismember("{}Nbot:IDpt".format(BOT_ID),chatID):
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton(r.RIDPHs,callback_data=json.dumps(["ShowDateUser","",userID]))]])
        Bot("sendMessage",{"chat_id":chatID,"text":r.RID.format(userID),"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})



    if text == c.ID and not redis.sismember("{}Nbot:IDSend".format(BOT_ID),chatID) and message.reply_to_message:
      us = message.reply_to_message.from_user.id
      Bot("sendMessage",{"chat_id":chatID,"text":us,"reply_to_message_id":message.message_id,"parse_mode":"html"})
    if re.search(c.idus,text) and not redis.sismember("{}Nbot:IDSend".format(BOT_ID),chatID):
      user = text.split("@")[1]
      try:
        getUser = client.get_users(user)
        us = getUser.id
        Bot("sendMessage",{"chat_id":chatID,"text":us,"reply_to_message_id":message.message_id,"parse_mode":"html"})
      except Exception as e:
        print(e)

    if re.search(c.ShowSudos, text):
      tx = (redis.get("{}Nbot:SHOWsudos".format(BOT_ID)) or "")
      Bot("sendMessage",{"chat_id":chatID,"text":tx,"reply_to_message_id":message.message_id,"parse_mode":"html"})
    if text == c.mymsgs:
      get = redis.hget("{}Nbot:{}:msgs".format(BOT_ID,chatID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.yourmsgs.format((get or 0)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
    if text == c.link:
      get = (redis.hget("{}Nbot:links".format(BOT_ID),chatID) or GetLink(chatID) or "none")
      Bot("sendMessage",{"chat_id":chatID,"text":r.showGPlk.format(get),"reply_to_message_id":message.message_id,"parse_mode":"html","disable_web_page_preview":True})

    if text == c.myedits:
      get = redis.hget("{}Nbot:{}:edits".format(BOT_ID,chatID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.youredits.format((get or 0)),"reply_to_message_id":message.message_id,"parse_mode":"html"})

    if text == c.myaddcontact:
      get = redis.hget("{}Nbot:{}:addcontact".format(BOT_ID,chatID),userID)
      Bot("sendMessage",{"chat_id":chatID,"text":r.youraddcontact.format((get or 0)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
    
    
    if not redis.sismember("{}Nbot:ReplySendBOT".format(BOT_ID),chatID):
      if redis.hexists("{}Nbot:TXreplys".format(BOT_ID),text):
        tx = redis.hget("{}Nbot:TXreplys".format(BOT_ID),text)
        Bot("sendMessage",{"chat_id":chatID,"text":tx.format(fn=Name(userFn),us=("@"+username or "none"),id=userID,rk=IDrank(redis,userID,chatID,r),cn=title),"reply_to_message_id":message.message_id,"parse_mode":"html"})
      
      if redis.hexists("{}Nbot:STreplys".format(BOT_ID),text):
        ID = redis.hget("{}Nbot:STreplys".format(BOT_ID),text)
        Bot("sendSticker",{"chat_id":chatID,"sticker":ID,"reply_to_message_id":message.message_id})
      
      if redis.hexists("{}Nbot:GFreplys".format(BOT_ID),text):
        ID = redis.hget("{}Nbot:GFreplys".format(BOT_ID),text)
        Bot("sendanimation",{"chat_id":chatID,"animation":ID,"reply_to_message_id":message.message_id})

      if redis.hexists("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),text):
        ID = redis.hget("{}Nbot:VOreplys".format(BOT_ID),text)
        Bot("sendvoice",{"chat_id":chatID,"voice":ID,"reply_to_message_id":message.message_id})



    if not redis.sismember("{}Nbot:ReplySend".format(BOT_ID),chatID):
      if redis.hexists("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),text):
        tx = redis.hget("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),text)
        Bot("sendMessage",{"chat_id":chatID,"text":tx.format(fn=Name(userFN),us=("@"+username or "n"),id=userID,rk=IDrank(redis,userID,chatID,r),cn=title),"reply_to_message_id":message.message_id,"parse_mode":"html"})
      
      if redis.hexists("{}Nbot:{}:STreplys".format(BOT_ID,chatID),text):
        ID = redis.hget("{}Nbot:{}:STreplys".format(BOT_ID,chatID),text)
        Bot("sendSticker",{"chat_id":chatID,"sticker":ID,"reply_to_message_id":message.message_id})
      
      if redis.hexists("{}Nbot:{}:GFreplys".format(BOT_ID,chatID),text):
        ID = redis.hget("{}Nbot:{}:GFreplys".format(BOT_ID,chatID),text)
        Bot("sendanimation",{"chat_id":chatID,"animation":ID,"reply_to_message_id":message.message_id})

      if redis.hexists("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),text):
        ID = redis.hget("{}Nbot:{}:VOreplys".format(BOT_ID,chatID),text)
        Bot("sendvoice",{"chat_id":chatID,"voice":ID,"reply_to_message_id":message.message_id})
