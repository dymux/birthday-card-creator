import sqlite3

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

class TicketsDB:
    def __init__(self):
        self.connection = sqlite3.connect("cards_db.db")
        self.connection.row_factory = dict_factory
        self.cursor = self.connection.cursor()
        self.setDatabase()

    def insertTicket(self, token, entrant_name, entrant_age, guest_name):
        data = [token, entrant_name, entrant_age, guest_name]
        self.cursor.execute("INSERT INTO tickets (random_token, entrant_name, entrant_age, guest_name) VALUES (?, ?, ?, ?)", data)
        self.connection.commit()

    def getTickets(self):
        self.cursor.execute("SELECT * FROM tickets")
        result = self.cursor.fetchall()
        print(result)
        return result

    def setDatabase(self):
        #self.cursor.execute("DROP TABLE tickets")
        self.cursor.execute("CREATE TABLE IF NOT EXISTS tickets (id INTEGER PRIMARY KEY, random_token INTEGER, entrant_name STRING, entrant_age INTEGER, guest_name STRING)")
        self.connection.commit()
