from flask import Flask, render_template
from services.database_service import get_cities, get_places_by_city, get_place, get_place_image
from services.recommendation_service import get_recommendations
from services.database_service import get_city
from flask import request

app = Flask(__name__)

@app.route('/')
def home():
    cities = get_cities()
    return render_template(
        'home.html',
        cities=cities
    )


@app.route('/city/<int:city_id>')
def city(city_id):
    sort = request.args.get(
        'sort',
        'score'
    )
    places = get_places_by_city(city_id, sort)
    city_data = get_city(city_id)
    return render_template(
        'city.html',
        city=city_data,
        places=places,
        sort=sort
    )


@app.route('/place/<int:place_id>')
def place(place_id):
    place = get_place(place_id)
    image = get_place_image(place_id)
    structural = get_recommendations(
        place_id,
    'structural'
    )

    same_city = get_recommendations(
        place_id,
    'image',
        same_city=True
    )

    other_city = get_recommendations(
        place_id,
    'image',
        same_city=False
    )

    return render_template(
        'place.html',
        place=place,
        image=image,
        structural=structural,
        same_city=same_city,
        other_city=other_city
    )

if __name__ == '__main__':
    app.run(debug=True)
