from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from models import Vehicle, Utilization, User, setup_db
import datetime as dt
#from flask_mysqldb import MySQL


application = Flask(__name__)
db = setup_db(application)

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

    

@application.route('/')
def hello():
    return 'Hello world!'


@application.route('/vehicles')
def list_cars():
    cars = Vehicle.query.all()
    dic = {}
    """
    for car in cars:
        dic[car.id] = {'brand': car.brand, 'model': car.model, 'num_doors': car.doors, 'type': car.vehicle_type}
    return jsonify(dic)
    """
    return render_template('vehicles.html', cars=cars)

@application.route('/utilizations')
def list_utilizations():
    utilizations = Utilization.query.all()
    dic = {}
    for use in utilizations:
        user = User.query.filter(User.id==use.user_id).one_or_none()
        dic[use.id] = {'vehicle': use.ref_vehicle, 'user': user.username, 'start_time': use.start_time, 'end_time': use.end_time}
    return jsonify(dic)



@application.route('/users')
def list_users():
    users = User.query.all()
    dic = {}
    for user in users:
        dic[user.id] = {'name': user.name, 'username': user.username, 'level': user.level, "enrolment date": user.enrolment_time}
    return jsonify(dic)


@application.route('/vehicles/<string:vehicle_type>')
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



@application.route('/render')
def render_temp():
    return render_template('index.html')


if __name__ == '__main__':
    application.run(debug=True, port=5000)