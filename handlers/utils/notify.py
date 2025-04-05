import asyncio
import logging
import config as cfg
from handlers.init_bot import bot
from aiogram.utils.formatting import Text, Bold, Code

logger = cfg.logger
CHAT_ID = cfg.CHAT_ID

async def send_msg(beacon, action, current_beacons):
    logging.warning(beacon)
    logging.warning(action)
    logging.warning(current_beacons)
    try:
        if action == 'add':
            message = Text(Bold("🩸 found new beacon 🩸\n\n"),
                           Bold("UUID:   "), Code(beacon.ID),
                           Bold("\nusername:   "), Code(beacon.Username),
                           Bold("\nOS:   "), Code(beacon.OS),
                           Bold("\nbuild:   "), Code(beacon.Version),
                           Bold("\nfile:   "), Code(beacon.Filename),
                           Bold("\nPID:   "), Code(beacon.PID),
                           Bold("\ntransport:   "), Code(beacon.Transport),
                           Bold("\nactive C2:   "), Code(beacon.ActiveC2),
                           Bold("\n\ncurrent beacons:   ", Code(current_beacons))
                           )
        if action == 'remove':
            message = Text(Bold("🗑 removed beacon 🗑\n\n"),
                           Bold("UUID:   "), Code(beacon.ID),
                           Bold("\nusername:   "), Code(beacon.Username),
                           Bold("\n\ncurrent beacons:   ", Code(current_beacons))
                           )
            #               Bold("\nOS:   "), Code(beacon.OS),
            #               Bold("\nfile:   "), Code(beacon.Filename),
            #               Bold("\nactive C2: "), Code(beacon.ActiveC2)
            #               )
            #message = Text(Bold("🗑 removed beacon 🗑\n\n"),
            #               Bold("UUID:   "), Code(beacon.ID),
            #               Bold("\nusername:   "), Code(beacon.Username),
            #               Bold("\nOS:   "), Code(beacon.OS),
            #               Bold("\nfile:   "), Code(beacon.Filename),
            #               Bold("\nactive C2: "), Code(beacon.ActiveC2)
            #               )
        await bot.send_message(chat_id=CHAT_ID, **message.as_kwargs())
    except Exception as e:
        logging.error("[x] error sending message")

    #msg = f"Beacon {event_type.upper()}: {beacon['ID']}"
    #await bot.send_message(chat_id=CHAT_ID, text=msg)
