import abce
import random

class Farm(abce.Agent):

    def init(self, capital=1, money=200, goods=0, land=1000, wage=0, capital_per_land = 0.2, farmable_land = 1,
             ideal_workers=0, non_harvest=0.75, people=0, goods_per_land=10, days_per_cycle=200, goods_per_capital=1):
        self.create("capital", capital)
        self.create("money", money)
        self.create("goods", goods)
        self.land = land
        self.wage = wage
        self.capital_per_land = capital_per_land
        self.farmable_land = 1
        self.ideal_capital = ideal_capital
        self.non_harvest = non_harvest
        self.create("people", people)
        self.goods_per_land = goods_per_land
        self.days_per_cycle = days_per_cycle
        self.goods_per_capital = goods_per_capital

    def find_people(self):
        self.create("people", random.uniform(2, 8))

    def find_land(self):
        self.land = random.uniform(2, 6)*500

    def find_ideal_capital(self):
        self.ideal_capital = self.land * self.capital_per_land

    def maintain_land(self):
        if self["capital"] <= self.ideal_capital:
            self.farmable_land = self["capital"] / (self.capital_per_land) * self.land
        elif self["capital"] > self.ideal_capital and self.farmable_land < 1:
            self.farmable_land = 1

    def harvest(self):
        max_goods = self.land * self.farmable_land * self.goods_per_land
        # ideal capital provides enough capital to upkeep land each day and enough capital to reap goods from land over entire harvest
        # harvest lasts 1/4 of cycle ie 0.25 times number of days per cycle
        day_goods = self.goods_per_capital * self["capital"]
        if day_goods + self["goods"] < max_goods
            self.create("goods", day_goods)
            self.farmable_land = day_goods / (self.land * self.goods_per_land)
        else:
            self.create("goods", day_goods - max_goods)
            self.farmable_land = 0