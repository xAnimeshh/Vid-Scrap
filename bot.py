# © Animesh Verma
# Don't Laugh at my codes... I'm a Piro Noob 👀

# The Logging Things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
from config import Config
from pyrogram import Client, filters 

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

if __name__ == "__main__" :
    app = Client(
        "Vid Scrap Bot",
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
    )
    app.set_parse_mode("markdown")
    app.run()
