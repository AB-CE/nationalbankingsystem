import abce
import random

class firm(abce.Agent):
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
    def init(self, money=0, inventory=0, ideal_num_workers=0, workers=0, price=0, wage=0,
             upper_inv=0, lower_inv=0, upper_price=0, lower_price=0, wage_increment=1,
             price_increment=1):
        """
        initializes starting characteristics
        """
        self.money = money
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
        self.create("inventory", productivity*self.workers)

    def determine_wage(self):
        """
        determines if the wage will be altered or not
        if the ideal number of workers wasn't satisfied then raises the wage
        if the number of workers offered exceeded 110% of the ideal number then lower the wage
        """
        excess = 1.1
        if self.ideal_num_workers >= self.workers:
            self.wage += 1
        elif self.ideal_num_workers == self.workers:
            if self.get_messages("max_employees") >= excess*self.ideal_num_workers:
                self.wage -= 1


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
        self.upper_inv = phi_upper*demand
        self.lower_inv = phi_lower*demand
        self.upper_price = const_upper*marginal_cost
        self.lower_price = const_lower*marginal_cost

    def determine_workers(self):
        """
        compares the inventory with the upper and lower bounds
        if above the high bound for inventory then decrease the ideal number of workers
        if below the low bound for inventory then increase the ideal number of workers
        """
        if self.inventory > self.upper_inv:
            self.ideal_num_workers -= 1
        elif self.inventory < self.lower_inv
            self.ideal_num_workers += 1

    def determine_prices(self):
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
            if offer.price >= self.price and self["inventory"] >= offer.quantity:
                self.accept(offer)
            elif offer.price >= self.price and self["inventory"] < offer.quantity:
                self.accept(offer, quantity=self["inventory"])
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
        give(person, "money", quantity=salary)

    def pay_profits(self):
        """
        pays workers/bosses (same agent) the extra profits
        """
        num_days_buffer = 5
        buffer = num_days_buffer*self.wage*self.workers
        profits = self["money"] - buffer
        give(person, "money", quantity=profits)


