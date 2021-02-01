import json

powerplant_types = ['gasfired', 'turbojet', 'windturbine']
fuel_associations = {"gasfired": "gas(euro/MWh)", "turbojet": 'kerosine(euro/MWh)'}
co2_production_rate = 0.3 # t/MWh


def calculate_powerplant_price(powerplants, prices):
    for powerplant in powerplants:
        if powerplant['type'] == 'windturbine':
            powerplant['price(eur/MWh)'] = 0
            powerplant['production_cost(euro)'] = 0
            powerplant['production(MWh)'] = round(powerplant['pmax'] * prices['wind(%)'] / 100, 2)
        else:
            fuel_type = fuel_associations[powerplant['type']]
            powerplant_fuel_prices = prices[fuel_type]
            powerplant['price(eur/MWh)'] = powerplant_fuel_prices / powerplant['efficiency']
            powerplant['production(MWh)'] = 0


def calculate_powerplant_price_with_co2(powerplants, prices):
    for powerplant in powerplants:
        if powerplant['type'] == 'windturbine':
            powerplant['price(eur/MWh)'] = 0
            powerplant['production(MWh)'] = round(powerplant['pmax'] * prices['wind(%)'] / 100, 2)
        else:
            fuel_type = fuel_associations[powerplant['type']]
            powerplant_fuel_prices = prices[fuel_type]
            powerplant['price(eur/MWh)'] = powerplant_fuel_prices / powerplant['efficiency'] + co2_production_rate * prices['co2(euro/ton)']
            powerplant['production(MWh)'] = 0


def sort_sources(powerplants):
    sorted_powerplants = sorted(powerplants, key=lambda powerplant: powerplant['price(eur/MWh)'])
    return sorted_powerplants


def allocation_of_resources(powerplants, load):
    remaining_load = load
    for index, powerplant in enumerate(powerplants):
        if remaining_load > powerplant['pmax']:
            # there is more load to cover, maximal production is needed
            if powerplant['type'] == 'windturbine':
                remaining_load -= powerplant['production(MWh)']
            else:
                powerplant['production(MWh)'] = powerplant['pmax']
                powerplant['production_cost(euro)'] = powerplant['production(MWh)'] * powerplant['price(eur/MWh)']
                remaining_load -= powerplant['production(MWh)']
        elif 0 < remaining_load < powerplant['pmin']:
            # minimal production of the powerplant is more than requiered load, so lets borrow production from previous sources
            production_to_borrow = powerplant['pmin'] - remaining_load
            for index_to_borrow in range(index - 1, -1, -1):
                if powerplants[index_to_borrow]['production(MWh)'] - production_to_borrow >= powerplants[index_to_borrow]['pmin']:
                    powerplants[index_to_borrow]['production(MWh)'] -= production_to_borrow
                    production_to_borrow = 0
                    powerplants[index_to_borrow]['production_cost(euro)'] = powerplants[index_to_borrow]['production(MWh)'] * powerplants[index_to_borrow]['price(eur/MWh)']
                    break
                else:
                    powerplants[index_to_borrow]['production(MWh)'] = powerplants[index_to_borrow]['pmin']
                    production_to_borrow -= powerplants[index_to_borrow]['production(MWh)'] - powerplants[index_to_borrow]['pmin']
                    powerplants[index_to_borrow]['production_cost(euro)'] = powerplants[index_to_borrow]['production(MWh)'] * powerplants[index_to_borrow]['price(eur/MWh)']

            if production_to_borrow != 0:
                # unable to borrow enough power from settled powerplats
                print("Unable to borrow enough power from settled powerplats")
            else:
                remaining_load = powerplant['pmin']
                powerplant['production(MWh)'] = remaining_load
                powerplant['production_cost(euro)'] = powerplant['production(MWh)'] * powerplant['price(eur/MWh)']
                remaining_load -= powerplant['production(MWh)']

        elif powerplant['pmin'] <= remaining_load <= powerplant['pmax']:
            # the powerplant is final that is used to supply load
            powerplant['production(MWh)'] = remaining_load
            powerplant['production_cost(euro)'] = powerplant['production(MWh)'] * powerplant['price(eur/MWh)']
            remaining_load -= powerplant['production(MWh)']
        else:
            powerplant['production(MWh)'] = 0
            powerplant['production_cost(euro)'] = 0
            continue

    if remaining_load != 0:
        print(f"Unable to supply enough production to meet requirements")


def produce_output(powerplants):
    output_list = []
    output_production = 0
    cost_of_production = 0

    for powerplant in powerplants:
        output_dictionary = {'name': powerplant['name'], 'p': round(powerplant['production(MWh)'], 1)}
        output_list.append(output_dictionary)
        output_production += powerplant['production(MWh)']
        cost_of_production += powerplant['production_cost(euro)']

    print(f"Output production {output_production}(MWh) at cost {cost_of_production} euro")
    return output_list


def processing_output(input):
    print(f"{input}")
    load = input["load"]
    fuels = input["fuels"]
    powerplants = input["powerplants"]

    wind_effectivity = fuels['wind(%)']
    gas_price = fuels['gas(euro/MWh)']
    kerosine_price = fuels['kerosine(euro/MWh)']
    co2 = fuels['co2(euro/ton)']

    calculate_powerplant_price(powerplants, fuels)
    sorted_powerplants = sort_sources(powerplants)
    allocation_of_resources(sorted_powerplants, load)
    output_list = produce_output(sorted_powerplants)
    json_output = json.dumps(output_list)
    return json_output
