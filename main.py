import abce
from firm import Firm
from people import People

num_people = 10
num_firms = 1
num_days = 7
price_for_produce = 120

simulation = abce.Simulation(name="economy", processes=1)

group_of_people = simulation.build_agents(People, "person", number=num_people)
group_of_firms = simulation.build_agents(Firm, "firm", number=num_firms, num_people=num_people)

economy_agents = group_of_people + group_of_firms # economy supergroup


for day in range(num_days):
    simulation.advance_round(day)
    group_of_people[0].print_possessions()
    group_of_firms[0].print_possessions()
    print()
    group_of_people.add_labour()
    group_of_firms.buy_labour()
    group_of_people.sell_labour()
    group_of_firms.production()
    group_of_people.buy_produce(price_for_produce)
    group_of_firms.sell_produce(price_for_produce)
    group_of_people[0].print_possessions()
    group_of_firms[0].print_possessions()
    total_net_worth_people = 0
    for i in range(num_people):
        total_net_worth_people += group_of_people[i].self["money"]
    print("net worth of people: ", total_net_worth_people)

    print()
    print()


simulation.finalize()