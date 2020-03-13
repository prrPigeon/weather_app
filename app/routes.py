import requests
from app import app, db
from flask import render_template, request, redirect, url_for
from pprint import pprint
from .models import City

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        add_city = request.form.get('city') #name atribute from input tag
        if add_city:
            new_city = City(name=add_city)
            db.session.add(new_city)
            db.session.commit()
    cities = City.query.all()
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=89d911f1a1f94d280c6a92b3b9114d9c'
    weather_data = []
    # city = 'Beograd'
    for city in cities:
        # print(city)
        req = requests.get(url.format(city.name)).json()
        # pprint(req)
        weather = {
            'city': city.name,
            'temperature': req['main']['temp'],
            'humidity': req['main']['humidity'],
            'description': req['weather'][0]['description'],
            'icon':req['weather'][0]['icon']
        }
    # pprint(weather)
        weather_data.append(weather)
    return render_template('weather.html', weather_data=weather_data) 

