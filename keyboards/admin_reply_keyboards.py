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
    "Изменить типы запчастей 🔧",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1,)
)

admin_change_spare_parts_products = get_keyboard(
    "Добавить вид 🔧 ➕",
    "Удалить вид 🔧 ❌",
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

admin_change_contact = get_keyboard(
    "Название 🪧",
    "Город 🏙",
    "Адрес 🏘",
    "Телефон ☎️",
    "Отмена 🔙",
    placeholder="Выберите действие...",
    sizes=(2, 2, 1)

)

admin_finish_action = get_keyboard(
    "Завершить",
    placeholder="Выберите действие...",
    sizes=(1,)
)

admin_change_promo = get_keyboard(
    "Добавить промо-акцию ➕",
    "Удалить промо-акцию ❌",
    "Проверить промо-код 🧑‍💻",
    "Отмена 🔙",
    placeholder="Выберите пункт меню...",
    sizes=(1,)
)
