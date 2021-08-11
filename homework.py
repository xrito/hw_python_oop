import datetime as dt


date_format = '%d.%m.%Y'
now = dt.datetime.now()


class Record:

    def __init__(self, amount, comment, date = None):
        self.amount = amount
        self.comment = comment
        self.date = date
        if date is not None:
            self.date = dt.datetime.strptime(date, date_format).date()
        else:
            self.date = dt.datetime.now().date()


class Calculator:
    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record): #добавляет новую запись о расходах в список records
        self.records.append(record)
        
    def sum_add_records(self):  # суммирует записи в списоке records
        return sum(record.amount for record in self.records) 

    def get_today_stats(self): # потрачено за день(без даты)
        day_amount = 0
        now = dt.datetime.now().date()
        for day in self.records:
            if day.date == now:
                day_amount += day.amount
        return day_amount

    def get_week_stats(self): # потрачено за неделю (с датой)
        now = dt.datetime.now().date()       
        week_amount = 0
        week_back = now - dt.timedelta(days=7)
        for week in self.records:
            if week.date >= week_back and week.date <= now:
               week_amount += week.amount
        return week_amount  


class CashCalculator(Calculator):
    USD_RATE = 61.0
    EURO_RATE = 71.0
    def get_today_cash_remained(self, currency): # остаток от лимита, в рублях или валюте
        sum_today = self.get_today_stats()
        if currency == 'rub':    
            if self.limit - sum_today > 0:
                return f'На сегодня осталось {abs(self.limit - sum_today)} руб'
            elif self.limit - sum_today == 0:
                return f'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг - {abs(self.limit - sum_today)} руб'
        elif currency == 'usd':
            if self.limit - sum_today > 0:
                return f'На сегодня осталось {round((abs(self.limit - sum_today) / self.USD_RATE), 2)} USD'
            elif self.limit - sum_today == 0:
                return f'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг - {round((abs(self.limit - abs(self.get_today_stats())) / self.USD_RATE), 2)} USD'
        elif currency == 'eur':
            if self.limit - sum_today > 0:
                return f'На сегодня осталось {round((abs(self.limit - sum_today) / self.EURO_RATE), 2)} Euro'
            elif self.limit - sum_today == 0:
                return f'Денег нет, держись'
            else:
                return f'Денег нет, держись: твой долг - {round((abs(self.limit - sum_today) / self.EURO_RATE), 2)} Euro'
        else: print('Неизвестная валюта')

class CaloriesCalculator(Calculator):

    def get_calories_remained(self): # съедено за неделю (с датой)
        sum_amount = self.get_today_stats()
        result = (self.limit - sum_amount)
        if self.limit - sum_amount >= 0:
            return f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {result} кКал'
        else:
            return f'Хватит есть!'