import abce
import random

class Farm(abce.Agent):

    def init(self, farm_money, farm_workers, farm_land, harvest_per_day, goods_per_land,
             goods_per_worker, ideal_workers, goods_price, days_harvest, wage_increment, price_increment, **_):
        self.create("money", farm_money)
        self.create("workers", farm_workers)
        self.land = farm_land
        self.harvest_per_day = harvest_per_day
        self.goods_per_land = goods_per_land
        self.goods_per_worker = goods_per_worker
        self.ideal_workers = ideal_workers
        self.goods_price = goods_price
        self.days_left = days_harvest
        self.wage_increment = wage_increment
        self.price_increment = price_increment
        self.wage = 10
        self.farmable_land = 0
        self.goods_to_sell = 0

    def grow_crops(self):
        """
        creates farmable land throughout the non-harvest period, from which crops can be taken
        """
        self.farmable_land += 0.01
        if self.farmable_land > 1:
            self.farmable_land = 1

    def harvest(self):
        """
        Converts farmable land into crops during the harvest period
        """
        max_goods = self.land * self.farmable_land * self.goods_per_land
        if self.harvest_per_day < max_goods:
            self.create("farm_goods", self.harvest_per_day)
            self.farmable_land = (max_goods - self.harvest_per_day) / (self.land * self.goods_per_land)
        else:
            self.create("farm_goods", max_goods)
            self.farmable_land = 0

    def find_ideal_workers(self):
        """
        finds the ideal number of workers to deliver the goods
         > Equal to the total number of goods divided by the days during the cycle and the goods each worker can deliver
        """
        self.ideal_workers = int(self["farm_goods"] / (self.days_left * self.goods_per_worker)) + 1
        self.days_left -= 1

    def determine_wage(self):
        """
        Sets the wages for the farm workers
        If they don't hire as many workers as they'd like they offer a higher wage. If their vacancies are oversubscribed
        they lower the offered wage.
        """
        messages = self.get_messages("max_employees")
        if self.ideal_workers > self['workers']:
            self.wage += random.uniform(0, self.wage_increment * self.wage)

        elif self.ideal_workers == self['workers']:
            max_employees = messages[0]
            if max_employees > self.ideal_workers:
                self.wage -= random.uniform(0, self.wage_increment * self.wage)
                if self.wage < 0:
                    self.wage = 0
        else:
            raise Exception()

    def transport_goods(self): # don't include this just pay workers flat price for 1 day work
        """
        Transports goods to the market. The workers are payed here
        """
        self.goods_to_sell = self["workers"] * self.goods_per_worker
        if self.goods_to_sell > self.notreserved("farm_goods"):
            self.goods_to_sell = self.not_reserved("farm_goods")
            workers_needed = int(self.not_reserved("farm_goods") / self.goods_per_worker) + 1
            fired_workers = self["workers"] - workers_needed
            self.destroy("workers", fired_workers)
        self.give("people", good='money', quantity=(self['workers'] * self.wage))

    def sell_harvest(self):
        """
        Sells the goods
        """
        for offer in self.get_offers("farm_goods"):
            if offer.price >= self.goods_price and self.goods_to_sell >= offer.quantity:
                self.accept(offer)
                self.log('sales', offer.quantity)
                self.goods_to_sell -= offer.quantity
            elif offer.price >= self.goods_price and self.goods_to_sell < offer.quantity:
                self.log('sales', self["farm_goods"])
                self.accept(offer, quantity=self.goods_to_sell)
                self.goods_to_sell = 0
            elif offer.price < self.goods_price:
                self.reject(offer)
                self.log('sales', 0)

    def transport_back(self):
        """
        Transports any remaining goods back to the farm
        """
        workers_needed = self.goods_to_sell / self.goods_per_worker
        fired_workers = self["workers"] - workers_needed
        self.destroy("workers", fired_workers)
        self.give("people", good='money', quantity=(self['workers'] * self.wage))

    def change_price(self):
        """
        Adjusts prices based on how many goods are sold
        """
        if self.goods_to_sell > 0:
            self.goods_price -= random.uniform(0, self.price_increment * self.goods_price)
        else:
            self.goods_price += random.uniform(0, self.price_increment * self.goods_price)

    def publish_vacencies(self):
        return {"name": self.name, "number": self.ideal_num_workers, "wage": self.wage}

    def send_prices(self):
        self.send_envelope('people', 'price', self.price)
        return self.price