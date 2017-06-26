from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session   = DBSession()

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
  """Show all restaurants"""
  restaurants = session.query(Restaurant).all()
  return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurants/JSON')
def showRestaurantsJSON():
  """Show all restaurants in JSON"""
  restaurants = session.query(Restaurant).all()
  return jsonify(Restaurant = [restaurant.serialize for restaurant in restaurants])


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
  """Create a new restaurant"""
  if request.method == 'POST':
    newRestaurant = Restaurant(name = request.form['name'])
    session.add(newRestaurant)
    session.commit()

    flash("New Restaurant Created")
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
  """Edit an existing restaurant"""
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()

  if request.method == 'POST':    
    restaurant.name = request.form['name']
    session.commit()

    flash("Restaurant Successfully Edited")
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
  """Delete an existing restaurant"""
  restaurant = session.query(Restaurant).filter_by(id = restaurant_id ).one()

  if request.method == 'POST':
    session.delete(restaurant)
    session.commit()

    flash("Restaurant Successfully Deleted")
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
  """Show the menu for a restaurant"""
  restaurantToShow = session.query(Restaurant).filter_by(id = restaurant_id).one()
  items            = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

  return render_template('menu.html', restaurant = restaurantToShow, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/JSON')
def showMenuJSON(restaurant_id):
  """Show the menu for a restaurant in JSON"""
  restaurantToShow = session.query(Restaurant).filter_by(id = restaurant_id).one()
  items            = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

  return jsonify(MenuItems = [i.serialize for i in items])


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  """Create a restaurant menu item"""
  if request.method == 'POST':
    newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
    session.add(newItem)
    session.commit()

    flash("Menu Item Created")
    return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
    return render_template('newMenuItem.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  """Edit a restaurant menu item"""
  editedItem = session.query(MenuItem).filter_by(id = menu_id).one()

  if request.method == 'POST':
    if request.form['name']:
      editedItem.name = request.form['name']
    if request.form['description']:
        editedItem.description = request.form['description']
    if request.form['price']:
        editedItem.price = request.form['price']
    if request.form['course']:
        editedItem.course = request.form['course']
    
    session.add(editedItem)
    session.commit()

    flash("Menu Item Successfully Edited")
    return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
    return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
  """Delete a restaurant menu item"""
  itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()

  if request.method == 'POST':
    session.delete(itemToDelete)
    session.commit()

    flash("Menu Item Successfully Deleted")
    return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
    return render_template('deleteMenuItem.html', item = itemToDelete)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/JSON/')
def showMenuItemJSON(restaurant_id, menu_id):
  """Show a restaurant menu item in JSON"""
  menuItem = session.query(MenuItem).filter_by(id = menu_id).one()
  return jsonify(MenuItem = menuItem.serialize)


if __name__ == '__main__':
  app.secret_key = 'movement_lifestyle'
  app.debug      = True
  app.run(host = '0.0.0.0', port = 5000)