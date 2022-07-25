import sqlite3



class ScriptsBot:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def add_in_order(self, id, title, count, img, price):
        self.cursor.execute("INSERT INTO user_order VALUES (?, ?, ?, ?, ?)", (id, title, count, img, price))
        self.connection.commit()

    def get_items(self, id):
        items = self.cursor.execute('SELECT * FROM user_order WHERE id = ?', (id,)).fetchall()
        item_list = [f'{item[1]} x{item[2]}' for item in items]
        return '\n'.join(item_list)

    def get_img(self, title, id):
        img = self.cursor.execute('SELECT img FROM user_order WHERE (title = ? and id = ?)', (title, id)).fetchall()
        return img

    def get_info_item(self, id):
        items = self.cursor.execute('SELECT * FROM user_order WHERE id = ?', (id,)).fetchall()
        return items

    def get_price_items(self, id):
        items = self.cursor.execute('SELECT price FROM user_order WHERE id = ?', (id,)).fetchall()
        prices = [item[0] for item in items]
        return sum(prices)

    def delete_item(self, title, id):
        self.cursor.execute("DELETE FROM user_order WHERE (title = ? and id = ?)", (title, id,))
        self.connection.commit()

    def clean(self, id):
        self.cursor.execute("DELETE FROM user_order WHERE id = ?", (id,))
        self.connection.commit()