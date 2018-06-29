import abce

class people(abce.Agent):

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

    def init(self, money=0, produce=0, population=0, workers=0):
        self.population = population
        self.create('money', money)
        self.produce = produce
        self.create('workers', workers)

    def start_work_day(self):
        """
        creates labour to add to the people's inventory
        """
        self.create('workers', self.population)

    def end_work_day(self):
        """
        destroys all labour
        """
        self.destroy('workers')

    def buy_produce(self, q, l, firm_price, firm_id):
        """
        Calculates the demand from each firm and makes buy offers for produce of this amount at this value, or as much
        as the people can afford

        Args:   q, l parameters as defined in the C-D utility function
                firm_price = the price the firm is selling the goods for
                firm_id = the number of the firm the people are trading with
        """
        I = self.not_reserved('money')
        demand = int((I/q)*(q/firm_price) ** (1/(1-l)))
        if I >= demand*firm_price:
            self.buy(('firm', firm_id), good='produce', quantity=demand, price=firm_price)
        else:
            self.buy(('firm', firm_id), good='produce', quantity=(int(self['money']/firm_price)), price=firm_price)
        return demand

    def send_workers(self, sum_wages, firm_wage, firm_id, vacancies):
        """
        Calculates the supply of employees for each firm, gives this amount of labour, or as much labour as possible
        to each firm

        Args:   sum_wages = the sum of the wages offered from every firm
                firm_wage = the wage the firm is offering
                firm_id = the number of the firm the people are trading with
        """
        willing_workers = self.population*(firm_wage/sum_wages)
        if vacancies <= willing_workers:
            self.send(('firm', firm_id), topic='max_employees', msg=willing_workers)
            self.give(('firm', firm_id), good='workers', quantity=vacancies)
        else:
            self.give(firm_id, good='workers', quantity=willing_workers)

    def print_possessions(self):
        """
        prints possessions and logs money of a person agent
        """
        print('    ' + self.group + str(dict(self.possessions())))
        self.log("money", self["money"])

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
