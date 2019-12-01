from utlis.rank import setrank,isrank,remrank,remsudos,setsudo
from utlis.send import send_msg, BYusers
from utlis.tg import Bot,Ckuser
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re, json
import importlib


def ranks(client, message,redis):
	type = message.chat.type
	userID = message.from_user.id
	chatID = message.chat.id
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

	if (rank is "sudo" or rank is "sudos" or rank is "creator" or rank is "owner"):
		if re.search(c.admins, text) and Ckuser(message):
			arrays = redis.smembers("{}Nbot:{}:admin".format(BOT_ID,chatID))
			b = BYusers(arrays,chatID,redis,client)
			kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","admin",userID]))]])
			if  b is not "":
				Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
			else:
				Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})
		
		if re.search(c.vips, text) and Ckuser(message):
			arrays = redis.smembers("{}Nbot:{}:vip".format(BOT_ID,chatID))
			b = BYusers(arrays,chatID,redis,client)
			kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","vip",userID]))]])
			if  b is not "":
				Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
			else:
				Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

		if re.search(c.setadmin, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.setadmin2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = setrank(redis,"admin",userId,chatID,"array")
				if setcr is "admin":
					send_msg("UD",client, message,r.DsetRK,"",getUser,redis)
				elif (setcr is True or setcr is 1):
					send_msg("UD",client, message,r.setRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if re.search(c.remadmin, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.remadmin2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = remrank(redis,"admin",userId,chatID,"array")
				if setcr:
					send_msg("UD",client, message,r.remRK,"",getUser,redis)
				elif not setcr:
					send_msg("UD",client, message,r.DremRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
	
		if re.search(c.setvip, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.setvip2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = setrank(redis,"vip",userId,chatID,"array")
				if setcr is "vip":
					send_msg("UD",client, message,r.DsetRK,"",getUser,redis)
				elif (setcr is True or setcr is 1):
					send_msg("UD",client, message,r.setRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if re.search(c.remvip, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.remvip2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = remrank(redis,"vip",userId,chatID,"array")
				if setcr:
					send_msg("UD",client, message,r.remRK,"",getUser,redis)
				elif not setcr:
					send_msg("UD",client, message,r.DremRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

	if (rank is "sudo" or rank is "sudos" or rank is "creator"):
		if re.search(c.owners, text) and Ckuser(message):
			arrays = redis.smembers("{}Nbot:{}:owner".format(BOT_ID,chatID))
			b = BYusers(arrays,chatID,redis,client)
			kb = InlineKeyboardMarkup([[InlineKeyboardButton(r.delList.format(text), callback_data=json.dumps(["delList","owner",userID]))]])
			if  b is not "":
				Bot("sendMessage",{"chat_id":chatID,"text":r.showlist.format(text,b),"reply_to_message_id":message.message_id,"parse_mode":"markdown","reply_markup":kb})
			else:
				Bot("sendMessage",{"chat_id":chatID,"text":r.listempty.format(text),"reply_to_message_id":message.message_id,"parse_mode":"markdown"})

		if re.search(c.setowner, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.setowner2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = setrank(redis,"owner",userId,chatID,"array")
				if setcr is "owner":
					send_msg("UD",client, message,r.DsetRK,"",getUser,redis)
				elif (setcr is True or setcr is 1):
					send_msg("UD",client, message,r.setRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if re.search(c.remowner, text) and Ckuser(message):
			if re.search("@",text):
				user = text.split("@")[1]
			if re.search(c.remowner2,text):
				user = text.split(" ")[2]
			if message.reply_to_message:
				user = message.reply_to_message.from_user.id
			if 'user' not in locals():return False
			try:
				getUser = client.get_users(user)
				userId = getUser.id
				userFn = getUser.first_name
				setcr = remrank(redis,"owner",userId,chatID,"array")
				if setcr:
					send_msg("UD",client, message,r.remRK,"",getUser,redis)
				elif not setcr:
					send_msg("UD",client, message,r.DremRK,"",getUser,redis)
			except Exception as e:
				Bot("sendMessage",{"chat_id":chatID,"text":r.userNocc,"reply_to_message_id":message.message_id,"parse_mode":"html"})
