from itertools import count
from os import read
from numpy import sort
import pandas as pd
from csv import DictWriter, reader
from tempfile import NamedTemporaryFile
import shutil
import csv

from sqlalchemy import null

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
file = open("/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv")
numline = len(file.readlines())

class objectList:
    def __init__(self,country,coi,rent,groc,res):
        self.country=country
        self.costOfIndex=coi
        self.rentIndex=rent
        self.grocIndex=groc
        self.resIndex=res

class HashTable:
    # Create empty bucket list of given size
    def __init__(self, size):
        self.size = size
        self.hash_table = self.create_buckets()

    def create_buckets(self):
        return [[] for _ in range(self.size)]

    # Insert values into hash map
    def set_val(self, key, hash_val, info):
        
        # Get the index from the key
        # using hash function
        # hashed_key = hash(key) % self.size
        
        # Get the bucket corresponding to index
        
        bucket = self.hash_table[hash_val]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            # check if the bucket has same key as
            # the key to be inserted
            if record_key == key:
                found_key = True
                break

        # If the bucket has same key as the key to be inserted,
        # Update the key value
        # Otherwise append the new key-value pair to the bucket
        if found_key:
            bucket[index] = (key, info)
        else:
            bucket.append((key, info))

    # Return searched value with specific key
    def get_val(self, key):
        
        # Get the index from the key using
        # hash function
        hashed_key = self.hashing(key)
        
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index,record in enumerate(bucket):
            record_key, record_val = record
            # print(record) 
            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                found_key = True
                break

        # print(bucket)   
        # print(index)
        # print(record_val.costOfIndex)
        # If the bucket has same key as the key being searched,
        # Return the value found
        # Otherwise indicate there was no record found
        if found_key:#print recrd val
            return (record_val)
        else:
            return "No record found"

    # Remove a value with specific key
    def delete_val(self, key):
        
        # Get the index from the key using
        # hash function
        hashed_key = hash(key) % self.size
        
        # Get the bucket corresponding to index
        bucket = self.hash_table[hashed_key]

        found_key = False
        for index, record in enumerate(bucket):
            record_key, record_val = record
            
            # check if the bucket has same key as
            # the key to be deleted
            if record_key == key:
                found_key = True
                break
        if found_key:
            bucket.pop(index)
        return

    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)

    # insert some values
    # list=[]
    # for i in range(numline):
    #     list.append(objectList())

    def hashing(self,eachCountry):
        hashed=1
        g=31
        for c in eachCountry:
                hashed=g*hashed + ord(c)
                # print(hashed)
                afterHash= hashed%self.size
                # count=count+1
                # print(afterHash)
        return afterHash


hash_table_object = HashTable(281)

def display():
    df=pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    # print(df.to_string())
    Country=df.Country
    coi=df['Cost of Living Index']
    rent=df['Rent Index']
    groc=df['Groceries Index']
    res=df['Restaurant Price Index']
    # print(coi)
    for i in range(numline-1):
        eachCountry=Country.iloc[i] 
        hashed=hashing(eachCountry)
        print(hashed)
        obj=objectList(eachCountry,coi,rent,groc,res)
        hash_table_object.set_val(eachCountry,hashed,obj)
        # print(hash_table_object)
    print()

def hashing(eachCountry):
    hashed=1
    g=31
    for c in eachCountry:
            hashed=g*hashed + ord(c)
            # print(hashed)
            afterHash= hashed%281
            # count=count+1
            #print(afterHash)
    return afterHash

def insert():
    df=pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    Country=df.Country
    coi=df['Cost of Living Index']
    rent=df['Rent Index']
    groc=df['Groceries Index']
    res=df['Restaurant Price Index']
    for i in range(numline-1):
        eachCountry=Country.iloc[i] 
        hashed=hashing(eachCountry)
        obj=objectList(eachCountry,coi,rent,groc,res)
        hash_table_object.set_val(eachCountry,hashed, obj)

# # search/access a record with key
def search():
    df=pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    Country=df.Country
    index=0
    i=1
    for i in range(numline-1):
        eachCountry=Country.iloc[i]
    city_search=input("Enter Country Name\n")
    searched=hash_table_object.get_val(city_search)
    j=0
    for count in Country:
        if(count==city_search):
            break
        else:
            j=j+1
    # print(j)
    # print(searched)
    # print(hash_table_object.get_val)
    # print("Cost of Living Index\t\t  Rent Index\t\t   Groceries Index\t\t    Restaurant Index")
    # print(searched.costOfIndex[j], searched.rentIndex[j], searched.grocIndex[j], searched.resIndex[j])
 

def add():
    addCountry=input("Enter the name of the Country to add\t")
    addCOI=input("Enter the Cost of Living Index to add\t")
    addRent=input("Enter the Rent Index to add\t")
    addGroc=input("Enter the Groceries Index to add\t")
    addRes=input("Enter the Restaurant Index to add\t")
    field_names = ['Country','Cost of Living Index','Rent Index','Groceries Index','Restaurant Price Index']
  
# Dictionary
    dict={'Country':addCountry,'Cost of Living Index':addCOI,'Rent Index':addRent,
        'Groceries Index':addGroc,'Restaurant Price Index':addRes}
    
    # Open your CSV file in append mode
    # Create a file object for this file
    with open('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv', 'a') as f_object:
        
        # Pass the file object and a list 
        # of column names to DictWriter()
        # You will get a object of DictWriter
        dictwriter_object = DictWriter(f_object, fieldnames=field_names)
    
        #Pass the dictionary as an argument to the Writerow()
        dictwriter_object.writerow(dict)
    
        #Close the file object
        f_object.close()


# delete or remove a value
def delete():
    # df=pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    # # Country=df.Country
    # # i=1
    # # for i in range(140):
    # #     eachCountry=Country.iloc[i]
    city_delete=input("Enter Country Name to delete\n")
    # hash_table.delete_val(city_delete)
    df = pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    df =  df[df.Country != city_delete] 

    # df.column_name != whole string from the cell
    # now, all the rows with the column: Name and Value: "dog" will be deleted
    df.to_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv', index=False)

    return "Country Deleted"

def modify():
    modCountry=input("Enter the Country to be modified\n")
    modCOI=input("Enter the Cost of Index to be modified\n")
    modRent=input("Enter the Rent Index to be modified\n")
    modGroc=input("Enter the Groceries Index to be modified\n")
    modRes=input("Enter the Restaurant Price Index to be modified\n")

    filename = '/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv'
    tempfile = NamedTemporaryFile(mode='w', delete=False)

    fields = ['Country','Cost of Living Index','Rent Index','Groceries Index','Restaurant Price Index']

    with open(filename, 'r') as csvfile, tempfile:
        reader = csv.DictReader(csvfile, fieldnames=fields)
        writer = csv.DictWriter(tempfile, fieldnames=fields)
        for row in reader:
            if row['Country'] == str(modCountry):
                print('Updating row', row['Country'])
                row['Cost of Living Index'], row['Rent Index'], row['Groceries Index'], row['Restaurant Price Index'] = modCOI, modRent, modGroc, modRes
            row = {'Country': row['Country'], 'Cost of Living Index': row['Cost of Living Index'], 'Rent Index': row['Rent Index'], 'Groceries Index': row['Groceries Index'], 'Restaurant Price Index':row['Restaurant Price Index']}
            writer.writerow(row)

    shutil.move(tempfile.name, filename)



print("A.Display all Countries\nB.Add Country\nC.Search Country\nD.Delete Country\nE.Modify\n")
choice=input("Enter you choice\n")
if choice == 'A':
    display()
elif choice == 'B':
    add()
elif choice == 'C':
    insert()
    search()
elif choice == 'D':
    insert()
    delete()
elif choice == 'E':
    modify()

