from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, MigrateCommand

application = Flask(__name__)


database_name = ""
database_path ="postgres://{}:{}@{}/{}".format('postgres', 'postgres','flask-db.csljbjej7s5s.us-west-2.rds.amazonaws.com', database_name)

application.config["SQLALCHEMY_DATABASE_URI"] = database_path
application.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(application)
#migrate = Migrate(application, db)



class CarsModel(db.Model):
    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True)
    brand = db.Column(db.String())
    model = db.Column(db.String())
    doors = db.Column(db.Integer())

    def __init__(self, brand, model, doors):
        self.brand = brand
        self.model = model
        self.doors = doors

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Car {self.brand}>"


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



#if __name__ == '__main__':
#    application.run(debug=True, port=5000)