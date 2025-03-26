import aiosqlite
import asyncio


class RolizMotoDB:

    def __init__(self, path=None):
        self.db_name = path
        if path is None:
            print('Ошибка!!! Не указана БД для подключения!')
            return
        else:
            self.lock = asyncio.Lock()

    async def __aenter__(self):
        self.db = await aiosqlite.connect(self.db_name)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.db.close()

    async def make_db(self) -> None:
        async with self.lock:
            create_table_users_db = '''
                CREATE TABLE IF NOT EXISTS users_db (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_name TEXT, 
                phone TEXT, 
                created_at TEXT
                )                 
                '''
            await self.db.execute(create_table_users_db)
            await self.db.commit()

        async with self.lock:
            create_table_products_db = '''
                CREATE TABLE IF NOT EXISTS products_db (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER, 
                title TEXT,
                brand TEXT,
                engine TEXT,
                year_of_release INTEGER
                description TEXT,
                spare_part_attribute INTEGER,
                price REAL, 
                condition TEXT,
                image_url TEXT,
                created_at TEXT,
                FOREIGN KEY (category_id) REFERENCES categories_db (category_id)
                )                 
                '''
            await self.db.execute(create_table_products_db)
            await self.db.commit()

        async with self.lock:
            create_table_categories_db = '''
                CREATE TABLE IF NOT EXISTS categories_db (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                category_name TEXT 
                )                 
                '''
            await self.db.execute(create_table_categories_db)
            await self.db.commit()

        async with self.lock:
            create_table_orders_db = '''
                CREATE TABLE IF NOT EXISTS orders_db (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                user_id INTEGER, 
                product_id INTEGER,
                quantity INTEGER,
                order_date TEXT,
                order_status TEXT, 
                order_promo TEXT,
                FOREIGN KEY (user_id) REFERENCES users_db (user_id),
                FOREIGN KEY (product_id) REFERENCES products_db (product_id)
                )                 
                '''
            await self.db.execute(create_table_orders_db)
            await self.db.commit()

        async with self.lock:
            create_table_price_history_db = '''
                CREATE TABLE IF NOT EXISTS price_history_db (
                price_history_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                product_id INTEGER, 
                price REAL,
                change_date TEXT,
                FOREIGN KEY (product_id) REFERENCES products_db (product_id)
                )                 
                '''
            await self.db.execute(create_table_price_history_db)
            await self.db.commit()

        async with self.lock:
            create_table_promo_db = '''
                CREATE TABLE IF NOT EXISTS promo_db (
                promo_code_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                code TEXT, 
                discount REAL,
                product_id INTEGER,
                valid_from TEXT,
                valid_to TEXT,
                used_by TEXT
                )                 
                '''
            await self.db.execute(create_table_promo_db)
            await self.db.commit()

        async with self.lock:
            create_table_statistic_db = '''
                CREATE TABLE IF NOT EXISTS price_statistic_db (
                statistic_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                product_id INTEGER, 
                view_count INTEGER,
                purchase_count INTEGER,
                date TEXT,
                FOREIGN KEY (product_id) REFERENCES products_db (product_id)
                )                 
                '''
            await self.db.execute(create_table_statistic_db)
            await self.db.commit()

        async with self.lock:
            create_table_promotion_db = '''
                CREATE TABLE IF NOT EXISTS promotion_db (
                promotion_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                title TEXT, 
                description TEXT,
                start_date TEXT,
                end_date TEXT
                )                 
                '''
            await self.db.execute(create_table_promotion_db)
            await self.db.commit()

        async with self.lock:
            create_table_contacts_db = '''
                CREATE TABLE IF NOT EXIST contacts_db (
                contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                city TEXT,
                address TEXT,
                phone TEXT
                )
            '''
            await self.db.execute(create_table_contacts_db)
            await self.db.commit()

    async def save_category(self, category: str = None) -> bool:
        if category is None:
            return False
        async with self.lock:
            save_category = '''
                INSERT INTO categories_db (category_name) VALUES (?)
            '''
            await self.db.execute(save_category, (category, ))
            await self.db.commit()
        return True

    async def get_categories(self) -> list:
        async with self.lock:
            get_categories = '''
                SELECT * FROM categories_db
            '''
            cursor = await self.db.execute(get_categories)
            result_list = await cursor.fetchall()
            await cursor.close()
        return result_list

    async def deleting_category(self, category_id: int):
        delete_category = '''
            DELETE FROM categories_db WHERE category_id = (?)
        '''
        await self.db.execute(delete_category, (category_id, ))
        await self.db.commit()
