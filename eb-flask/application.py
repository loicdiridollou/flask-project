from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from models import Vehicle, Utilization, User, setup_db
import datetime as dt
from forms import *



application = Flask(__name__)
db = setup_db(application)
application.config.from_object('config')

migrate = Migrate(application, db)

@application.cli.command("initdb")
def reset_db():
    db.drop_all()
    db.create_all()
    
    db.session.add(Vehicle(brand="Ferrari", model="F458", doors=3, vehicle_type="car"))
    db.session.add(Vehicle(brand="Porsche", model="918 Spyder", doors=3, vehicle_type="car"))
    db.session.add(Vehicle(brand="Citroën", model="C4 Picasso", doors=5, vehicle_type="car"))
    db.session.add(Vehicle(brand="Volvo", model="XNR Electric", doors=2, vehicle_type="truck"))
    db.session.add(Vehicle(brand="Freightliner", model="eCascadia", doors=2, vehicle_type="truck"))

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
    cars = Vehicle.query.all()
    return render_template('pages/vehicles.html', vehicles=cars)


@application.route('/vehicles/<int:vehicle_id>')
def vehicle_by_id(vehicle_id):
    vehicle = Vehicle.query.filter(Vehicle.id==vehicle_id).one()
    dic = {'id': vehicle.id, 'brand': vehicle.brand, 'model': vehicle.model, 'num_doors': vehicle.doors, 'vehicle_type': vehicle.vehicle_type}
    return render_template('pages/show_vehicle.html', vehicle=dic)

 

@application.route('/vehicles/type/<string:vehicle_type>')
def vehicles_by_type(vehicle_type):
    vehicles = Vehicle.query.filter(Vehicle.vehicle_type==vehicle_type).all()
    dic = {}
    for vehicle in vehicles:
        dic[vehicle.id] = {'brand': vehicle.brand, 'model': vehicle.model, 'num_doors': vehicle.doors, 'vehicle_type': vehicle.vehicle_type}
    return jsonify(dic)


@application.route('/vehicles', methods=['POST'])
def add_cars():
    body = request.get_json()

    new_brand = body.get('brand', None)
    new_model = body.get('model', None)
    new_doors = body.get('doors', None)
    new_type = body.get('type', None)

    try:
        vehicle = Vehicle(brand=new_brand, model=new_model, doors=new_doors, vehicle_type=new_type)
        vehicle.insert()

        #selection = Book.query.order_by(Book.id).all()
        #current_books = paginate_books(request, selection)

        return jsonify({
            'success': True,
            'created': car.id,
            #'books': current_books,
            #'total_books': len(Book.query.all())
        })

    except:
        abort(422)


@application.route('/vehicles/create', methods=['GET'])
def create_vehicle_form():
  form = VehicleForm()
  return render_template('forms/new_vehicle.html', form=form)


@application.route('/vehicles/create', methods=["POST"])
def create_vehicle():
    error = False
    try:
        name = request.form['name']
        genres = ','.join(request.form.getlist('genres'))
        city = request.form['city']
        address = request.form['address']
        state =  request.form['state']
        phone = request.form['phone']
        fb_link = request.form['facebook_link']
        img_link = request.form['image_link']
        seeking_talent = request.form['seeking_talent'] == 'Yes'
        seeking_description = request.form['seeking_description']
        website_link = request.form['website_link']

        print(request.form)
    except:
        error = True
        #db.session.rollback()
        flash('An error occurred. Venue ' + request.form['name'] + ' could not be listed.')
    finally:
        # on successful db insert, flash success
        #if not error:
        #flash('Venue ' + request.form['name'] + ' was successfully listed!')
        # TODO: on unsuccessful db insert, flash an error instead.
        # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
        #return render_template('pages/home.html')
        return jsonify(request.form)


@application.route('/vehicles/<int:vehicle_id>/edit', methods=['GET'])
def edit_vehicle_form(vehicle_id):
  form = VehicleForm()
  vehicle = Vehicle.query.filter(Vehicle.id == vehicle_id).one()
  vehicle_dic =  {'id': vehicle.id, 'brand': vehicle.brand, 'model': vehicle.model, 'num_doors': vehicle.doors, 'vehicle_type': vehicle.vehicle_type}

  return render_template('forms/edit_vehicle.html', form=form, vehicle=vehicle_dic)



@application.route('/vehicles/<int:vehicle_id>', methods=['PATCH'])
def update_cars(vehicle_id):
    body = request.get_json()

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
        if 'type' in body:
            vehicle.vehicle_type = body.get('type', None)

        vehicle.update()


        #selection = Book.query.order_by(Book.id).all()
        #current_books = paginate_books(request, selection)

        return jsonify({
            'success': True,
            'update': vehicle.id,
            #'books': current_books,
            #'total_books': len(Book.query.all())
        })

    except:
        abort(422)



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
    dic = {}
    for user in users:
        dic[user.id] = {'name': user.name, 'username': user.username, 'level': user.level, "enrolment date": user.enrolment_time}
    return jsonify(dic)

@application.route('/users/create', methods=['GET'])
def create_user():
    form = UserForm()
    return render_template('forms/new_venue.html', form=form)

@application.route('/users/search')
def search_user():
    dic = {}
    return jsonify(dic)





@application.route('/render')
def render_temp():
    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True, port=5000)