import  abce

class Firm(abce.Agent):
    """
    Firm in the economy
    have money which they exchange for labour

    """
    def init(self, money=10000, num_people=20, labour=0, produce=0):
        self.create("money", money)
        self.num_people = num_people
        self.labour = labour
        self.produce = produce

    def buy_labour(self, labour_cost):
        for offer in self.get_offers("labour"):
            if offer.price <= self.not_reserved("money") and offer.price <= labour_cost:
                self.accept(offer)

    def production(self):
        self.create("produce", self["labour"])
        self.destroy("labour", self["labour"])


    def sell_produce(self, produce_price):
        for offer in self.get_offers("produce"):
            if offer.price >= produce_price and self["produce"] >= 1:
                self.accept(offer)

    def print_possessions2(self):
        print('    ' + self.group + str(dict(self.possessions())))


#    def logger(self):
#        self.log("v", 5)

    def getvalue(self):
        return self["money"]

    def getvaluegoods(self):
        return self["produce"]

