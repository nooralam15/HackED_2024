#Main code for the Earthwork Cost and Bid Estimation

#Import main library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def load_soil_data_from_csv(file_path):
    # loads soil data from a csv file 
    try:
        soil_data = pd.read_csv(file_path)
        return soil_data.values
        # convert DataFrame to NumPy Array
    except FileNotFoundError:
        print("")
        print("Error: No soil data file was submitted.")
        print("")
        return np.array([])
    
#This function will create a menu that will loop through the code
def menu():
    print("Welcome to Earth 2 Build, a premium cost and biddding estimation tool for Engineering EarthWork")
    userInput = input("Please Pick a Number from the Menu: \n 1. Upload Elevation Data \n 2. Estimate Excavation Cost \n 3. Plot Soil Profile \n 0. Quit Program ")

    return userInput

def main():
    #load soil data from CSV file
    soil_data = load_soil_data_from_csv("soil_data.csv")

    #display information about the soil data
    #display_soil_info()

    choice = menu()
    while choice != 0:
        if choice == 1:
            display_soil_info(soil_data)
        elif choice == 2:
            estimate_excavation_cost(soil_data)
        elif choice == 3:
            plot_soil_profile(soil_data)

main()




