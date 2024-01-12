#Main code for the Earthwork Cost and Bid Estimation

#Import main library
from openai import OpenAI
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 
from keys import *
import matplotlib.image as mpimg
from tabulate import tabulate
import textwrap
import csv

client = OpenAI(api_key = chatGPT_Key)

print("\n***BACKGROUND DESCRIPTION OF MAIN MENU***")
menu_description = """
The program's main menu presents users with a range of options tailored for effective navigation and utilization. 
The menu is structured to facilitate various tasks related to Civil Engineering Earthwork. By selecting option 0, 
users can exit the program when their tasks are complete. By selecting option 1, users can set a maximum elevation 
limit, providing flexibility in analyzing and constraining soil data. By selecting option 2, users can visualize and 
comprehend the soil data, promoting a comprehensive understanding of the project's foundation. By selecting option 3, 
users can run the program's cost-estimating tool, a crucial aspect of project planning. Lastly, by selecting option 4, 
users can plot and save an updated soil profile, aiding in visualizing changes and updates in the geological composition. 
This well-organized and feature-rich main menu ensures that users can efficiently engage with the program, performing tasks 
ranging from data exploration to cost estimation with ease.
"""

# Set the desired width for formatting
width = 100

# Use textwrap to format the text
formatted_text = textwrap.fill(menu_description, width=width)

# Print the formatted text
print(formatted_text)

def main():
    # Load and display the image
    display_image("earth2build.png")

    print("\n\nWelcome to Earth-2-Build, a premium cost and bidding estimation tool for Civil Engineering Earthwork! \n")
    while True:
        # Get user input for soil data file
        soil_data_file_path = input("\nEnter the path to your soil data file (type: filename.csv): ")
        try:
            # Load soil data from user-provided CSV file
            soil_data = load_soil_data_from_csv(soil_data_file_path)
            if len(soil_data) > 0:  # Check if soil_data has elements
                break  # Break out of the loop if soil data is successfully loaded
            else:
                print("Error: Soil data file is empty. Please try again.")
        except FileNotFoundError:
            print("\nError: Soil data file not found at the specified path. Please try again.")
        except pd.errors.ParserError:
            print("\nError: Unable to parse the soil data file. Please make sure it is a valid CSV file.")
        except Exception as e:
            print(f"\nError: {str(e)} Please try again.")
    
    # Main loop with menu options
    while True:
        userInput = menu()
        if userInput == 0:
            print("Exiting program... Thanks for using Earth-2-Build!")
            break  # Exit the outer loop, ending the program
        elif userInput == 1:
            soil_data = soil_data_limit(soil_data)
        elif userInput == 2:
            estimate_excavation_cost(soil_data)
        elif userInput == 3:
            plot_soil_profile(soil_data)
        elif userInput == 4:
            # Restart the program
            print("Restarting the program...\n")
            soil_data = load_soil_data_from_csv(soil_data_file_path)

# Add this function to display the image
def display_image(image_path):
    img = mpimg.imread(image_path)
    imgplot = plt.imshow(img)
    plt.axis('off')  # Turn off axis labels and ticks
    plt.show()

#This function initializes the csv file for later use in future functions
def load_soil_data_from_csv(file_path):
    # loads soil data from a csv file 
    soil_data = pd.read_csv(file_path)
    return soil_data.values.tolist()

# This function will create a menu that will loop through the code
def menu():
    while True:
        print("\nMAIN MENU")
        print("0. Exit Program")
        print("1. Soil Data - Elevation Limit")
        print("2. Estimate Excavation Cost")
        print("3. Plot of Soil Profile - Excavation")
        print("4. Restart Program")
        print()

        # checks if the entered float value is between 0 and 4 (inclusive) and then checks if it's an integer using userInput.is_integer(). 
        # If both conditions are true, the float value is converted to an integer (int(userInput)) and returned from the function. If any of 
        # these conditions is false, an error message is printed, and the user is prompted again.

        try:
            userInput = float(input("\nuserInput (0-4)? "))
            if 0 <= userInput <= 4 and userInput.is_integer():
                return int(userInput)
            else:
                print("Invalid input. Please enter an integer between 0 and 4.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

# This function limits the csv soil data to fit the user criteria
def soil_data_limit(soil_data):
    min_elevation, max_elevation = soil_data_min_max(soil_data)
    print("\nSELECTED: MAXIMUM ELEVATION LIMIT")
    print("Minimum Elevation:", min_elevation)
    print("Maximum Elevation:", max_elevation)

    # Handle input for the limit value with proper error checking
    valid=True
    while valid:
        limit_value_str = input("\nMaximum Elevation Limit (m) OR type 'exit' to return to the main menu: ")
        if limit_value_str.lower() == 'exit':
            print("Returning to the MAIN MENU.")
            return soil_data  # Exit the function and return to the main menu
        try:
            limit_value = float(limit_value_str)
            if min_elevation <= limit_value and limit_value <= max_elevation:
                valid = False  # Exit the loop if a valid float is entered within the range
            else:
                print("Invalid input. Maximum Elevation must be within the range.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

    # Filter soil data based on Maximum Elevation Limit
    filtered_soil_data = [entry for entry in soil_data if entry[2] <= limit_value]

    # Ask the user if they want to save the filtered data to a CSV file
    save_to_csv = input("\nDo you want to save the filtered data to a CSV file? (y/n): ").lower()
    if save_to_csv == 'y':
        csv_filename = input("Enter the CSV file name (without extension): ")
        csv_filename += '.csv'
        save_soil_data_to_csv(filtered_soil_data, csv_filename)
        print(f"Filtered soil data saved to {csv_filename}")
    elif save_to_csv == 'n':
        print("Filtered soil data not saved to a CSV file.")

    print("Soil data filtered based on Maximum Elevation Limit.")
    return filtered_soil_data

# Helper function to save soil data to a CSV file
def save_soil_data_to_csv(soil_data, filename):
    with open(filename, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Northing", "Easting", "Elevation(m)"])
        csv_writer.writerows(soil_data)

#This function returns the max and min values of the CSV file
def soil_data_min_max(soil_data):
    elevations = [entry[2] for entry in soil_data]  # Assuming the third column represents elevation
    min_elevation = min(elevations)
    max_elevation = max(elevations)
    return min_elevation, max_elevation

# calculates the cut and fill needed for earthwork
def estimate_excavation_cost(soil_data):
    # Get user input for elevation values
    min_elevation, max_elevation = soil_data_min_max(soil_data)
    print("\nSELECTED: ESTIMATE EXCAVATION COST")
    print("Min Elevation:", min_elevation)
    print("Max Elevation:", max_elevation)

    while True:
        try:
            base_elevation_input = input("\nEnter Base Foundation Elevation (m) OR type 'exit' to return to the main menu: ")
            if base_elevation_input.lower() == 'exit':
                print("Returning to the main menu.")
                return
            base_elevation = float(base_elevation_input)
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

    # If fill_volume is greater than cut_volume, set new_fill_volume
    if fill_volume > cut_volume:
        new_fill_volume = fill_volume

    # Calculate final volumes
    total_cut_volume = cut_volume
    total_fill_volume = max((new_fill_volume - (footing_volume + slab_volume)), 0)
    soil_needed = max((fill_volume - cut_volume), 0)

    # Print results as a table
    results_table = [
        ["Total Volumes for Project", ""],
        ["Soil Cut Volumes", f"{total_cut_volume:.2f} Cu.M"],
        ["Soil Fill Volumes", f"{total_fill_volume:.2f} Cu.M"],
        ["Soil Needed", f"{soil_needed:.2f} Cu.M"]
    ]
    # Specify numalign to center align numerical values
    print("")
    print(tabulate(results_table, headers="firstrow", tablefmt="grid", numalign="center"))
    print("")

    #Processing Cost estimation using chatGPT
    gpt(total_cut_volume, total_fill_volume)


def gpt(cut_volume, fill_volume):
    print("\n **ESTIMATE COSTS BREAKDOWN**")
    location = input("\nPlease provide location of project (FORMAT: City, Province/State, Country): ")
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
    
    # First API call
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
    print("\nSELECTED: PLOT OF SOIL PROFILE - EXCAVATION")
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
    plt.xlabel('NORTHING')
    plt.ylabel('EASTING')
    plt.title('SOIL PROFILE - EXCAVATION - 2D CONTOUR MAP')
    plt.grid(True)
    plt.show()

main()