from datetime import datetime

from flask_wtf import Form
from wtforms import DateTimeField, SelectField, SelectMultipleField, StringField
from wtforms.validators import DataRequired


class UtilizationForm(Form):
    artist_id = StringField("artist_id")
    venue_id = StringField("venue_id")
    start_time = DateTimeField(
        "start_time", validators=[DataRequired()], default=datetime.today()
    )


class VehicleForm(Form):
    brand = StringField("brand", validators=[DataRequired()])
    model = StringField("model", validators=[DataRequired()])
    year = SelectField(
        "year",
        validators=[DataRequired()],
        choices=[
            ("1980", 1980),
            ("2010", 2010),
        ],
    )
    num_doors = StringField("num_doors", validators=[DataRequired()])
    vtype = SelectField(
        "vtype",
        validators=[DataRequired()],
        choices=[
            ("Sedan", "Sedan"),
            ("Coupe", "Coupe"),
            ("Hatchback", "Hatchback"),
            ("Sportcar", "Sportcar"),
            ("SUV", "SUV"),
            ("Convertible", "Convertible"),
            ("Truck", "Truck"),
            ("Motorcycle", "Motorcycle"),
        ],
    )
    licence = SelectMultipleField(
        "licence",
        validators=[DataRequired()],
        choices=[
            ("Motorcycle", "Motorcycle"),
            ("Car", "Car"),
            ("Truck", "Truck"),
        ],
    )
    power = StringField("power", validators=[DataRequired()])
    transmission = StringField("transmission", validators=[DataRequired()])
    category = SelectField(
        "category",
        validators=[DataRequired()],
        choices=[("car", "Car"), ("truck", "Truck"), ("motorcycle", "Motorcycle")],
    )


class UserForm(Form):
    name = StringField("name", validators=[DataRequired()])
    username = StringField("city", validators=[DataRequired()])
    level = SelectField(
        "level",
        validators=[DataRequired()],
        choices=[
            ("employee", "Employee"),
            ("manager", "Manager"),
            ("administrator", "Administrator"),
        ],
    )
    image_link = StringField("image_link")
    licences = SelectMultipleField(
        "licences",
        validators=[DataRequired()],
        choices=[
            ("Motorcycle", "Motorcycle"),
            ("Car", "Car"),
            ("Truck", "Truck"),
        ],
    )
    phone = StringField("phone")
    enrolment_time = DateTimeField(
        "enrolment_time", validators=[DataRequired()], default=datetime.today()
    )
