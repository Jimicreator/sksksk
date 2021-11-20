#    Copyright (C) @DevsExpo 2020-2021
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.

import requests
from telethon.tl.types import InputWebDocument
from telethon import TelegramClient, events
from starkfunc import check_if_subbed
from telethon import custom, events, Button
from telethon.tl.functions.users import GetFullUserRequest
from telethon.tl.types import MessageEntityMentionName
from Configs import Config
from loggers import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import os
import random
import re
from math import ceil
import telethon
from pymongo import MongoClient
from main_startup.config_var import Config
from pymongo.errors import ConnectionFailure
from telethon import Button, custom, events, functions
from dB import get_user_limit, add_user_to_db, get_all_users, dl_all_users, dl_one_user, add_hits_to_db, rm_all_hits, all_hit, rm_hit, hit_exists

bot = TelegramClient("bot", api_id=Config.API_ID, api_hash=Config.API_HASH)
warnerstarkbot = bot.start(bot_token=Config.BOT_TOKEN)


try:
    mongo_client = MongoClient(Config.MONGO_DB)
    mongo_client.server_info()
except ConnectionFailure:
    print("Invalid Mongo DB URL. Please Check Your Credentials! Friday is Exiting...")
    quit(1)

@warnerstarkbot.on(events.NewMessage(pattern="^/start$"))
async def hmm(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	return
    st = await event.client(GetFullUserRequest(event.sender_id))
    user_text = f"""**Hello {st.user.first_name},
Welcome To {Config.ACCOUNT_GEN_NAME} Limited/Unlimited Account Generator Bot

To Know About commands type:
/cmds

Bot Made With ❤️ By @Jimi_Bots**
""" 
    await event.reply(user_text) 
    
@warnerstarkbot.on(events.NewMessage(pattern="^/(help|cmds|commands|cmd|command)$"))
async def cmds(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	return
    st = await event.client(GetFullUserRequest(event.sender_id))
    help_text = f"""**Hello {st.user.first_name},
My Commands Are As Follows:

/start - To Restart Bot..!
/cmds - To Get Help Menu
/generate - To Generate Zee5 Accounts
/about - To Get Your Current Info

Share And Support Us...❤️**
"""
    await event.reply(help_text)     
    
@warnerstarkbot.on(events.NewMessage(pattern="^/(generate|gen|account)$"))
async def hmm(event):
    if Config.JTU_ENABLE:
    	starky = await check_if_subbed(Config.CHANNEL_USERNAME, event, warnerstarkbot)
    	if starky is False:
        	await event.reply("**I am Sorry To Say That, To Access Me You Have To Be The Member Of Our Channel To Use This Bot..!**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        	return
    hmmw = await event.reply("**Generating Account...Stay Tuned.**")
    if get_user_limit(int(event.sender_id)) >= Config.GEN_LIMIT_PERDAY:
        await hmmw.edit(f"**Your Daily Limit is exhausted, Kindly Contact the admins to increase ur limit\n\nBy The Way Daily Limit is {Config.GEN_LIMIT_PERDAY} accounts per day**", buttons=[[custom.Button.url("Join Channel", Config.CHANNEL_URL)]])
        return
    add_user_to_db(int(event.sender_id), int(1))
    hits = all_hit()
    sed = random.choice(hits)
    user_s = await warnerstarkbot.get_me()
    username = user_s.username
    email, password = sed.split(":")
    await hmmw.edit(
        f"<b><u>{Config.ACCOUNT_GEN_NAME} Account Generated.</u></b> \n<b>Email :</b> <code>{email}</code> \n<b>Password :</b><code>{password}</code> \n<b>You Can Check Your Limit or Info By /about<b> \n<b>Generated By @{username}</b>",
        parse_mode="HTML")
    
@warnerstarkbot.on(events.NewMessage(pattern="^/reset$"))
async def reset(event):
    if event.sender_id != Config.OWNER_ID:
        return
    dl_all_users()
    await event.reply("`Reset Sucessfull Done!`") 
    
    
@warnerstarkbot.on(events.NewMessage(pattern="^/broadcast"))
async def reset(event):
    if event.sender_id != Config.OWNER_ID:
        return
    error = 0
    ds = event.text.split(" ", maxsplit=1)[1]
    ok = get_all_users()
    if not ok:
        await event.reply("Wut? No Users In Your Bot, But U Want To Broadcast. WTF")
        return
    for s in ok:
        try:
            await warnerstarkbot.send_message(int(s['user']), ds)
        except:
            error += 1
            pass
    await event.reply(f"Broadcast Done With {error} And Sucess in {len(ok) - error}!")    
        
async def clear_data():
    ok = get_all_users()
    if not ok:
        return
    for s in ok:
        try:
            await warnerstarkbot.send_message(int(s['user']), "**Limit Has Been Reset , Generate Your Accounts Now !**")
        except:
            error += 1
            pass
    dl_all_users()
        
@warnerstarkbot.on(events.NewMessage(pattern="^/about$"))
async def a(event):
    info_s = get_user_limit(event.sender_id)
    await event.reply(f"**📡Your Account Information\n\nUser-ID : {event.sender_id} \nLimit Used : {info_s} \nLimit Left : {Config.GEN_LIMIT_PERDAY-info_s}**")


scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")
scheduler.add_job(clear_data, trigger="cron", hour=6)
scheduler.start()

print("Bot Started Successfully")


def startbot():
    warnerstarkbot.run_until_disconnected()

if __name__ == "__main__":
    startbot()
