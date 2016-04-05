__author__ = 'Marco Maio'

import time

class Handler():
    def __init__(self, stocks_today=None, investments_by_name=None, investments_by_availability=None):
        # input data assessment
        if stocks_today is None:
            raise ValueError('Stocks_today container not specified!')
        elif investments_by_name is None:
            raise ValueError('Investments_by_name container not specified!')
        elif investments_by_availability is None:
            raise ValueError('Investments_by_availability container not specified!')

        self.__stocks_today = stocks_today
        self.__investments_by_name = investments_by_name
        self.__investments_by_availability = investments_by_availability


    def get_amount_by_stock_name(self, stock_name):
        if stock_name is None or len(stock_name) == 0:
            raise ValueError('Stock name not specified!')

        return self.__stocks_today[stock_name]["EUR"] *\
               self.__stocks_today[stock_name]["Numbers of parts"]


    def get_amount_total_investment(self):
        tot = 0
        for i in self.__stocks_today:
            tot += self.get_amount_by_stock_name(i)
        return tot


    def get_total_amount_by_date(self, date=None, stock_name="", closest_availability_only=False):
        if date is None or len(date) == 0:
            raise ValueError('Date not specified!')

        dates = [d for d in self.__investments_by_availability.keys() if  len(d) > 0]
        eligible_dates =[]
        for d in dates:
            if time.strptime(date, "%d/%m/%Y") >= time.strptime(d, "%d/%m/%Y"):
                if not closest_availability_only or date.split('/')[2] == d.split('/')[2]:
                    eligible_dates.append(d)
        if len(eligible_dates)== 0:
             raise ValueError('No fund available by the ' + date)

        tot = 0
        stocks = set()
        for ed in eligible_dates:
            for k, v in self.__investments_by_availability[ed].items():
                if stock_name in k:
                    stocks.add(k)
                    tot += self.__stocks_today[k]["EUR"] * v

        return tot, stocks


    def get_paid_by_stock_name(self, stock_name=None):
        if stock_name is None or len(stock_name) == 0:
            raise ValueError('Stock name not specified!')
        if stock_name not in self.__stocks_today:
            raise ValueError('Please provide a valid stock name!')
        tot = 0.0
        for k, v in self.__investments_by_name[stock_name].items():
            tot += v['Number of actions bought'] * v['Purchase value']

        return tot


    def get_total_gain(self):
        tot_paid = 0.0
        for stock_name in self.__investments_by_name:
            tot_paid += self.get_paid_by_stock_name(stock_name)
        tot = self.get_amount_total_investment()
        gain = tot - tot_paid
        percentage_gain = (tot/tot_paid - 1)*100

        return gain, percentage_gain


    def get_gain_by_stock_name(self, stock_name):
        if stock_name is None or len(stock_name) == 0:
            raise ValueError('Stock name not specified!')
        if stock_name not in self.__stocks_today:
            raise ValueError('Please provide a valid stock name!')
        tot_paid = self.get_paid_by_stock_name(stock_name)
        tot = self.get_amount_by_stock_name(stock_name)
        gain = tot - tot_paid
        percentage_gain = (tot/tot_paid - 1)*100

        return gain, percentage_gain

    def get_next_available_amount(self):
        dates = [d for d in self.__investments_by_availability.keys() if len(d) > 0]
        min_date = None
        min_date_str = ""
        for d in dates:
            current_date = time.strptime(d, "%d/%m/%Y")
            if min_date is None or min_date > current_date:
                min_date = current_date
                min_date_str = d

        return min_date_str, self.get_total_amount_by_date(min_date_str)
