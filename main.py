import abce
from firm import Firm
from people import People
from farm import Farm

params = dict(
    population=1000,
    people_money=1000,
    num_firms=20,
    num_farms=20,
    firm_money=2000,
    farm_money=3000,
    farm_workers=5,
    farm_land=5000,
    harvest_per_day=100,
    goods_per_land=10,
    goods_per_worker=100,
    goods_price=30,
    days_harvest=100,

    num_days=2000,

    l=0.5,  # constant from CS equation

    num_days_buffer=10,  # number of days worth of wages a firm will keep after giving profits

    phi_upper=10,  # phi_upper * demand gives upper bound to inventory
    phi_lower=2,
    excess=1.1,  # if number of workers offered to work for firm exceeds 110% of ideal number, decrease wage
    wage_increment=0.01,
    price_increment=0.01,
    worker_increment=0.01,
    productivity=1,
    wage_acceptance=1,
    farm_wage_incriment=0.01,
    farm_price_incriment=0.01)
simulation = abce.Simulation(name='economy', processes=1)
group_of_firms = simulation.build_agents(Firm, "firm", number=params["num_firms"], **params)
people = simulation.build_agents(People, "people", number=1, **params)
farms = simulation.build_agents(Farm, "farm", number=params["num_farms"], **params)

for r in range(params["num_days"]):
    simulation.time = r

    group_of_firms.panel_log(variables=['wage', 'ideal_num_workers'], goods=['workers'])
    people.create_labor()

    vacancies_list = list(group_of_firms.publish_vacencies())

    people.send_workers(vacancies_list)

    group_of_firms.production()
    group_of_firms.pay_workers()
    group_of_firms.pay_dividents()
    group_of_firms.send_prices()
    people.get_prices()
    demand = people.buy_goods()

    group_of_firms.sell_goods()
    group_of_firms.determine_bounds(demand=list(demand)[0])
    (group_of_firms + people).print_possessions()
    group_of_firms.determine_wage()
    group_of_firms.expand_or_change_price()
    (people + group_of_firms).destroy_unused_labor()
    people.consumption()
    group_of_firms.determine_profits()

print('done')

simulation.graph()
simulation.finalize()
