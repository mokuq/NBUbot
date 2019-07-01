# it is a bot with a webhook
import telebot # pip install pyTelegramBotAPI
import urllib
import json
import datetime
from bottoken import TOKEN, SECRET
from flask import Flask, request, abort


bot = telebot.TeleBot(TOKEN, threaded=False)
bot.remove_webhook()
url = "https://vmokuq.pythonanywhere.com/{}".format(SECRET)
bot.set_webhook(url = url)

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

def get_rate(currency):
	currencyname = currency.replace("/", "").upper()
	listofcurrencies = ["AUD", "CAD", "CNY", "HRK", "CZK", "DKK", "HKD", "HUF", "INR", "IDR", "IRR", "ILS", "JPY", "KZT", "KRW", "MXN", "MDL", "NZD", "NOK", "RUB", "SAR", "SGD", "ZAR", "SEK", "CHF", "EGP", "GBP", "USD", "BYN", "AZN", "RON", "TRY", "XDR", "BGN", "EUR", "PLN", "DZD", "BDT", "AMD", "IQD", "KGS", "LBP", "LYD", "MYR", "MAD", "PKR", "VND", "THB", "AED", "TND", "UZS", "TWD", "TMT", "GHS", "RSD", "TJS", "GEL", "XAU", "XAG", "XPT", "XPD"]
	if currencyname not in listofcurrencies:
	    answer =  "Please, specify a currency name in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc."
	    return answer

	# https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20181030&json
	todaydate = datetime.datetime.now().strftime("%Y%m%d")
	URL= 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currencyname + '&date=' + todaydate + '&json'
	content = urllib.request.urlopen(URL)
	try:
		answer = f"NBU rate {currencyname} / HRN =  {json.load(content)[0]['rate']} for today ({todaydate})"
	except IndexError:
		answer = "Please, specify a currency name in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc"
	return answer

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    answer = message.chat.first_name + ", good day! Please select a currency: \n /USD \n /EUR \n etc.\n Full list of available currencies: /list"
    bot.send_message(message.chat.id, answer)

@bot.message_handler(commands=['list'])
def send_list(message):
    answer = '''List of currencies: \n/AUD\n /CAD\n /CNY\n /HRK\n /CZK\n /DKK\n /HKD\n /HUF\n /INR\n /IDR\n /IRR\n /ILS\n /JPY\n /KZT\n /KRW\n /MXN\n /MDL\n /NZD\n /NOK\n /RUB\n /SAR\n /SGD\n /ZAR\n /SEK\n /CHF\n /EGP\n /GBP\n /USD\n /BYN\n /AZN\n /RON\n /TRY\n /XDR\n /BGN\n /EUR\n /PLN\n /DZD\n /BDT\n /AMD\n /IQD\n /KGS\n /LBP\n /LYD\n /MYR\n /MAD\n /PKR\n /VND\n /THB\n /AED\n /TND\n /UZS\n /TWD\n /TMT\n /GHS\n /RSD\n /TJS\n /GEL\n /XAU\n /XAG\n /XPT\n /XPD'''

    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=["text"])
def sendcurrency(message):
    print("========================")
    print(str(message.from_user.id))

    with open("stat.txt", "a") as file:
        file.write(str(message.chat.id)+","+ datetime.datetime.now().strftime("%Y%m%d%H%M%S")+"\n")


    bot.send_message(message.chat.id, get_rate(message.text))

@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact"])
def sendmessage(message):
    bot.send_message(message.chat.id, "This content is not supported. Please, specify a currency name in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc ")
# audio, document, photo, sticker, video, video_note, voice, location, contact


@app.route('/')
def index():
    return 'Hello!'

