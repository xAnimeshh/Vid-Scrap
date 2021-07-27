import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import shutil
import time
from config import Config
from pyrogram import Client, filters 

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from .ffmpeg import generate_screen_shots
from .progress import progress_for_pyrogram


@Client.on_message(filters.command(["generate_ss","screenshot"]))
async def generate_screen_shot(bot, update):
    if update.reply_to_message is not None:
        download_location = Config.DOWNLOAD_LOCATION + "/"
        a = await bot.send_message(
            chat_id=update.chat.id,
            text="**✅ Okay... Generating ScreenShots...!**",
            reply_to_message_id=update.message_id
        )
        c_time = time.time()
        the_real_download_location = await bot.download_media(
            message=update.reply_to_message,
            file_name=download_location,
            progress=progress_for_pyrogram,
            progress_args=(
                "**✅ Okay... Generating ScreenShots...!**",
                a,
                c_time
            )
        )
        if the_real_download_location is not None:
            await bot.edit_message_text(
                text="**✅ Successfully Generated Screenshots... Now Uploading them 👇🏻**",
                chat_id=update.chat.id,
                message_id=a.message_id
            )
            tmp_directory_for_each_user = Config.DOWNLOAD_LOCATION + "/" + str(update.from_user.id)
            if not os.path.isdir(tmp_directory_for_each_user):
                os.makedirs(tmp_directory_for_each_user)
            images = await generate_screen_shots(
                the_real_download_location,
                tmp_directory_for_each_user,
                False,
                5,
                9
            )
            logger.info(images)
            await bot.edit_message_text(
                text="**🥳 Uploading To Telegram...**",
                chat_id=update.chat.id,
                message_id=a.message_id
            )
            media_album_p = []
            if images is not None:
                i = 0
                caption = "__**© Coded By Animesh Verma**__"
                for image in images:
                    if os.path.exists(image):
                        if i == 0:
                            media_album_p.append(
                                pyrogram.types.InputMediaPhoto(
                                    media=image,
                                    caption=caption,
                                    parse_mode="html"
                                )
                            )
                        else:
                            media_album_p.append(
                                pyrogram.types.InputMediaPhoto(
                                    media=image
                                )
                            )
                        i = i + 1
            await bot.send_media_group(
                chat_id=update.chat.id,
                disable_notification=True,
                reply_to_message_id=a.message_id,
                media=media_album_p
            )
            #
            try:
                shutil.rmtree(tmp_directory_for_each_user)
                os.remove(the_real_download_location)
            except:
                pass
            await bot.edit_message_text(
                text="**😝 Successfully Uploaded ScreenShots... 📸\n✅ Thanks for Using Meh..!**",
                chat_id=update.chat.id,
                message_id=a.message_id,
                disable_web_page_preview=True
            )
    else:
        await bot.send_message(
            chat_id=update.chat.id,
            text="**😓 You Noobie, Reply to a Telegram Media to Generate ScreenShots...!**",
            reply_to_message_id=update.message_id
        )
