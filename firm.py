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
    def init(self, firm_money=10000, ideal_num_workers=10, price=20, wage=10, upper_inv=0,
             lower_inv=0, upper_price=0, lower_price=0, wage_increment=10, price_increment=10,
             probability=75, phi_upper=10, phi_lower=2, const_upper=1.5, const_lower=1.05,
             excess=1.1, num_days_buffer=10, **_):
        """
        initializes starting characteristics
        """
        self.create("money", firm_money)
        self.ideal_num_workers = ideal_num_workers
        self.price = price
        self.wage = wage
        self.upper_inv = upper_inv
        self.lower_inv = lower_inv
        self.upper_price = upper_price
        self.lower_price = lower_price
        self.wage_increment = wage_increment
        self.price_increment = price_increment
        self.probability = probability
        self.phi_upper = phi_upper
        self.phi_lower = phi_lower
        self.const_upper = const_upper
        self.const_lower = const_lower
        self.excess = excess
        self.num_days_buffer = num_days_buffer

    def production(self):
        """
        produces goods to add to inventory based on number of workers and productivity
        """
        productivity = 1
        before = self["produce"]
        assert productivity * self["workers"] >= 0
        self.create("produce", productivity*self["workers"])
        self.log("production", self["produce"] - before)

    def determine_wage(self):
        """
        determines if the wage will be altered or not
        if the ideal number of workers wasn't satisfied then raises the wage
        if the number of workers offered exceeded 110% of the ideal number then lower the wage
        """
        max_wage_change = self.wage_increment
        if self.ideal_num_workers > self['workers']:
            self.wage += random.uniform(0, max_wage_change)
            self.get_messages("max_employees")
        elif self.ideal_num_workers == self['workers']:
            max_employees = self.get_messages("max_employees")[0]
            if max_employees > self.excess * self.ideal_num_workers:
                self.wage -= random.uniform(0, max_wage_change)
                if self.wage < 0:
                    self.wage = 0
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


        marginal_cost = self.wage
        self.upper_inv = self.phi_upper*list(demand)[self.id]
        self.lower_inv = self.phi_lower*list(demand)[self.id]
        self.lower_price = self.const_lower*marginal_cost
        self.upper_price = self.const_upper*marginal_cost
        self.log('upper_inv', self.upper_inv)
        self.log('lower_inv', self.lower_inv)
        self.log('demand', list(demand)[self.id])


    def determine_workers(self):
        """
        compares the inventory with the upper and lower bounds
        if above the high bound for inventory then decrease the ideal number of workers
        if below the low bound for inventory then increase the ideal number of workers
        """
        if self['produce'] > self.upper_inv:
            self.ideal_num_workers -= 0.1 * self.ideal_num_workers
            if self.ideal_num_workers < 0:
                self.ideal_num_workers = 0
        elif self['produce'] < self.lower_inv:
            self.ideal_num_workers += 0.1 * self.ideal_num_workers

    def determine_price(self):
        """
        compares the inventory with the upper and lower bounds and if the price is within
        the upper and lower price range
        if the price is within the bounded range then:
        if the inventory is below the lower bound then increase price with a probability
        if the inventory is above the upper bound then decrease price with a probability
        """
        probability = 100 # 75% chance that price is changed given satisfied conditions
        if self['produce'] < self.lower_inv and self.price < self.upper_price:
            if random.randint(1, 100) <= probability:
                self.price += random.uniform(0, self.price_increment)
        elif self['produce'] > self.upper_inv and self.price > self.lower_price:
            if random.randint(1, 100) <= probability:
                self.price -= random.uniform(0, self.price_increment)
                self.price = max(self.lower_price, self.price)
        self.log('price', self.price)

    def sell_goods(self):
        """
        sells the goods to the employees
        """
        for offer in self.get_offers("produce"):
            if offer.price >= self.price and self["produce"] >= offer.quantity:
                self.accept(offer)
                self.log('sales', offer.quantity)
            elif offer.price >= self.price and self["produce"] < offer.quantity:
                self.log('sales', self["produce"])
                self.accept(offer, quantity=self["produce"])
            elif offer.price < self.price:
                self.reject(offer)
                self.log('sales', 0)

    def pay_workers(self):
        """
        pays the workers
        if the salary owed is greater than owned money:
        gives out all money and reduces wage by 1 unit
        """
        salary = self.wage * self['workers']
        if salary > self["money"]:
            salary = self["money"]
            self.wage -= self.wage_increment
            self.wage = max(0, self.wage)
        self.give("people", "money", quantity=salary)

    def pay_profits(self):
        """
        pays workers/bosses (same agent) the extra profits
        """
        buffer = self.num_days_buffer * self.wage * self.ideal_num_workers
        profits = self["money"] - buffer
        if profits > 0:
            self.give("people", "money", quantity=profits)

        self.log('dividends', max(0, profits))

    def getvalue_ideal_num_workers(self):
        return (self.name, self.ideal_num_workers)

    def getvalue_wage(self):
        return self.wage

    def publish_vacencies(self):
        return {"name": self.name, "number": self.ideal_num_workers, "wage": self.wage}

    def send_prices(self):
        self.send_envelope('people', 'price', self.price)
        return self.price

    def print_possessions(self):
        """
        prints possessions and logs money of a person agent
        """
        self.log("money", self["money"])
        self.log("produce", self["produce"])
        self.log("workers", self["workers"])

    def end_work_day(self):
        """
        """
        self.destroy('workers')
