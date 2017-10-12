from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])


# ADD JSON API ENDPOINT HERE

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def menuJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(id = menu_id).one()
    return jsonify(item.serialize)

@app.route('/')
@app.route('/restaurants/<int:restaurant_id>/menu')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant=restaurant, items = items, restaurant_id = restaurant_id)




@app.route('/restaurants/<int:restaurant_id>/new', methods=['GET','POST'])
def newMenuItem(restaurant_id):
	
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)




@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
	editedItem = session.query(MenuItem).filter_by(id = menu_id).one()
        originalName = editedItem.name
	if request.method == 'POST':
	        editedItem.name = request.form.get('name')
	        editedItem.description = request.form.get('name')
	        editedItem.price = request.form.get('price')
	        editedItem.course = request.form.get('course')
		session.add(editedItem)
		session.commit()
                flash("menu item {} has been edited to {}".format(originalName, editedItem.name))
                #flash("menu item has been edited")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		
		return render_template('editmenuitem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)
	

@app.route('/restaurants/<int:restaurant_id>/<int:menu_id>/delete/', methods = ['GET','POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
            session.delete(deleteItem)
            session.commit()
            flash("menu item {} has been deleted".format(deleteItem.name))
	    return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
            return render_template('deletemenuitem.html', item = deleteItem)


if __name__ == '__main__':
        app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
