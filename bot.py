#    This file is part of the ChannelAutoForwarder distribution (https://github.com/xditya/ChannelAutoForwarder).
#    Copyright (c) 2021-2022 Aditya
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, version 3.
#
#    This program is distributed in the hope that it will be useful, but
#    WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
#    General Public License for more details.
#
#    License can be found in < https://github.com/xditya/ChannelAutoForwarder/blob/main/License> .

import logging
from telethon import TelegramClient, events, Button
from decouple import config

logging.basicConfig(
    format="[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s", level=logging.INFO
)

# start the bot
logging.info("Starting...")
try:
    apiid = 2992000
    apihash = "235b12e862d71234ea222082052822fd"
    bottoken = "6320216767:AAGWg4iaa1b5nceptKcMO8gtv4PqdZh1fM0"
    frm = [int(-1001638858603)]
    tochnls = [int(-1001959515403)]
    datgbot = TelegramClient("bot", apiid, apihash).start(bot_token=bottoken)
except:
    logging.error("Environment vars are missing! Kindly recheck.")
    logging.info("Bot is quiting...")
    exit()


@datgbot.on(events.NewMessage(pattern="/start"))
async def _(event):
    await event.reply("@DroneBots")


@datgbot.on(events.NewMessage(pattern="/help"))
async def helpp(event):
    await event.reply(
        "**Help**\n\nThis bot will send all new posts in one channel to the other channel. (without forwarded tag)!\nIt can be used only in two channels at a time, so kindly deploy your own bot from [here](https://github.com/xditya/ChannelAutoForwarder).\n\nAdd me to both the channels and make me an admin in both, and all new messages would be autoposted on the linked channel!!\n\nLiked the bot? Drop a ♥ to @xditya_Bot :)"
    )


@datgbot.on(events.NewMessage(incoming=True, chats=frm))
async def _(event):
    for tochnl in tochnls:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await datgbot.send_file(
                    tochnl, photo, caption=event.text, link_preview=False
                )
            elif event.media:
                try:
                    if event.media.webpage:
                        await datgbot.send_message(
                            tochnl, event.text, link_preview=False
                        )
                except Exception:
                    media = event.media.document
                    await datgbot.send_file(
                        tochnl, media, caption=event.text, link_preview=False
                    )
                finally:
                    return
            else:
                await datgbot.send_message(tochnl, event.text, link_preview=False)
        except Exception as exc:
            logging.error(
                "TO_CHANNEL ID is wrong or I can't send messages there (make me admin).\nTraceback:\n%s",
                exc,
            )


logging.info("Bot has started.")
logging.info("Do visit @its_xditya..")
datgbot.run_until_disconnected()
