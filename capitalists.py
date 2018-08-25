class Capitalists:

    def init(self, capitalists_money, capitalist_population, **_):
        self.create("money", capitalists_money)
        self.population = capitalist_population

    def get_prices(self):
        """
        reads the messages from the firms and creates a price list
        """
        price_msg = self.get_messages("price")
        for msg in price_msg:
            self.price_dict[msg.sender] = msg.content
        return self.price_dict

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

    def buy_goods(self):
        """
        Calculates the demand from each firm and makes buy offers for produce of this amount at this value, or as much
        as the people can afford

        Args:   q, l parameters as defined in the C-D utility function
                firm_price = the price the firm is selling the goods for
                firm_id = the number of the firm the people are trading with
        """
        q = self.find_q()
        print("q", q)
        self.log('q', q)

        demand_list = []
        l = self.l
        print("monsey", self["money"], self.not_reserved("money"))
        I = self.not_reserved('money')
        assert np.isfinite(I)
        for firm in range(self.num_firms):  # fix systematic advantage for 0 firm
            firm_price = float(self.price_dict['firm', firm])
            demand = (I / q) * (q / firm_price) ** (1 / (1 - l))
            self.buy(('firm', firm), good='produce', quantity=demand, price=firm_price)
            demand_list.append(demand)
            print(firm_price)
        self.log('total_demand', sum(demand_list))
        print(demand_list)
        return demand_list

    def print_possessions(self):
        """
        logs the money of the farmers agent
        """
        self.log("money", self["money"])

    def consumption(self):
        self.log("consumption", self["produce"])
        self.destroy("produce")
