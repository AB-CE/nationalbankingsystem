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

    """
    def init(self, money=0, inventory=0, ideal_num_workers=0, workers=0, price=0, wage=0,
             upper_inv=0, lower_inv=0, upper_price=0, lower_price=0):
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

    def production(self):
        """
        produces goods to add to inventory based on number fo workers and
        productivity
        """
        productivity = 1
        self.create("inventory", productivity*self.workers)

    def determine_wage(self, demand):
        """

        """

        if self.ideal_num_workers != self.workers:
            self.wage += 1
        elif self.ideal_num_workers == self.workers:

            # get messages and find out how many workers were offered,
            # if num_offered > 1.1*ideal_num_workers:
            #     lower the wage

    def determine_bounds(self, demand):
        """

        :param demand:
        :return:
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
        if self.inventory > self.upper_inv:
            self.ideal_num_workers -= 1
        elif self.inventory < self.lower_inv
            self.ideal_num_workers += 1

    def determine_prices(self):
        probability = 75 # 75% chance that price is changed given satisfied conditions
        if self.inventory < self.lower_inv and self.price < self.upper_price:
            if random.randint(1, 100) < probability:
                self.price += 1
        elif self.inventory > self.upper_inv and self.price > self.lower_price:
            if random.randint(1, 100) < probability:
                self.price -= 1

