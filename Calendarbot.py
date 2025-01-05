from telegram import Update, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from datetime import datetime

# Полное расписание тренировок
schedule = {
    "Пн": "Понедельник:\n- Спортзал\n- Жим лежа\n- Приседания\n- Становая тяга",
    "Вт": "Вторник:\n- Кардио\n- Бег на 5 км\n- Планка 5 минут",
    "Ср": "Среда:\n- Тайский бокс\n- Удары руками и ногами\n- Спарринги",
    "Чт": "Четверг:\n- Спортзал\n- Жим гантелей\n- Тяга в наклоне\n- Приседания с гантелями",
    "Пт": "Пятница:\n- Кардио\n- Интервальный бег\n- Растяжка",
    "Сб": "Суббота:\n- Йога\n- Растяжка\n- Медитация",
    "Вс": "Воскресенье:\n- Отдых\n- Восстановление"
}

# Функция для получения текущего дня недели
def get_today_day() -> str:
    days = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
    today = datetime.now().weekday()  # Текущий день недели (0 = Пн, 6 = Вс)
    return days[today]

# Функция для отображения кнопок в строке ввода
async def show_schedule(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [KeyboardButton("Понедельник"), KeyboardButton("Вторник")],
        [KeyboardButton("Среда"), KeyboardButton("Четверг")],
        [KeyboardButton("Пятница"), KeyboardButton("Суббота")],
        [KeyboardButton("Воскресенье")],
        [KeyboardButton("Сегодня")],  # Кнопка для сегодняшнего дня
        [KeyboardButton("Вся неделя")]  # Кнопка для всей недели
    ]
    
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)  # resize_keyboard для корректного отображения
    await update.message.reply_text("Выберите день недели:", reply_markup=reply_markup)

# Функция для обработки нажатия кнопок
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text

    # Логика для обработки выбранного дня недели
    if text == "Сегодня":
        day_name = get_today_day()  # Получаем текущий день недели
    elif text == "Вся неделя":
        # Отправляем расписание на всю неделю
        week_schedule = "\n\n".join(schedule.values())
        await update.message.reply_text(f"График на всю неделю:\n\n{week_schedule}")
        return
    elif text in ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]:
        # Если текст соответствует дню недели
        day_name = {
            "Понедельник": "Пн",
            "Вторник": "Вт",
            "Среда": "Ср",
            "Четверг": "Чт",
            "Пятница": "Пт",
            "Суббота": "Сб",
            "Воскресенье": "Вс"
        }[text]  # Преобразуем текст кнопки в ключ расписания
    else:
        return  # Если текст не соответствует ни одному из ожидаемых значений, ничего не делаем

    # Отправляем расписание для выбранного дня
    if day_name in schedule:
        await update.message.reply_text(schedule[day_name])

# Главная функция
def main():
    # Создание приложения с токеном
    application = Application.builder().token("8043229668:AAFnzOAVmpjQFeC4Vdp13MPwjIrJ-sb7Ig0").build()

    # Обработчик команды /start для отображения клавиатуры
    application.add_handler(CommandHandler("start", show_schedule))

    # Обработчик текстовых сообщений, чтобы обработать выбор дня
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, button))

    # Запуск бота
    application.run_polling()

if __name__ == "__main__":
    main()


# cd C:\Users\Roman\Documents\Project TG-Bot-Rasp

# python Calendarbot.py