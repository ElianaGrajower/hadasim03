from flask import Flask, request, jsonify, make_response, render_template, url_for, flash, redirect, escape
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from datetime import datetime

# create an instance of flask
app = Flask(__name__)
# create an API object
api = Api(app)
app.secret_key = "caircocoders-ednalan"
# create database mysql
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Green135@localhost/emp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#sqlalchemy mapper
db = SQLAlchemy(app)
migrate = Migrate(app, db)

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(80), primary_key=False)
    lastname = db.Column(db.String(80), primary_key=False)
    address = db.Column(db.String(200), primary_key=False)
    dateofbirth = db.Column(db.Date, primary_key=False)
    phone = db.Column(db.String(9), primary_key=False, nullable=True)
    cellphone = db.Column(db.String(10), primary_key=False)
    image_data = db.Column(db.String(255), primary_key=False, nullable=True)

    def __init__(self, firstname, lastname, city, street, building, dateofbirth, cellphone, phone=None, image_data=None):
        self.firstname = firstname
        self.lastname = lastname
        self.address = f"{city}, {street} {building}"
        self.dateofbirth = dateofbirth
        self.phone = phone
        self.cellphone = cellphone
        self.image_data = image_data

    def __repr__(self):
        return f"{self.firstname} - {self.lastname} - {self.address} - {self.dateofbirth} - {self.phone} " \
               f"- {self.cellphone} - {self.image_data}"


class Covid_Info(db.Model):
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    employee = db.relationship("Employee", backref="covid_info")
    vaccines = db.Column(db.JSON, nullable=True)
    infected_date = db.Column(db.Date, nullable=True)
    recovered_date = db.Column(db.Date, nullable=True)

    def __init__(self, emp_id, vaccines=None, infected_date=None, recovered_date=None):
        self.emp_id = emp_id
        self.vaccines = vaccines
        self.infected_date = infected_date
        self.recovered_date = recovered_date

    def __repr__(self):
        return f"{self.emp_id} - {self.vaccines} - {self.infected_date} - {self.recovered_date}"

# For GET all employees request to http://localhost:5000/
class GetAllEmployees(Resource):
    def get(self):
        employees = Employee.query.all()
        emp_list = []
        for emp in employees:
            my_date = emp.dateofbirth
            date_string = my_date.strftime("%Y-%m-%d")
            emp_data = {'id': emp.id, 'FirstName': emp.firstname, 'LastName': emp.lastname, 'Address': emp.address,
                        'DateOfBirth': date_string, 'Phone': emp.phone, 'CellPhone': emp.cellphone,
                        'Image': emp.image_data}
            emp_list.append(emp_data)
        return {'Employees': emp_list}, 200


# For GET employee request to http://localhost:5000/?
class GetEmployee(Resource):
    def get(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}, 404
        my_date = emp.dateofbirth
        date_string = my_date.strftime("%Y-%m-%d")
        emp_data = {'id': emp.id, 'FirstName': emp.firstname, 'LastName': emp.lastname, 'Address': emp.address,
                    'DateOfBirth': date_string, 'Phone': emp.phone, 'CellPhone': emp.cellphone, 'Image': emp.image_data}
        return {f"Employee {id}": emp_data}, 200

# For GET all covid_info request to http://localhost:5000/covid
class GetAllCovid_Info(Resource):
    def get(self):
        # Query all Covid_Info records from the database
        covid_info_list = Covid_Info.query.all()
        # Create a list to hold the Covid_Info objects
        covid_info_objs = []
        # Loop through the list of Covid_Info records and create Covid_Info objects
        for cov in covid_info_list:
            inf_date = cov.infected_date
            inf_string = inf_date.strftime("%Y-%m-%d") if inf_date else None
            rec_date = cov.recovered_date
            rec_string = rec_date.strftime("%Y-%m-%d") if rec_date else None
            cov_data = {'id': cov.emp_id, 'VaccineInfo': cov.vaccines, 'InfectedDate': inf_string,
                        'RecoveredDate': rec_string}
            covid_info_objs.append(cov_data)
        # Return the list of Covid_Info objects
        return {'Covid_Info': covid_info_objs}, 200

# For GET covid_info request to http://localhost:5000/covid/?
class GetCovid_Info(Resource):
    def get(self, id):
        # Query Covid_Info records from the database
        cov = Covid_Info.query.get(id)
        if cov is None:
            return {'error': 'not found'}, 404
        inf_date = cov.infected_date
        inf_string = inf_date.strftime("%Y-%m-%d") if inf_date else None
        rec_date = cov.recovered_date
        rec_string = rec_date.strftime("%Y-%m-%d") if rec_date else None
        cov_data = {'id': cov.emp_id, 'VaccineInfo': cov.vaccines, 'InfectedDate': inf_string,
                    'RecoveredDate': rec_string}
        return {f"Covid_Info {cov.emp_id}": cov_data}, 200

# For Post employee request to http://localhost:5000/add
class AddEmployee(Resource):
    def post(self):
        if request.is_json:
            # Checks if its receiving all the data in the correct format
            firstName = request.json.get('FirstName')
            if not firstName:
                return {'error': 'missing first name'}, 400
            lastName = request.json.get('LastName')
            if not lastName:
                return {'error': 'missing last name'}, 400
            city = request.json.get('City')
            if not city:
                return {'error': 'missing city'}, 400
            street = request.json.get('Street')
            if not street:
                return {'error': 'missing street'}, 400
            building = request.json.get('Building')
            if not building:
                return {'error': 'missing building'}, 400
            # convert date string to date object
            date_string = request.json.get('DateOfBirth')
            if not date_string:
                return {'error': 'missing date of birth'}, 400
            try:
                date_of_birth = datetime.strptime(date_string, '%Y-%m-%d').date()
            except ValueError:
                return {'error': 'Date of birth not in date form'}, 400
            phone = request.json.get('Phone')
            if not lastName:
                phone = None
            cellPhone = request.json.get('CellPhone')
            if not cellPhone:
                return {'error': 'missing cell phone number'}, 400
            image = request.json.get('Image')
            if not image:
                image = None
            emp = Employee(firstname=firstName, lastname=lastName, city=city, street=street, building=building,
                           dateofbirth=date_of_birth, phone=phone, cellphone=cellPhone, image_data=image)
            db.session.add(emp)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'id': emp.id, 'First Name': emp.firstname, 'Last Name': emp.lastname,
                                          'Address': emp.address, 'Date Of Birth': date_string, 'Phone': emp.phone,
                                          'CellPhone': emp.cellphone, 'Image': emp.image_data}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400

# For Post covid_info request to http://localhost:5000/covid/add
class AddCovid_Info(Resource):
    def post(self):
        if request.is_json:
            id_emp = request.json['id']
            # Checks if its receiving all the data in the correct format
            # Check if emp_id exists in the employee table
            if not Employee.query.filter_by(id=id_emp).first():
                return {'error': 'Employee does not exist'}, 404
            existing_record = Covid_Info.query.get(id_emp)
            if existing_record:
                return {"message": f"Covid information with id {id_emp} already exists."}, 409
            # convert date string to date object
            inf_string = request.json.get('InfectedDate', '')
            if inf_string:
                try:
                    inf_date = datetime.strptime(inf_string, '%Y-%m-%d').date()
                except ValueError:
                    return {'error': 'Infected date not in date form'}, 400
            else:
                inf_date = None
            rec_string = request.json.get('RecoveredDate', '')
            if rec_string:
                try:
                    rec_date = datetime.strptime(rec_string, '%Y-%m-%d').date()
                except ValueError:
                    return {'error': 'Recovered date not in date form'}, 400
            else:
                rec_date = None
            if inf_date is None and rec_date is not None:
                return {'error': 'Cannot have a recovery date without an infected date.'}, 400
            cov = Covid_Info(emp_id=id_emp, vaccines=request.json.get('VaccineInfo'), infected_date=inf_date,
                             recovered_date=rec_date)
            db.session.add(cov)
            db.session.commit()
            # return a json response
            return make_response(jsonify({'id': cov.emp_id, 'VaccineInfo': cov.vaccines, 'InfectedDate': inf_string,
                        'RecoveredDate': rec_string}), 201)
        else:
            return {'error': 'Request must be JSON'}, 400


# For update request to http://localhost:5000/update/? #updates an employee of a given id
class UpdateEmployee(Resource):
    def put(self, id):
        if request.is_json:
            emp = Employee.query.get(id)
            if emp is None:
                return {'error': 'not found'}, 404
            else:
                date_string = request.json['DateOfBirth']
                date_of_birth = datetime.strptime(date_string, '%Y-%m-%d').date()
                emp.firstname = request.json['FirstName']
                emp.lastname = request.json['LastName']
                emp.city = request.json['City']
                emp.street = request.json['Street']
                emp.building = request.json['Building']
                emp.address = f"{request.json['City']}, {request.json['Street']} {request.json['Building']}"
                emp.dateofbirth = date_of_birth
                emp.phone = request.json['Phone']
                emp.cellphone = request.json['CellPhone']
                db.session.commit()
                return 'Updated', 200
        else:
            return {'error': 'Request must be JSON'}, 400

# For delete request to http://localhost:5000/delete/?
class DeleteEmployee(Resource): #deletes an employee of a given id
    def delete(self, id):
        emp = Employee.query.get(id)
        if emp is None:
            return {'error': 'not found'}, 404
        db.session.delete(emp)
        db.session.commit()
        return f'{id} is deleted', 200


@app.route('/unvaccinated', methods=['GET']) #counts the amount of people who are unvaccinated
def count_unvaccinated():
    count = 0
    covid_info_list = Covid_Info.query.all()
    for cov in covid_info_list:
        if cov.vaccines is None:
            count += 1
    return f"unvaccinated: {count}"


#urls
api.add_resource(GetAllEmployees, '/')
api.add_resource(AddEmployee, '/add')
api.add_resource(UpdateEmployee, '/update/<int:id>')
api.add_resource(DeleteEmployee, '/delete/<int:id>')

api.add_resource(GetEmployee, '/<int:id>')
api.add_resource(GetCovid_Info, '/covid/<int:id>')

api.add_resource(GetAllCovid_Info, '/covid')
api.add_resource(AddCovid_Info, '/covid/add')

#
if __name__ == '__main__':
    app.run(debug=True)















