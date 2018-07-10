import abce
import random

class Farm(abce.Agent):

    def init(self, money=200, farm_goods=0, land=1000, wage=0, farmable_land=0, harvest_per_day=50, goods_to_sell=0,
             workers=0, goods_per_land=10, goods_per_worker=25, ideal_workers=0, good_price=0, days_harvest=80, goods_per_land=20,
             excess=1.1, wage_incriment=0.02, price_incriment = 0.02):
        self.create("money", money)
        self.create("farm_goods", farm_goods)
        self.land = land
        self.wage = wage
        self.ideal_workers = ideal_workers
        self.create("workers", workers)
        self.goods_per_worker = goods_per_worker
        self.price_dict = {}
        self.farmable_land = farmable_land
        if self.farmable_land > 1:
            raise Exception()
        self.goods_to_sell = goods_to_sell
        self.good_price = good_price
        self.harvest_per_day = harvest_per_day
        self.goods_per_land = goods_per_land
        self.days_harvest = days_harvest
        self.excess = excess
        self.wage_incriment = wage_incriment
        self.price_incriment = price_incriment

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
        # ideal capital provides enough capital to upkeep land each day and enough capital to reap goods from land over entire harvest
        # harvest lasts 1/4 of cycle ie 0.25 times number of days per cycle
        if self.harvest_per_day < max_goods:
            self.create("farm_goods", self.harvest_per_day)
            self.farmable_land = (max_goods - self.harvest_per_day) / (self.land * self.goods_per_land)
        else:
            self.create("farm_goods", max_goods)
            self.farmable_land = 0
        print("MAX GOODS:", max_goods)
        print("GOODS TODAY", day_goods)
        print("GOODS:", self['farm_goods'])
        print("FARMABLE LAND:", self.farmable_land)

    def find_ideal_workers(self):
        """
        finds the ideal number of workers to deliver the goods
         > Equal to the total number of goods divided by the days during the cycle and the goods each worker can deliver
        """
        self.ideal_workers = int(self["farm_goods"] / (self.days_harvest * self.goods_per_worker)) + 1

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
            if max_employees > self.excess * self.ideal_workers:
                self.wage -= random.uniform(0, self.wage_increment * self.wage)
                if self.wage < 0:
                    self.wage = 0
        else:
            raise Exception()

    def transport_goods(self):
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
            if offer.price >= self.good_price and self.goods_to_sell >= offer.quantity:
                self.accept(offer)
                self.log('sales', offer.quantity)
                self.goods_to_sell -= offer.quantity
            elif offer.price >= self.good_price and self.goods_to_sell < offer.quantity:
                self.log('sales', self["farm_goods"])
                self.accept(offer, quantity=self.goods_to_sell)
                self.goods_to_sell = 0
            elif offer.price < self.good_price:
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
            self.price -= random.uniform(0, self.price_increment * self.price)
        else:
            self.price += random.uniform(0, self.price_increment * self.price)