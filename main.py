import abce
import pandas as pd
import os
from firm import Firm
from people import People
from farm import Farm
from farmers_class import Farmers
import  plotly
import plotly.plotly as py
import plotly.graph_objs as go
plotly.tools.set_credentials_file(username='MayaKearney', api_key='XekHnBBOjROj1uJjKb8y')



params = dict(
    population=10000,
    farmers_population=10000,
    people_money=1000,
    farmers_money=500,
    num_firms=20,
    num_farms=20,
    firm_money=2000,
    farm_money=3000,
    farm_workers=5,
    farm_land=1000,
    harvest_per_day=100,
    goods_per_land=10,
    goods_per_worker=500,
    goods_price=30,
    days_harvest=90,
    harvest_start=7 * 30,
    maintenance_goods=1,
    reserve=30,
    farm_wage_increment=0.01,
    farm_price_increment=0.01,

    num_days=1300,

    l=0.5,  # constant from CS equation

    num_days_buffer=10,  # number of days worth of wages a firm will keep after giving profits

    phi_upper=10,  # phi_upper * demand gives upper bound to inventory
    phi_lower=2,
    excess=1.1,  # if number of workers offered to work for firm exceeds 110% of ideal number, decrease wage
    wage_increment=0.01,
    price_increment=0.01,
    worker_increment=0.01,
    productivity=1,
    wage_acceptance=1)
simulation = abce.Simulation(name='economy', processes=1)
group_of_firms = simulation.build_agents(Firm, "firm", number=params["num_firms"], **params)
people = simulation.build_agents(People, "people", number=1, **params)
farms = simulation.build_agents(Farm, "farm", number=params["num_farms"], **params)
farmers = simulation.build_agents(Farmers, "farmers", number=1, **params)


def main(params):

    for date in pd.date_range(start='1/1/1880', periods=params['num_days'], freq='D'):
        simulation.time = int(('%04i' % date.year)[2:] + '%02i' % date.month + '%02i' % date.day)

        group_of_firms.panel_log(variables=['ideal_num_workers'], goods=['workers'])


        people.create_labour()
        print(date.dayofyear, end='')

        if params['harvest_start'] == date.dayofyear:
            farms.reset_days_left()
        if params['harvest_start'] < date.dayofyear < params['harvest_start'] + params['days_harvest'] and date.year > 1880:
            print('*')
            farms.harvest()
            farms.find_ideal_workers()

            vacancies_list = list((group_of_firms + farms).publish_vacancies())
            people.send_workers(vacancies_list)

            farms.transport_goods()
            farms.send_prices()
            (people).get_prices()
            (people).buy_farm_goods()
            farms.sell_harvest()
            farms.change_price()
            farms.determine_wage()
            farms.redistribute_profits(days=366 - date.dayofyear)
            farms.end_harvest()

        else:
            print('.')
            farms.grow_crops()
            vacancies_list = list(group_of_firms.publish_vacancies())
            people.send_workers(vacancies_list)
            farms.redistribute_profits(days=365 - date.dayofyear)

        farms.log_sales()

        group_of_firms.production()
        group_of_firms.pay_workers()
        group_of_firms.pay_dividents()
        group_of_firms.send_prices()
        (people + farmers).get_prices()
        demand = (people + farmers).buy_goods()

        group_of_firms.sell_goods()
        group_of_firms.determine_bounds(demand=list(demand)[0])
        (group_of_firms + people + farms).print_possessions()
        group_of_firms.determine_wage()
        group_of_firms.expand_or_change_price()
        (people + group_of_firms).destroy_unused_labor()
        (people + farmers).consumption()
        group_of_firms.determine_profits()

        people.consume_farm_goods()
        farmers.dassert()


    print('done')

    #simulation.graph()
    #os.remove(simulation.path + 'panel_people.csv')
    path = simulation.path
    simulation.graph()

    def GraphFn(graphing_variable, agent):
        """
        function that takes in graphing variable as parameter and the produces a graph
        using plotly
        """
        df = pd.read_csv(path + "/panel_" + agent + ".csv")

        print("start graph fn")
        x_data = [[] for _ in range(params["num_" + agent + "s"])]
        y_data = [[] for _ in range(params["num_" + agent + "s"])]

        for i in range(len(df)):
            name = df["name"][i]
            number = int(name[4:])
            x_data[number].append(df["round"][i])
            y_data[number].append(df[graphing_variable][i])

        data = []

        for i in range(params["num_" + agent + "s"]):
            data.append(go.Scatter(x=x_data[i],
                                    y=y_data[i],
                                    mode="lines"))

        py.plot(data)
        print("end graph fn")

    def GraphFn_People(graphing_variable, agent):
        """
        function that takes in graphing variable as parameter and the produces a graph
        using plotly
        """
        df = pd.read_csv(path + "/panel_" + agent + ".csv")

        print("start graph fn")
        x_data = [[]]
        y_data = [[]]

        for i in range(len(df)):
            name = df["name"][i]
            number = int(name[4:])
            x_data[number].append(df["round"][i])
            y_data[number].append(df[graphing_variable][i])

        data = []

        data.append(go.Scatter(x=x_data[0],
                                y=y_data[0],
                                mode="lines"))

    #GraphFn("money", "farm")
    #GraphFn_People("money", "people")

if __name__ == '__main__':
    main(params)