import abce
from random import randrange

class People(abce.Agent):
    """
    People in the economy,
    have 1 labour each day which they can trade for money,
    have an amount of money
    """
    def init(self, firm_number, money=0, labour=0, produce=0, total_firms=0):
        self.money = money
        self.labour = labour
        self.firm_number = firm_number
        self.total_firms = total_firms


    def add_labour(self):
        self.create("labour", 1)


    def sell_labour(self, labour_cost):
        self.sell(("firm", self.firm_number), good="labour", quantity=1, price=labour_cost)

    def buy_produce(self, cost):
        while self.not_reserved("money") >= cost:
            self.buy(("firm", randrange(self.total_firms)), good="produce", quantity=1, price=cost)

    def destroy_labour(self):
        self.destroy("labour", self.labour)


    def print_possessions(self):
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])

    def getvalue(self):
        return self["money"]

    def getvaluegoods(self):
        return self["produce"]
