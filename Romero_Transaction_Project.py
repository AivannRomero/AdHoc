import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
pd.options.display.float_format = "{:,.2f}".format

def nameandquantity(x,y):
    index=np.char.find(x,'(',start=0,end=None)
    quantity=int(x[index+2:-1])
    productname=x[:index-1]
    if productname in monthly_transactions[y]:
        monthly_transactions[y][productname]+=quantity
    else:
        monthly_transactions[y][productname]=0
        monthly_transactions[y][productname]+=quantity
    
data = (json.load(open('transaction-data-adhoc-analysis.json')))

monthly_transactions={}
monthly_transactions["Brand"] = {'HealthyKid 3+,Gummy Vitamins':'HealthyKid 3+', 'HealthyKid 3+,Yummy Vegetables':'HealthyKid 3+', 'HealthyKid 3+,Nutrional Milk':'HealthyKid 3+', 'Exotic Extras,Kimchi and Seaweed':'Exotic Extras', 'Exotic Extras,Beef Chicharon':'Exotic Extras',  'Candy City,Orange Beans':'Candy City', 'Candy City,Gummy Worms':'Candy City'}
monthly_transactions["Price"] = {'HealthyKid 3+,Gummy Vitamins':1500, 'HealthyKid 3+,Yummy Vegetables':500, 'HealthyKid 3+,Nutrional Milk':1990, 'Exotic Extras,Kimchi and Seaweed':799, 'Exotic Extras,Beef Chicharon':1299,  'Candy City,Orange Beans':199, 'Candy City,Gummy Worms':150}
vnameandquantity=np.vectorize(nameandquantity)

for transactions in data:
    foodbought=np.array(transactions['transaction_items'].split(';'))
    monthdate=(transactions['transaction_date'][:7]) 
    if monthdate in monthly_transactions:
        vnameandquantity(foodbought,monthdate)
    else:
        monthly_transactions[monthdate]={}
        vnameandquantity(foodbought,monthdate)

df = pd.DataFrame(monthly_transactions)

print("Table for the number of units sold each month per item with their corresponding price, brand, and grand total. \n")
print(df.to_string())
print("\n-----------------------\n")
                         
print("Table for the total sales per month of each item with their corresponding price, brand, and grand total. \n")
newdf = df.copy(deep=True)
newdf[newdf.columns[2:df.shape[1]]] = newdf[newdf.columns[2:df.shape[1]]].mul(newdf["Price"], axis=0)
newdf["Grand Total"]=newdf.sum(axis=1,numeric_only=True)
print(newdf)

print("\n-----------------------\n")
print("Table for percentage change in sales from the previous month with their corresponding price, and brand. \n")
new2df = newdf.copy(deep=True)
del new2df["Grand Total"]
del new2df["Price"]
del new2df["Brand"]
new2df=new2df.T
new2df=new2df.div(new2df.shift(1)).astype(float)-1
new2df=new2df.T
new2df=(new2df.fillna(0))*100
print(new2df)
#bar graph
df[df.columns[2:df.shape[1]-1]].T.plot(kind='bar')
plt.title("Bar Graph Of The Number Of Units Sold For Each Month")
plt.show()
#pie chart
newdf[newdf.columns[-1]].T.plot(kind='pie',autopct='%1.1f%%')
plt.ylabel("")
plt.title("Pie Chart For The Grand Total Sales Of All Months")
plt.show()
#line graph
new2df.T.plot()
plt.title("Line Chart For The Movement Of Sales Of Units For Each Month")
plt.show()
