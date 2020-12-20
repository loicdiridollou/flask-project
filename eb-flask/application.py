from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand
from models import setup_db, CarsModel


application = Flask(__name__)
setup_db(application)







@application.route('/')
def hello():
    return 'Hello world!'


@application.route('/cars')
def cars():
    cars = CarsModel.query.all()
    dic = {}
    for car in cars:
        dic[car.id] = {'brand': car.brand, 'model': car.model, 'num_doors': car.doors}
    return jsonify(dic)


@application.route('/cars', methods=['POST'])
def add_cars():
    body = request.get_json()

    new_brand = body.get('brand', None)
    new_model = body.get('model', None)
    new_doors = body.get('doors', None)

    try:
        car = CarsModel(brand=new_brand, model=new_model, doors=new_doors)
        car.insert()

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


@application.route('/cars/<int:car_id>', methods=['PATCH'])
def update_cars(car_id):
    body = request.get_json()


    try:
        car = CarsModel.query.filter(CarsModel.id==car_id).one_or_none()
        print(car)
        if car is None:
            abort(404)
        print(1)
        
        if 'brand' in body:
            car.brand = body.get('brand')
        if 'model' in body:
            car.model = body.get('model')
        if 'doors' in body:
            car.doors = body.get('doors')
        print(2)
        car.update()


        #selection = Book.query.order_by(Book.id).all()
        #current_books = paginate_books(request, selection)

        return jsonify({
            'success': True,
            'update': car.id,
            #'books': current_books,
            #'total_books': len(Book.query.all())
        })

    except:
        abort(422)


#if __name__ == '__main__':
#    application.run(debug=True, port=5000)