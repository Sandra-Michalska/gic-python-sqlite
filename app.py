from flask import Flask, render_template, send_file
from io import BytesIO
import sqlite3 

  
app = Flask(__name__) 


@app.route('/i/<int:ident>')
def image_from_sqlite(ident):
    connect = sqlite3.connect("companyData.db") 
    cursor = connect.cursor()
    cursor.execute("SELECT logo_image FROM COMPANY_DATA WHERE id = ?", (ident,))
    result = cursor.fetchall()
    image_bytes = result[0][0] # Get the right column
    bytes_io = BytesIO(image_bytes)
    return send_file(bytes_io, mimetype='image/jpeg')
    

@app.route("/")
def index():
    # Convert digital data to binary format
    def convertToBinaryData(image_name):
        with open(image_name, "rb") as file:
            blobData = file.read()
        return blobData

    connect = sqlite3.connect("companyData.db") 
    connect.execute("CREATE TABLE IF NOT EXISTS COMPANY_DATA (id INTEGER PRIMARY KEY, logo_name TEXT NOT NULL, logo_image BLOB NOT NULL, company_name TEXT NOT NULL, description TEXT NOT NULL)")

    class CompanyData:
        def __init__(self, id, logo_name, logo_image, company_name, description):
            self.id = id
            self.logo_name = logo_name
            self.logo_image = logo_image
            self.company_name = company_name
            self.description = description

    company_data_list = []

    company_data_list.append(CompanyData(1, "cdproject1", convertToBinaryData("images/cdproject1.png"), "CD Project", "Szukamy super cool developerów!"))
    company_data_list.append(CompanyData(2, "cdproject2", convertToBinaryData("images/cdproject2.jpeg"), "CD Project 2", "Szukamy cool developerów!"))
    company_data_list.append(CompanyData(3, "cdproject3", convertToBinaryData("images/cdproject3.jpeg"), "CD Project 3", "Szukamy super developerów!"))
    
    with connect as db_data:
        cursor = db_data.cursor()
        for data in company_data_list:
            cursor.execute("INSERT OR REPLACE INTO COMPANY_DATA (id, logo_name, logo_image, company_name, description) VALUES (?,?,?,?,?)", 
                                                     (data.id, data.logo_name, data.logo_image, data.company_name, data.description))
        db_data.commit()

    cursor.execute("SELECT * FROM COMPANY_DATA") 
    fetchedCompanyData = cursor.fetchall() 
    return render_template("index.html", companyData=fetchedCompanyData)  


if __name__ == "__main__": 
    app.run(debug=True) 