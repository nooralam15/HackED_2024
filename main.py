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
        if userInput ==1:
            soil_data_limit(soil_data)
        elif userInput == 2:
            display_soil_data(soil_data)
        elif userInput == 3:
            estimate_excavation_cost(soil_data)
        elif userInput == 4:
            plot_soil_profile(soil_data)

#This function initializes the csv file for later use in future functions
def load_soil_data_from_csv(file_path):
    # loads soil data from a csv file 
    try:
        soil_data = pd.read_csv(file_path)
        return soil_data.values.tolist()  # Convert DataFrame to Python list
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
    print("1. Select Elevations for Excavation")
    print("2. Selected Soil Data")
    print("3. Estimate Excavation Cost")
    print("4. Plot Soil Profile")
    print()
    
    userInput = int(input("userInput (0-3)? "))
    while not (0 <= userInput <=3):
        userInput = int(input("userInput (0-3)? "))
    return userInput

#This function will display the soil data points from the csv file
def soil_data_limit(soil_data):
    min_elevation, max_elevation = soil_data_min_max(soil_data)
    print("Min Elevation:", min_elevation)
    print("Max Elevation:", max_elevation)
    limit_value = float(input("Limit Value? "))
    
    while not (min_elevation <= limit_value <= max_elevation):
        limit_value = float(input("Limit Value? "))
    
    p = 1
    while p < len(soil_data):
        if soil_data[p][2] > limit_value:  # Assuming the third column represents elevation
            del soil_data[p]
        else:
            p += 1

def soil_data_min_max(soil_data):
    elevations = [entry[2] for entry in soil_data]  # Assuming the third column represents elevation
    min_elevation = min(elevations)
    max_elevation = max(elevations)
    return min_elevation, max_elevation    

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

    # Creating a meshgrid for the contour plot
    x = np.array(northing)
    y = np.array(easting)
    X, Y = np.meshgrid(x, y)
    Z = np.array(elevation).reshape(len(y), len(x))

    # Plotting the contour map
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')

    ax.contour3D(X, Y, Z, 50, cmap='viridis')  # Adjust the number of contours as needed
    ax.set_xlabel('Northing')
    ax.set_ylabel('Easting')
    ax.set_zlabel('Elevation')
    ax.set_title('Contour Map')

    plt.show()

main()




