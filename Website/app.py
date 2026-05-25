from flask import Flask, render_template
from services.database_service import get_cities, get_places_by_city, get_place, get_place_image
from services.recommendation_service import get_structural_recommendations, get_image_recommendations

app = Flask(__name__)


@app.route('/')
def home():
    cities = get_cities()
    return render_template(
        'home.html',
        cities=cities
    )


@app.route('/city/<city>')
def city(city):
    places = get_places_by_city(city)
    return render_template(
        'city.html',
        city=city,
        places=places
    )


@app.route('/place/<int:place_id>')
def place(place_id):
    place = get_place(place_id)
    image = get_place_image(place_id)
    structural = get_structural_recommendations(place_id)
    image_recommendations = get_image_recommendations(place_id)

    return render_template(
        'place.html',
        place=place,
        image=image,
        structural=structural,
        image_recommendations=image_recommendations
    )


if __name__ == '__main__':
    app.run(debug=True)