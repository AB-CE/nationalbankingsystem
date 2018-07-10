import abce
import random

class Farm(abce.Agent):

    def init(self, money=200, farm_goods=0, land=1000, wage=0, farmable_land=1, harvest_per_day=50, goods_to_sell=0,
             workers=0, goods_per_land=10, goods_per_worker=25, ideal_workers=0):
        self.create("money", money)
        self.create("farm_goods", farm_goods)
        self.land = land
        self.wage = wage
        self.ideal_workers = ideal_workers
        self.create("workers", workers)
        self.goods_per_worker = goods_per_worker
        self.price_dict = {}
        self.farmable_land = farmable_land
        self.goods_to_sell = goods_to_sell
        self.harvest_per_day = harvest_per_day
        if self.farmable_land > 1:
            raise Exception()

    def find_land(self):
        self.land = random.randrange(2, 6)*500
        print("LAND:", self.land)

    def harvest(self):
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

    def determine_wage(self):

    def transport_goods(self):
        self.goods_to_sell = self["workers"] * self.goods_per_worker
        if self.goods_to_sell > self.notreserved("farm_goods"):
            self.goods_to_sell = self.not_reserved("farm_goods")
        self.give(people, good='money', quantity=(self['workers'] * self.wage))

    def sell_harvest(self):


















#    def find_q(self):
#        """
#        returns the parameter q as defined in the C-D utility function
#        """
#        L = self.l
#        q = 0
#        for id in range(self.num_firms):
#            q += self.price_dict[('firm', id)] ** (L / (L - 1))
#        q = float(q) ** ((L - 1) / L)
#        return q

#    def buy_produce(self):
#        q = self.find_q()
#        self.log('q', q)

#        probability_list = []
#        l = self.l

#        for firm in range(self.num_firms):  # fix systematic advantage for 0 firm
#            firm_price = float(self.price_dict['firm', firm])
#            probability = (1 / q) * (q / firm_price) ** (1 / (1 - l))
#            probability_list.append(probability)

#        self.buy(('firm', firm), good='produce', quantity=(self.ideal_workers - self['capital']), price=firm_price)

#        self.log('total_demand', sum(demand_list))
#        return demand_list

 ##   def produce_into_capital(self):
  #      if self.farmable_land < 1 and self.notreserved("produce") > self.produce_per_capital:
   #         self.destroy("produce", self.produce_per_capital)
    #        self.create("capital", 1)


#    def maintain_land(self):
#        if self["workers"] <= self.ideal_workers:
#            self.farmable_land = self["workers"] / self.ideal_workers
#        else:
#            self.farmable_land = 1
#        print("FARMABLE LAND:", self.farmable_land)
#    simulation = abce.Simulation(name='economy', processes=1)

#    def find_ideal_workers(self):
#        self.ideal_workers = self.land / self.land_per_worker
#        print("IDEAL WORKERS:", self.ideal_workers)


farm = simulation.build_agents(Farm, "farm", number=1, capital=150)
farm.find_land()
farm.find_people()
farm.find_ideal_workers()
farm.maintain_land()
for r in range(100):
    print("count", r)
    farm.harvest()