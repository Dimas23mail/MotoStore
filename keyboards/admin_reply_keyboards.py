from keyboards.reply_keyboard import get_keyboard

# Клавиатура клиента для главного меню
start_admin_reply_keyboard = get_keyboard(
    "Посмотреть товары 🏍 🛵 🔧",
    "Акции и скидки 💰",
    "Контакты ☎️ 📱",
    "Админ-панель 🛠",
    placeholder="Выберите пункт меню...",
    sizes=(1, )
)

admin_main_menu = get_keyboard(
    "Изменить наши товары 🏍 🛵 🔧",
    "Изменить промо-акции 🎁",
    "Изменить контакты ☎️ 📱",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1, )
)

admin_change_category_products = get_keyboard(
    "Добавить категорию ➕",
    "Удалить категорию ❌",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1,)
)

admin_change_products_menu = get_keyboard(
    "Изменить товар 📄",
    "Добавить товар ➕",
    "Удалить товар ❌",
    "Изменить категории товаров",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1,)
)

admin_change_promo_menu = get_keyboard(
    "Изменить промо 📄",
    "Добавить промо ➕",
    "Удалить промо ❌",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1,)
)

admin_change_contact_menu = get_keyboard(
    "Изменить контактные данные 📄",
    "Добавить данные ➕",
    "Удалить данные ❌",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1,)
)

admin_change_place_info = get_keyboard(
    "Название 📄",
    "Описание 📖",
    "Город 🌆",
    "Адрес 🏣",
    "Телефон 📞",
    "Фото 📸",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(2,)
)

admin_finish_action = get_keyboard(
    "Завершить",
    placeholder="Выберите действие...",
    sizes=(1,)
)
