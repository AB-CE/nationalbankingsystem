import abce

class People(abce.Agent):
    """
    People in the economy,
    have 1 labour each day which they can trade for money,
    have an amount of money
    """
    def init(self, firm_number, money=0, labour=0, produce=0):
        self.money = money
        self.labour = labour
        self.firm_number = firm_number


    def add_labour(self):
        self.create("labour", 1)

    def sell_labour(self, price_for_labour=100):
        for offer in self.get_offers("labour"):
            if offer.price >= price_for_labour and self["labour"] >= 1:
                self.accept(offer)

    def buy_produce(self, cost):
        while self.not_reserved("money") >= cost:
            self.buy(("firm", 0), good="produce", quantity=1, price=cost)



    def print_possessions(self):
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])

    def getvalue(self):
        return self["money"]

    def getvaluegoods(self):
        return self["produce"]
