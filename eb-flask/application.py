from flask import Flask, request, jsonify, abort, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from models import setup_db, VehicleModel


application = Flask(__name__)
db = setup_db(application)

migrate = Migrate(application, db)

@application.route('/')
def hello():
    return 'Hello world!'


@application.route('/vehicles')
def cars():
    cars = VehicleModel.query.all()
    dic = {}
    for car in cars:
        dic[car.id] = {'brand': car.brand, 'model': car.model, 'num_doors': car.doors}
    return jsonify(dic)


@application.route('/vehicles/<string:vehicle_type>')
def vehicles_by_type(vehicle_type):
    vehicles = VehicleModel.query.filter(VehicleModel.vehicle_type==vehicle_type).all()
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
        vehicle = VehicleModel(brand=new_brand, model=new_model, doors=new_doors, vehicle_type=new_type)
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
        vehicle = VehicleModel.query.filter(VehicleModel.id==vehicle_id).one_or_none()
        
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