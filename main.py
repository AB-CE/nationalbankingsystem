import abce
from firm import Firm
from people import People
params = dict(
    _population=1000,
    people_money=1000,
    num_firms=20,
    num_employees=1000,
    firm_money=2000,

    num_days=1000,

    l=0.5, # constant from CS equation

    num_days_buffer=10, # number of days worth of wages a firm will keep after giving profits

    probability=75,  # 75% chance of increasing price when conditions are satisfied

    phi_upper=10, # phi_upper * demand gives upper bound to inventory
    phi_lower=2,
    const_upper=1.5, # const_upper * marginal_cost gives upper bound to price
    const_lower=1.05,

    excess=1.1, # if number of workers offered to work for firm exceeds 110% of ideal number, raise wage
    wage_increment=10,
    price_increment=10
)
simulation = abce.Simulation(name='economy', processes=1)
group_of_firms = simulation.build_agents(Firm, "firm", number=params["num_firms"], **params)
people = simulation.build_agents(People, "people", number=1, population=params["_population"],
                                 money=params["people_money"], **params)


for r in range(params["num_days"]):
    simulation.time = r

    group_of_firms.panel_log(variables=['wage', 'ideal_num_workers'], goods=['workers'])
    people.start_work_day()

    vacancies_list = list(group_of_firms.publish_vacencies())

    people.send_workers(vacancies_list)

    group_of_firms.production()
    group_of_firms.pay_workers()
    group_of_firms.pay_profits()
    demand_list = []
    group_of_firms.send_prices()
    people.get_prices()

    demand = people.buy_produce()
    demand_list = list(demand)[0]

    group_of_firms.sell_goods()
    people.end_work_day()
    group_of_firms.determine_bounds(demand=demand_list)
    people.print_possessions()
    group_of_firms.print_possessions()
    group_of_firms.determine_wage()
    group_of_firms.determine_workers()
    group_of_firms.determine_price()
    group_of_firms.end_work_day()
    people.consumption()

print('done')

simulation.graph()
simulation.finalize()
