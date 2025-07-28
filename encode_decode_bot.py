from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from cryptography.fernet import Fernet
import asyncio
import os

load_dotenv('BOT_TOKEN.env')
TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

def get_key_encodeText(text): # выводит ключ и зашифрованный текст
    key = Fernet.generate_key()
    f = Fernet(key)
    token = f.encrypt(text)

    return key, token

def get_decode_text(key, text): # выводит расшифрованный текст
    f = Fernet(key)
    token = f.decrypt(text.encode('utf-8'))

    return token

@dp.message(lambda message: message.text == '/start') # выводит приветствие
async def start(message: Message):
    await message.answer('Привет, я бот для шифрования и расшифрования текста. Если у тебя есть key и зашифрованный текст, то напиши /decode <key> <text> и я расшифрую текст (если key будет правильным). А чтобы зашифровать текст напиши /encode <text>. С моей помощью вы сможете безопасно хранить свои данные (не сообщайте ключ никому, а то ваши данные могут украсть)')

@dp.message(lambda message: message.text.startswith('/encode')) # шифрует сообщение и выдаёт зашифрованное сообщение и ключ к расшифровке
async def encode(message: Message):
    parts = message.text.split()

    if len(parts) > 1:
        try:
            text = " ".join(parts[1:])

            key, token = get_key_encodeText(text.encode('utf-8'))

            await message.answer(f'Ключ: {key}\n\n Зашифрованный текст: {token}')
        except Exception as e:
            print(f'Ошибка {e}')
    else:
        await message.answer('Недостаточно данных для шифрования текста')

@dp.message(lambda message: message.text.startswith('/decode')) # расшифровывает текст по ключу и зашифрованному тексту
async def decode(message: Message):
    parts = message.text.split(" ", 2)

    if len(parts) > 2:
        try:
            key = parts[1]
            text = parts[2]

            token = get_decode_text(key, text)
            await message.answer(f'Расшифрованный текст: {token.decode('utf-8')}')
        except Exception as e:
            print(f'Ошибка {str(e)}')
    else:
        await message.answer('Недостаточно данных для расшифрования текста')

async def main(): # главный цикл программы
    while True:
        try:
            print('Запуск бота')
            await dp.start_polling(bot)
        except Exception as e:
            print(f'Ошибка {e}')
            print('Перезапуск бота')
            await asyncio.sleep(3)

if __name__ == '__main__':
    asyncio.run(main())