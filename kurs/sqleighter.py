import sqlite3

class SQLighter:

    def __init__(self, database):
        """Подключаемся к БД и сохраняем курсор соединения"""
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def get_subscriptions(self, status = True):
        """Получаем всех активных подписчиков бота"""
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    def subscriber_exists(self, user_id):
        """Проверяем, есть ли уже юзер в базе"""
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    def add_subscriber(self, user_id, status = True):
        """Добавляем нового подписчика"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)", (user_id,status))

    def update_subscription(self, user_id, status):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def update_wallet(self, user_id, wallet):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `wallet` = ?  WHERE `user_id` = ?", (wallet, user_id))

    def subscriber_wallet(self, user_id):
        """Получаем баланс"""
        with self.connection:
            result = self.cursor.execute('SELECT min(wallet) FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            wallet = result[0][0]
            return wallet

    def subscriber_passed(self, user_id):
        """Получаем список пройденных викторин"""
        with self.connection:
            result = self.cursor.execute('SELECT is_rand, is_erud, is_music, is_eat FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            is_quiz = result[0]
            return is_quiz

    def subscriber_quiz(self, user_id):
        """Получаем список пройденных викторин"""
        with self.connection:
            result = self.cursor.execute('SELECT rand_id, erud_id, music_id, eat_id FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            is_quiz = result[0]
            return is_quiz

    def update_quiz11_subscription(self, user_id, is_rand, ):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `is_rand` = ?  WHERE `user_id` = ?", (is_rand, user_id))

    def update_quiz12_subscription(self, user_id,  rand_id):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `rand_id` = ?  WHERE `user_id` = ?", (rand_id, user_id))

    def update_quiz21_subscription(self, user_id, is_erud, ):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `is_erud` = ?  WHERE `user_id` = ?", (is_erud, user_id))

    def update_quiz22_subscription(self, user_id,  rand_id):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `rand_id` = ?  WHERE `erud_id` = ?", (rand_id, user_id))

    def update_quiz31_subscription(self, user_id, is_rand, ):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `is_music` = ?  WHERE `user_id` = ?", (is_rand, user_id))

    def update_quiz32_subscription(self, user_id,  rand_id):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `rand_id` = ?  WHERE `music_id` = ?", (rand_id, user_id))

    def update_quiz41_subscription(self, user_id, is_rand, ):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `is_eat` = ?  WHERE `user_id` = ?", (is_rand, user_id))

    def update_quiz42_subscription(self, user_id,  rand_id):
        """Обновляем статус подписки пользователя"""
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `eat_id` = ?  WHERE `user_id` = ?", (rand_id, user_id))


    def close(self):
        """Закрываем соединение с БД"""
        self.connection.close()