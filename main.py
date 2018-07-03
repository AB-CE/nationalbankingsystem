import abce
from firm import Firm
from people import People

_population = 1000
people_money = 200000

num_firms = 20
num_employees = 1000
firm_money = 800000

num_days = 1000
L = 0.5
demand = num_employees / num_firms

simulation = abce.Simulation(name='economy', processes=1)
group_of_firms = simulation.build_agents(Firm, "firm", number=num_firms, money=firm_money,)
people = simulation.build_agents(People, "people", number=1, population=_population, money=people_money,
                                 num_firms=num_firms)

group_of_firms.determine_bounds([demand] * num_firms)



for r in range(num_days):
    simulation.time = r

    people.start_work_day()

    group_of_firms.determine_workers()
    group_of_firms.determine_price()

    vacancies_list = list(group_of_firms.publish_vacencies())

    people.send_workers(vacancies_list)



    group_of_firms.production()
    demand_list = []
    group_of_firms.getvalue_price()
    people.get_prices()

    demand = people.buy_produce()
    demand_list = list(demand)[0]

    group_of_firms.sell_goods()
    group_of_firms.pay_workers()
    group_of_firms.pay_profits()
    people.end_work_day()
    group_of_firms.determine_bounds(demand=demand_list)
    people.print_possessions()
    group_of_firms.print_possessions()
    group_of_firms.determine_wage()
    group_of_firms.end_work_day()
    people.consumption()

print('done')

simulation.graph()
simulation.finalize()
