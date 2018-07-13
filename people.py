import abce


class People(abce.Agent):

    """
    People:
    - Represents the total american population
    - Gains units of labour equal to their population at the start of each day
    - Destroys all excess labour at the end of each day
    - Buys produce from firms
        - Demand is decided by C-D utility function
        - If they can't afford to meet their demand, they buy as much produce ss possible
    - Offers to sell labour to every firm at the start of each day
        - Maximum labour offered is proportional to firm wages
        - Sends a message to the firm each round telling the firm their offer
        - If they have less labour than the maximum labour offered, they will sell ll their labour
        - Otherwise, they will sell the maximum
    """

    def init(self, people_money, population, l, num_firms, wage_acceptance, maintenance_goods, reserve,
             num_farms, days_harvest, **_):
        self.name = "people"
        self.population = population
        self.create('money', people_money)
        self.produce = 0
        self.num_firms = num_firms
        self.price_dict = {}
        self.price_dict_farm = {}
        self.l = l
        self.wage_acceptance = wage_acceptance
        self.maintenance_goods = maintenance_goods
        self.reserve = reserve
        self.num_farms = num_farms

    def create_labour(self):
        """
        creates labour to add to the people's inventory
        """
        self.create('workers', self.population)

    def destroy_unused_labor(self):
        """
        destroys all labour
        """
        self.destroy('workers')

    def consumption(self):
        self.log("consumption", self["produce"])
        self.destroy("produce")

    def find_q(self):
        """
        returns the parameter q as defined in the C-D utility function
        """
        L = self.l
        q = 0
        for id in range(self.num_firms):
            q += self.price_dict[('firm', id)] ** (L / (L - 1))
        q = float(q) ** ((L - 1) / L)
        return q


    def find_q_farms(self):
        """
        returns the parameter q as defined in the C-D utility function
        """
        L = self.l
        q = 0
        for id in range(self.num_farms):
            q += self.price_dict[('farm', id)] ** (L / (L - 1))
        q = float(q) ** ((L - 1) / L)
        return q

    def buy_goods(self):
        """
        Calculates the demand from each firm and makes buy offers for produce of this amount at this value, or as much
        as the people can afford

        Args:   q, l parameters as defined in the C-D utility function
                firm_price = the price the firm is selling the goods for
                firm_id = the number of the firm the people are trading with
        """
        q = self.find_q()
        self.log('q', q)

        demand_list = []
        l = self.l

        I = self.not_reserved('money')
        for firm in range(self.num_firms):  # fix systematic advantage for 0 firm
            firm_price = float(self.price_dict['firm', firm])
            demand = (I / q) * (q / firm_price) ** (1 / (1 - l))
            self.buy(('firm', firm), good='produce', quantity=demand, price=firm_price)
            demand_list.append(demand)
        self.log('total_demand', sum(demand_list))
        return demand_list

    def send_workers(self, vacancies_list):
        """
        Calculates the supply of employees for each firm, gives this amount of labour, or as much labour as possible
        to each firm

        Args:   sum_wages = the sum of the wages offered from every firm
                firm_wage = the wage the firm is offering
                firm_id = the number of the firm the people are trading with
        """
        wages = [vacancy["wage"] for vacancy in vacancies_list]

        max_wage = max(wages)

        distances = [1 - ((max_wage - wage) / max_wage) ** self.wage_acceptance for wage in wages]

        norm = sum(distances)

        for vacancies, dist in zip(vacancies_list, distances):
            firm = vacancies["name"]
            willing_workers = self.population / norm * dist
            if vacancies["number"] <= willing_workers:
                self.send(firm, 'max_employees', willing_workers)
                self.give(firm, good='workers', quantity=vacancies["number"])
            else:
                self.give(firm, good='workers', quantity=willing_workers)

    def print_possessions(self):
        """
        prints possessions and logs money of a person agent
        """
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])
        self.log("workers", self["workers"])

    def getvalue(self):
        """
        returns the value of money owned by a person agent
        """
        return self["money"]

    def getvaluegoods(self):
        """
        returns the amount of produce owned by the person agent
        """
        return self["produce"]

    def get_prices(self):
        """
        reads the messages from the firms and creates a price list
        """
        price_msg = self.get_messages("price")
        for msg in price_msg:
            self.price_dict[msg.sender] = msg.content
        return self.price_dict

    def buy_farm_goods(self):
        if self["farm_goods"] < self.population * (self.maintenance_goods + self.reserve):
            q = self.find_q_farms()
            self.log('q', q)

            demand_list = []
            l = self.l

            # I must reflect tht they're only buying a certain number of necessaties
            I = self.not_reserved('money')
            for farm in range(self.num_farms):  # fix systematic advantage for 0 firm
                goods_price = float(self.price_dict['farm', farm])
                demand = (I / q) * (q / goods_price) ** (1 / (1 - l))
                self.buy(('farm', farm), good='farm_goods', quantity=demand, price=goods_price)
                demand_list.append(demand)
            self.log('total_demand', sum(demand_list))
            return demand_list

    def consume_farm_goods(self):
        """
        Each person consumes the farm goods they must consume per day
        """
        if self["farm_goods"] > self.maintenance_goods * self.population:
            self.destroy("farm_goods", self.maintenance_goods * self.population)
        elif 0 < self["farm_goods"] < self.maintenance_goods * self.population:
            self.destroy("farm_goods")
        else:
            pass

    def find_reserve(self):
        """
        Finds how many goods each person must keep in their reserve. This is such that they can consume their maintenance
        goods per day that is not the harvest.
        """
        self.reserve = self.days_harvest * 11 * self.maintenance_goods




