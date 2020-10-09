import pandas as pd
import os
import csv
from app import app, db,Category, Meal


t=pd.read_csv('meals.csv',sep=';')
t.dropna(inplace=True)
print(t.shape)
print(t.iloc[0])
for index, meal in t.iterrows(): 
    print (meal["title"], meal["price"]) 
    meal_add = Meal(id=meal['id'], title=meal['title'], price=meal['price'],\
            description=meal['description'], picture = meal['picture'],category_id=meal['category_id'])
    db.session.add(meal_add)
    db.session.commit()  
  



t=pd.read_csv('Categories.csv',sep=';')
t.dropna(inplace=True)
print(t.shape)
print(t.iloc[0])
for index, cat in t.iterrows(): 
    print (cat["title"], cat["id"]) 
    cat_add = Category(id=cat['id'], title=cat['title'])
    db.session.add(cat_add)
    db.session.commit()  