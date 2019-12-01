from utlis.rank import setrank ,isrank ,remrank ,setsudos ,remsudos ,setsudo,IDrank,GPranks
from utlis.send import send_msg, BYusers, sendM
from handlers.delete import delete
from utlis.tg import Bot, Ckuser
from handlers.ranks import ranks
from handlers.locks import locks
from handlers.gpcmd import gpcmd
from handlers.sudo import sudo
from handlers.all import allGP
from utlis.tg import Bot,Del24
from config import *

from pyrogram import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
import threading, requests, time, random, re , json,datetime
import importlib

def updateHandlers(client, message,redis):

	type = message.chat.type
	userID = message.from_user.id
	chatID = message.chat.id
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
	if (type is "supergroup" or type is "group") and message.outgoing != True:
		userID = message.from_user.id
		chatID = message.chat.id
		rank = isrank(redis,userID,chatID)
		group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatID)
		text = message.text
		title = message.chat.title
		if text and group is False:
			if (rank is "sudo" or rank is "sudos") or (redis.get("{}Nbot:autoaddbot".format(BOT_ID)) and GPranks(userID,chatID) == "creator"):
				if text == c.add:
					if redis.get("{}Nbot:autoaddbotN".format(BOT_ID)):
						auN = int(redis.get("{}Nbot:autoaddbotN".format(BOT_ID)))
					else:
						auN = 1
					if auN >= Bot("getChatMembersCount",{"chat_id":chatID})["result"] and not (rank is "sudo" or rank is "sudos"):
						Bot("sendMessage",{"chat_id":chatID,"text":r.Toolow.format((int(redis.get("{}Nbot:autoaddbotN".format(BOT_ID))) or 0)),"reply_to_message_id":message.message_id,"parse_mode":"html"})
						return False
					GetME = Bot("getChatMember",{"chat_id":chatID,"user_id":BOT_ID})["result"]
					if (not GetME["can_change_info"] or not GetME["can_delete_messages"] or not GetME["can_invite_users"] or not GetME["can_restrict_members"] or not GetME["can_pin_messages"] or not GetME["can_promote_members"]):
						Bot("sendMessage",{"chat_id":chatID,"text":r.GiveMEall,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						return False

				if text == c.add and not redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),chatID) and Ckuser(message):
					locksarray = {'Llink','Llongtext','Lmarkdown','Linline','Lfiles','Lcontact','Lbots','Lfwd','Lnote'}
					for lock in locksarray:
						redis.sadd("{}Nbot:{}".format(BOT_ID,lock),chatID)
					ads = Bot("getChatAdministrators",{"chat_id":chatID})
					for ad in ads['result']:
						userId = ad["user"]["id"]
						userFn = ad["user"]["first_name"]
						if ad['status'] == "administrator" and int(userId) != int(BOT_ID):
							setrank(redis,"admin",userId,chatID,"array")
						if ad['status'] == "creator":
							setrank(redis,"creator",userId,chatID,"one")
					add = redis.sadd("{}Nbot:groups".format(BOT_ID),chatID)
					Bot("exportChatInviteLink",{"chat_id":chatID})
					Bot("sendMessage",{"chat_id":chatID,"text":r.doneadd.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html"})

				elif text == c.add and redis.sismember("{}Nbot:disabledgroups".format(BOT_ID),chatID)  and Ckuser(message):
					redis.sadd("{}Nbot:groups".format(BOT_ID),chatID)
					redis.srem("{}Nbot:disabledgroups".format(BOT_ID),chatID)
					redis.hdel("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID)
					Bot("sendMessage",{"chat_id":chatID,"text":r.doneadd2.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html"})
				if text == c.disabl  and Ckuser(message):
					Bot("sendMessage",{"chat_id":chatID,"text":r.disabled.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html"})

		if text and group is True:
			if (rank is "sudo" or rank is "sudos") or (redis.get("{}Nbot:autoaddbot".format(BOT_ID)) and GPranks(userID,chatID) == "creator"):
				if text == c.add  and Ckuser(message):
					Bot("sendMessage",{"chat_id":chatID,"text":r.doneadded.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html"})
				if text == c.disabl  and Ckuser(message):
					redis.srem("{}Nbot:groups".format(BOT_ID),chatID)
					redis.sadd("{}Nbot:disabledgroups".format(BOT_ID),chatID)
					NextDay_Date = datetime.datetime.today() + datetime.timedelta(days=1)
					redis.hset("{}Nbot:disabledgroupsTIME".format(BOT_ID),chatID,str(NextDay_Date))
					Bot("sendMessage",{"chat_id":chatID,"text":r.disabl.format(title),"reply_to_message_id":message.message_id,"parse_mode":"html"})
		
		if (rank is "sudo" or rank is "sudos") and group is True:
			t = threading.Thread(target=sudo,args=(client, message,redis))
			t.setDaemon(True)
			t.start()

		if text and (rank is "sudo" or rank is "sudos" or rank is "creator" or rank is "owner") and group is True:
			t = threading.Thread(target=ranks,args=(client, message,redis))
			t.setDaemon(True)
			t.start()
		if text and (rank is "sudo" or rank is "sudos" or rank is "creator" or rank is "owner" or rank is "admin") and group is True and re.search(c.startlock,text):
			if Ckuser(message):
				t = threading.Thread(target=locks,args=(client, message,redis))
				t.setDaemon(True)
				t.start()
		if (rank is False or rank is 0) and group is True:
			t = threading.Thread(target=delete,args=(client, message,redis))
			t.setDaemon(True)
			t.start()

		if (rank is "sudo" or rank is "sudos" or rank is "creator" or rank is "owner" or rank is "admin") and group is True:
			t = threading.Thread(target=gpcmd,args=(client, message,redis))
			t.setDaemon(True)
			t.start()
		if  group is True:
			t = threading.Thread(target=allGP,args=(client, message,redis))
			t.setDaemon(True)
			t.start()


	if type is "private" and message.outgoing != True:
		text = message.text
		rank = isrank(redis,userID,chatID)
		if (rank is "sudo" or rank is "sudos"):
			t = threading.Thread(target=sudo,args=(client, message,redis))
			t.setDaemon(True)
			t.start()
		if text and re.search("^/start$",text):
			redis.sadd("{}Nbot:privates".format(BOT_ID),userID)
			print("start")
		if text and re.search("^/start (.*)$",text):
			tx = text.replace("/start ","")
			split = tx.split("=")
			order = split[0]
			print(split)

			if order == "showreplylistBOT":
				chatId = split[1]
				userId = split[2]
				TY = split[3]
				rank = isrank(redis,userId,chatId)
				if (rank == "sudo" or rank == "sudos"):
					li = redis.hkeys("{}Nbot:{}".format(BOT_ID,TY))
					if li:
						i = 1
						words = ""
						for word in li:
							words = words+"\n"+str(i)+" - {"+word+"}"
							i += 1
							if len(words) > 3000:
								Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
								words = ''
						Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Delall2R,callback_data=json.dumps(["del{}".format(TY+'BOT'),"",userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.DelallR,"reply_to_message_id":message.message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})
					
			if order == "showreplylist":
				chatId = split[1]
				userId = split[2]
				TY = split[3]
				group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatId)
				rank = isrank(redis,userId,chatId)
				if (rank is not False or rank is not  0 or rank != "vip" or rank != "admin") and group is True:
					li = redis.hkeys("{}Nbot:{}:{}".format(BOT_ID,chatId,TY))
					if li:
						i = 1
						words = ""
						for word in li:
							words = words+"\n"+str(i)+" - {"+word+"}"
							i += 1
							if len(words) > 3000:
								Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
								words = ''
						Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Delall2R,callback_data=json.dumps(["del{}".format(TY),chatId,userID])),]])
						Bot("sendMessage",{"chat_id":chatID,"text":r.DelallR,"reply_to_message_id":message.message_id,"disable_web_page_preview":True,"reply_markup":reply_markup})

			if order == "showBlocklist":
				chatId = split[1]
				userId = split[2]
				TY = split[3]
				group = redis.sismember("{}Nbot:groups".format(BOT_ID),chatId)
				rank = isrank(redis,userId,chatId)
				if (rank is not False or rank is not  0 or rank != "vip") and group is True:
					redis.hset("{}Nbot:{}:TXreplys".format(BOT_ID,chatID),tx,text)
					li = redis.smembers("{}Nbot:{}:{}".format(BOT_ID,chatId,TY))
					print(li)
					if li:
						i = 1
						words = ""
						for ID in li:
							reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Blocklistone,callback_data=json.dumps(["delfromb",TY,userID,chatId])),]])
							if TY == "blockanimations":
								Bot("sendAnimation",{"chat_id":userId,"animation":ID,"reply_markup":reply_markup})
							if TY == "blockSTICKERs":
								Bot("sendSticker",{"chat_id":userId,"sticker":ID,"reply_markup":reply_markup})
							if TY == "blockphotos":
								Bot("sendPhoto",{"chat_id":userId,"photo":ID,"reply_markup":reply_markup})
							if TY == "blockTEXTs":
								words = words+"\n"+str(i)+" - {"+ID+"}"
								i += 1
								print(len(words))
								if len(words) > 3000:
									Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})
									words = ''
						if TY == "blockTEXTs":

							Bot("sendMessage",{"chat_id":userId,"text":words,"reply_to_message_id":message.message_id,"parse_mode":"html"})

						reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(r.Delall2,callback_data=json.dumps(["delBL",TY,userID,chatId])),]])
						Bot("sendMessage",{"chat_id":userId,"text":r.Delall,"reply_to_message_id":message.message_id,"parse_mode":"html","reply_markup":reply_markup})
					else:
						Bot("sendMessage",{"chat_id":userId,"text":r.listempty2,"reply_to_message_id":message.message_id,"parse_mode":"html"})
