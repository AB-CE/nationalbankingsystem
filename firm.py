import abce
import random


class Firm(abce.Agent):
    """
    Firm:
    - employs workers each round
    - offers wage based on if they found workers at the previous wage level
        - increases wage when they didn't find enough workers in previous round
        - decreases wage when they did find enough workers in previous x rounds
    - has an inventory of goods with upper and lower bounds on ideal amount
        - hires workers when they have a lower than ideal amount of inventory
        - fires workers when they have higher than ideal amount of inventory
    - prices, based on high and lower bounds
        - if inventory is low and price isn't above upper bound, increase price
        with a probability p
        - if inventory is high and price isn't below lower bound, lower price with
        a probability p
    - pay workers
    - pay left over profits to workers
    """
    def init(self, money=10000, inventory=10, ideal_num_workers=10, workers=0, price=10, wage=10,
             upper_inv=0, lower_inv=0, upper_price=0, lower_price=0, wage_increment=1,
             price_increment=0):
        """
        initializes starting characteristics
        """
        self.create("money", money)
        self.inventory = inventory
        self.ideal_num_workers = ideal_num_workers
        self.workers = workers
        self.price = price
        self.wage = wage
        self.upper_inv = upper_inv
        self.lower_inv = lower_inv
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.wage_increment = wage_increment
        self.price_increment = price_increment

    def production(self):
        """
        produces goods to add to inventory based on number of workers and productivity
        """
        productivity = 1
        before = self["produce"]
        assert productivity*self["workers"] >= 0
        self.create("produce", productivity*self["workers"])
        self.log("production", self["produce"] - before)


    def determine_wage(self):
        """
        determines if the wage will be altered or not
        if the ideal number of workers wasn't satisfied then raises the wage
        if the number of workers offered exceeded 110% of the ideal number then lower the wage
        """
        excess = 1.1
        if self.ideal_num_workers >= self.workers:
            self.wage += 1
            self.get_messages("max_employees")
        elif self.ideal_num_workers == self.workers:
            if self.get_messages("max_employees") >= excess*self.ideal_num_workers:
                self.wage -= 1
            else:
                self.get_messages("max_employees")
        else:
            self.get_messages("max_employees")


    def determine_bounds(self, demand):
        """
        determines the bound on the prices and inventory amounts

        Args:
            demand: number of units of goods demanded by people from firm
        """
        phi_upper = 0.8
        phi_lower = 0.2
        const_upper = 1.5
        const_lower = 1.05
        marginal_cost = self.wage
        self.upper_inv = phi_upper*list(demand)[self.id]
        self.lower_inv = phi_lower*list(demand)[self.id]
        self.lower_price = const_lower*marginal_cost
        self.upper_price = const_upper*marginal_cost


    def determine_workers(self):
        """
        compares the inventory with the upper and lower bounds
        if above the high bound for inventory then decrease the ideal number of workers
        if below the low bound for inventory then increase the ideal number of workers
        """
        if self.inventory > self.upper_inv:
            self.ideal_num_workers -= random.randrange(0, 20)
            if self.ideal_num_workers < 0:
                self.ideal_num_workers = 0
        elif self.inventory < self.lower_inv:
            self.ideal_num_workers += random.randrange(0, 20)

    def determine_price(self):
        """
        compares the inventory with the upper and lower bounds and if the price is within
        the upper and lower price range
        if the price is within the bounded range then:
        if the inventory is below the lower bound then increase price with a probability
        if the inventory is above the upper bound then decrease price with a probability
        """
        probability = 75 # 75% chance that price is changed given satisfied conditions
        if self.inventory < self.lower_inv and self.price < self.upper_price:
            if random.randint(1, 100) < probability:
                self.price += self.price_increment
        elif self.inventory > self.upper_inv and self.price > self.lower_price:
            if random.randint(1, 100) < probability:
                self.price -= self.price_increment

    def sell_goods(self):
        """
        sells the goods to the employees
        """
        for offer in self.get_offers("produce"):
            if offer.price >= self.price and self["produce"] >= offer.quantity:
                self.accept(offer)
            elif offer.price >= self.price and self["produce"] < offer.quantity:
                self.accept(offer, quantity=self["produce"])
            elif offer.price < self.price:
                self.reject(offer)

    def pay_workers(self):
        """
        pays the workers
        if the salary owed is greater than owned money:
        gives out all money and reduces wage by 1 unit
        """
        salary = self.wage*self.workers
        if salary > self["money"]:
            salary = self["money"]
            self.wage -= self.wage_increment
        self.give("people", "money", quantity=salary)

    def pay_profits(self):
        """
        pays workers/bosses (same agent) the extra profits
        """
        num_days_buffer = 5
        buffer = num_days_buffer*self.wage*self.ideal_num_workers
        profits = self["money"] - buffer
        if profits > 0:
            self.give("people", "money", quantity=profits)

    def getvalue_ideal_num_workers(self):
        return (self.name, self.ideal_num_workers)

    def getvalue_wage(self):
        return self.wage

    def publish_vacencies(self):
        return {"name": self.name, "number": self.ideal_num_workers, "wage": self.wage}

    def getvalue_price(self):
        self.send_envelope('people', 'price', self.price)
        return self.price

    def print_possessions(self):
        """
        prints possessions and logs money of a person agent
        """
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])
        self.log("produce", self["produce"])
        self.log("workers", self["workers"])

    def end_work_day(self):
        """


        """
        self.destroy('workers')


