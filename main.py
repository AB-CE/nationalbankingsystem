import abce
from firm import firm
from people import people

_population = 1000
people_money = 200000

num_firms = 10
num_employees = 100
firm_money = 800000

num_days = 10
L = 0.5
demand = 4

simulation = abce.Simulation(name='economy', processes=1)
group_of_firms = simulation.build_agents(firm, "firm", number=num_firms, money=firm_money,)
people = simulation.build_agents(people, "people", number=1, population=_population, money=people_money)


def find_q():
    """
    returns the parameter q as defined in the C-D utility function
    """
    q_j = [wage ** (1 / (L-1)) for wage in list(group_of_firms.getvalue_wage())]
    q = sum(q_j)
    return q


group_of_firms.determine_bounds([demand] * num_firms)



for r in range(num_days):
    simulation.time = r
    # gives labour for
    people.start_work_day()

    group_of_firms.determine_wage()
    group_of_firms.determine_workers()
    group_of_firms.determine_price()

    vacancies_list = list(group_of_firms.getvalue_ideal_num_workers())
    wage_list = list(group_of_firms.getvalue_wage())


    sum_wages = sum(wage_list)
    print(wage_list)
    print(vacancies_list)
    firm_id = group_of_firms.firm_id
    print(type(firm_id))
    for v, vacency in enumerate(vacancies_list):
        people.send_workers(sum_wages=sum_wages, firm_wage = wage_list[v], firm_id=v, vacancies=vacency)
    group_of_firms.production()
    price_list = list(group_of_firms.getvalue_price())
    demand_list = []
    demand = people.buy_produce(q=find_q(), l=L, firm_price=price_list[v], firm_id=v)
    demand_list.append(list(demand))
    group_of_firms.sell_goods()
    group_of_firms.pay_workers()
    group_of_firms.pay_profits()
    people.end_work_day()
    group_of_firms.determine_bounds(demand=demand_list)

print('done')

simulation.finalize()