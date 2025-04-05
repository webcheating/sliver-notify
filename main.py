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
    #try:
    logger.info(f'[+] fine')
    while True:
        try:
            sessions = await client.sessions()
            beacons = await client.beacons()
            extract = await extract_all_beacons(beacons, sessions)
        except Exception as e:
            logger.error("error occured: ", e)
        #extract = await extract_all_beacons(old_beacons, sessions)
        #try:
        #    current_beacons = await asyncio.wait_for(client.beacons(), timeout=10)
        #except asyncio.TimeoutError:
        #    logger.error("[sliver] timeout expired, retrying...")
        #    continue
        #logger.info("fine")
        current_beacons = extract_beacon_dict(await client.beacons())
        old_ids = set(old_beacons.keys())
        current_ids = set(current_beacons.keys())
        added_ids = current_ids - old_ids
        removed_ids = old_ids - current_ids
        if added_ids:
            for beacon_id in added_ids:
                beacon = current_beacons[beacon_id]
                await send_msg(beacon, 'add', len(current_beacons))
                logger.info(f'[+] added beacon {beacon.ID}')
                logger.info(f'[*] full beacon data: {beacon}')
        if removed_ids:
            for beacon_id in removed_ids:
                beacon = old_beacons[beacon_id]
                await send_msg(beacon, 'remove', len(current_beacons))
                logger.info(f'[x] removed beacon {beacon.ID}')
        old_beacons = current_beacons
        await asyncio.sleep(2)
    #except asyncio.CancelledError:
    #    logger.info("[sliver] sliver task cancelled")
    #finally:
    #    logger.info("[sliver] stoppped")

async def run_bot():
    #await dp.start_polling(bot)
    try:
        await dp.start_polling(bot)
    except asyncio.CancelledError:
        await bot.stop_polling()

async def gather(*tasks, **kwargs):
    tasks = [ task if isinstance(task, asyncio.Task) else asyncio.create_task(task)
              for task in tasks ]
    try:
        return await asyncio.gather(*tasks, **kwargs)
    except BaseException:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        raise

async def main():
    #logger.warning("test1")
    sliver_task = asyncio.create_task(sliver())
    bot_task = asyncio.create_task(run_bot())
    stop_event = asyncio.Event()
    #logger.warning("test2")
    def handle_sig():
        #logger.error("[x] force exit 3")
        stop_event.set()

    loop = asyncio.get_running_loop()
    loop.add_signal_handler(signal.SIGINT, handle_sig)
    loop.add_signal_handler(signal.SIGTERM, handle_sig)
    #await stop_event.wait()
    
    #logger.warning("test3")
    #for task in [sliver_task, bot_task]:
    #    task.cancel()
    #    try:
    #        await asyncio.wait_for(task, timeout=10)
    #    except asyncio.TimeoutError:
    #        logger.error(f"task {task} expired")

    #    await bot.session.close()
    
    try:
        logger.warning("test4")
        #await asyncio.gather(sliver_task, bot_task, return_exceptions=True)
        await gather(sliver(), run_bot())
    except:
        logger.error("[x] fatal error")
        for i in [sliver_task, bot_task]:
            i.cancel()
    finally:
        logger.info("fatal error")
        #await sleep(2)

if __name__ == "__main__":
    #asyncio.run(send_message())
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.error("[x] force exit 1")
