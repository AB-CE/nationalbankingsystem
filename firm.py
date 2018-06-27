import  abce

class Firm(abce.Agent):
    """
    Firm in the economy
    have money which they exchange for labour

    Accepts buy offers from random agents

    """
    def init(self, money=10000, num_people, labour=0, produce=0):
        """creates a firm with 10000 money"""
        self.create("money", money)
        self.num_people = num_people
        self.labour = labour
        self.produce = produce

    def buy_labour(self, labour_cost):
        """accepts sell offers of labour from a person agent"""
        for offer in self.get_offers("labour"):
            if offer.price <= self.not_reserved("money") and offer.price <= labour_cost:
                self.accept(offer)

    def production(self):
        """creates one produce and destroys one labour"""
        self.create("produce", self["labour"])
        self.destroy("labour", self["labour"])


    def sell_produce(self, produce_price):
        """accepts buy offer of produce from all person agents"""
        for offer in self.get_offers("produce"):
            if offer.price >= produce_price and self["produce"] >= 1:
                self.accept(offer)

    def print_possessions2(self):
        """prints possessions and logs money belonging to a firm"""
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])


    def getvalue(self):
        """returns money belonging to firm"""
        return self["money"]

    def getvaluegoods(self):
        """returns number of goods belonging to firm"""
        return self["produce"]

