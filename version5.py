import pandas as pd
from tabulate import tabulate
import os.path
from os import path
import matplotlib.pyplot as plt 

def read_data(label):
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    
    data = pd.read_csv(f'./resources/{label}.csv', index_col=0, names=months)

    return data

def plot_data(cities, data_map, months_chosen):
    num_data_types = len(data_map)
    fig, axs = plt.subplots(num_data_types, 1, figsize=(12, 8 * num_data_types), constrained_layout=True)

    if num_data_types == 1:
        axs = [axs]

    for ax, (data_label, data) in zip(axs, data_map.items()):
        for city in cities:
            city_data = data.loc[city, months_chosen]
            ax.plot(months_chosen, city_data, marker='o', label=f"{city.capitalize()}")
        ax.set_title(f"{data_label}")
        ax.legend()
        ax.grid(True)

    plt.show()

def display_data(city, data, months, data_label):
    city_data = data.loc[city, months]
    min_value = city_data.min()
    max_value = city_data.max()
    avg_value = city_data.mean()
    min_month = city_data.idxmin()
    max_month = city_data.idxmax()

    table_data = [months, city_data]

    print(f"{data_label}:")
    print(tabulate(table_data, tablefmt="grid"))
    print(f"Minimum occurs in {min_month.capitalize()}: {min_value:.1f}")
    print(f"Maximum occurs in {max_month.capitalize()}: {max_value:.1f}")
    print(f"Average value: {avg_value:.2f}\n")

    result = f"{data_label}:\n"
    result += f'{tabulate(table_data, tablefmt="grid")}\n'
    result += f"Minimum occurs in {min_month.capitalize()}: {min_value:.1f}\n"
    result += f"Maximum occurs in {max_month.capitalize()}: {max_value:.1f}\n"
    result += f"Average value: {avg_value:.2f}\n"
    result += "-" * 50 + "\n"
    
    return result

def convert_month(month):
    match month:
        case 'jan':
            return 'January'
        case 'feb':
            return 'February'
        case 'mar':
            return 'March'
        case 'apr':
            return 'April'
        case 'may':
            return 'May'
        case 'jun':
            return 'June'
        case 'jul':
            return 'July'
        case 'aug':
            return 'August'
        case 'sep':
            return 'September'
        case 'oct':
            return 'October'
        case 'nov':
            return 'November'
        case 'dec':
            return 'December'
        case _:
            return month.capitalize()

def save_results(results):
    while True:
        save_choice = input("Do you want to save these results in a file (enter 'yes' or 'no')? ").lower().strip() 
        if save_choice in ['yes', 'no']:
            if save_choice == 'yes':
                file_path = input("Enter the file path: ").strip()
                real_path = f'./storage/{file_path}'
                if path.exists(real_path):
                    while True:
                        update_choice = input("This file exists. Do you want to update this file (enter 'yes' or 'no')? ").lower().strip()
                        if update_choice in ['yes', 'no']:
                            if update_choice == 'yes':
                                with open(real_path, 'a') as file:
                                    file.write(results)
                                    print("File updated successfully.")
                            else:
                                with open(real_path, 'w') as file:
                                    file.write(results)
                                    print("File overwritten successfully.")
                                    break
                        else:
                            print("Invalid choice. Please enter 'yes' or 'no'.")
                else:
                    with open(real_path, 'w') as file:
                        file.write(results)
                        print("File created successfully.")
            break
        else:
            print("Invalid choice. Please enter 'yes' or 'no'.") 

def sort_months(months):
    month_order = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4, 'May': 5, 'June': 6,
        'July': 7, 'August': 8, 'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    return sorted(months, key=lambda x: month_order[x])

def vaildate_input(data_chosen, label):
    match label:
        case 'city':
            temp_data = read_data('temperature')
            valid_cities = temp_data.index.str.lower().tolist()

            cities_display = []
            for city in data_chosen.split():
                if city not in valid_cities:
                    print(f"{city} is not a legal value (ignored)")
                else:
                    cities_display.append(city)

            return cities_display
        case 'data_type':
            data_types = ['temp', 'rain', 'sun']
            data_display = []
            if data_chosen == 'all' or 'all' in data_chosen:
                data_display = data_types
            else:
                for dt in data_chosen.split():
                    if dt not in data_types:
                        print(f"{dt} is not a legal value (ignored)")
                    else:
                        data_display.append(dt)

            return data_display
        case 'months':
            months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
            months_full = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']
            months_display = []
            if data_chosen == 'all' or 'all' in data_chosen:
                months_display = months_full
            else:
                for month in data_chosen.split():
                    if month not in months and month.capitalize() not in months_full:
                        print(f"{month} is not a legal value (ignored)")
                    else:
                        if len(month) == 3:
                            month = convert_month(month)
                        months_display.append(month)
            months_display = sort_months(months_display)
            
            return months_display

def main():
    temp_data = read_data('temperature')
    rainfall_data = read_data('rainfall')
    sunshine_data = read_data('sunshine')

    data_type_map = {
        'temp': 'Temperature',
        'rain': 'Rainfall',
        'sun': 'Sunshine hours'
    }

    data_map = {
        'temp': temp_data,
        'rain': rainfall_data,
        'sun': sunshine_data
    }

    while True:
        print("Welcome to CLIP, the CLImate Plotter")
        print("loading the data... done!", end="\n")

        cities_chosen = input("choose the cities: ").lower().strip()
        data_chosen = input("choose the data: temp(erature) rain(fall) sun(shine hours) OR all: ").lower().strip()
        months_chosen = input("choose the months: jan(uary) feb(ruary) mar(ch) apr(il) may jun(e) jul(y) aug(ust) sep(tember) oct(ober) nov(ember) dec(ember) OR all: ").lower().strip()

        cities_display = vaildate_input(cities_chosen, 'city')
        data_display = vaildate_input(data_chosen, 'data_type')
        months_display = vaildate_input(months_chosen, 'months')
        
        # display data on console
        results = ""
        for city in cities_display:
            print(f"\nData for {city.capitalize()}")
            results += f"Data for {city.capitalize()}:\n"
            for data_type in data_display:
                if data_type == 'temp':
                    results += display_data(city, temp_data, months_display, "Temperature")
                elif data_type == 'rain':
                    results += display_data(city, rainfall_data, months_display, "Rainfall")
                elif data_type == 'sun':
                    results += display_data(city, sunshine_data, months_display, "Sunshine hours")
            results += "\n"

        # plot data
        if len(cities_display) > 0 and len(data_display) > 0:
            selected_data_map = {data_type_map[data]: data_map[data] for data in data_display}
            plot_data(cities_display, selected_data_map, months_display)

        # save results
        save_results(results)

        # continue?
        while True:
            is_continue = input("Do you want to continue (enter 'yes' or 'no')? ").lower().strip()
            if is_continue in ['yes', 'no']:
                if is_continue == 'no':
                    return
                else:
                    break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.")
        
if __name__ == "__main__":
    main()
