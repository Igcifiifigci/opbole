import logging
from telegram import InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import CommandHandler, InlineQueryHandler, ConversationHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, ParseMode
from telegram.ext import Updater, CallbackQueryHandler, CallbackContext , Filters
import random
import json
from telegram.ext.dispatcher import run_async
import time
import casinoDB as DB
import os
import requests

DB_PATH='casino.db'
conn = DB.init(DB_PATH)
DB.setup(conn)

#state
ONE , TWO , THREE , FOUR , FIVE,  *_ = range(100)
#callback data
owners = [163494588]

updater = Updater(token='2114784645:AAE6vtKRhvmBussdmpmyw1ar1tNi4DuY3VM', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

def start(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    exist = DB.get_user_value(conn , id, "white")
    text = f"Welcome <b>{name}</b> to <u><b><i>Casino 482</i></b></u>\n\n" \
           f"We have registered you under our player lists with your below information\n" \
           f"\n# username : <code>{username}</code>\n# ID : <code>{id}</code>"
    if exist == None:
     context.bot.send_photo(chat_id = update.effective_chat.id, caption = text , photo = "https://telegra.ph/file/b50d95b7d42b2f866fcac.jpg", parse_mode=ParseMode.HTML)
     DB.add_user(conn , id)
    else:
        context.bot.send_message(chat_id = update.effective_chat.id , text = "You are already a member")

def games(update , context):
    text = "<b><u>Available Games</u></b>\n\n/Dice\n/Hilo\n/Blackjack\n/Wheel"
    context.bot.send_message(chat_id = update.effective_chat.id, text = text, parse_mode = ParseMode.HTML)

def value(update , context):
    text = "<b><u>Values of each chips</u></b>\n\n⚪️ white chip : 1$\n" \
           "🔴 red chip : 5$\n🟠 orange chip : 25$\n🟡 yellow chip : 100$\n🔵 blue chip : 500$" \
           "\n🟣 purple chip : 2000$\n⚫️ black chip : 15000$"
    context.bot.send_message(chat_id = update.effective_chat.id , text = text, parse_mode = ParseMode.HTML)

def wallet(update , context):
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(conn, id, "vip")
    worth = DB.get_user_value(conn, id, "worth")
    white = DB.get_user_value(conn , id, "white")
    red = DB.get_user_value(conn, id, "red")
    orange = DB.get_user_value(conn, id, "orange")
    yellow = DB.get_user_value(conn, id, "yellow")
    blue = DB.get_user_value(conn, id, "blue")
    purple = DB.get_user_value(conn, id, "purple")
    black = DB.get_user_value(conn, id, "black")

    value = (white*1)+(red*5)+(orange*25)+(yellow*100)+(blue*500)+(purple*2500)+(black*15000)
    update.message.reply_text(f"<u><b>{name}'s Wallet</b></u>\n"
                              f"🎖 VIP : {VIP}\n\n"
                              f"<b>⚪️White Chip</b> : {white}\n"
                              f"<b>🔴Red Chip</b> : {red}\n"
                              f"<b>🟠Orange Chip</b> : {orange}\n"
                              f"<b>🟡Yellow Chip</b> : {yellow}\n"
                              f"<b>🔵Blue Chip</b> : {blue}\n"
                              f"<b>🟣Purple Chip</b> : {purple}\n"
                              f"<b>⚫Black Chip</b> : {black}\n\n"
                              f"<i>Net Worth</i> : {value}$",
                              parse_mode=ParseMode.HTML)


def add(update , context):
    if not update.message.reply_to_message:
             update.message.reply_text('reply to someone')
             return
    type = update.message.text.split()[1]
    units = update.message.text.split()[2]
    user_name = update.message.from_user.first_name
    to = update.message.reply_to_message.from_user.first_name
    user_id = update.message.reply_to_message.from_user.id
    id = update.message.from_user.id

    a = context.bot.get_chat_member(chat_id=update.effective_chat.id, user_id=update.effective_user.id).status
    msg = int(units)
    if id in owners:
        if type == "white":
         DB.add_white(conn, user_id, units)
         update.message.reply_text(f'{to} received {units}  ⚪️ white chips')
        if type == "red":
         DB.add_red(conn, user_id, units)
         update.message.reply_text(f'{to} received {units}  🔴 red chips')
        if type == "orange":
         DB.add_orange(conn, user_id, units)
         update.message.reply_text(f'{to} received {units}  🟠 orange chips')
        if type == "yellow":
         DB.add_yellow(conn, user_id, units)
         update.message.reply_text(f'{to} received {units} 🟡 yellow chips')
        if type == "blue":
         DB.add_blue(conn, user_id, units)
         update.message.reply_text(f'{to} received {units} 🔵 blue chips')
        if type == "purple":
         DB.add_purple(conn, user_id, units)
         update.message.reply_text(f'{to} received {units} 🟣 purple chips')
        if type == "black":
         DB.add_black(conn, user_id, units)
         update.message.reply_text(f'{to} received {units} ⚫️ black chips')
    else:
         update.message.reply_text('not authorized')
         return -1

def dice(update , context):
    cd = context.chat_data
    query = update.callback_query
    id = update.effective_user.id
    name = update.effective_user.first_name
    username = update.effective_user.name
    VIP = DB.get_user_value(conn, id, "vip")
    cd["worth"] = worth = DB.get_user_value(conn, id, "worth")
    cd["white"] = white = DB.get_user_value(conn , id, "white")
    cd["red"] = red = DB.get_user_value(conn, id, "red")
    cd["orange"] = orange = DB.get_user_value(conn, id, "orange")
    cd["yellow"] = yellow = DB.get_user_value(conn, id, "yellow")
    cd["blue"] = blue = DB.get_user_value(conn, id, "blue")
    cd["purple"] = purple = DB.get_user_value(conn, id, "purple")
    cd["black"] = black = DB.get_user_value(conn, id, "black")

    cd['default'] = default = 2
    cd['pays'] = pays = 2
    dict = {'white':1,'red':5, 'orange':25, 'yellow':100, 'blue':500, 'purple':2000, 'black':15000}

    cd["using"] = using = "⚪️ white chip"
    cd["amount"] = amount = 1

    value = (cd['white']*1)+(cd['red']*5)+(cd['orange']*25)+(cd['yellow']*100)+(cd['blue']*500)+(cd['purple']*2500)+(cd['black']*15000)
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
        update.message.reply_text("play in pm")
        return -1'''
    context.bot.send_photo(chat_id = update.effective_chat.id, photo = "https://telegra.ph/file/0fa477ea66eaa5e349686.jpg", caption =
                           "<b>Dice game is the most classical casino game\nRoll over the target to win!</b>", parse_mode = ParseMode.HTML)

    keyboard = [
        [InlineKeyboardButton("change odd", callback_data="odd"), InlineKeyboardButton("change chip", callback_data="chip")],
        [InlineKeyboardButton(" - ", callback_data="minus"),InlineKeyboardButton(f"{amount}", callback_data="amount"), InlineKeyboardButton(" + ", callback_data="add")],
        [InlineKeyboardButton("Play", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(f"<b><u>Dice</u></b>\n"
                              f"<i>Net Worth</i> : {value}$\n\n"
                              f"<b>⚪️White Chip</b> : {white}\n"
                              f"<b>🔴Red Chip</b> : {red}\n"
                              f"<b>🟠Orange Chip</b> : {orange}\n"
                              f"<b>🟡Yellow Chip</b> : {yellow}\n"
                              f"<b>🔵Blue Chip</b> : {blue}\n"
                              f"<b>🟣Purple Chip</b> : {purple}\n"
                              f"<b>⚫Black Chip</b> : {black}\n\n"
                              f"Chip in use :{using}\nBet amount : {amount}\nBet size : {dict['white']*amount}$\n\n"
                              f"<b>Game Odd = {default}</b>\n"
                              f"<b>Game Payout = {pays}x</b>\n"
                              , reply_markup=reply_markup,parse_mode = ParseMode.HTML)

    return ONE

def dicebackodd(update , context):
    cd = context.chat_data
    query = update.callback_query
    white = cd['white']
    red = cd['red']
    orange = cd['orange']
    yellow =cd['yellow']
    blue = cd['blue']
    purple = cd['purple']
    black = cd['black']
    default = cd['default']

    changed = query.data
    cd['default'] = changed
    if query.data =="backfromodd":
        changed = 2

    dict = {'white':1,'red':5, 'orange':25, 'yellow':100, 'blue':500, 'purple':2000, 'black':15000}

    cd["using"] = using = "⚪️ white chip"
    cd["amount"] = amount = 1

    value = (cd['white']*1)+(cd['red']*5)+(cd['orange']*25)+(cd['yellow']*100)+(cd['blue']*500)+(cd['purple']*2500)+(cd['black']*15000)
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
        update.message.reply_text("play in pm")
        return -1'''
    keyboard = [
        [InlineKeyboardButton("change odd", callback_data="odd"), InlineKeyboardButton("change chip", callback_data="chip")],
        [InlineKeyboardButton(" - ", callback_data="minus"),InlineKeyboardButton(f"{amount}", callback_data="amount"), InlineKeyboardButton(" + ", callback_data="add")],
        [InlineKeyboardButton("Play", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"<b><u>Dice</u></b>\n"
                              f"<i>Net Worth</i> : {value}$\n\n"
                              f"<b>⚪️White Chip</b> : {white}\n"
                              f"<b>🔴Red Chip</b> : {red}\n"
                              f"<b>🟠Orange Chip</b> : {orange}\n"
                              f"<b>🟡Yellow Chip</b> : {yellow}\n"
                              f"<b>🔵Blue Chip</b> : {blue}\n"
                              f"<b>🟣Purple Chip</b> : {purple}\n"
                              f"<b>⚫Black Chip</b> : {black}\n\n"
                              f"Chip in use :{using}\nBet amount : {amount}\nBet size : {dict['white']*amount}$\n\n"
                              f"<b>Game Odd = {changed}</b>\n"
                              f"<b>Game Payout = {changed}x</b>\n", reply_markup=reply_markup,parse_mode = ParseMode.HTML)

    return ONE

def dicebackchip(update , context):
    cd = context.chat_data
    query = update.callback_query
    white = cd['white']
    red = cd['red']
    orange = cd['orange']
    yellow =cd['yellow']
    blue = cd['blue']
    purple = cd['purple']
    black = cd['black']
    default = cd['default']
    newchip = query.data
    x = 1
    if cd['default'] == 2:
        x = cd['default']
    if cd['default'] !=2:
        x = cd['changed']

    if query.data =="backfromchip":
        newchip = "⚪️white"

    dict = {'white':1,'red':5, 'orange':25, 'yellow':100, 'blue':500, 'purple':2000, 'black':15000}

    cd["using"] = using = "⚪️ white chip"
    cd["amount"] = amount = 1

    value = (cd['white']*1)+(cd['red']*5)+(cd['orange']*25)+(cd['yellow']*100)+(cd['blue']*500)+(cd['purple']*2500)+(cd['black']*15000)
    '''Chat = update.effective_chat
    if update.effective_chat.type != Chat.PRIVATE:
        update.message.reply_text("play in pm")
        return -1'''
    keyboard = [
        [InlineKeyboardButton("change odd", callback_data="odd"), InlineKeyboardButton("change chip", callback_data="chip")],
        [InlineKeyboardButton(" - ", callback_data="minus"),InlineKeyboardButton(f"{amount}", callback_data="amount"), InlineKeyboardButton(" + ", callback_data="add")],
        [InlineKeyboardButton("Play", callback_data="play")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"<b><u>Dice</u></b>\n"
                              f"<i>Net Worth</i> : {value}$\n\n"
                              f"<b>⚪️White Chip</b> : {white}\n"
                              f"<b>🔴Red Chip</b> : {red}\n"
                              f"<b>🟠Orange Chip</b> : {orange}\n"
                              f"<b>🟡Yellow Chip</b> : {yellow}\n"
                              f"<b>🔵Blue Chip</b> : {blue}\n"
                              f"<b>🟣Purple Chip</b> : {purple}\n"
                              f"<b>⚫Black Chip</b> : {black}\n\n"
                              f"Chip in use :{newchip}\nBet amount : {amount}\nBet size : {dict['white']*amount}$\n\n"
                              f"<b>Game Odd = {x}</b>\n"
                              f"<b>Game Payout = {x}x</b>\n", reply_markup=reply_markup,parse_mode = ParseMode.HTML)

    return ONE


def diceodd(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    keyboard = [
        [InlineKeyboardButton("1.1x", callback_data="1.1"),InlineKeyboardButton("1.5x", callback_data="1.5"),InlineKeyboardButton("2x", callback_data="2")],
        [InlineKeyboardButton("3x", callback_data="3"),InlineKeyboardButton("5x", callback_data="5"),InlineKeyboardButton("10x", callback_data="10"),],
        [InlineKeyboardButton("Back", callback_data="backfromodd")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(f"<b><u>Click the button below to change to your desired odd of the game</u></b>\n\n"
                       f"1.1x - win rate 90%\n"
                       f"1.5x - win rate 66%\n"
                       f"2.0x - win rate 50%\n"
                       f"3.0x - win rate 33%\n"
                       f"5.0x - win rate 20%\n"
                       f"10x - win rate 10%", reply_markup=reply_markup, parse_mode =ParseMode.HTML)

    return ONE

def dicechip(update , context):
    cd = context.chat_data
    query = update.callback_query
    query.answer()
    text = "<b><u>Values of each chips</u></b>\n\n⚪️ white chip : 1$\n" \
           "🔴 red chip : 5$\n🟠 orange chip : 25$\n🟡 yellow chip : 100$\n🔵 blue chip : 500$" \
           "\n🟣 purple chip : 2000$\n⚫️ black chip : 15000$\n\n click below to switch out chips"
    keyboard = [
        [InlineKeyboardButton("⚪ white", callback_data="⚪️white"), InlineKeyboardButton("🔴red", callback_data="🔴 red")
         ],
        [InlineKeyboardButton("🟠orange", callback_data="🟠 orange"), InlineKeyboardButton("🟡yellow", callback_data="🟡 yellow")
          ],
        [InlineKeyboardButton("🔵blue", callback_data="🔵 blue"),InlineKeyboardButton("🟣purple", callback_data="🟣 purple"),
         InlineKeyboardButton("⚫️Black", callback_data="⚫ black")],
        [InlineKeyboardButton("Back", callback_data="backfromchip")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    query.edit_message_text(text = text,  reply_markup=reply_markup, parse_mode=ParseMode.HTML)

    return ONE

def diceminus(update , context):
    pass

def diceadd(update , context):
    pass

def diceplay(update , context):
    pass

DICE_HANDLER = ConversationHandler(
        entry_points=[CommandHandler('dice', dice)],
        states={
            ONE: [CallbackQueryHandler(diceodd, pattern='^' + str("odd") + '$'),
CallbackQueryHandler(dicechip, pattern='^' + str("chip") + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('1.1') + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('1.5') + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('2') + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('3') + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('5') + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('10') + '$'),
                  CallbackQueryHandler(dicebackodd, pattern='^' + str('backfromodd') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('⚪ white') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('🔴 red') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('🟠 orange') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('🟡 yellow') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('🔵 blue') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('🟣 purple') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('⚫ black') + '$'),
CallbackQueryHandler(dicebackchip, pattern='^' + str('backfromchip') + '$'),



            ],
            TWO: [

            ],
        },
        fallbacks=[],

    allow_reentry=True,
    per_user=False
    )


START_HANDLER = CommandHandler('start', start)
WALLET_HANDLER = CommandHandler('wallet', wallet)
GAMES_HANDLER = CommandHandler('games', games)
ADD_HANDLER = CommandHandler('add', add)
VALUE_HANDLER = CommandHandler('value', value)

dispatcher.add_handler(START_HANDLER)
dispatcher.add_handler(WALLET_HANDLER)
dispatcher.add_handler(GAMES_HANDLER)
dispatcher.add_handler(ADD_HANDLER)
dispatcher.add_handler(DICE_HANDLER)
dispatcher.add_handler(VALUE_HANDLER)

logger = logging.getLogger()
updater.start_polling(clean = True)
