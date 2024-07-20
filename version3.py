import pandas as pd
from tabulate import tabulate
import os.path
from os import path
import matplotlib.pyplot as plt 

def read_data():
    months = ['January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December']
    
    temp_data = pd.read_csv('./resources/temperature.csv', index_col=0, names=months)
    rainfall_data = pd.read_csv('./resources/rainfall.csv', index_col=0, names=months)
    sunshine_data = pd.read_csv('./resources/sunshine.csv', index_col=0, names=months)

    return temp_data, rainfall_data, sunshine_data

def plot_data(city, data, months, data_label):
    plt.plot(months, data, c='green')
    plt.title(data_label)
    plt.legend([city.capitalize()])
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
    
    return result, city_data

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

def main():
    while True:
        print("Welcome to CLIP,  the CLImate Plotter")
        print("loading the data...", end="\n")

        temp_data, rainfall_data, sunshine_data = read_data()

        print("done!")

        valid_cities = temp_data.index.str.lower().tolist()

        data_types = ['temp', 'rain', 'sun']
        
        months = ['jan', 'feb', 'mar', 'apr', 'may', 'jun',
                'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        months_full = ['January', 'February', 'March', 'April', 'May', 'June',
                'July', 'August', 'September', 'October', 'November', 'December']

        cities_chosen = input("choose the cities: ").lower().strip()
        data_chosen = input("choose the data: temp(erature) rain(fall) sun(shine hours) OR all: ").lower().strip()
        months_chosen = input("choose the months: jan(uary) feb(ruary) mar(ch) may jun(e) jul(y) aug(ust) sep(tember) oct(ober) nov(ember) dec(ember) OR all: ").lower().strip()

        cities_display = []
        for city in cities_chosen.split():
            if city not in valid_cities:
                print(f"{city} is not a legal value (ignored)")
            else:
                cities_display.append(city)
        
        data_display = []
        if data_chosen == 'all' or 'all' in data_chosen:
            data_display = data_types
        else:
            for dt in data_chosen.split():
                if dt not in data_types:
                    print(f"{dt} is not a legal value (ignored)")
                else:
                    data_display.append(dt)
        
        months_display = []
        if months_chosen == 'all' or 'all' in months_chosen:
            months_display = months_full
        else:
            for month in months_chosen.split():
                if month not in months and month.capitalize() not in months_full:
                    print(f"{month} is not a legal value (ignored)")
                else:
                    if len(month) == 3:
                        month = convert_month(month)
                    months_display.append(month)

        results = ""
        for city in cities_display:
            print(f"\nData for {city.capitalize()}")
            city_label = f"Data for {city.capitalize()}:\n"
            for data_type in data_display:
                if data_type == 'temp':
                    result, city_data = display_data(city, temp_data, months_display, "Temperature")
                    plot_data(city, city_data, months_display, "Temperature")
                elif data_type == 'rain':
                    result, city_data = display_data(city, rainfall_data, months_display, "Rainfall")
                    plot_data(city, city_data, months_display, "Rainfall")
                elif data_type == 'sun':
                    result, city_data = display_data(city, sunshine_data, months_display, "Sunshine hours")
                    plot_data(city, city_data, months_display, "Sunshine hours")

            results += f"{city_label}\n{result}\n"

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
                                        file.write(result)
                                        print("File updated successfully.")
                                else:
                                    with open(real_path, 'w') as file:
                                        file.write(result)
                                        print("File overwritten successfully.")
                                break
                            else:
                                print("Invalid choice. Please enter 'yes' or 'no'.")
                    else:
                        with open(real_path, 'w') as file:
                            file.write(result)
                            print("File created successfully.")
                break
            else:
                print("Invalid choice. Please enter 'yes' or 'no'.") 

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
