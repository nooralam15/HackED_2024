import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def main():
    #load soil data from CSV file
    soil_data = load_soil_data_from_csv("soil_data.csv")

    #display information about the soil data
    display_soil_info()

    choice = menu()

    while choice != 0:
        if choice == 1:
            display_soil_info(soil_data)
        elif choice == 2:
            estimate_excavation_cost(soil_data)
        elif choice == 3:
            plot_soil_profile(soil_data)

        choice = menu()