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
        """adds one labour to person agent, usually called at start of day"""
        self.create("labour", 1)


    def sell_labour(self, labour_cost):
        """sell offer to person agent's assigned firm"""
        self.sell(("firm", self.firm_number), good="labour", quantity=1, price=labour_cost)

    def buy_produce(self, cost):
        """makes buy offer produce to a random firm"""
        while self.not_reserved("money") >= cost:
            self.buy(("firm", randrange(self.total_firms)), good="produce", quantity=1, price=cost)

    def destroy_labour(self):
        """destroys all labour person agent owns"""
        self.destroy("labour", self.labour)


    def print_possessions(self):
        """prints possessions and logs money of a person agent"""
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])

    def getvalue(self):
        """returns the value of money owned by a person agent"""
        return self["money"]

    def getvaluegoods(self):
        """returns the amount of produce owned by the person agent"""
        return self["produce"]
