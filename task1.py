import threading
from time import sleep
import queue


class Table:

    def __init__(self, number):
        self.number = number
        self.is_busy = False


class Cafe:

    def __init__(self, tables):  # очередь посетителей(создаётся внутри init)
        self.tables = tables
        self.queue = queue.Queue()
        self.customer_ = 0

    def customer_arrival(self):  # моделирует приход посетителя(каждую секунду)

        while self.customer_ <= 19:
            self.customer_ += 1
            print(f'Посетитель номер {self.customer_} прибыл.', flush=True)
            customer_thread = Customer(self.customer_, self)
            customer_thread.start()

            sleep(1)

    def serve_customer(self, customer):  # моделирует обслуживание посетителя

        table_found = False
        for table in self.tables:
            if not table.is_busy:
                table.is_busy = True
                print(f'Посетитель номер {self.customer_} сел за стол {table.number}.')
                sleep(5)
                table.is_busy = False
                print(f'Посетитель номер {self.customer_} покушал и ушёл.')
                table_found = True
                break
        if not table_found:
            print(f'Посетитель номер {self.customer_} ожидает свободный стол.')
            self.queue.put(customer)
            self.queue.get()


class Customer(threading.Thread):  # Запускается, если есть свободные столы
    def __init__(self, number, cafe):
        super().__init__()

        self.number = number
        self.cafe = cafe

    def run(self):
        cafe.serve_customer(self)





# Создаем столики в кафе
table1 = Table(1)
table2 = Table(2)
table3 = Table(3)
tables = [table1, table2, table3]

# Инициализируем кафе
cafe = Cafe(tables)

# Запускаем поток для прибытия посетителей
customer_arrival_thread = threading.Thread(target=cafe.customer_arrival)

customer_arrival_thread.start()

# Ожидаем завершения работы прибытия посетителей
customer_arrival_thread.join()

