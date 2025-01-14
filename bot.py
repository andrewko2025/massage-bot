
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import Conflict, TelegramError

import sys
import logging
from telegram.error import Conflict, TelegramError

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# В функции main() измените код на:
def main():
    try:
        application = Application.builder().token(TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # Добавляем обработчик ошибок
        application.add_error_handler(error_handler)
        
        print("Бот запущен...")
        application.run_polling(drop_pending_updates=True)
    except Conflict:
        print("Ошибка: Бот уже запущен в другом месте")
        sys.exit(1)
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        sys.exit(1)

# Добавьте функцию обработки ошибок:
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Exception while handling an update: {context.error}")

from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Замените '7619639027:AAFaw97l38wBEwejyg04N_VURbgSOectv6Q' на токен вашего бота, полученный от @BotFather
TOKEN = '7619639027:AAFaw97l38wBEwejyg04N_VURbgSOectv6Q'

# Основное меню
MAIN_MENU = [
    ['📅 Записаться на массаж', '💰 Цены'],
    ['ℹ️ Обо мне', '📞 Контакты'],
    ['❓ Частые вопросы']
]

# Ответы на частые вопросы
FAQ = {
    "Какие виды массажа вы предлагаете?": "Мы предлагаем следующие виды массажа:\n- Классический\n- Спортивный\n- Лечебный\n- Релаксационный\n- Антицеллюлитный",
    "Сколько длится сеанс?": "Стандартная продолжительность сеанса - 60 минут",
    "Как подготовиться к массажу?": "Рекомендации перед массажем:\n1. Примите душ\n2. Приходите за 10 минут до начала сеанса\n3. Сообщите массажисту о противопоказаниях\n4. Не принимайте пищу за час до массажа",
    "Есть ли противопоказания?": "Основные противопоказания:\n- Острые воспалительные процессы\n- Повышенная температура\n- Онкологические заболевания\n- Период обострения хронических заболеваний\nДля точной консультации обратитесь к врачу."
}

# Цены на услуги
PRICES = """
🏷️ цены:

Приём 1500 THB 
С выездом к вам 2500 THB 
"""

# Информация 
ABOUT_US = """
Здравствуйте! Мое имя Косых Андрей!

Практика более 10 лет
— лечебный классический
— реабилитация после операций, травм и переломов опорно-двигательного аппарата
— расслабляющий общий массаж
— баночный 

Медицинское образование со спец курсом по программе «Медицинский массаж» (КБМК им.Крутовского).
Опыт в реабилитации взрослых и детей после переломов и операций опорно-двигательного аппарата более 2х лет в Российско-Финском медицинском центре Terve.

Более 15000 часов массажа и 4500 благодарных пациентов.
"""

# Контактная информация
CONTACTS = """
📞 Наши контакты:

Телефон: +7 (983) 366-00-11
Адрес: ул. Примерная, д. 123
График работы: 
Пн 8:00 до 12:00
Вт 8:00 до 12:00
Ср 8:00 до 12:00
Чт 8:00 до 12:00
Пт 8:00 до 12:00
Сб 8:00 до 12:00

🌍 Соц сети:
Instagram: http://instagram.com/medic_mass
VK: vk.com/medic_mass
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    keyboard = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
    await update.message.reply_text(
        "👋 Добро пожаловать!\n"
        "Выберите интересующий вас раздел:",
        reply_markup=keyboard
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик текстовых сообщений"""
    text = update.message.text

    if text == "📅 Записаться на массаж":
        await update.message.reply_text(
                        "t.me/andrew_ko"
        )
    elif text == "💰 Цены":
        await update.message.reply_text(PRICES)
    elif text == "ℹ️ Обо мне":
        await update.message.reply_text(ABOUT_US)
    elif text == "📞 Контакты":
        await update.message.reply_text(CONTACTS)
    elif text == "❓ Частые вопросы":
        faq_keyboard = [[KeyboardButton(question)] for question in FAQ.keys()]
        faq_keyboard.append(["🔙 Вернуться в главное меню"])
        markup = ReplyKeyboardMarkup(faq_keyboard, resize_keyboard=True)
        await update.message.reply_text("Выберите вопрос:", reply_markup=markup)
    elif text == "🔙 Вернуться в главное меню":
        keyboard = ReplyKeyboardMarkup(MAIN_MENU, resize_keyboard=True)
        await update.message.reply_text("Выберите раздел:", reply_markup=keyboard)
    elif text in FAQ:
        await update.message.reply_text(FAQ[text])
    else:
        await update.message.reply_text(
            "Извините, я вас не понял. Пожалуйста, воспользуйтесь меню или напишите мне напрямую: "
            "t.me/andrew_ko"
        )

def main():
    """Запуск бота"""
    application = Application.builder().token(TOKEN).build()

    # Регистрация обработчиков
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запуск бота
    application.run_polling()

if __name__ == '__main__':
    main()
