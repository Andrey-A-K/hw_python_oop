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
        total = 0
        for record in self.records:
            if record.date == date:
                total += record.amount
        return total

    def get_today_stats(self):  # возвращает сумму за сегодня
        today = self.date_now()
        return self.get_stats(today)

    def today_remained(self):  # возвращает остаток на сегодня
        return abs(self.limit - self.get_today_stats())

    def get_week_stats(self):  # возвращает сумму за 7 дней
        today = self.date_now()
        total = 0
        for i in range(7):
            date = today - dt.timedelta(days=i)
            total += self.get_stats(date)
        return total


class CaloriesCalculator(Calculator):
    def get_calories_remained(self):
        if self.get_today_stats() >= self.limit:
            return 'Хватит есть!'
        else:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{self.today_remained()} кКал')


class CashCalculator(Calculator):
    USD_RATE = 74.0
    EURO_RATE = 90.0
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        if currency == 'rub':
            return self.get_for_currency('руб', self.RUB_RATE)
        elif currency == 'usd':
            return self.get_for_currency('USD', self.USD_RATE)
        elif currency == 'eur':
            return self.get_for_currency('Euro', self.EURO_RATE)

    def get_for_currency(self, currency, rate):
        if self.get_today_stats() == self.limit:
            return('Денег нет, держись')
        elif self.get_today_stats() < self.limit:
            return(f'На сегодня осталось '
                   f'{round((self.today_remained() / rate ), 2)} {currency}')
        else:
            return(f'Денег нет, держись: твой долг - '
                   f'{round((self.today_remained() / rate ), 2)} {currency}')
