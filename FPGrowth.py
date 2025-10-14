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


# ## 6. FP-Growth

# In[299]:


from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.frequent_patterns import association_rules

#set start time
start_time_fpg = time.time()

#extract the transaction column as a python list
#mlxtend requires one hot encoded format
transactions = []
for i in range(len(database['Transaction'])):
  transactions.append(database['Transaction'][i])

#convert the list into one-hot encoded columns (T/F for each item)
transac_encoder = TransactionEncoder()

#take all the unique values and transform it to a matrix
transac_array = transac_encoder.fit(transactions).transform(transactions)

#convert the matrix to a Panda dataframe
transac_df = pd.DataFrame(transac_array, columns=transac_encoder.columns_)

# #print out result
# print(transac_df)


# In[300]:


#run fp growth algorithm
frequent_itemsets_fpg = fpgrowth(transac_df, min_support=(min_support/100), use_colnames=True)

# #print out result
# print(frequent_itemsets_fpg)


# In[301]:


#generate association rules from the frequent itemsets
association_rules_fpg = association_rules(frequent_itemsets_fpg, min_threshold=(min_confidence/100))

#make sure that association rules ha no empty X or Y for X->Y
association_rules_fpg = association_rules_fpg.dropna(subset=['antecedents', 'consequents'])

# #print out result
# print(association_rules_fpg)


# In[302]:


#print out results
print("FP-Growth Results")

#define the outputs that we are looking for
first_elem_fpg = ""
second_elem_fpg = ""
confidence_fpg = 0
support_fpg = 0

#start loop to go thru each row collecting X, Y, confidence and support and print
for index, row in association_rules_fpg.iterrows():
  first_elem_fpg = list(row['antecedents'])
  second_elem_fpg = list(row['consequents'])
  confidence_fpg = row['confidence']
  support_fpg = row['support']
  print("X:", first_elem_fpg)
  print("Y:", second_elem_fpg)
  print("Rule:", first_elem_fpg, "->", second_elem_fpg)
  print("Support: ", support_fpg)
  print("Confidence: ", confidence_fpg)
  print()

#set end time
end_time_fpg = time.time()

#compute total time for fpg algorithm
total_time_fpg = end_time_fpg - start_time_fpg
print("Total time for FP-Growth Algorithm: ", total_time_fpg, "seconds")

