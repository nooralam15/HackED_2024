#Main code for the Earthwork Cost and Bid Estimation

#Import main library
from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from keys import *
import matplotlib.image as mpimg
from tabulate import tabulate

client = OpenAI(api_key = chatGPT_Key)

def main():
    #load soil data from CSV file
    soil_data = load_soil_data_from_csv("soil_data.csv")

# Display loading image
    display_image("earth2build.png")

    print("\n\nWelcome to Earth-2-Build, a premium cost and bidding estimation tool for Civil Engineering Earthwork! \n")
    userInput = menu()

    while userInput != 0:
        if userInput == 1:
            soil_data_limit(soil_data)
        elif userInput == 2:
            display_soil_data(soil_data)
        elif userInput == 3:
            estimate_excavation_cost(soil_data)
        elif userInput == 4:
            plot_soil_profile(soil_data)
        userInput = menu()

# Add this function to display the image
def display_image(image_path):
    img = mpimg.imread(image_path)
    imgplot = plt.imshow(img)
    plt.axis('off')  # Turn off axis labels and ticks
    plt.show()

#This function initializes the csv file for later use in future functions
def load_soil_data_from_csv(file_path):
    # loads soil data from a csv file 
    try:
        soil_data = pd.read_csv(file_path)
        return soil_data.values.tolist()  # Convert DataFrame to Python list
    except FileNotFoundError:
        print("\nError: No soil data file was submitted.")
        return np.array([])

#This function will create a menu that will loop through the code
def menu():
    print("\nMAIN MENU")
    print("0. Exit Program")
    print("1. Maximum Elevation Limit")
    print("2. Updated Soil Data")
    print("3. Estimate Excavation Cost")
    print("4. Plot Updated Soil Profile")
    print()
    
    userInput = int(input("\nuserInput (0-4)? "))
    while not (0 <= userInput <=4):
        userInput = int(input("\nuserInput (0-4)? "))
    return userInput

#This function limits the csv soil data to fit the user criteria
def soil_data_limit(soil_data):
    min_elevation, max_elevation = soil_data_min_max(soil_data)
    print("\nMinimum Elevation:", min_elevation)
    print("Maximum Elevation:", max_elevation)

    # Handle input for the limit value with proper error checking
    valid=True
    while valid:
        limit_value_str = input("\nMaximum Elevation Limit? ")
        try:
            limit_value = float(limit_value_str)
            if min_elevation <= limit_value and limit_value <= max_elevation:
                valid = False  # Exit the loop if a valid float is entered within the range
            else:
                print("Invalid input. Maximum Elevation must be within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    p = 0
    while p < len(soil_data):
        if soil_data[p][2] > limit_value:  # Assuming the third column represents elevation
            del soil_data[p]
        else:
            p = p + 1

    print("Soil data filtered based on Maximum Elevation Limit.")
    return soil_data


#This function returns the max and min values of the CSV file
def soil_data_min_max(soil_data):
    elevations = [entry[2] for entry in soil_data]  # Assuming the third column represents elevation
    min_elevation = min(elevations)
    max_elevation = max(elevations)
    return min_elevation, max_elevation


#This function displays the soil data to the user
def display_soil_data(soil_data):
    print("")
    print("SOIL DATA:")
    print("%-9.9s  %-9.9s  %-15.15s" % ("Northing", "Easting", "Elevation(m)"))
    
    #Seperates data points into Northing, Easting, and Elevations
    for k in range(0, len(soil_data)):
        northing = soil_data[k][0]
        easting = soil_data[k][1]
        elevation = soil_data[k][2]
        
        print("%-9.1f  %-9.1f  %-15.1f" % (northing, easting, elevation))

# calculates the cut and fill needed for earthwork
def estimate_excavation_cost(soil_data):
    # Get user input for elevation values
    min_elevation, max_elevation = soil_data_min_max(soil_data)
    print("\nMin Elevation:", min_elevation)
    print("Max Elevation:", max_elevation)

    while True:
        try:
            base_elevation = float(input("\nEnter Base Foundation Elevation(m): "))
            if min_elevation <= base_elevation <= max_elevation:
                break
            else:
                print("Invalid input. Elevation must be within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")
    
    # Conversion factor: Assuming each data point represents a square meter
    conversion_factor = 1.2

    # Next 2 while loops obtains information regarding footing and slab volume
    while True:
        units_from_revit = input("\nAre Footing Volume units from Revit in Yards? (y/n): ").lower()
        if units_from_revit == 'y':
            try:
                CuY_to_CuM = float(input("Enter Footing Volume: "))
                if 0 <= CuY_to_CuM:
                    print("Converting units from Yards to Meters...")
                    CuY_to_CuM_conversion = 0.764555
                    footing_volume = CuY_to_CuM * CuY_to_CuM_conversion
                    print(f"Conversion complete! Footing Volume in Cu. M is: {footing_volume:.2f} Cu. M")
                    break
                else:
                    print("Invalid input. Volume must be non-negative.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif units_from_revit == 'n':
            try:
                footing_volume = float(input("\nEnter Footing Volume (Cu. M): "))
                if 0 <= footing_volume:
                    break
                else:
                    print("Invalid input. Volume must be non-negative.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")
    
    while True:
        units_from_revit = input("\nAre Slab Volume units from Revit in Yards? (y/n): ").lower()
        if units_from_revit == 'y':
            try:
                CuY_to_CuM = float(input("Enter Slab Volume: "))
                if 0 <= CuY_to_CuM:
                    print("Converting units from Yards to Meters...")
                    CuY_to_CuM_conversion = 0.764555
                    slab_volume = CuY_to_CuM * CuY_to_CuM_conversion
                    print(f"Conversion complete! Slab Volume in Cu. M is: {slab_volume:.2f} Cu. M")
                    break
                else:
                    print("Invalid input. Volume must be non-negative.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        elif units_from_revit == 'n':
            try:
                slab_volume = float(input("\nEnter Slab Volume (Cu. M): "))
                if 0 <= slab_volume:
                    break
                else:
                    print("Invalid input. Volume must be non-negative.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

    # Calculate cut and fill volumes
    cut_volume = 0
    fill_volume = 0

    new_fill_volume = fill_volume  # Initialize new_fill_volume

    for entry in soil_data:
        elevation = entry[2]  # Assuming the third column represents elevation
        if elevation < base_elevation:
            fill_volume += (base_elevation - elevation) * conversion_factor
        elif elevation > base_elevation:
            cut_volume += (elevation - base_elevation) * conversion_factor

    # Check if fill_volume is less than cut_volume and set fill_volume to 0
    if fill_volume < cut_volume:
        new_fill_volume = 0
        
    # Calculate final volumes
    total_cut_volume = cut_volume
    total_fill_volume = max((new_fill_volume - (footing_volume + slab_volume)), 0)

    # Print results as a table
    results_table = [
        ["Total Volumes for Project", "", ""],
        ["Cut Soil Volumes", f"{total_cut_volume:.2f} Cu.M"],
        ["Fill Soil Volumes", f"{total_fill_volume:.2f} Cu.M"],
        ["Soil that can be Reused", f"{fill_volume:.2f} Cu.M"]
    ]
    # Specify numalign to center align numerical values
    print("")
    print(tabulate(results_table, headers="firstrow", tablefmt="grid", numalign="center"))
    
    #Processing Cost estimation using chatGPT
    gpt(total_cut_volume, total_fill_volume)


def gpt(cut_volume, fill_volume):
    location = input("Please provide location of project: ")
    time_of_year = input("Please provide the time of year (Month/Season/All year) of project:  ")
    project_length = input("Please provide an estimated project time length (hours/days/months/week): ")
    response = client.chat.completions.create(
model = "gpt-3.5-turbo",
temperature = 0.2,
max_tokens = 1000,
messages = [
    {"role": "system", "content": "Assume that you are a construction company that has been assigned with the task of cutting and filling soil. Your job is to provide an estimate for the construction costs. We are cutting soil of" + str(cut_volume) + "cubic meters and that we are filling" + str(fill_volume) + ". Also, the project will takr place in" + location + " and will occur during" + time_of_year + " and will take" + project_length + "I want you to provide a construction cost estimate for the project and please provide a raw number. Make sure you include everything, from labour costs, equipment rentals (Dump trucks,) etc. Use an estimated cost based on average rates in the location provided. Give us an actual number based on average data. Nothing specific"}
    ]
    )

    edit_Response = response.choices[0].message.content
    
    response = client.chat.completions.create(
model = "gpt-3.5-turbo",
temperature = 0.2,
max_tokens = 1000,
messages = [
    {"role": "user", "content": "I want you to take the response given in" + edit_Response + "And I only want you to extract the numbers. Do NOT explain anything. Just provide a short header, and the costs in an organized table." }
    ]
    )
    print("")
    print(response.choices[0].message.content)

# This function will plot the csv soil data as a contour map
def plot_soil_profile(data):
    # Seperates data points into Northing, Easting, and Elevations
    northing, easting, elevation = [], [], []
    for k in range(0, len(data)):
        northing.append(data[k][0])
        easting.append(data[k][1])
        elevation.append(data[k][2])

    # Creating a contour plot
    plt.figure(figsize=(8, 6))
    contour_plot = plt.tricontourf(northing, easting, elevation, levels=20, cmap='viridis')
    plt.colorbar(contour_plot, label='Elevation')  # Add a colourbar for reference
    plt.xlabel('Northing')
    plt.ylabel('Easting')
    plt.title('2D Contour Map')
    plt.grid(True)
    plt.show()

main()