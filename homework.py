import datetime as dt


class Record:
    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        if date is None:
            self.date = dt.datetime.now().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):  # добавляет новые записи в БД
        self.records.append(record)

    @staticmethod
    def date_now():  # обновляет дату каждый день
        return dt.datetime.now().date()

    def get_stats(self, date):  # возвращает сумму за указанную дату
        return sum(record.amount for record in self.records
                   if record.date == date)

    def get_today_stats(self):  # возвращает сумму за сегодня
        today = self.date_now()
        return self.get_stats(today)

    def today_remained(self):  # возвращает остаток на сегодня
        return abs(self.limit - self.get_today_stats())

    def get_week_stats(self):  # возвращает сумму за 7 дней
        return sum(n.amount for n in self.records if self.date_now()
                   >= n.date > self.date_now() - dt.timedelta(days=7))


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        comparison = self.get_today_stats() >= self.limit
        if comparison:
            return 'Хватит есть!'
        else:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.today_remained()} кКал')


class CashCalculator(Calculator):
    USD_RATE = 60.0
    EURO_RATE = 70.0
    RUB_RATE = 1
    lists = {'rub': ['руб', RUB_RATE],
             'usd': ['USD', USD_RATE],
             'eur': ['Euro', EURO_RATE]}

    def remains(self, currency):
        return round((self.today_remained() / self.lists[currency][1]), 2)

    def get_today_cash_remained(self, currency):
        comparison = self.limit - self.get_today_stats()
        money = self.lists[currency][0]
        if comparison == 0:
            return ('Денег нет, держись')
        elif comparison > 0:
            return ('На сегодня осталось '
                    f'{self.remains(currency)} {money}')
        else:
            return (f'Денег нет, держись: твой долг '
                    f'- {self.remains(currency)} {money}')
