#!/usr/bin/python3.6

import telebot # pip install pyTelegramBotAPI
import urllib
import json
import datetime
from bottoken import TOKEN

bot = telebot.TeleBot(TOKEN)

def get_rate(currency):
	currencyname = currency.replace("/", "").upper()
	# https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=EUR&date=20181030&json
	todaydate = datetime.datetime.now().strftime("%Y%m%d")
	URL= 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currencyname + '&date=' + todaydate + '&json'
	content = urllib.request.urlopen(URL)
	try:
		answer = f"NBU rate {currencyname} / HRN =  {json.load(content)[0]['rate']} for today ({todaydate})"
	except IndexError:
		answer = "Plese, specify currency in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc"
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

if __name__ == '__main__':
    bot.infinity_polling(True)
