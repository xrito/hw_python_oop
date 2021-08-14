import datetime as dt

date_format = '%d.%m.%Y'


class Record:

    def __init__(self, amount, comment, date=None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.date.today()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        # Добавляет новую запись в список.
        self.records.append(record)

    def sum_add_records(self):
        # Суммирует записи в списке records.
        return sum(record.amount for record in self.records)

    def get_today_stats(self):
        now = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == now)

    def get_week_stats(self):
        now = dt.date.today()
        week_back = now - dt.timedelta(days=7)
        return sum(record.amount for record in self.records
                   if now >= record.date >= week_back)

    def remainder(self):
        return self.limit - self.get_today_stats()


class CashCalculator(Calculator):
    USD_RATE = 61.0
    EURO_RATE = 71.0

    def get_today_cash_remained(self, currency):
        remainder = self.remainder()
        cur_l = {
            'eur': [self.EURO_RATE, 'Euro'],
            'usd': [self.USD_RATE, 'USD'],
            'rub': [1, 'руб']
        }
        cur_r = abs(round((remainder / cur_l[currency][0]), 2))
        currency_name = cur_l[currency][1]
        if remainder < 0:
            return (f'Денег нет, держись: '
                    f'твой долг - {cur_r} {currency_name}')
        if remainder > 0:
            return f'На сегодня осталось {cur_r} {currency_name}'
        return 'Денег нет, держись'


class CaloriesCalculator(Calculator):

    def get_calories_remained(self):
        if self.remainder() > 0:
            return ('Сегодня можно съесть что-нибудь ещё, '
                    'но с общей калорийностью не более '
                    f'{self.remainder()} кКал')
        return 'Хватит есть!'
