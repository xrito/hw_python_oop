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

    # добавляет новую запись в словарь
    def add_record(self, record):
        self.records.append(record)

    # суммирует записи в списоке records
    def sum_add_records(self):
        return sum(record.amount for record in self.records)

    # потрачено за день(без даты)

    def get_today_stats(self):
        now = dt.date.today()
        return sum(record.amount for record in self.records
                   if record.date == now)

    # потрачено за неделю (с датой)
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

    # остаток от лимита, в рублях или валюте
    def get_today_cash_remained(self, currency):
        cur_l = {"eur": [self.EURO_RATE, 'Euro'], "usd": [
            self.USD_RATE, 'USD'], "rub": [1, 'руб']}
        cur_r = abs(self.remainder() / cur_l[currency][0])
        if self.remainder() < 0:
            return (f'Денег нет, держись: '
                    f'твой долг - {cur_r:.2f} {cur_l[currency][1]}')
        elif self.remainder() == 0:
            return 'Денег нет, держись'
        else:
            return f'На сегодня осталось {cur_r:.2f} {cur_l[currency][1]}'


class CaloriesCalculator(Calculator):

    # съедено за неделю (с датой)
    def get_calories_remained(self):
        if self.remainder() >= 0:
            return (f'Сегодня можно съесть что-нибудь ещё, '
                    f'но с общей калорийностью не более '
                    f'{self.remainder()} кКал')
        else:
            return 'Хватит есть!'
