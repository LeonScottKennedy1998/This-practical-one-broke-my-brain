from customer import Customer
from employee import Employee
from database import Database

def main():
    db = Database('airline.db')

    while True:
        print("Добро пожаловать в нашу Авиакомпанию")
        print("1. Регистрация нового пользователя")
        print("2. Авторизация")
        print("3. Выход")

        choice = input("Выберите действие (1/2/3): ")

        if choice == '1':
            register_user(db)
        elif choice == '2':
            login_user(db)
        elif choice == '3':
            print("Выход из программы.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

def register_user(db):
    print("1. Регистрация сотрудника")
    print("2. Регистрация клиента")

    user_type = input("Выберите тип пользователя (1/2): ")

    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    if user_type == '1':
        db.add_employee(username, password)
        print("Сотрудник зарегистрирован.")
    elif user_type == '2':
        db.add_customer(username, password)
        print("Клиент зарегистрирован.")
    else:
        print("Неверный выбор. Регистрация отменена.")


def login_user(db):
    username = input("Введите имя пользователя: ")
    password = input("Введите пароль: ")

    db.cursor.execute("SELECT * FROM employees WHERE username=? AND password=?", (username, password))
    employee = db.cursor.fetchone()

    db.cursor.execute("SELECT * FROM customers WHERE username=? AND password=?", (username, password))
    customer = db.cursor.fetchone()

    if employee:
        print(f"Добро пожаловать, сотрудник {Employee(username, password, employee).username}!")
        employee_menu(db)
    elif customer:
        print(f"Добро пожаловать, клиент {Customer(username, password, customer).username}!")
        customer_menu(db, Customer(username, password, customer[0]).customer_id)
    else:
        print("Неверное имя пользователя или пароль.")
        return None

def customer_menu(db, customer_id):
    while True:
        print("\nМеню клиента:")
        print("1. Оформить билет")
        print("2. Посмотреть самолеты")
        print("3. Посмотреть билеты")
        print("4. Вернуться в главное меню")

        choice = input("Выберите действие (1/2/3/4): ")

        if choice == '1':
            book_ticket(db, customer_id)
        elif choice == '2':
            view_airplanes(db)
        elif choice == '3':
            view_tickets(db)
        elif choice == '4':
            print("Возвращение в главное меню.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

def employee_menu(db):
    while True:
        print("\nМеню сотрудника:")
        print("1. Действия с билетами")
        print("2. Добавить с данными о самолётах самолете")
        print("3. Вернуться в главное меню")

        choice = input("Выберите действие (1/2/3): ")

        if choice == '1':
            manage_tickets(db)
        elif choice == '2':
            manage_airplanes(db)
        elif choice == '3':
            print("Возвращение в главное меню.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

def book_ticket(db, customer_id):
    print("Оформление билета")

    departure_location = input("Введите место отправления: ")
    arrival_location = input("Введите место прибытия: ")
    departure_time = input("Введите время вылета: ")
    condition_id = input("Введите условие полета (бизнес, эконом, первый класс): ")

    db.add_ticket(customer_id, departure_location, arrival_location, departure_time, condition_id)
    print("Билет оформлен.")

def manage_tickets(db):
    while True:
        print("1. Просмотреть все билеты")
        print("2. Удалить билет")
        print("3. Вернуться в меню сотрудника")

        choice = input("Выберите действие (1/2/3): ")

        if choice == '1':
            view_tickets(db)
        elif choice == '2':
            delete_ticket(db)
        elif choice == '3':
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2 или 3.")

def view_tickets(db):
    tickets = db.get_all_tickets()

    if not tickets:
        print("Нет доступных билетов.")
        return

    print("Список билетов:")
    for ticket in tickets:
        print(f"ID: {ticket[0]}, Клиент: {ticket[1]}, Место отправления: {ticket[2]}, Место прибытия: {ticket[3]}, Время: {ticket[4]}, Условия полёта: {ticket[5]}")

def delete_ticket(db):
    view_tickets(db)

    ticket_id = input("Введите ID билета для удаления (или 0 для возврата в главное меню): ")

    if ticket_id == '0':
        return

    db.cursor.execute("SELECT * FROM tickets WHERE ticket_id=?", (ticket_id,))
    selected_ticket = db.cursor.fetchone()

    if not selected_ticket:
        print("Неверный ID билета.")
        return

    db.delete_ticket(ticket_id)
    print("Билет удален.")

def manage_airplanes(db):
    while True:
        print("\nУправление информацией о самолетах:")
        print("1. Добавить данные о самолете")
        print("2. Удалить данные о самолете")
        print("3. Посмотреть данные о самолетах")
        print("4. Вернуться в меню сотрудника")

        choice = input("Выберите действие (1/2/3/4): ")

        if choice == '1':
            add_airplane(db)
        elif choice == '2':
            delete_airplane(db)
        elif choice == '3':
            view_airplanes(db)
        elif choice == '4':
            print("Возвращение в меню сотрудника.")
            break
        else:
            print("Неверный выбор. Пожалуйста, выберите 1, 2, 3 или 4.")

def view_airplanes(db):
    airplanes = db.get_all_airplanes()

    if not airplanes:
        print("Нет данных о самолетах.")
        return

    print("Данные о самолетах:")
    for airplane in airplanes:
        print(f"ID: {airplane[0]}, Модель: {airplane[1]}, Срок службы: {airplane[2]}")

def add_airplane(db):
    print("Добавление данных о самолете")

    model = input("Введите модель самолета: ")
    service_life = input("Введите срок службы самолета: ")

    db.add_airplane(model, service_life)
    print("Данные о самолете добавлены.")

def delete_airplane(db):
    view_airplanes(db)

    airplane_id = input("Введите ID самолета для удаления (или 0 для возврата в меню): ")

    if airplane_id == '0':
        return

    db.cursor.execute("SELECT * FROM airplanes WHERE airplane_id=?", (airplane_id,))
    selected_airplane = db.cursor.fetchone()

    if not selected_airplane:
        print("Неверный ID самолета.")
        return

    db.delete_airplane(airplane_id)
    print("Данные о самолете удалены.")



if __name__ == "__main__":
    main()
