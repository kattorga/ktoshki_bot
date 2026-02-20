#python bot.py
import telebot
import time
import os

TOKEN = '8224970362:AAFSU2qoO2MDrKHzwce7ArkZkRK9Rlf3DKg'  
bot = telebot.TeleBot(TOKEN)

photos_and_captions = [
    {
        'file': 'photo1.jpg',
        'caption': 'Наша первая совместная фотография. Попросила Валю аккуратно сфоткать нас вместе, а потом бесконечно смотрела на эту фотку и не могла поверить, что это реально. С первого дня общения поняла, что *ТЫ* станешь для меня очень близким человеком!'
    },
    {
        'file': 'photo2.jpg',
        'caption': '*С ТОБОЙ* Шаверно!'
    },
    {
        'file': 'photo3.jpg',
        'caption': 'Ну уж очень люблю эту фотку. *ТЕБЯ* хочется бесконечно обнимать и крепко крепко целовать, не замечая как впечатывается мой нос'
    },
    {
        'file': 'photo4.jpg',
        'caption': '*С ТОБОЙ* хочется бесконечно смеяться, я люблю наш рофлян в 48й и очень люблю нас, когда мы наедине'
    },
    {
        'file': 'photo5.jpg',
        'caption': 'Хочется бесконечно смотреть на *ТВОЮ* улыбку и улыбаться в ответ, такой красивой улыбки я никогда не видела\n\n(Ты тут такой мили я умираю)'
    },
    {
        'file': 'photo6.jpg',
        'caption': '*С ТОБОЙ* я чувствую себя самой самой красивой, ну это и понятно, ведь меня одаривают комплиментами каждый день'
    },
    {
        'file': 'photo7.jpg',
        'caption': '*С ТОБОЙ* хочется тупорыло фоткаться, а потом смеяться над этим. А еще бесконечно представлять как было бы круто жить вместе'
    },
    {
        'file': 'photo8.jpg',
        'caption': '*С ТОБОЙ* можно творить полную хуйню и продолжать ловить на себе твой теплый и любящий взгляд'
    },
    {
        'file': 'photo9.jpg',
        'caption': '*ТЕБЕ* хочется дарить все мое тепло и нежность, потому что ты мне даришь не меньше. Я наполняюсь этой теплотой'
    },
    {
        'file': 'photo10.jpg',
        'caption': 'Это я хз что, мне просто смешно'
    },
    {
        'file': 'photo11.jpg',
        'caption': '*ТЕБЯ* хочется бесконечно смущать и смущаться в ответ.\n\nС тобой хочется все'
    }
]

# Словарь для хранения состояния
user_states = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_states[chat_id] = 0
    
    bot.send_message(
        chat_id,
        "С 23 февраля, любимый! \n\n"
        "Так как я честно не знала как тебя можно порадовать и немного отвлечь в силу обстоятельств, решила приготовить такой прекольчик🤨.\n\n"
        "Эта идея пришла мне пока я сидела на толчке, мне стало забавно и я решила попробовать.\n\n"
        "В этот день все поздравляют своих мужчин с праздником. Для меня ты - самый важный мужчина!\n\n"
    )
    
    send_next_button(chat_id)

def send_next_button(chat_id):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = telebot.types.KeyboardButton('➡️ ДАЛЕЕ')
    markup.add(btn)
    
    bot.send_message(
        chat_id,
        "Готов? Нажимай ДАЛЕЕ, чтобы увидеть следующее фото...",
        reply_markup=markup
    )

@bot.message_handler(func=lambda message: message.text == '➡️ ДАЛЕЕ')
def send_next_photo(message):
    chat_id = message.chat.id
    current_index = user_states.get(chat_id, 0)
    
    if current_index < len(photos_and_captions):
        photo_data = photos_and_captions[current_index]
        
        try:
            with open(photo_data['file'], 'rb') as f:
                # Отправляем с Markdown для курсива
                bot.send_photo(
                    chat_id, 
                    f, 
                    caption=photo_data['caption'],
                    parse_mode='Markdown'
                )
            
            user_states[chat_id] = current_index + 1
            
            if user_states[chat_id] < len(photos_and_captions):
                send_next_button(chat_id)
            else:
                markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
                btn = telebot.types.KeyboardButton('ЕЩЕ РАЗ С НАЧАЛА')
                markup.add(btn)
                
                bot.send_message(
                    chat_id,
                    "Вот такой маленький прикольчик у меня вышел.\n\n"
                    "Надеюсь у меня вышло хоть немного отвлечь тебя от нынешней заебы и поднять настроение.\n\n"
                    "*Я тебя очень очень люблю!*",
                    parse_mode='Markdown',
                    reply_markup=markup
                )
                
        except Exception as e:
            bot.send_message(
                chat_id,
                f"Ой, что-то пошло не так с фото {current_index + 1} 😅"
            )
            user_states[chat_id] = current_index + 1
            send_next_button(chat_id)
    else:
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn = telebot.types.KeyboardButton('ЕЩЕ РАЗ С НАЧАЛА')
        markup.add(btn)
        
        bot.send_message(
            chat_id,
            "Мы уже всё посмотрели! Хочешь повторить?",
            reply_markup=markup
        )

@bot.message_handler(func=lambda message: message.text == 'ЕЩЕ РАЗ С НАЧАЛА')
def restart(message):
    chat_id = message.chat.id
    user_states[chat_id] = 0
    send_next_button(chat_id)

if __name__ == '__main__':
    print("Бот запущен...")
    bot.infinity_polling()