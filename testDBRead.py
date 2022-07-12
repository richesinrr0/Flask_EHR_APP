from flask import Flask, render_template, request, send_file
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import sqlite3
from pathlib import Path


app = Flask(__name__)

# the name of the database; add path if necessary
db_name = 'test_database'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + db_name

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# this variable, db, will be used for all SQLAlchemy commands
db = SQLAlchemy(app)

# each table in the database needs a class to be created for it
# db.Model is required - don't change it
# identify all columns by name and data type
class EHR(db.Model):
    __tablename__ = 'EHR'
    patient_id = db.Column(db.Integer, primary_key=True)
    patient_first_name = db.Column(db.String)
    patient_middle_name = db.Column(db.String)
    patient_last_name = db.Column(db.String)
    pref_name = db.Column(db.String)
    social = db.Column(db.String)
    dob = db.Column(db.String)
    m_address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    zip = db.Column(db.String)
    status = db.Column(db.String)
    sex = db.Column(db.String)

first_name, last_name = '',''

@app.route('/form')
def form():
    return render_template('index.html')


@app.route('/data/', methods = ['POST', 'GET'])
def data():
    global first_name
    global last_name
    try:
        if request.method == 'GET':
            return f"The URL /data is accessed directly. Try going to '/form' to submit form"
        if request.method == 'POST':
            if request.form['action'] == 'submit':
                form_data = request.form
                first_name, last_name = form_data['first_name'], form_data['last_name']
                results = EHR.query.filter(EHR.patient_first_name==form_data['first_name'], EHR.patient_last_name==form_data['last_name']).all()
                len_results = range(len(results)+1)
                return render_template('displayDataF.html', results = zip(len_results,results),all='\u00A0download\u00A0')
            elif request.form['action'] == 'see all':
                results = EHR.query.filter().all()
                len_results = range(len(results)+1)
                return render_template('displayData.html', results = zip(len_results,results),all='download')
 
    except Exception as e:
        # e holds description of the error
        error_text = '<p>The error:<br>' + str(e) + '</p>'
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/getCSV', methods = ['POST']) 
def get_csv():
    try:
        #need first and last names or all button from index.html
        #pass names or * into sql query
        if request.method == 'POST':
            
            if request.form['action'] == 'download':
                
                conn = sqlite3.connect('test_database') 
                c = conn.cursor()
                c.execute('''
                SELECT * FROM EHR
                ''')
                df = pd.DataFrame(c.fetchall(), columns=['patient_id', 'patient_first_name', 'patient_middle_name', 'patient_last_name',
                        'pref_name', 'social', 'dob', 'm_address', 'city', 'state', 'zip', 'status', 'sex'])
                downloads_path = str(Path.home() / 'Downloads')
                #df.to_csv(downloads_path + '/EHRTable.csv')
                df.to_csv('/Users/rossrichesin/Desktop/EHRTable.csv')
                return ('', 204)
            else:
                conn = sqlite3.connect('test_database') 
                c = conn.cursor()
                c.execute(
                f'SELECT * FROM EHR WHERE patient_first_name == "{first_name}" and patient_last_name == "{last_name}"'
                )
                df = pd.DataFrame(c.fetchall(), columns=['patient_id', 'patient_first_name', 'patient_middle_name', 'patient_last_name',
                        'pref_name', 'social', 'dob', 'm_address', 'city', 'state', 'zip', 'status', 'sex'])
                downloads_path = str(Path.home() / 'Downloads')
                df.to_csv('/Users/rossrichesin/Desktop/EHRTable.csv')
                #df.to_csv(downloads_path + '/EHRTable.csv')
                return ('', 204)

    except Exception as e:
        hed = '<h1>Something is broken in get_csv :(</h1>'
        return hed + str(e)


if __name__ == '__main__':
    app.run(debug=True)