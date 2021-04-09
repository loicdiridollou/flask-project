from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField
from wtforms.validators import DataRequired, AnyOf, URL

class UtilizationForm(Form):
    artist_id = StringField(
        'artist_id'
    )
    venue_id = StringField(
        'venue_id'
    )
    start_time = DateTimeField(
        'start_time',
        validators=[DataRequired()],
        default= datetime.today()
    )

class VehicleForm(Form):
    brand = StringField(
        'brand', validators=[DataRequired()]
    )
    model = StringField(
        'model', validators=[DataRequired()]
    )
    year = SelectField(
        'year', validators=[DataRequired()],
        choices=[
            ('1980', 1980),
            ('2010', 2010),
        ]
    )
    num_doors = StringField(
        'num_doors', validators=[DataRequired()]
    )
    vtype = SelectField(
        'vtype', validators=[DataRequired()],
        choices=[
            ('Sedan', 'Sedan'),
            ('Coupe', 'Coupe'),
            ('Hatchback', 'Hatchback'),
            ('Sportcar', 'Sportcar'),
            ('SUV', 'SUV'),
            ('Convertible', 'Convertible'),
            ('Truck', 'Truck'),
            ('Motorcycle', 'Motorcycle')
        ]
    )
    licence = SelectMultipleField(
        'licence', validators=[DataRequired()],
        choices=[
            ('Motorcycle', 'Motorcycle'),
            ('Car', 'Car'),
            ('Truck', 'Truck'),
        ]
    )
    power = StringField(
        'power', validators=[DataRequired()]
    )
    transmission = StringField(
        'transmission', validators=[DataRequired()]
    )
    category = SelectField(
        'category', validators=[DataRequired()],
        choices=[
            ('car', 'Car'),
            ('truck', 'Truck'),
            ('motorcycle', 'Motorcycle')
        ]
    )
    

class UserForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    city = StringField(
        'city', validators=[DataRequired()]
    )
    state = SelectField(
        'state', validators=[DataRequired()],
        choices=[
            ('AL', 'AL'),
            ('AK', 'AK'),
            ('AZ', 'AZ'),
            ('AR', 'AR'),
            ('CA', 'CA'),
            ('CO', 'CO'),
            ('CT', 'CT'),
            ('DE', 'DE'),
            ('DC', 'DC'),
            ('FL', 'FL'),
            ('GA', 'GA'),
            ('HI', 'HI'),
            ('ID', 'ID'),
            ('IL', 'IL'),
            ('IN', 'IN'),
            ('IA', 'IA'),
            ('KS', 'KS'),
            ('KY', 'KY'),
            ('LA', 'LA'),
            ('ME', 'ME'),
            ('MT', 'MT'),
            ('NE', 'NE'),
            ('NV', 'NV'),
            ('NH', 'NH'),
            ('NJ', 'NJ'),
            ('NM', 'NM'),
            ('NY', 'NY'),
            ('NC', 'NC'),
            ('ND', 'ND'),
            ('OH', 'OH'),
            ('OK', 'OK'),
            ('OR', 'OR'),
            ('MD', 'MD'),
            ('MA', 'MA'),
            ('MI', 'MI'),
            ('MN', 'MN'),
            ('MS', 'MS'),
            ('MO', 'MO'),
            ('PA', 'PA'),
            ('RI', 'RI'),
            ('SC', 'SC'),
            ('SD', 'SD'),
            ('TN', 'TN'),
            ('TX', 'TX'),
            ('UT', 'UT'),
            ('VT', 'VT'),
            ('VA', 'VA'),
            ('WA', 'WA'),
            ('WV', 'WV'),
            ('WI', 'WI'),
            ('WY', 'WY'),
        ]
    )
    phone = StringField(
        # TODO implement validation logic for state
        'phone'
    )
    image_link = StringField(
        'image_link'
    )
    genres = SelectMultipleField(
        # TODO implement enum restriction
        'genres', validators=[DataRequired()],
        choices=[
            ('Alternative', 'Alternative'),
            ('Blues', 'Blues'),
            ('Classical', 'Classical'),
            ('Country', 'Country'),
            ('Electronic', 'Electronic'),
            ('Folk', 'Folk'),
            ('Funk', 'Funk'),
            ('Hip-Hop', 'Hip-Hop'),
            ('Heavy Metal', 'Heavy Metal'),
            ('Instrumental', 'Instrumental'),
            ('Jazz', 'Jazz'),
            ('Musical Theatre', 'Musical Theatre'),
            ('Pop', 'Pop'),
            ('Punk', 'Punk'),
            ('R&B', 'R&B'),
            ('Reggae', 'Reggae'),
            ('Rock n Roll', 'Rock n Roll'),
            ('Soul', 'Soul'),
            ('Other', 'Other'),
        ]
    )
    facebook_link = StringField(
        # TODO implement enum restriction
        'facebook_link', validators=[URL()]
    )

    website_link = StringField(
        # TODO implement enum restriction
        'website_link', validators=[URL()]
    )

    seeking_description = StringField(
        # TODO implement enum restriction
        'seeking_description'
    )
    seeking_venue = SelectField(
        'seek_venue', validators=[DataRequired()],
        choices = ['Yes', 'No'],
        default = 'No'
    )
