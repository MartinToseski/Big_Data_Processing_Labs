from flask import Flask, render_template
from services.database_service import get_cities, get_places_by_city, get_place_by_id
from services.recommendation_service import get_structural_recommendations, get_same_city_image_recommendations, get_other_city_image_recommendations

app = Flask(__name__)


@app.route('/')
def home():
    cities = get_cities()
    return render_template('home.html', cities=cities)


@app.route('/city/<city_name>')
def city_page(city_name):
    places = get_places_by_city(city_name)
    return render_template(
        'city.html',
        city=city_name,
        places=places
    )


@app.route('/place/<int:place_id>')
def place_page(place_id):
    place = get_place_by_id(place_id)

    structural = get_structural_recommendations(place_id)
    same_city = get_same_city_image_recommendations(place_id)
    other_city = get_other_city_image_recommendations(place_id)

    return render_template(
        'place.html',
        place=place,
        structural=structural,
        same_city=same_city,
        other_city=other_city
    )


if __name__ == '__main__':
    app.run(debug=True)