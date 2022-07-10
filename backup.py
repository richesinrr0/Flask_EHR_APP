from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


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


@app.route('/form')
def form():
    return render_template('index.html')


@app.route('/data/', methods = ['POST', 'GET'])
def data():
    try:
        #records = EHR.query.filter(EHR.patient_first_name==name, EHR.patient_last_name==lname).all()
        if request.method == 'GET':
            return f"The URL /data is accessed directly. Try going to '/form' to submit form"
        if request.method == 'POST':
            if request.form['action'] == 'submit':
                form_data = request.form
                results = EHR.query.filter(EHR.patient_first_name==form_data['first_name'], EHR.patient_last_name==form_data['last_name']).all()
            
                return render_template('displayData.html', results = results)
            elif request.form['action'] == 'see all':
                results = EHR.query.filter().all()
                return render_template('displayData.html', results = results)
 
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/getCSV') # this is a job for GET, not POST
def get_csv():
    try:
        #need first and last names or all button from index.html
        #pass names or * into sql query
        if request.method == 'POST':
            if request.form['action'] == 'download':

                '''
                conn = sqlite3.connect('test_database') 
                c = conn.cursor()
                c.execute('''
                #SELECT * FROM EHR
                ''')

                df = pd.DataFrame(c.fetchall(), columns=['patient_id', 'patient_first_name', 'patient_middle_name', 'patient_last_name',
                        'pref_name', 'social', 'dob', 'm_address', 'city', 'state', 'zip', 'status', 'sex'])
                df=pd.to_csv('/Users/rossrichesin/Desktop/EHRTable')
                '''


    except Exception as e:
        hed = '<h1>Something is broken in get_csv :(</h1>'
        return hed + str(e)


#download as csv button








@app.route('/')
def index():
    try:
        records = EHR.query.filter_by(patient_first_name='john')
        record_text = '<ul>'
        for record in records:
            record_text += '<li>' + record.patient_first_name + ', ' + record.patient_last_name + '</li>'
        record_text += '</ul>'
        return record_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


@app.route('/form', methods=['POST'])
def index():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    submit = request.form['action'] == 'submit'
    # get a list of unique values in the style column
    try:
        if submit:
            records = EHR.query.filter_by(patient_first_name.like(first_name),patient_first_name.like(last_name)).all()
            record_text = '<ul>'
            for record in records:
                record_text += '<li>' + record.patient_first_name + ', ' + record.patient_last_name + '</li>'
            record_text += '</ul>'
            return record_text
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text
        

    #return redirect(url_for('index'))
    #return render_template('index.html', styles=names)

if __name__ == '__main__':
    app.run(debug=True)