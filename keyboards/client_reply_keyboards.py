from keyboards.reply_keyboard import get_keyboard

# Клавиатура клиента для главного меню
start_client_reply_keyboard = get_keyboard(
    "Посмотреть товары 🏍",
    "Акции и скидки 💰",
    "Контакты ☎️ 📱",
    placeholder="Выберите пункт меню...",
    sizes=(1, )
)
