#Main code for the Earthwork Cost and Bid Estimation

#Import main library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

def main():
    #load soil data from CSV file
    soil_data = load_soil_data_from_csv("soil_data.csv")

    #display information about the soil data
    #display_soil_info()

    userInput = menu()
    while userInput != 0:
        if userInput == 1:
            display_soil_info(soil_data)
        elif userInput == 2:
            estimate_excavation_cost(soil_data)
        elif userInput == 3:
            plot_soil_profile(soil_data)

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
    print("")
    print("0. Exit Program")
    print("1. Display Soil Data")
    print("2. Estimate excavation cost")
    print("3. Plot Soil Profile")
    print()
    
    userInput = int(input("userInput (0-3)?"))
    while not (0 <= userInput <=3):
        userInput = int(input("userInput (0-3)?"))
    return userInput

def display_soil_data(soil_data):
    print("")
    print("SOIL DATA: ")
    print("Northing Easting Elevation(m)")
    for row  in soil_data:
        print("%-3d %=14s")

main()




