#!/usr/bin/env python
# coding: utf-8

# ## 2. Dataset Creation

# ### 2.2 Loading data

# In[4]:


import pandas as pd
import numpy as np
import time
import os


# In[5]:


#create preprocessing function to clean up raw data
def preprocess(db):
  #clean up header by removing whitespace
  db.columns = db.columns.str.strip()

  #split list of elements from transaction column by comma delimitation
  db['Transaction'] = db['Transaction'].str.split(',')

  #remove any whitespace in the elements from each transaction
  db['Transaction'] = db['Transaction'].apply(lambda x: [item.strip() for item in x])

  #create list of itens
  item_list = []
  for i in range(len(db['Transaction'])):
    for j in range(len(db['Transaction'][i])):
      if db['Transaction'][i][j] not in item_list:
        item_list.append(db['Transaction'][i][j])

  # #create list of transactions
  # transactions = []
  # for i in range(len(db['Transaction'])):
  #   transactions.append(db['Transaction'][i])

  return db, item_list



# ## 3. User Input

# Before we run the models we need to establish the values of support and confidence.
# 
# The support measures the frequency of an item or itemset occurs. It will measure the popularity of itemset in relation to the transactions. For example, we have total transactions of 10 and itens X and Z can be found together in 3 transactions. In this case the support is 3/10 = 30%
# 
# The confidence will provide how likelihood that the items purchased together. It will measure the correlation of the itens. For example, we have total transaction of 10 and the itens X and Z can found together in 3 transactions but item X can be found in a total of 5 transactions. The X->Z confidence in this case will be 3/5 = 60%
# 
# 
# In short, high support value improves reliability by filtering out rare patterns, while high confidence value improves prediction by filtering out unreliable associations.

# In[8]:


#list of retail store corresponding to index 0 to 4
all_retail_stores = ('amazon', 'kmart', 'bestbuy', 'nike', 'walmart')

print("Welcome to Apriori 2.0!")
print("Please select one of the following retail store (type corresponding number only):")
#print out number 1. and the first retail store from the list and so on
for i in range(len(all_retail_stores)):
  print(str(i + 1) + ". " + all_retail_stores[i])
print("6. Exit")

########################################
'''Input of the retail store number'''
########################################
user_input = input()



try:
    #make sure the input is a number
    retail_store_number = int(user_input)

    #check if user input is valid (int number between 1 to 5)
    if 1 <= retail_store_number <= 5:
      retail_store = all_retail_stores[retail_store_number - 1]
      print("You selected " + retail_store + "!")

      ########################################
      '''Input of the minimum support value'''
      ########################################
      #ask user to provide minimum support and store it
      print("Please enter the percentage of minimum support(values between 1 and 100)")
      try:
        min_support = int(input())
        if 1 <= min_support <= 100:
          print("Minimum support is " + str(min_support) + "%")

          #########################################################
          '''Input of the minimum confidence value'''
          #########################################################
          #ask user to provide minimum confidence and store it
          print("Please enter the percentage of minimum confidence(values between 1 and 100)")
          try:
            min_confidence = int(input())
            if 1 <= min_confidence <= 100:
              print("Minimum confidence is " + str(min_confidence) + "%")

            #error message if wrong number for confidence input
            else:
              print("Invalid Confidence value input. Please try again.")
              exit
          #error message if not a number for confidence input
          except ValueError:
            print("Invalid Confidence value input. Please try again.")
            exit
          #########################################################
          '''End of validation of the entered minimum confidence'''
          #########################################################


        #error message if wrong number for support input
        else:
          print("Invalid Support value input. Please try again.")
          exit
      #error message if not a number for support input
      except ValueError:
        print("Invalid Support value input. Please try again.")
        exit
      ########################################
      '''End of validation of the entered minimum support value'''
      ########################################


    #check if user wants to exit (number 6)
    elif int(user_input) == 6:
      print("Thank you for using Apriori 2.0!")
      exit

    #if the input is not a valid number it will come out an error message
    else:
      print("Invalid Retail store input. Please try again.")
      exit

#if the input is not a number it will come out an error message
except ValueError:
  print("Invalid Retail store input. Please try again.")
  exit

########################################
'''End of validation of the entered retail store number'''
########################################


#Load dataset selected
db_raw = pd.read_csv('Data/' + ( retail_store + '.csv'), encoding='cp1252') 
#Preprocess the data
database, item_list = preprocess(db_raw)

# print(item_list)
# print(database)


# ## 4. Brute Force Algorithm

# This algorithm will evaluate every possible combination of itens for the provided support and confidence values by the user. This algorithm takes more time to find all the itens combinations that equal or greater than the two metric parameters.
# 
# First step is to find all the possible unique combinations of the elements. As we create the combinations we will count how many transactions have that specific combination. The computed number is the frequency of the combination thru all the transactions. 
# 
# Itemset level is defined as the number of itens we are considering for the all possible combinations. For example, the itemset 1 has one only iten purchased, then itemset 2 has all the possible combinations of purchase of two itens.
# 
# We can stop the process when we get to an itemset level where all the combinations have frequency equals to zero because for sure the next level will not have any frequency as well.

# In[26]:


from itertools import combinations
from collections import Counter

#set initial time
start_time_bf = time.time()

#create a dictionary with all the possible unique combinations of itens
all_combinations = {}

'''Initial ideal was to implement loop for each item set
but since we have 9 or 10 different itens it will be very mannual code as you can see below.
The commented out code below shows the iterations up to three itens.
We will use an alternative way that will save us time and effort.
The 'combinations' function from itertool library will perform the same idea of what it is written below but for all the itens


#add single itens to dictionary
for item in item_list:
  all_combinations[item] = 0

#add unique pairs of itens to dictionary
for i in range(len(item_list)):
  for j in range(i + 1, len(item_list)):
    all_combinations[item_list[i] + " ; " + item_list[j]] = 0

#add unique combinations of three itens to dictionary
for i in range(len(item_list)):
  for j in range(i + 1, len(item_list)):
    for k in range(j + 1, len(item_list)):
      all_combinations[item_list[i] + " ; " + item_list[j] + " ; " + item_list[k]] = 0
'''

#define the max number of itemset
max_item_set = len(item_list)

#Start loop thru the each itemset
for item_set in range(1, max_item_set + 1):

  #Add a flag to make sure we can find at least one combination for this itemset level
  itemset_with_combinations = False

  # print(f"Processing {item_set} itemset")

  #compute all the unique itens combination possible for this itemset level
  current_itemset_combinations = {}
  for item_combination in combinations(item_list, item_set):
    key = ' ; '.join(item_combination)
    current_itemset_combinations[key] = 0

  #Count the frequencies for this itemset level
  for transaction in database['Transaction']:
    for item in current_itemset_combinations:
        if set(item.split(' ; ')).issubset(set(transaction)):
            current_itemset_combinations[item] += 1

  #check if there is combinations found in this itemset 
  #and record to dictionary with all combinations
  for key, value in current_itemset_combinations.items():
      if value > 0:
          all_combinations[key] = value
          itemset_with_combinations = True

  #if there is no combinations found in this itemset
  if not itemset_with_combinations:
      # print(f"No frequent itemsets found for #{item_set} itemset")
      break


# #print out the quantity of elements in the dictionary
# print("\nThe dictionary with all the combinations has", len(all_combinations), "different elements")

# #print all the possible combinations until first itemset level with all combination zeros
# #print all the frequencies
# for key, value in all_combinations.items():
#     print(f"{key}: {value}")


# Now that we have all the possible combinations and its frequency, our next step will be to compute the support for each element from the dictionary.Then, we will create a support dictionary that includes only the elements that have a support equal or greater than the one entered by the user.
# 
# Support calculation is just the number of transactions that can has a certain element from the dictionary divide by the total number of transactions from the dataset. We will come out with the frequency of single item from the dictionary.

# In[28]:


#define a dictionary for support requirement achieved
support_dict = {}

#define total number of transactions
total_transactions = len(database)

#compute support and add to the support dictionary
for key, value in all_combinations.items():
  support = value / total_transactions
  if support >= (min_support / 100):
    support_dict[key] = support

# #title for output
# print("Support Dictionary")

# #print out the support dictionary
# for key, value in support_dict.items():
#   print(f"{key}: {value}")


# Final step is to find the confidence for all possible combinations of the elements from the support dictionary

# In[30]:


from itertools import permutations

#define confidence dictionary
confidence_dict = {}

#create function to check all the permutations between itens in a transaction
def find_key(items, dictionary):

    #for one element in the transaction
    if len(items) == 1:
        key = items[0]
        return key if key in dictionary else None

    #for more than 1 element in the transaction
    for p in permutations(items):
        key = ' ; '.join(p)
        if key in dictionary:
            return key
    
    #for no key found 
    return None

#compute confidence for each element from the support dictionary
for support_itemset, support_value in support_dict.items():
  #split into different elements in each itemset
  #before:  Java: The Complete Reference ; Java For Dummies
  #now:   ['Java: The Complete Reference', 'Java For Dummies'])
  support_item = support_itemset.split(' ; ')

  # create rule to to deal with itemset with 2 or more elements, others can be skipped
  if len(support_item) < 2:
    continue

  #compute all combinations of itens (X->Y)
  for i in range(1, len(support_item)):
    #find X(antecedent)
    for combination_x in combinations(support_item, i):

        #find Y(consequent)
        combination_y = list(set(support_item) - set(combination_x))

        #find key for x and y if they exists
        xkey = find_key(list(combination_x), support_dict)
        ykey = find_key(list(combination_y), support_dict)

        #continue if both keys exists
        if xkey and ykey:
            #retrieve support count for X(antecedent)
            support_x = support_dict[xkey]
            
            #retrieve support count for Y(consequent)
            support_y = support_dict[ykey]

            #compute confidence
            confidence = support_value / support_x
            
            #store if confidence is greater than minimun confidence
            if confidence >= (min_confidence / 100):
                x_out = ' ; '.join(sorted(list(combination_x)))
                y_out = ' ; '.join(sorted(combination_y))
                confidence_dict[x_out + " -> " + y_out] = confidence

# #title for output
# print("Confidence Dictionary")

# #print out confidence
# for key, value in confidence_dict.items():
#   print(f"{key}: {value}")


# In[31]:


#final results
print("Brute Force Results")

#define the outputs that we are looking for
first_elem_bf = ""
second_elem_bf = ""
confidence_bf = 0
support_bf = 0

#loop thru the confidence dictionary to come up with the results
for key, value in confidence_dict.items():
    #find X and Y for X->Y and store them as first and second element
    first_elem_bf = key.split(" -> ")[0]
    second_elem_bf = key.split(" -> ")[1]

    #store confidence values
    confidence_bf = value

    #create key to search in the support dictionary (A->B)
    all_possible_items = first_elem_bf.split(' ; ') + second_elem_bf.split(' ; ')
    
    support_key_bf = None

    #check all the permutation of the items to find the correct key
    for p in permutations(all_possible_items):
        current_key_option = ' ; '.join(p)
        if current_key_option in support_dict:
            support_key_bf = current_key_option
            break # Stop once the key is found
    


    #find support value
    if support_key_bf:
        support_bf = support_dict[support_key_bf]
    
        #print out the results
        print("X:", first_elem_bf)
        print("Y:", second_elem_bf)
        print("Rule:", first_elem_bf, "->", second_elem_bf)
        print("Support: ", support_bf)
        print("Confidence: ", confidence_bf)
        print()

    else:
        print(f"\nWarning: Could not find support for the key '{support_key_bf}'. Skipping.")

#set final time
end_time_bf = time.time()

#compute total time for brute force algorithm
total_time_bf = end_time_bf - start_time_bf
print("Total time for Brute Force Algorithm: ", total_time_bf, "seconds")

