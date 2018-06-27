import  abce

class Firm(abce.Agent):
    """
    Firm in the economy
    have money which they exchange for labour

    Accepts buy offers from random agents

    """
    def init(self, money=10000, num_people=10, labour=0, produce=0, new_price=60):
        """creates a firm with 10000 money"""
        self.create("money", money)
        self.num_people = num_people
        self.labour = labour
        self.produce = produce
        self.new_price = new_price

    def buy_labour(self, labour_cost):
        """accepts sell offers of labour from a person agent"""
        for offer in self.get_offers("labour"):
            if offer.price <= self.not_reserved("money") and offer.price <= labour_cost:
                self.accept(offer)

    def production(self):
        """creates one produce and destroys one labour"""
        self.create("produce", 2*self["labour"])
        self.destroy("labour", self["labour"])


    def sell_produce(self):
        """accepts buy offer of produce from all person agents"""
        print(self["money"])
        ratio = 10000/self["money"]
        holder = ratio*self.new_price
        if holder < 50:
            holder = 50
        elif holder > 300:
            holder = 300
        self.new_price = int(holder)
        for offer in self.get_offers("produce"):
            if offer.price >= self.new_price and self["produce"] >= offer.quantity:
                self.accept(offer)
            elif offer.price < self.new_price and self["produce"] >= offer.quantity:
                self.reject(offer)
                self.send(offer.sender, topic="minprice", msg=self.new_price)
            elif offer.price >= self.new_price and self["produce"] < offer.quantity:
                self.reject(offer)
                self.send(offer.sender, topic="maxquantity", msg=self["produce"])
            else:
                self.reject()


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

