from flask import Flask, render_template 
import sqlite3 

  
app = Flask(__name__) 


connect = sqlite3.connect('companyData.db') 
connect.execute('CREATE TABLE IF NOT EXISTS COMPANY_DATA (logo TEXT, name TEXT, text TEXT)') 


@app.route('/')
def index(): 
    class CompanyData:
        def __init__(self, logo, name, text):
            self.logo = logo
            self.name = name
            self.text = text

    companyDataList = []

    companyDataList.append(CompanyData("LOGO 1", "CD Project", "Szukamy super cool developerów!"))
    companyDataList.append(CompanyData("LOGO 2", "CD Project 2", "Szukamy cool developerów!"))
    companyDataList.append(CompanyData("LOGO 3", "CD Project 3", "Szukamy super developerów!"))
    
    with sqlite3.connect("companyData.db") as dbData: 
        cursor = dbData.cursor()

        for data in companyDataList:
            cursor.execute("INSERT INTO COMPANY_DATA (logo, name, text) VALUES (?,?,?)", 
                          (data.logo, data.name, data.text)) 

        dbData.commit()

    cursor.execute('SELECT * FROM COMPANY_DATA') 
    fetchedCompanyData = cursor.fetchall() 
    return render_template("index.html", companyData=fetchedCompanyData)  


if __name__ == '__main__': 
    app.run(debug=True) 