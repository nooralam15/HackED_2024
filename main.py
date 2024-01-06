#Main code for the Earthwork Cost and Bid Estimation

#Import main library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D

def main():
    #load soil data from CSV file
    soil_data = load_soil_data_from_csv("soil_data.csv")

    #display information about the soil data
    #display_soil_info()

    userInput = menu()

    while userInput != 0:
        if userInput == 1:
            display_soil_data(soil_data)
        elif userInput == 2:
            estimate_excavation_cost(soil_data)
        elif userInput == 3:
            plot_soil_profile(soil_data)

#This function initializes the csv file for later use in future functions
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
    
    userInput = int(input("userInput (0-3)? "))
    while not (0 <= userInput <=3):
        userInput = int(input("userInput (0-3)? "))
    return userInput

#This function will display the soil data points from the csv file
def display_soil_data(soil_data):
    print("")
    print("SOIL DATA:")
    print("%-9.9s  %-9.9s  %-15.15s" % ("Northing", "Easting", "Elevation(m)"))
    
    #Seperates data points into Northing, Easting, and Elevations
    for k in range(0, len(soil_data)):
        northing = soil_data[k][0]
        easting = soil_data[k][1]
        elevation = soil_data[k][2]
        
        print("%-7.1d  %-7.1d  %-6d" % (northing, easting, elevation))

#This function will plot the csv soil data as a contour map
def plot_soil_profile(data):
    #Seperates data points into Northing, Easting, and Elevations
    for k in range(0, len(data)):
        northing = data[k][0]
        easting = data[k][1]
        elevation = data[k][2]
    
    X, Y = np.meshgrid(northing, easting)
    Z = np.array(elevation).reshape(len(y), len(x))

    X = northing.unique()
    Y = easting.unique()
    Z = elevation.values.reshape(len(X), len(Y)).T

    plt.figure(figsize=(8, 6))
    contour_plot = plt.tricontourf(X, Y, Z, levels=20, cmap='viridis')
    plt.colorbar(contour_plot, label='Elevation')  # Add a colorbar for reference
    plt.xlabel('Northing')
    plt.ylabel('Easting')
    plt.title('2D Contour Map')
    plt.grid(True)
    plt.show()

main()




