"""
Starter code: Fetch covid cases data for Utah from the CDC API

Dataset:
Weekly United States COVID-19 Cases by State (ARCHIVED)

IMPORTANT:
- This dataset is WEEKLY, not daily.  The day shown is the end of week date.
- This starter code prints RAW JSON text.
- You are expected to parse and analyze the data.
"""
import json
import requests
from datetime import datetime
from collections import defaultdict

DATASET_ID = "pwn4-m3yp"
BASE_URL = f"https://data.cdc.gov/resource/{DATASET_ID}.json"




key_new = "new_cases"
key_date = "date_updated"

State_Populations = {}
f = open('states.csv', 'r')
for line in f:
    parts = line.strip().split(',')
    state = parts[0]
    population = int(parts[1])
    State_Populations[state] = population
f.close()



results_final = []

def state_data(state):
    population = State_Populations[state]
    
    # FETCH DATA FOR THIS SPECIFIC STATE
    params = {
        "$where": f"state='{state}' AND end_date >= '2020-01-01' AND end_date <= '2023-12-31'",
        "$order": "end_date ASC"
    }
    req = requests.get(BASE_URL, params=params)
    lst = json.loads(req.text)
    
    # Now continue with the rest of your code...
    json_file = open(f"{state}.json", 'w')
    json.dump(lst, json_file, indent=2)
    json_file.close()


        #calculate the average weekly cases and stuff

    total = 0
    for chungus in lst:
        total += int(float(chungus['new_cases']))
    average = total / len(lst)

    #find the highest particular week type stuff 
    max_cases = 0
    max_date = ""
    for chungus in lst:
        cases = int(float(chungus['new_cases']))
        if cases > max_cases:
            max_cases = cases
            #cut it off at 10 because of all the dumb T---000-00-0-00-00-0-
            max_date = chungus['end_date'][:10]

    #group by month and then find the highest month cause you know 
    months = {}
    for chungus in lst:
        end_date = chungus['end_date']
        year = end_date[:4]
        month = end_date[5:7]
        month_key = year + "-" + month

        cases = int(float(chungus['new_cases']))
        if month_key in months:
            months[month_key] += cases
        else:
            months[month_key] = cases
        
    #find the month with the most cases whatattt whattt
    most_month_key = ""
    most_month_cases = 0
    for month_key in months:
        if months[month_key] > most_month_cases:
            most_month_cases = months[month_key]
            most_month_key = month_key
    
    #make the months have names cause thats what he did in his result
    month_names = ["January", "February", "March", "April", "May", "June", "July", 
    "August", "September", "October", "November", "December"]
    year = most_month_key[:4]
    month_num = int(most_month_key[5:7])
    month_display = month_names[month_num - 1] + " " + year

    #calculate percentage
    percentage = (most_month_cases / population) * 100

    #print results for this state
    print(f"State name: {state}")
    print(f"Average number of new weekly cases: {average:.2f}")
    print(f"Date with the highest amount of new cases: {month_display} ({most_month_cases})")
    print(f"Date with the highest amonut of new cases as a percentage of popoulation: {percentage:.2f}% (Population: {population})")

    results_final.append({
        'state' : state,
        'percentage': percentage,
        'month' : month_display,
        'cases' : most_month_cases,
        'population' : population
    })

#do every state 
for state in State_Populations:
    state_data(state)

    #find highest and lowest percentages in the data burh
highest = results_final[0]
lowest = results_final[0]
for chungus in results_final:
    if chungus['percentage'] > highest['percentage']:
        highest = chungus
    if chungus['percentage'] < lowest['percentage']:
        lowest = chungus    

#print the final highest percents and thel ikes and make it look cool like his

print("-" * 60)
print("SUMMARY ACROSS ALL STATES".center(60,'='))
print(f"State with the Highest percentage of population in its highest month: {highest['state']} - {highest['percentage']:.2f}% in {highest['month']} ({highest['cases']}) cases: Population: {highest['population']}")
print(f"State with the lowest percentage of population in its highest month: {lowest['state']} - {lowest['percentage']:.2f}% in {lowest['month']} ({lowest['cases']}) cases: Population: {lowest['population']}")