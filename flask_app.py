# it is a bot with a webhook
import telebot  # pip install pyTelegramBotAPI
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import urllib
import json
import datetime
from config import TOKEN, SECRET, URL
from flask import Flask, request, abort


bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
url = URL + SECRET
bot.set_webhook(url=url)

app = Flask(__name__)


@app.route('/{}'.format(SECRET), methods=["POST"])
def telegram_webhook():
    if request.headers.get('content-type') == 'application/json':
        # json_string = request.get_data().decode('utf-8')
        json_string = request.stream.read().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return 'ok', 200
    else:
        abort(403)


listofcurrencies = ["AUD", "CAD", "CNY", "HRK", "CZK", "DKK", "HKD", "HUF", "INR", "IDR", "IRR", "ILS", "JPY", "KZT", "KRW", "MXN", "MDL", "NZD", "NOK", "RUB", "SAR", "SGD", "ZAR", "SEK", "CHF", "EGP", "GBP", "USD",
                    "BYN", "AZN", "RON", "TRY", "XDR", "BGN", "EUR", "PLN", "DZD", "BDT", "AMD", "IQD", "KGS", "LBP", "LYD", "MYR", "MAD", "PKR", "VND", "THB", "AED", "TND", "UZS", "TWD", "TMT", "GHS", "RSD", "TJS", "GEL", "XAU", "XAG", "XPT", "XPD"]
lstcur = '''List of currencies: \n/AUD\n /CAD\n /CNY\n /HRK\n /CZK\n /DKK\n /HKD\n /HUF\n /INR\n /IDR\n /IRR\n /ILS\n /JPY\n /KZT\n /KRW\n /MXN\n /MDL\n /NZD\n /NOK\n /RUB\n /SAR\n /SGD\n /ZAR\n /SEK\n /CHF\n /EGP\n /GBP\n /USD\n /BYN\n /AZN\n /RON\n /TRY\n /XDR\n /BGN\n /EUR\n /PLN\n /DZD\n /BDT\n /AMD\n /IQD\n /KGS\n /LBP\n /LYD\n /MYR\n /MAD\n /PKR\n /VND\n /THB\n /AED\n /TND\n /UZS\n /TWD\n /TMT\n /GHS\n /RSD\n /TJS\n /GEL\n /XAU\n /XAG\n /XPT\n /XPD'''


def stat(id):
    with open("stat.txt", "a") as file:
        file.write(str(id)+";" + datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"\n")


def get_rate(currency):
    currencyname = currency.replace("/", "").upper()
    if currencyname not in listofcurrencies:
        answer = "Please, specify a currency name in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc."
        return answer

    # https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20181030&json
    todaydate = datetime.datetime.now().strftime("%Y%m%d")
    URL = 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currencyname + '&date=' + todaydate + '&json'
    content = urllib.request.urlopen(URL)
    try:
        answer = f"NBU rate {currencyname} / UAH =  {json.load(content)[0]['rate']} for today ({todaydate})"
    except IndexError:
        answer = "Something went wrong. Please try againe later"
    return answer


def gen_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2
    markup.add(InlineKeyboardButton("USD", callback_data="USD"),
               InlineKeyboardButton("EUR", callback_data="EUR"),
               InlineKeyboardButton("other", callback_data="other"))
    return markup


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Please, select a  currency", reply_markup=gen_markup())


@bot.message_handler(commands=['list'])
def send_list(message):

    bot.send_message(message.chat.id, lstcur)


@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
def sendmessage(message):
    bot.send_message(
        message.chat.id, "This content is not supported. Please, specify a currency name in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc ")


@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "other":
        bot.send_message(call.from_user.id, lstcur)
    else:
        bot.send_message(call.from_user.id, get_rate(call.data))
        stat(call.from_user.id)


@bot.message_handler(content_types=["text"])
def message_handler(message):
    txt = message.text.replace("/", "").upper()
    if txt in listofcurrencies:
        bot.send_message(message.chat.id, get_rate(message.text))
    else:
        bot.send_message(message.chat.id, "Please, select a  currency", reply_markup=gen_markup())

    stat(message.chat.id)


@app.route('/')
def index():
    return 'Hello!'
