import datetime as dt
from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
#from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import Vehicle, Utilization, User, setup_db
from forms import *



application = Flask(__name__)
db = setup_db(application)
application.config.from_object('config')

migrate = Migrate(application, db)

@application.cli.command("initdb")
def reset_db():
    db.drop_all()
    db.create_all()
    
    db.session.add(Vehicle(brand="Ferrari", model="F458", doors=3, power=200, year=2000, licence='Car', transmission=8, vtype='Sportcar', category='car'))
    db.session.add(Vehicle(brand="Porsche", model="918 Spyder", doors=3, vtype="car"))
    db.session.add(Vehicle(brand="Citroën", model="C4 Picasso", doors=5, vtype="car"))
    db.session.add(Vehicle(brand="Volvo", model="XNR Electric", doors=2, vtype="truck"))
    db.session.add(Vehicle(brand="Freightliner", model="eCascadia", doors=2, vtype="truck"))

    u1 = User(username="jean_dupont", name="Jean Dupont", enrolment_time=dt.datetime(2020, 1, 5, 12, 30), level="manager")
    u2 = User(username="marc_lhermitte", name="Marc L'Hermitte", enrolment_time=dt.datetime(2020, 1, 5, 12, 30), level="employee")
    u3 = User(username="jeanmichel_serre", name="Jean-Michel Serre", enrolment_time=dt.datetime(2020, 1, 5, 12, 30), level="manager")
    u4 = User(username="kevin_chan", name="Kevin Chan", enrolment_time=dt.datetime(2020, 1, 5, 12, 30), level="employee")
    db.session.add(u1)
    db.session.add(u2)
    db.session.add(u3)
    db.session.add(u4)
    
    
    util1 = Utilization(ref_vehicle=1, start_time=dt.datetime(2020, 6, 5, 12, 30), end_time=dt.datetime(2020, 6, 6, 12, 30))
    util1.user = u2
    db.session.add(util1)
    
    util2 = Utilization(ref_vehicle=2, start_time=dt.datetime(2020, 6, 6, 12, 30), end_time=dt.datetime(2020, 6, 8, 12, 30))
    util2.user = u3
    db.session.add(util2)

    util3 = Utilization(ref_vehicle=4, start_time=dt.datetime(2020, 6, 8, 12, 30), end_time=dt.datetime(2020, 6, 9, 12, 30))
    util3.user = u1
    db.session.add(util3)    
    
    db.session.commit()

    
#######################################################
# Home endpoints
#######################################################

@application.route('/')
def index():
    return render_template('pages/home.html')


#######################################################
# Vehicle endpoints
#######################################################

@application.route('/vehicles')
def vehicles():
    vecs = Vehicle.query.all()
    
    return render_template('pages/vehicles.html', vehicles=vecs)


@application.route('/vehicles/<int:vehicle_id>')
def vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.filter(Vehicle.id==vehicle_id).one()
    vehicle_dic =  {'id': vehicle.id, 
                  'brand': vehicle.brand, 
                  'model': vehicle.model, 
                  'num_doors': vehicle.doors, 
                  'vtype': vehicle.vtype,
                  'year': vehicle.year,
                  'licence': vehicle.licence,
                  'transmission': vehicle.transmission,
                  'category': vehicle.category}
    return render_template('pages/show_vehicle.html', vehicle=vehicle_dic)

 

@application.route('/vehicles/type/<string:vehicle_type>')
def vehicles_by_type(vehicle_type):
    vehicles = Vehicle.query.filter(Vehicle.vehicle_type==vehicle_type).all()
    dic = {}
    for vehicle in vehicles:
        dic[vehicle.id] = {'brand': vehicle.brand, 'model': vehicle.model, 'num_doors': vehicle.doors, 'vtype': vehicle.vtype}
    return jsonify(dic)


@application.route('/vehicles/create', methods=['GET'])
def create_vehicle_form():
  form = VehicleForm()
  return render_template('forms/new_vehicle.html', form=form)

@application.route('/vehicles/create', methods=['POST'])
def add_cars():
    body = request.form

    try:
        vehicle = Vehicle(brand=body.get('brand', None), model=body.get('model', None),
                          doors=body.get('doors', None), vtype=body.get('vtype', None),
                          year = body.get('year', 0), power=body.get('power', 0),
                          licence=body.get('licence', ''), transmission=body.get('transmission', ''), 
                          category=body.get('category', ''))
        vehicle.insert()
        
        return redirect(url_for('vehicle_by_id', vehicle_id=vehicle.id))
    
    except:
        abort(422)    


@application.route('/vehicles/<int:vehicle_id>/edit', methods=['GET'])
def edit_vehicle_form(vehicle_id):
    form = VehicleForm()
    vehicle = Vehicle.query.filter(Vehicle.id == vehicle_id).one()
    vehicle_dic =  {'id': vehicle.id, 
                    'brand': vehicle.brand, 
                    'model': vehicle.model, 
                    'num_doors': vehicle.doors, 
                    'vtype': vehicle.vtype,
                    'year': vehicle.year,
                    'licence': vehicle.licence.split(', '),
                    'power': vehicle.power,
                    'transmission': vehicle.transmission}

    return render_template('forms/edit_vehicle.html', form=form, vehicle=vehicle_dic)



@application.route('/vehicles/<int:vehicle_id>/edit', methods=['POST'])
def update_cars(vehicle_id):
    body = request.form
    
    try:
        vehicle = Vehicle.query.filter(Vehicle.id==vehicle_id).one_or_none()
        
        if vehicle is None:
            abort(404)
       
        if 'brand' in body:
            vehicle.brand = body.get('brand')
        if 'model' in body:
            vehicle.model = body.get('model')
        if 'doors' in body:
            vehicle.doors = body.get('doors')
        if 'vtype' in body:
            vehicle.vtype = body.get('vtype', None)
        if 'licence' in body:
            vehicle.licence = ', '.join(request.form.getlist('licence'))
        if 'power' in body:
            vehicle.power = body.get('power')
        if 'year' in body:
            vehicle.year = body.get('year')
        if 'transmission' in body:
            vehicle.transmission = body.get('transmission')
        vehicle.update()
        return redirect(url_for('vehicle_by_id', vehicle_id=vehicle_id))
    except:
        abort(422)



@application.route('/vehicles/<int:vehicle_id>', methods=["DELETE"])
def delete_vehicle(vehicle_id):
    error = False
    try:
        vehicle = Vehicle.query.filter(Vehicle.id==vehicle_id).one()
        db.session.delete(vehicle)
        db.session.commit()
    except():
        db.session.rollback()
        error = True
    finally:
        db.session.close()
    if error:
        abort(500)
    else:
        return jsonify({'success': True})
    


#######################################################
# Utilization endpoints
#######################################################

@application.route('/utilizations')
def utilizations():
    utilizations = Utilization.query.all()
    dic = {}
    for use in utilizations:
        user = User.query.filter(User.id==use.user_id).one_or_none()
        dic[use.id] = {'vehicle': use.ref_vehicle, 'user': user.username, 'start_time': use.start_time, 'end_time': use.end_time}
    return jsonify(dic)


#######################################################
# User endpoints
#######################################################

@application.route('/users')
def users():
    users = User.query.all()
    return render_template('pages/users.html', users=users)


@application.route('/users/<int:user_id>')
def show_user(user_id):
    user = User.query.filter(User.id == user_id).one_or_none()
    
    data = {
        'id': user.id,
        'username': user.username,
        'name': user.name,
        'enrolment_time': user.enrolment_time,
        'level': user.level,
        'licences': user.licences.split(','),
        'phone': user.phone,
        'photo': user.photo
    }
    
    return render_template('pages/show_user.html', user=data)


@application.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    if request.method == 'GET':
        form = UserForm()
        user = User.query.filter(User.id == user_id).one_or_none()
        data = {
            'id': user.id,
            'username': user.username,
            'name': user.name,
            'enrolment_time': user.enrolment_time,
            'level': user.level,
            'licences': user.licences.split(','),
            'photo': user.photo
        }

        return render_template('forms/edit_user.html', form=form, user=data)
    elif request.method == 'POST':
        body = request.form
        return redirect(url_for('show_user', user_id=user_id))


@application.route('/users/create', methods=['GET', 'POST'])
def create_user():
    if request.method == "GET":
        form = UserForm()
        return render_template('forms/new_user.html', form=form)
    elif request.method == "POST":
        body = request.form
        print(body)
        user = User(username=body.get('username', None),
                    name=body.get('name', None),
                    enrolment_time=body.get('enrolment_time', None),
                    level=body.get('level', None),
                    licences=','.join(request.form.getlist('licences')),
                    phone=body.get('phone', None))

        user.insert()
        return redirect(url_for('show_user', user_id=user.id))


@application.route('/users/search')
def search_user():
    dic = {}
    return jsonify(dic)




@application.route('/render')
def render_temp():
    return render_template('index.html')


if __name__ == '__main__':
    application.run(host='0.0.0.0', port='5000')