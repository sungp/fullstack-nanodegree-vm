from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)



#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}

restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]


#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
  return render_template("restaurants.html", restaurants = restaurants) 

@app.route('/restaurants/new/')
def newRestaurants():
  return "This page will be for making a new restaurant"

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurants(restaurant_id):
  return "This page will be fo editing restaurant {}".format(restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurants(restaurant_id):
  return "This page will be fo deleting restaurant {}".format(restaurant_id)


if __name__ == '__main__':
        app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
