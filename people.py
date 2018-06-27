import abce
from random import randrange

class People(abce.Agent):
    """
    People in the economy,
    have 1 labour each day which they can trade for money,
    have an amount of money
    """
    def init(self, firm_number, list_offers=[], money=0, labour=0, produce=10, total_firms=0, offer_price=0, total_people=0):
        self.produce = produce
        self.money = money
        self.labour = labour
        self.firm_number = firm_number
        self.total_firms = total_firms
        self.total_people = total_people
        self.list_offers = list_offers
        self.offer_price = offer_price

    def add_labour(self):
        """adds one labour to person agent, usually called at start of day"""
        self.create("labour", 1)


    def sell_labour(self, labour_cost):
        """sell offer to person agent's assigned firm"""
        self.sell(("firm", self.firm_number), good="labour", quantity=1, price=labour_cost)

    def buy_produce(self, cost):
        """makes buy offer produce to a random firm"""
        self.offer_price = cost
        quant = int(self.not_reserved("money")/self.offer_price)
        if self.not_reserved("money") >= self.offer_price:
            print("COST: ", cost)
            offer = self.buy(("firm", randrange(self.total_firms)), good="produce", quantity=quant, price=cost)
            self.list_offers.append(offer)

    def check_rejection(self):
        """"""
        print("CHECK1")
        for i in range(self.total_people):
            if self.list_offers[i].status == "rejected":
                message_list = self.get_messages("minprice")

                for msg in message_list:
                    print("MESSAGE: ", msg)
                    print(type(msg))
                    self.buy_produce(msg)

    def destroy_labour(self):
        """destroys all labour person agent owns"""
        self.destroy("labour", self.labour)

    def destroy_produce(self):
        """destroys one owned produce"""
        self.destroy("produce", 1)


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
