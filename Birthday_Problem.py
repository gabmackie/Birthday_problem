"""
For explanations of the birthday problem, please see https://en.wikipedia.org/wiki/Birthday_problem
or a video from numberphile https://www.youtube.com/watch?v=a2ey9a70yY0
"""
import decimal as dec
from math import factorial
import numpy as np
import matplotlib.pyplot as plt
from random import randint

# Define how many decimal points you want to be working with. Otherwise python rounds and it's annoying
dec.getcontext().prec = 100


def calculation(group, days):
    # To find the change that at least 2 people share a birthday, we first calculate the chance that no pairs share a birthday
    
    # First, if the group is larger than the days, the chance of no matches is 0
    if group > days:
        chance_no_matches = 0
        
    # Otherwise we perform the actual calculation. In this condensed form
    # It is as accurate as the extended calculation to 100sf when I coded them both and compared them,
    # and they likely only differ because of rounding at different points of the calculation
    else:
        chance_no_matches = factorial(days-1)/(factorial(days-group)*(days**(group-1)))
    
    
    # We then take the reverse probability to get the one we want
    chance_match = 1-chance_no_matches
    
    # Convert to a regular percentage by multiplying by 100
    match_percent = chance_match*100
    
    
    # Here we want to print the result sensibly, to an appropriate number of decimal places
    # we don't need to show the same number of significant figures for 99.9985% as we do for 99.999999927%
    # This gives us a counter who's value is the number of decimals that equal 9, plus 2
    # We start by setting our counter to 2 decimal places
    counter = 2
    
    # We convert the odds to a string to work with
    decimals = str(chance_match)
    
    # We then run a loop as many times as we have decimal places
    for digit in range(len(decimals)):
        # If the digit at that point is a 9, we move our counter 1 along
        if decimals[digit] == '9':
            counter += 1
        
        # Once we get to a non-9 digit, we end the loop
        else:
            break
    
    # We print the results nicely
    print(f'The probablility that at least 2 people out of a group of {group} share a birthday is {match_percent:.{counter}f}%')
    
    # We also want to show it in scientific notation
    # Here it is easier to show it as 1 minus the likelihood of no pairs sharing a birthday
    # First we convert the probability to percentage
    convert_to_percent = chance_no_matches*100
    #Then we convert it to scientific notation
    scientific = '{:.2e}'.format(convert_to_percent)
    # Then we print it
    print(f'In scientific notation this is (100 - {scientific})%')
    
    return(match_percent)


# A function to run our simple simulation (two or more matches)
def simulation(group, total, trials, simple, exact, match):
    
    # Create holding variables, for the match/no match outcomes, and the rate as it changes
    match_outcomes = []
    match_rate = []
    
    # We now run our simulation for the preset number of trials
    for x in range(trials):
        # Create an empty list for the birthdays
        birthdays = []
        
        # We need to pick a birthday for each person in our group
        for i in range(int(group)):
            # We pick a random day of the year to be out birthday
            random_birthday = randint(1, total)
            # We then append it to our list of birthdays
            birthdays.append(random_birthday)
        
        # If it's the simple simulation (2 or more) then we run that function
        # There are two functions because the simple one is less computationally demanding (I think),
        # so if we can get away with doing less we will
        if simple:
            matches = simple_sim(birthdays)
        
            # If there aren't matches, set hit to 0
            if matches == 0:
                hit = 0
            # If there are, set it to 100. This allows us to easily calculate percentage
            else:
                hit = 100        
        
        # If it isn't the simple simulation, we run the more complex function
        else:
            hit = complex_sim(birthdays, match, exact)
            
        
        # Add hit to our outcomes list
        match_outcomes.append(hit)
        # Convert it to a numpy array
        match_array = np.array(match_outcomes)
        # Calculate the average match rate and add that to our rate list
        match_rate.append(match_array.mean())
    
    text = f'{match}'
    if exact:
        text = 'exactly ' + text
    else:
        text = text + ' or more'
    
    # Print the results of our simulation
    print(f'The probability of a group of size {group} having {text} matches over 1000 trials is {match_array.mean()}%')

    return(match_rate)


# The function to run our simple simulation (2 or more)
def simple_sim(birthdays):
    # Here we convert our birthdays to a set, which keeps only unique values
    unique_birthdays = set(birthdays)
    
    # We compare the length of the birthdays and unique birthdays lists
    matches = len(birthdays) - len(unique_birthdays)
    
    return(matches)


# The function to run our complex simulation (not 2 or more)
def complex_sim(birthdays, match, exact):
    
    # Here we hold the number of matches in a dictionary
    match_count = {}
    # Set hit to 0 so if we find no matches it's set properly
    hit = 0
    
    # We run through the birthdays list
    for day in birthdays:
        # For each day, we check how many times that day occurs
        count = birthdays.count(day)
        
        # If the day is in our counting dict, do nothing
        if day in match_count:
            continue
        
        # If it isn't, add it to the dict with the count as the value
        else:
            match_count[day] = count
    
    # Run through the dict, extracting the values as well as the keywords
    for k, v in match_count.items():
        
        if exact:
            # If we want an exact match, that's what we look for
            if v == match:
                # If we get it, hit is set to 100
                hit = 100
        else:
            # If we don't need an exact match, we compare to match or more
            if v >= match:
                hit = 100
                
    return(hit)
            

# Our function to draw a graph of the match rate
def draw_graph(match_rate, simple, match_percent):
    # Set plot style to something nice
    plt.style.use("ggplot")
    
    # Make a figure and plot the win rate
    plt.figure()
    plt.plot(match_rate)
    
    # We can only do this if it's a simple
    if simple:
        # Add a straight line for the actual, calculated percentage
        plt.hlines(y=match_percent, xmin=0, xmax=trials, color = 'blue')
    
    # Label the axes
    plt.xlabel("Number of trials")
    plt.ylabel("Percent of trials with a match")




# Define the size of the group you want
group = dec.Decimal(23)
# Define our days
days = dec.Decimal(365)
# Define how many matches we want
match = 2

# Do we want to run a simulation?
sim = True
# How many trials do we want to run
trials = 1000
# Do we want an exact match (compared to match or greater)
exact = True
# Do we want a graph of our simulation
graph = True


# Now we determine which functions we have to run
if match == 2 and not exact:
    # Here we run the precise calculation
    match_percent = calculation(group, days)
    # And set it so our simulation knows its a simple calculation
    simple = True
else:
    # Otherwise, we set our values to false for use in future functions
    match_percent = False
    simple = False

# If we wanted the simulation, then we run that function
if sim:
    match_rate = simulation(group, days, trials, simple, exact, match)

# If we wanted the graph, then we run that function
if graph:
    draw_graph(match_rate, simple, match_percent)



