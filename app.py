import json
import shutil
from tempfile import NamedTemporaryFile
from flask import Flask, redirect, render_template, url_for,request
import pandas as pd
import csv
from zmq import has

file = open("/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv")
numline = len(file.readlines())
# df=pd.read_csv("/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv")
# df.to_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv', index=None)

app = Flask(__name__,)     #template_folder='templateFiles', static_folder='staticFiles'

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
        for index, record in enumerate(bucket):
            record_key, record_val = record
            
            # check if the bucket has same key as
            # the key being searched
            if record_key == key:
                found_key = True
                break

        # If the bucket has same key as the key being searched,
        # Return the value found
        # Otherwise indicate there was no record found
        if found_key:
            return record_val
        else:
            return "No record found"

    # Remove a value with specific key
    # def delete_val(self, key):
        
    #     # Get the index from the key using
    #     # hash function
    #     hashed_key = hashing(key) % self.size
        
    #     # Get the bucket corresponding to index
    #     bucket = self.hash_table[hashed_key]

    #     found_key = False
    #     for index, record in enumerate(bucket):
    #         record_key, record_val = record
            
    #         # check if the bucket has same key as
    #         # the key to be deleted
    #         if record_key == key:
    #             found_key = True
    #             break
    #     if found_key:
    #         bucket.pop(index)
    #     return

    # To print the items of hash map
    def __str__(self):
        return "".join(str(item) for item in self.hash_table)

    # insert some values

    def hashing(self,eachCountry):
        hashed=1
        g=31
        for c in eachCountry:
                hashed=g*hashed + ord(c)
                afterHash= hashed%self.size
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
        print(coi)
        for i in range(numline-1):
            eachCountry=Country.iloc[i] 
            hashed=hashing(eachCountry)
            obj=objectList(eachCountry,coi,rent,groc,res)
            hash_table_object.set_val(eachCountry,hashed,obj)


def hashing(eachCountry):
    hashed=1
    g=31
    for c in eachCountry:
            hashed=g*hashed + ord(c)
            afterHash= hashed%281
    return afterHash

@app.route('/')
def index():
    return render_template('index.html')
 
@app.route('/show_data',  methods=("POST", "GET"))
def showData():
    data=pd.read_csv("/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv")
    return render_template('show_csv_data.html', tables=[data.to_html()], titles=[''])

@app.route('/show_hashTable',  methods=("POST", "GET"))
def showHashTable():
    hash_table_object = HashTable(100)
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
        hash_table_object.set_val(eachCountry,hashed,obj)
    hash_table=pd.DataFrame(json.dumps(list(hash_table_object)))
    return render_template('show_hashTable.html', tables=[hash_table.to_html()], titles=[''])

@app.route("/add_country",  methods=['GET','POST'])
def add():
    if request.method == 'POST':
        Country = request.form['con']
        Cost = request.form['coi']
        Rent_Index = request.form['rentIndex']
        Groceries_Index = request.form['grocIndex']
        Restaurant_Price_Index = request.form['resIndex']
    field_names = ['Country','Cost of Living Index','Rent Index','Groceries Index','Restaurant Price Index']
# Dictionary
    dict={'Country':Country,'Cost of Living Index':Cost,'Rent Index':Rent_Index, 'Groceries Index':Groceries_Index,'Restaurant Price Index':Restaurant_Price_Index}
    with open('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv', 'a') as f_object:
        dictwriter_object = csv.DictWriter(f_object, fieldnames=field_names)
        dictwriter_object.writerow(dict)
        f_object.close()
    
    return "Country Added"

@app.route("/delete_country", methods=['GET','POST'])
def delete():
    if request.method == 'POST':
        city_delete = request.form['delcityname']
    df = pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    df =  df[df.Country != city_delete] 
    # df.column_name != whole string from the cell
    df.to_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv', index=False)

    return 'Country Deleted'

@app.route("/search", methods=['GET','POST'])
def search():
    if request.method == 'POST':
        city_search = request.form['searchcityname']
    hash_table_object= HashTable(281)
    df=pd.read_csv('/home/sanjanajoshi/Downloads/Cost_of_Living_Index_2022.csv')
    Country=df.Country
    coi=df['Cost of Living Index']
    rent=df['Rent Index']
    groc=df['Groceries Index']
    res=df['Restaurant Price Index']
    i=1
    for i in range(numline-1):
        eachCountry=Country.iloc[i]
        hashed=hashing(eachCountry)
        obj=objectList(eachCountry,coi,rent,groc,res)
        hash_table_object.set_val(eachCountry,hashed,obj)
    searched=hash_table_object.get_val(city_search)
    j=0
    for count in Country:
        if(count==city_search):
            break
        else:
            j=j+1
    # print(searched.costOfIndex[j], searched.rentIndex[j], searched.grocIndex[j], searched.resIndex[j])

    return render_template('search.html', value=searched, j=j)

@app.route("/modify_country", methods=['GET','POST'])
def modify():
    if request.method == 'POST':
        modCountry=request.form['Modcon']
        modCOI=request.form['Modcoi']
        modRent=request.form['ModrentIndex']
        modGroc=request.form['ModgrocIndex']
        modRes=request.form['ModresIndex']

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

    return "Country Modified"

if __name__=='__main__':
   app.run(debug=True)





