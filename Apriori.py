#!/usr/bin/env python
# coding: utf-8

# ### 2.2 Loading data

# In[111]:


import pandas as pd
import numpy as np
import time
import os


# In[122]:


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

# In[257]:


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


# ## 5. Apriori

# In[297]:


from apyori import apriori

#set start time
start_time_apriori = time.time()

#extract the transaction column as a python list
#apyori does not support panda format here
transactions = []
for i in range(len(database['Transaction'])):
  transactions.append(database['Transaction'][i])

#run the apriori method
association_rules_apriori = apriori(transactions=transactions, #use list of transactions as the input
                                    min_support=(min_support/100), #convert the entered min support value to decimal
                                    min_confidence=(min_confidence/100)) #convert entered confidence value to decimal

#convert all the associations to a list
apriori_results = list(association_rules_apriori)

#if there is no association print out a message
if apriori_results == []:
  print("No association found")
else:
  print("Apriori Results")


#define the outputs that we are looking for
first_elem_apriori = ""
second_elem_apriori = ""
confidence_apriori = 0
support_apriori = 0



#list comes out in this format
#[RelationRecord(items=frozenset({'XX'}), support=XX, ordered_statistics=[OrderedStatistic(items_base=frozenset(), items_add=frozenset({'XX'}), confidence=0.55, lift=1.0)]),
#it is a list with a lof of relations recorded
#we need to access inside each relation record so lets create a loop
for relation_record in apriori_results:
  #record the support
  support_apriori = relation_record.support

  #create another loop to access inside the ordered statistics data
  for item_recorded in relation_record.ordered_statistics:

    #if there is no value for the first or secound element skip to the end
    if not item_recorded.items_base or not item_recorded.items_add:
      continue

    #find x and y for X->Y and store them as first and second element
    #create another loop to access the item base (X)
    for item in item_recorded.items_base:
      first_elem_apriori = item

    #create another loop to access the item add (Y)
    for item in item_recorded.items_add:
      second_elem_apriori = item

    #store confidence values
    confidence_apriori = item_recorded.confidence

    #print out the results

    print("X:", first_elem_apriori)
    print("Y:", second_elem_apriori)
    print("Rule:", first_elem_apriori, "->", second_elem_apriori)
    print("Support: ", support_apriori)
    print("Confidence: ", confidence_apriori)
    print()

#set end time
end_time_apriori = time.time()

#compute total time for apriori algorithm
total_time_apriori = end_time_apriori - start_time_apriori
print("Total time for Apriori Algorithm: ", total_time_apriori, "seconds")


