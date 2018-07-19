import abce
import random


class Farm(abce.Agent):
    def init(self, farm_money, farm_land, harvest_per_day, goods_per_land, goods_per_worker,
             goods_price, days_harvest, farm_wage_increment, farm_price_increment, num_farms, **_):
        self.create("money", farm_money)
        self.land = farm_land
        self.harvest_per_day = harvest_per_day
        self.goods_per_land = goods_per_land
        self.goods_per_worker = goods_per_worker
        self.goods_price = goods_price
        self.days_left = days_harvest
        self.days_harvest = days_harvest
        self.wage_increment = farm_wage_increment
        self.price_increment = farm_price_increment
        self.wage = 10
        self.farmable_land = 0
        self.goods_to_sell = 0
        self.ideal_workers= 10
        self.sales = 0

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
        self.ideal_workers = max(1, self["farm_goods"] / ((self.days_left + 1) * self.goods_per_worker))
        if self["money"] < self.ideal_workers * self.wage:
            self.ideal_workers = self["money"] / self.wage
        self.days_left -= 1
        self.days_left = max(0, self.days_left)

    def reset_days_left(self):
        self.days_left = self.days_harvest

    def determine_wage(self):
        """
        Sets the wages for the farm workers
        If they don't hire as many workers as they'd like they offer a higher wage. If their vacancies are oversubscribed
        they lower the offered wage.
        """
        messages = self.get_messages("max_employees")
        if self.ideal_workers > self['workers']:
            self.wage += random.uniform(0, self.wage_increment * self.wage)

        elif self.ideal_workers <= self['workers']:
            max_employees = messages[0]
            if max_employees > self.ideal_workers:
                self.wage -= random.uniform(0, self.wage_increment * self.wage)
                if self.wage < 0:
                    self.wage = 0
        else:
            raise Exception(self.ideal_workers - self['workers'])

    def transport_goods(self): # don't include this just pay workers flat price for 1 day work
        """
        Transports goods to the market. The workers are payed here
        """
        self.goods_to_sell = self["workers"] * self.goods_per_worker
        if self.goods_to_sell > self.not_reserved("farm_goods"):
            self.goods_to_sell = self.not_reserved("farm_goods")
        self.give("people", good='money', quantity=(self['workers'] * self.wage))
        self.destroy("workers")

    def sell_harvest(self):
        """
        Sells the goods
        """
        for offer in self.get_offers("farm_goods"):
            if offer.price >= self.goods_price and self.goods_to_sell >= offer.quantity:
                self.accept(offer)
                self.sales = offer.quantity
                self.goods_to_sell -= offer.quantity
            elif offer.price >= self.goods_price and self.goods_to_sell < offer.quantity:
                self.sales = self.goods_to_sell
                self.accept(offer, quantity=self.goods_to_sell)
                self.goods_to_sell = 0
            elif offer.price < self.goods_price:
                self.reject(offer)
                self.sales = 0

    def log_sales(self):
        self.log('sales', self.sales)
        self.sales = 0

#    def transport_back(self):
 #       """
  #      Transports any remaining goods back to the farm
   #     """
    #    workers_needed = self.goods_to_sell / self.goods_per_worker
     #   fired_workers = max(0, self["workers"] - workers_needed)
      #  self.destroy("workers", fired_workers)
       # self.give("people", good='money', quantity=(self['workers'] * self.wage))
        #self.destroy("workers")

    def change_price(self):
        """
        Adjusts prices based on how many goods are sold
        """
        if self.goods_to_sell > 0 and self.wage < self.goods_per_worker * self.goods_price:
            self.goods_price -= random.uniform(0, self.price_increment * self.goods_price)
        else:
            self.goods_price += random.uniform(0, self.price_increment * self.goods_price)

    def publish_vacancies(self):
        if self.not_reserved("money") > 2 * self.ideal_workers * self.wage:
            return {"name": self.name, "number": self.ideal_workers, "wage": self.wage}
        else:
            return{"name": self.name, "number": (self.not_reserved("money") / (2 * self.wage)), "wage": self.wage}

    def send_prices(self):
        self.send_envelope('people', 'price', self.goods_price)
        return self.goods_price

    def print_possessions(self):
        """
        prints possessions and logs money of a person agent
        """
        #print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])
        self.log("workers", self["workers"])
        self.log('wage_farm', self.wage)
        self.log('ideal_workers_farms', self.ideal_workers)
        self.log('farm_goods', self['farm_goods'])

    def print_possessions2(self):
        """
        prints possessions and logs money of a person agent
        """
        #print('    ' + self.group + str(dict(self.possessions())))
        print("FARM", self.id)
        print("money", self["money"])
        print('farm_goods', self['farm_goods'])

    def end_harvest(self):
        """
        At the end of harvest, farms mst destroy their produce
        """
        if self.days_left == 1:
            self.destroy("farm_goods")