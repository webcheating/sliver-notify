import asyncio
import signal
from colorlog import ColoredFormatter
from aiogram import Dispatcher
from aiogram.utils.formatting import Text, Bold, Code
from sliver import *
import config as cfg
from src.utils.notify import send_msg
from src.init_bot import bot
from src import info
from src import menu

TOKEN = cfg.TOKEN
CHAT_ID = cfg.CHAT_ID
CFG_PATH = cfg.CFG_PATH
logger = cfg.logger

dp = Dispatcher()
dp.include_router(menu.router)

def extract_beacon_dict(beacons_list):
    return {beacon.ID: beacon for beacon in beacons_list}

async def extract_all_beacons(beacons, sessions):
    info.current_beacons(beacons, sessions)

async def take_shot(sessions, session):
    session = await client.interact_session(sessions[session].ID)
    whoami = await session.whoami()
    message = Text(Bold("output: \n"), Code(whoami))
    session_exec(message)
    

async def sliver():
    config = SliverClientConfig.parse_config_file(CFG_PATH)
    client = SliverClient(config)
    await client.connect()
    
    old_beacons = extract_beacon_dict(await client.beacons())
    sessions = await client.sessions()
    logger.info(f'[*] current sessions: {len(sessions)}')
    beacons = await client.beacons()
    logger.info(f'[*] current beacons: {len(beacons)}')
    logger.info(f'[+] fine')
    try:
        while True:
            try:
                sessions = await client.sessions()
                beacons = await client.beacons()
                extract = await extract_all_beacons(beacons, sessions)
            except Exception as e:
                logger.error(f"error occured: {e}")
            #extract = await extract_all_beacons(old_beacons, sessions)
            #try:
            #    current_beacons = await asyncio.wait_for(client.beacons(), timeout=10)
            #except asyncio.TimeoutError:
            #    logger.error("[sliver] timeout expired, retrying...")
            #    continue
            #logger.info("fine")

            #current_beacons = extract_beacon_dict(await client.beacons())
            try:
                current_beacons = extract_beacon_dict(await asyncio.wait_for(client.beacons(), timeout=4))
            except asyncio.TimeoutError:
                logger.warning("[sliver] Timeout while polling beacons — skipping cycle")
                continue
            old_ids = set(old_beacons.keys())
            current_ids = set(current_beacons.keys())
            added_ids = current_ids - old_ids
            removed_ids = old_ids - current_ids
            if added_ids:
                for beacon_id in added_ids:
                    logger.error(f'IDS: {added_ids}')
                    beacon = current_beacons[beacon_id]
                    await send_msg(beacon, 'add', len(current_beacons))
                    logger.info(f'[+] added beacon {beacon.ID}')
                    logger.info(f'[*] full beacon data: {beacon}')
            if removed_ids:
                for beacon_id in removed_ids:
                    logger.error(f'IDS: {removed_ids}')
                    beacon = old_beacons[beacon_id]
                    await send_msg(beacon, 'remove', len(current_beacons))
                    logger.info(f'[x] removed beacon {beacon.ID}')
            old_beacons = current_beacons
    except asyncio.CancelledError:
        logger.info("[sliver] sliver task cancelled")
        raise
    #finally:
    #    logger.info("[sliver] stoppped")

async def run_bot():
    try:
        logger.info("[*] starting bot...")
        await dp.start_polling(bot, handle_signals=False)
    except asyncio.CancelledError:
        logger.warning("[bot] CancelledError received")
        #await dp.stop_polling()
        await bot.session.close()
        raise

async def main():
    #sliver_task = asyncio.create_task(sliver())
    sliver_task = asyncio.create_task(sliver(), name="sliver")
    #bot_task = asyncio.create_task(run_bot())
    bot_task = asyncio.create_task(run_bot(), name="bot")
    tasks = [bot_task, sliver_task]
    
    try:
        logger.info("[*] starting tasks...")
        await asyncio.gather(*tasks, return_exceptions=False)
        #await asyncio.gather(bot_task, sliver_task, return_exceptions=True)
    except asyncio.CancelledError:
        logger.error("[x] fatal error")
        for task in tasks:
            task.cancel()
        #await asyncio.gather(*tasks, return_exceptions=False)
        #await asyncio.gather(*tasks, return_exceptions=True)
        #for i in [sliver_task, bot_task]:
        #    i.cancel()
    finally:
        logger.error("[x] fatal error")
        #await sleep(2)

if __name__ == "__main__":
    #asyncio.run(send_message())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("[x] force exit 1")
