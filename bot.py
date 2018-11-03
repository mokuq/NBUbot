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
	tadaydate = datetime.datetime.now().strftime("%Y%m%d")
	URL= 'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode=' + currencyname + '&date=' + tadaydate + '&json'
	content = urllib.request.urlopen(URL)
	try:
		answer = f"NBU rate {currencyname} / HRN =  {json.load(content)[0]['rate']} for today ({tadaydate})"
	except IndexError:
		answer = "Plese, specify currency in a right way: \n /USD or \n /EUR  or \n USD, EUR \n etc"
	return answer	

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    answer = message.chat.first_name + ", good day! Please select a currency: \n /USD \n /EUR \n etc"
    bot.send_message(message.chat.id, answer)


@bot.message_handler(content_types=["text"])
def sendcurrency(message):
    bot.send_message(message.chat.id, get_rate(message.text))

if __name__ == '__main__':
    bot.polling(none_stop=True)
