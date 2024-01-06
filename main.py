#Main code for the Earthwork Cost and Bid Estimation

#Import main library
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt 

#This function will create a menu that will loop through the code
def menu():

def main():
    #load soil data from CSV file
    soil_data = load_soil_data_from_csv("soil_data.csv")

    #display information about the soil data
    display_soil_info()

    choice = menu()

main()