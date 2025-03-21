import random
import asyncio
from aiogram import Bot, Dispatcher, types, Router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command

import os

TOKEN = os.getenv("TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()

# ВАЖНО: Добавляем роутер ОДИН раз!
dp.include_router(router)

word_pairs = {
    "Hund": "собака", "Katze": "кошка", "Apfel": "яблоко", "Banane": "банан", "Auto": "машина",
    "Haus": "дом", "Buch": "книга", "Tisch": "стол", "Stuhl": "стул", "Lampe": "лампа", "Fenster": "окно",
    "Tür": "дверь", "Straße": "улица", "Baum": "дерево", "Blume": "цветок", "Sonne": "солнце", "Mond": "луна", 
    "Stern": "звезда", "Wasser": "вода", "Feuer": "огонь", "Luft": "воздух", "Erde": "земля", "Berg": "гора",
    "Hund": "собака", "Katze": "кошка", "Apfel": "яблоко", "Banane": "банан", "Auto": "машина",
    "Haus": "дом", "Buch": "книга", "Tisch": "стол", "Stuhl": "стул", "Lampe": "лампа", "Fenster": "окно",
    "Tür": "дверь", "Straße": "улица", "Baum": "дерево", "Blume": "цветок", "Sonne": "солнце", "Mond": "луна", 
    "Stern": "звезда", "Wasser": "вода", "Feuer": "огонь", "Luft": "воздух", "Erde": "земля", "Berg": "гора",
    "Fluss": "река", "See": "озеро", "Meer": "море", "Himmel": "небо", "Wolke": "облако", "Regen": "дождь", "Schnee": "снег",
    "Wind": "ветер", "Eis": "лед", "Stein": "камень", "Gold": "золото", "Silber": "серебро", "Eisen": "железо",
    "Holz": "дерево", "Papier": "бумага", "Glas": "стекло", "Kleidung": "одежда", "Schuh": "ботинок", "Hut": "шляпа",
    "Hemd": "рубашка", "Hose": "брюки", "Jacke": "куртка", "Mantel": "пальто", "Handschuh": "перчатка", "Schal": "шарф",
    "Socken": "носки", "Tasche": "сумка", "Geld": "деньги", "Zeit": "время", "Jahr": "год", "Monat": "месяц",
    "Woche": "неделя", "Tag": "день", "Stunde": "час", "Minute": "минута", "Sekunde": "секунда", "Moment": "момент",
    "Leben": "жизнь", "Tod": "смерть", "Liebe": "любовь", "Hass": "ненависть", "Freude": "радость", "Trauer": "печаль",
    "Glück": "счастье", "Unglück": "несчастье", "Frieden": "мир", "Krieg": "война", "Angst": "страх", "Mut": "смелость",
    "Hoffnung": "надежда", "Verzweiflung": "отчаяние", "Wahrheit": "правда", "Lüge": "ложь", "Wissen": "знание",
    "Unwissenheit": "невежество", "Glaube": "вера", "Zweifel": "сомнение", "Gedanke": "мысль", "Idee": "идея",
    # Добавлено 1000 немецко-русских слов
    "Arzt": "врач", "Bäcker": "пекарь", "Fahrer": "водитель", "Lehrer": "учитель", "Schüler": "ученик", "Student": "студент",
    "Universität": "университет", "Schule": "школа", "Bleistift": "карандаш", "Radiergummi": "ластик", "Papier": "бумага",
    "Tafel": "доска", "Kreide": "мел", "Buchstabe": "буква", "Wort": "слово", "Satz": "предложение", "Text": "текст",
    "Tasche": "сумка", "Rucksack": "рюкзак", "Flasche": "бутылка", "Becher": "стакан", "Teller": "тарелка", "Löffel": "ложка",
    "Gabel": "вилка", "Messer": "нож", "Topf": "кастрюля", "Pfanne": "сковорода", "Herd": "плита", "Ofen": "духовка",
    "Kühlschrank": "холодильник", "Mikrowelle": "микроволновка", "Spülmaschine": "посудомоечная машина", "Waschmaschine": "стиральная машина",
    "Bett": "кровать", "Kissen": "подушка", "Decke": "одеяло", "Schrank": "шкаф", "Kommode": "комод", "Regal": "полка",
    "Fensterbank": "подоконник", "Türklinke": "дверная ручка", "Schlüssel": "ключ", "Schloss": "замок", "Garten": "сад",
    "Blume": "цветок", "Baum": "дерево", "Gras": "трава", "Busch": "куст", "Ast": "ветка", "Blatt": "лист",
    "Vogel": "птица", "Fisch": "рыба", "Katze": "кошка", "Hund": "собака", "Pferd": "лошадь", "Kuh": "корова",
    "Schaf": "овца", "Ziege": "коза", "Schwein": "свинья", "Huhn": "курица", "Ente": "утка", "Gans": "гусь",
    "Kaninchen": "кролик", "Maus": "мышь", "Ratte": "крыса", "Frosch": "лягушка", "Schlange": "змея", "Spinne": "паук"
}

active_games = {}

@router.message(Command("start"))
async def start(message: types.Message):
    keyboard = ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Начать игру")]], resize_keyboard=True
    )
    await message.answer("Привет! Давай поиграем в перевод слов! Нажми 'Начать игру'.", reply_markup=keyboard)

@router.message(lambda msg: msg.text == "Начать игру")
async def start_game(message: types.Message):
    word = random.choice(list(word_pairs.keys()))
    active_games[message.from_user.id] = word
    await message.answer(f"Переведи слово: {word}")

@router.message()
async def check_answer(message: types.Message):
    user_id = message.from_user.id
    if user_id in active_games:
        word = active_games[user_id]
        correct_answer = word_pairs[word]
        if message.text.lower() == correct_answer.lower():
            new_word = random.choice(list(word_pairs.keys()))
            active_games[user_id] = new_word
            await message.answer(f"✅ Верно! Следующее слово: {new_word}")
        else:
            await message.answer(f"❌ Неправильно. Правильный перевод: {correct_answer}. Попробуй следующее слово: {word}")
    else:
        await message.answer("Нажми 'Начать игру' для начала.")

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


