from django.shortcuts import render
from django.http import HttpResponse
import telebot
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

bot = telebot.TeleBot('2045837540:AAEfPRWhSNkZR2IpbVmMQHC9qOplDpcgnA0')

@csrf_exempt
def telegram(request):
    if request.method == 'POST':
        json_str = request.body.decode('utf-8')
        update = telebot.types.Update.de_json(json_str)
        bot.process_new_updates([update])
        return HttpResponse('')
    else:
        return HttpResponse('This is a Telegram bot!')
