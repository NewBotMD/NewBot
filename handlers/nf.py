from utlis.rank import setrank,isrank,remrank,remsudos,setsudo, GPranks
from utlis.send import send_msg, BYusers,Name
from utlis.locks import st
from utlis.tg import Bot
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json,datetime
import importlib


def nf(client, message,redis):
  type = message.chat.type
  userID = message.from_user.id
  chatID = message.chat.id
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
  group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
  rank = isrank(redis,userID,chatID)
  if group is True:
    
    if message.new_chat_members:


      if (rank is False or rank is 0) and GPranks(userID,chatID) == "member" and message.new_chat_members[0].is_bot:
        if redis.sismember("{}Nbot:Lbots".format(BOT_ID),chatID):#16
          first_name = message.new_chat_members[0].first_name
          username = message.new_chat_members[0].username
          Bot("kickChatMember",{"chat_id":chatID,"user_id":message.new_chat_members[0].id})
          Bot("sendMessage",{"chat_id":chatID,"text":r.kickbotadd.format(username,first_name),"reply_to_message_id":message.message_id,"parse_mode":"html"})

      if redis.sismember("{}Nbot:Ljoin".format(BOT_ID),chatID):#17
        Bot("deleteMessage",{"chat_id":chatID,"message_id":message.message_id})
        
      if redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID) and rank != "creator":
        ID = redis.hget("{}Nbot:pinmsgs".format(BOT_ID),chatID)
        Bot("pinChatMessage",{"chat_id":chatID,"message_id":ID})
        
      if message.new_chat_members and not redis.sismember("{}Nbot:welcomeSend".format(BOT_ID),chatID):
        wl = (redis.hget("{}Nbot:welcome".format(BOT_ID),chatID) or "")
        userId = message.new_chat_members[0].id
        userFn = message.new_chat_members[0].first_name
        T ="<a href=\"tg://user?id={}\">{}</a>".format(userId,Name(userFn))
        Bot("sendMessage",{"chat_id":chatID,"text":wl.format(us=T),"reply_to_message_id":message.message_id,"parse_mode":"html"})
        
      if message.new_chat_members:
        userId = message.new_chat_members[0].id
        if userID != userId:
          redis.hincrby("{}Nbot:{}:addcontact".format(BOT_ID,chatID),userID)
          
      if message.pinned_message:
        if redis.sismember("{}Nbot:Lpin".format(BOT_ID),chatID) and rank != "creator":
          ID = redis.hget("{}Nbot:pinmsgs".format(BOT_ID),chatID)
          Bot("pinChatMessage",{"chat_id":chatID,"message_id":ID})
    
      if message.new_chat_members:
        chatID = message.chat.id
        userId = message.new_chat_members[0].id
        if redis.sismember("{}Nbot:restricteds".format(BOT_ID),userId):
          Bot("restrictChatMember",{"chat_id": chatID,"user_id": userId,"can_send_messages": 0,"can_send_media_messages": 0,"can_send_other_messages": 0,"can_send_polls": 0,"can_change_info": 0,"can_add_web_page_previews": 0,"can_pin_messages": 0,})
        if redis.sismember("{}Nbot:bans".format(BOT_ID),userId):
          Bot("kickChatMember",{"chat_id":chatID,"user_id":userId})
          

    if message.left_chat_member:
      if message.left_chat_member.id == int(BOT_ID):
        redis.srem("{}Nbot:groups".format(BOT_ID),chatID)
        redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),chatID)
        NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
        redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID,str(NextDay_Date))
