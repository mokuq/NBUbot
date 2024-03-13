# it is a bot with a webhook
import urllib
import json
import datetime

import telebot  # pip install pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from flask import Flask, request, abort

from config import TOKEN, SECRET, URL

bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
url = URL + SECRET
bot.set_webhook(url=url)

app = Flask(__name__)


@app.route('/{}'.format(SECRET), methods=["POST"])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.stream.read().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        abort(403)


list_of_currencies = ["AUD", "CAD", "CNY", "HRK", "CZK", "DKK", "HKD", "HUF", "INR", "IDR", "IRR", "ILS", "JPY", "KZT",
                      "KRW", "MXN", "MDL", "NZD", "NOK", "SAR", "SGD", "ZAR", "SEK", "CHF", "EGP", "GBP", "USD",
                      "BYN", "AZN", "RON", "TRY", "XDR", "BGN", "EUR", "PLN", "DZD", "BDT", "AMD", "IQD", "KGS", "LBP",
                      "LYD", "MYR", "MAD", "PKR", "VND", "THB", "AED", "TND", "UZS", "TWD", "TMT", "GHS", "RSD", "TJS",
                      "GEL", "XAU", "XAG", "XPT", "XPD"]
lst_cur = '''List of currencies: \n/AUD\n /CAD\n /CNY\n /HRK\n /CZK\n /DKK\n /HKD\n /HUF\n /INR\n /IDR\n /IRR\n /ILS
/JPY\n /KZT\n /KRW\n /MXN\n /MDL\n /NZD\n /NOK\n  /SAR\n /SGD\n /ZAR\n /SEK\n /CHF\n /EGP\n /GBP\n /USD\n /BYN
/AZN\n /RON\n /TRY\n /XDR\n /BGN\n /EUR\n /PLN\n /DZD\n /BDT\n /AMD\n /IQD\n /KGS\n /LBP\n /LYD\n /MYR\n /MAD\n /PKR
/VND\n /THB\n /AED\n /TND\n /UZS\n /TWD\n /TMT\n /GHS\n /RSD\n /TJS\n /GEL\n /XAU\n /XAG\n /XPT\n /XPD'''


def get_rate(currency):
    currency_name = currency.replace("/", "").upper()
    if currency_name not in list_of_currencies:
        response = "Please, specify a currency name in the right way: \n /USD or \n /EUR or \n USD, EUR, etc."
        return response

    today_date = datetime.datetime.now().strftime("%Y%m%d")
    url_full = ('https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currency_name + '&date='
                + today_date
                + '&json')
    content = urllib.request.urlopen(url_full)
    try:
        response = f"NBU rate {currency_name} / UAH =  {json.load(content)[0]['rate']} for today ({today_date})"
    except IndexError:
        response = "Something went wrong. Please try again later"

    return response


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("USD", callback_data="get_rate/USD"),
        InlineKeyboardButton("EUR", callback_data="get_rate/EUR"),
        InlineKeyboardButton("other", callback_data="other")
    )
    return markup


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Please, select a  currency", reply_markup=gen_markup())


@bot.message_handler(commands=['list'])
def send_list(message):
    bot.send_message(message.chat.id, lst_cur)


@bot.message_handler(
    content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
def send_message(message):
    bot.send_message(
        message.chat.id,
        "This content is not supported. Please, specify a currency name in a right way: \n /USD or \n /EUR  or \n "
        "USD, EUR \n etc ")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    callback_data = call.data.split("/")
    action = callback_data[0]
    if action == "get_rate":
        currency_code = callback_data[1]
        response = get_rate(currency_code)
        bot.send_message(call.from_user.id, response)
    elif action == "other":
        bot.send_message(call.from_user.id, lst_cur)


@bot.message_handler(content_types=["text"])
def message_handler(message):
    txt = message.text.replace("/", "").upper()
    if txt in list_of_currencies:
        bot.send_message(message.chat.id, get_rate(message.text))
    else:
        bot.send_message(message.chat.id, "Please, select a  currency", reply_markup=gen_markup())


@app.route('/')
def index():
    return 'Hello!'
