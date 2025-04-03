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
                created_at TEXT,
                date_of_last_visit TEXT,
                user_tg_id INTEGER,
                user_name TEXT, 
                phone TEXT,
                email TEXT, 
                promo_id INTEGER
                )                 
                '''
            await self.db.execute(create_table_users_db)
            await self.db.commit()

        async with self.lock:
            create_table_spare_types_db = '''
                CREATE TABLE IF NOT EXISTS spare_types_db (
                spare_types_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                spare_types_name TEXT 
                )                 
                '''
            await self.db.execute(create_table_spare_types_db)
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
            create_table_sub_categories_db = '''
                CREATE TABLE IF NOT EXISTS sub_categories_db (
                sub_category_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                sub_category_name TEXT,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories_db (category_id) 
                )                 
                '''
            await self.db.execute(create_table_sub_categories_db)
            await self.db.commit()

        async with self.lock:
            create_table_products_db = '''
                CREATE TABLE IF NOT EXISTS products_db (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_id INTEGER,
                sub_category_id INTEGER, 
                title TEXT,
                brand TEXT,
                engine TEXT,
                spare_types_id INTEGER,
                description TEXT,
                spare_part_attribute INTEGER,
                price REAL, 
                image_url TEXT,
                created_at TEXT,
                FOREIGN KEY (category_id) REFERENCES categories_db (category_id),
                FOREIGN KEY (sub_category_id) REFERENCES sub_categories_db (sub_category_id),
                FOREIGN KEY (spare_types_id) REFERENCES spare_types_db (spare_types_id)
                )                 
                '''
            await self.db.execute(create_table_products_db)
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
                title_id INTEGER,
                code TEXT, 
                discount REAL,
                product_id INTEGER,
                valid_from TEXT,
                valid_to TEXT,
                used_by TEXT,
                FOREIGN KEY (title_id) REFERENCES promo_title_db (title_id)
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
                promo_code_id INTEGER,
                title_id INTEGER, 
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                FOREIGN KEY (promo_code_id) REFERENCES promo_db (promo_code_id),
                FOREIGN KEY (title_id) REFERENCES promo_title_db (title_id)
                )                 
                '''
            await self.db.execute(create_table_promotion_db)
            await self.db.commit()

        async with self.lock:
            create_table_promo_title_db = '''
                CREATE TABLE IF NOT EXISTS promo_title_db (
                title_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title_name TEXT
                )
            '''
            await self.db.execute(create_table_promo_title_db)
            await self.db.commit()

        async with self.lock:
            create_table_contacts_db = '''
                CREATE TABLE IF NOT EXISTS contacts_db (
                contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                city TEXT,
                address TEXT,
                phone TEXT
                )
            '''
            await self.db.execute(create_table_contacts_db)
            await self.db.commit()

    async def save_new_user(self, created_at: str = None, user_tg_id: int = None) -> bool:
        if created_at is None or user_tg_id is None:
            return False
        async with self.lock:
            save_user = '''
                INSERT INTO users_db (created_at, date_of_last_visit, user_tg_id) VALUES (?, ?, ?)
            '''
            await self.db.execute(save_user, (created_at, created_at, user_tg_id, ))
            await self.db.commit()
        return True

    async def change_user_visit_field(self, user_id: int = None, date_of_last_visit: str = None) -> bool:
        if user_id is None or date_of_last_visit is None:
            return False
        async with self.lock:
            change_visit_field = '''
                UPDATE users_db SET date_of_last_visit = (?) WHERE user_id = (?)
            '''
            await self.db.execute(change_visit_field, (date_of_last_visit, user_id))
            await self.db.commit()
        return True

    async def test_user(self, user_tg_id: int = None) -> bool | int:
        if user_tg_id is None:
            return False
        else:
            async with self.lock:
                get_one_user = '''
                    SELECT user_id FROM users_db WHERE user_tg_id = (?)        
                '''
                cursor = await self.db.execute(get_one_user, (user_tg_id,))
                result = await cursor.fetchone()
                await cursor.close()
        return result[0] if result else False

    async def delete_contact(self, contact_id: int = None) -> bool:
        if contact_id is None:
            return False
        else:
            async with self.lock:
                delete_contact = '''
                    DELETE FROM contacts_db WHERE contact_id = (?)
                '''
                await self.db.execute(delete_contact, (contact_id,))
                await self.db.commit()
        return True

    async def get_one_contact(self, contact_id: int = None) -> tuple | None:
        if contact_id is None:
            return None
        else:
            get_one_contact = '''
                SELECT * FROM contacts_db WHERE contact_id = (?)
            '''
            cursor = await self.db.execute(get_one_contact, (contact_id, ))
            result_tuple = await cursor.fetchone()
            await cursor.close()
        return result_tuple

    async def get_all_contacts(self) -> list:
        async with self.lock:
            get_all_contacts = '''
                SELECT * FROM contacts_db
            '''
            cursor = await self.db.execute(get_all_contacts)
            result_list = await cursor.fetchall()
            await cursor.close()
        return result_list.copy()

    async def update_contact(self, contact_id: int = None, contact_title: str = None, contact_city: str = None,
                             contact_address: str = None, contact_phone: str = None) -> bool:
        if contact_id is None:
            return False
        print(f"contact_title = {contact_title}\ncontact_city = {contact_city}")
        async with self.lock:
            if contact_title:
                update_contact = '''
                    UPDATE contacts_db SET title = (?) WHERE contact_id = (?)
                '''
                await self.db.execute(update_contact, (contact_title, contact_id))
                await self.db.commit()
            elif contact_city:
                update_contact = '''
                    UPDATE contacts_db SET city = (?) WHERE contact_id = (?)
                '''
                await self.db.execute(update_contact, (contact_city, contact_id))
                await self.db.commit()
            elif contact_address:
                update_contact = '''
                    UPDATE contacts_db SET address = (?) WHERE contact_id = (?)
                '''
                await self.db.execute(update_contact, (contact_address, contact_id))
                await self.db.commit()
            elif contact_phone:
                update_contact = '''
                    UPDATE contacts_db SET phone = (?) WHERE contact_id = (?)
                '''
                await self.db.execute(update_contact, (contact_phone, contact_id))
                await self.db.commit()
            return True

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

    async def save_contacts(self, source_tuple: tuple = None) -> bool:
        if source_tuple is None:
            return False
        async with self.lock:
            save_contact = '''
                INSERT INTO contacts_db (title, city, address, phone) VALUES (?, ?, ?, ?)
            '''
            await self.db.execute(save_contact, source_tuple)
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
        return result_list.copy()

    async def get_sub_categories(self, category_id: int = 0) -> list:
        async with self.lock:
            get_sub_categories = '''
                SELECT sub_categories_db.sub_category_id, sub_categories_db.sub_category_name 
                FROM sub_categories_db
                JOIN categories_db
                ON sub_categories_db.category_id = (?)
            '''
            cursor = await self.db.execute(get_sub_categories, (category_id, ))
            result_list = await cursor.fetchall()
            await cursor.close()
        print(f"result_list = {result_list}")
        return result_list.copy()

    async def deleting_category(self, category_id: int):
        delete_category = '''
            DELETE FROM categories_db WHERE category_id = (?)
        '''
        await self.db.execute(delete_category, (category_id, ))
        await self.db.commit()

    async def get_spare_types(self) -> list:
        get_spare_types = '''
            SELECT * FROM spare_types_db
        '''
        cursor = await self.db.execute(get_spare_types)
        result_list = await cursor.fetchall()
        await cursor.close()

        return result_list.copy()

    async def deleting_spare_types(self, category_id: int):
        delete_spare_types = '''
            DELETE FROM spare_types_db WHERE category_id = (?)
        '''
        await self.db.execute(delete_spare_types, (category_id, ))
        await self.db.commit()

    async def save_spare_types(self, spare_types: str = None) -> bool:
        if spare_types is None:
            return False
        async with self.lock:
            save_spare_types = '''
                INSERT INTO spare_types_db (spare_types_name) VALUES (?)
            '''
            await self.db.execute(save_spare_types, (spare_types, ))
            await self.db.commit()
        return True

    async def get_all_promo_by_date(self, now_date: str = "") -> list | None:
        async with self.lock:
            get_all_promo = '''
                SELECT title, description, start_date, end_date FROM promotion_db 
                WHERE (start_date < ? and end_date > ?)
            '''
            cursor = await self.db.execute(get_all_promo, (now_date, now_date, ))
            result_list = await cursor.fetchall()
            await cursor.close()
        return result_list.copy()

    async def get_all_promo(self) -> list:
        async with self.lock:
            get_all_promo = '''
                SELECT * FROM promo_title_db
            '''
            cursor = await self.db.execute(get_all_promo)
            result_list = await cursor.fetchall()
            await cursor.close()
        return result_list.copy()

    async def save_new_promo_title(self, title_name: str = None):
        if title_name is None:
            return False
        async with self.lock:
            save_new_promo_title = '''
                INSERT INTO promo_title_db (title_name) VALUES (?)
            '''
            await self.db.execute(save_new_promo_title, (title_name,))
            await self.db.commit()

            get_saved_promo_id = '''
                SELECT title_id FROM promo_title_db WHERE title_name = (?)
            '''
            cursor = await self.db.execute(get_saved_promo_id, (title_name, ))
            result_list = await cursor.fetchone()
            await cursor.close()
        return result_list
