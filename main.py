import abce
from firm import Firm
from people import People

population = 10
num_firms = 3
num_days = 7
price_for_produce = 120
price_for_labour = 100

simulation = abce.Simulation(name="economy", processes=1)

people_per_firm = int(population / num_firms)
remaining_people = population % num_firms

# makes a list for the number of employees per firm and accounts for when population isn't divisible by number of firms
list_employees = []
count = 0
for i in range(num_firms):
    count += 1
    if count <= remaining_people:
        list_employees.append(people_per_firm + 1)
    elif count > remaining_people:
        list_employees.append(people_per_firm)

# makes a list of dictionaries, for building all firm agents with correct num_people parameter
num_people = []
for i in range(num_firms):
    num_people.append({"num_people":list_employees[i]})

group_of_firms = simulation.build_agents(Firm, "firm", agent_parameters=num_people)

# makes a list of the firm each person is in
list_firmnumber = []
for i in range(population):
    firmid = i % num_firms
    list_firmnumber.append({"firm_number":firmid})

# creates population of people agents, includes the firm_number they are assigned/employed to
group_of_people = simulation.build_agents(People, "person", agent_parameters=list_firmnumber)

economy_agents = group_of_people + group_of_firms # economy supergroup


for day in range(num_days):
    simulation.advance_round(day)
    group_of_people.print_possessions()
    group_of_firms.print_possessions2()
    print()
    group_of_people.add_labour()
    group_of_people.sell_labour(labour_cost=price_for_labour)
    group_of_firms.buy_labour(labour_cost=price_for_labour)
    group_of_firms.production()
    group_of_people.buy_produce(price_for_produce)
    group_of_firms.sell_produce(price_for_produce)
    #group_of_people[0].print_possessions()
    #group_of_firms[0].print_possessions()
    total_net_worth_people = 0
    group_of_firms.panel_log(goods="money")
    print(list(group_of_people.getvalue()))
    for i in range(population):
        networthpeople = list(group_of_people.getvalue())[i] + price_for_produce*list(group_of_people.getvaluegoods())[i]
        total_net_worth_people += networthpeople
    print("net worth of people: ", total_net_worth_people)
    firmnetworth = list(group_of_firms.getvalue())[0] + price_for_produce * list(group_of_firms.getvaluegoods())[0]
    print("net worth of firm: ", firmnetworth)

    print()
    print()


simulation.graph()