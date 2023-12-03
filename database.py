import sqlite3
class Database:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS employees (
                        employee_id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS customers (
                        customer_id INTEGER PRIMARY KEY,
                        username TEXT NOT NULL,
                        password TEXT NOT NULL
                    )
                ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS tickets (
                        ticket_id INTEGER PRIMARY KEY,
                        customer_id INTEGER,
                        departure_location TEXT NOT NULL,
                        arrival_location TEXT NOT NULL,
                        departure_time TEXT NOT NULL,
                        condition_id TEXT NOT NULL,
                        FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
                    )
                ''')
        self.cursor.execute('''
                    CREATE TABLE IF NOT EXISTS airplanes (
                        airplane_id INTEGER PRIMARY KEY,
                        model TEXT NOT NULL,
                        service_life INTEGER NOT NULL
                    )
                ''')
        self.conn.commit()

    def add_employee(self, username, password):
        self.cursor.execute('INSERT INTO employees (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def add_customer(self, username, password):
        self.cursor.execute('INSERT INTO customers (username, password) VALUES (?, ?)', (username, password))
        self.conn.commit()

    def add_ticket(self, customer_id, departure_location, arrival_location, departure_time, condition_id):
        self.cursor.execute('''
            INSERT INTO tickets (customer_id, departure_location, arrival_location, departure_time, condition_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (customer_id, departure_location, arrival_location, departure_time, condition_id))
        self.conn.commit()

    def delete_ticket(self, ticket_id):
        self.cursor.execute('DELETE FROM tickets WHERE ticket_id = ?', (ticket_id,))
        self.conn.commit()

    def get_all_tickets(self):
        self.cursor.execute('SELECT * FROM tickets')
        return self.cursor.fetchall()

    def add_airplane(self, model, service_life):
        self.cursor.execute('INSERT INTO airplanes (model, service_life) VALUES (?, ?)', (model, service_life))
        self.conn.commit()

    def get_all_airplanes(self):
        self.cursor.execute('SELECT * FROM airplanes')
        return self.cursor.fetchall()

    def delete_airplane(self, airplane_id):
        self.cursor.execute('DELETE FROM airplanes WHERE airplane_id=?', (airplane_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()
