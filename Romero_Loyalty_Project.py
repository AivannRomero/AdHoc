import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.float_format = "{:,.2f}".format

data = (json.load(open('transaction-data-adhoc-analysis.json')))

monthly_transactions={0:set()}
repeater_customers={}
engaged_customers={}
inactive_customers={}
monthly_customers={}
runninglist_customers=set()
returning_customers={}
unique_customers={}

for transactions in data:
    customers=transactions['name']
    monthdate=int((transactions['transaction_date'][6:7]))
    if monthdate in monthly_transactions:
        monthly_transactions[monthdate].add(customers)
    else:
        monthly_transactions[monthdate]=set()
        monthly_transactions[monthdate].add(customers)

runninglist_engaged_customers=monthly_transactions[1]

for month in np.arange(1,13):
    if month!=0 and month in monthly_transactions:
        repeater_customers[month]=len(monthly_transactions[month].intersection(monthly_transactions[month-1]))
        runninglist_engaged_customers=runninglist_engaged_customers.intersection(monthly_transactions[month])
        returning_customers[month]=len(runninglist_customers.intersection(monthly_transactions[month]))
        engaged_customers[month]=len(runninglist_engaged_customers)
        runninglist_customers.update(monthly_transactions[month])
        inactive_customers[month]=len(runninglist_customers)-len(monthly_transactions[month])
        monthly_customers[month]=len(monthly_transactions[month])
        unique_customers[month]=monthly_customers[month]-returning_customers[month]

database={"Repeater Customers":repeater_customers,"Engaged Customers":engaged_customers,"Inactive Customers":inactive_customers,"Total Customers":monthly_customers}

df = pd.DataFrame(database)
df = df.T

df.rename(columns=lambda x: "2022/0"+str(x) if (x<10) else "2022/"+str(x), inplace=True)
print("Table for the number of Repeater, Engaged, Inactive, and Total Customers per month. \n")
print(df.to_string())
print("\n-----------------------\n")

newdf = df.copy(deep=True)
newdf = newdf.div(newdf.iloc[-1])
newdf = newdf.drop('Total Customers')

print("Table for the percentage of Repeater, Engaged, and Inactive Customers in relation to the Total Customers per month. \n")
print(newdf.to_string())
print("\n-----------------------\n")

newdf2 = pd.DataFrame({"Returning Customers":returning_customers,"Unique Customers":unique_customers, "Total Customers":monthly_customers})
newdf2 = newdf2.T
newdf2.rename(columns=lambda x: "2022/0"+str(x) if (x<10) else "2022/"+str(x), inplace=True)

print("Table for the number of Returning Customers, Unique Customers, and Total Customers per month.\n*Note: Returning Customers are customers who has bought before in any previous months and has bought again in the current month.\n*Note: Unique Customers are customers who has only bought at the current month.\n")
print(newdf2.to_string())

#bar graph
df.T.plot(kind='bar')
plt.title("Bar Graph Of The Number Of Repeater, Engaged, Inactive, And Total Customers Per Month")
plt.show()
#line graph
newdf.T.plot(kind='line')
plt.title("Line Graph Of The Percentage Of Repeater, Engaged, and Inactive Customers In Relation To Hhe Total Customers Per Month")
plt.show()
#line graph
newdf2.T.plot(kind='line')
plt.title("Line Graph Of The Amount of Returning, Unique, and Total Customers")
plt.show()
#print(monthly_transactions)