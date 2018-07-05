import abce

class Farm(abce.Agent):

    def init(self, farm_workers=100, money=200, produce=0, land=1000, wage=0, workers_per_land = 5, farmable_land = 1,
             ideal_workers=0, non_harvest=0.75):
        self.create["farm_workers"] = farm_workers
        self.create["money"] = money
        self.create["produce"] = produce
        self.land = land
        self.wage = wage
        self.workers_per_land = wrokers_per_land
        self.farmable_land = 1
        self.ideal_workers = ideal_workers
        self.non_harvest = non_harvest

    def find_ideal_workers(self):
        ideal_workers = self.land * self.workers_per_land * self.farmable_land
        self.ideal_workers = ideal_workers

    def work_non_harvest(self, ideal_workers):
        if self["workers"] < ideal_workers:
            