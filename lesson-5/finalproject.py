from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

#Fake Restaurants
restaurant  = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
  """Show all restaurants"""
  return render_template('restaurants.html', restaurants = restaurants)


@app.route('/restaurant/new/', methods=['GET', 'POST'])
def newRestaurant():
  """Create a new restaurant"""
  if request.method == 'POST':
    # newRestaurant = Restaurant(name = request.form['name'])
    # session.add(newItem)
    # session.commit()
    restaurants.append({'name': request.form['name'], 'id': '4'})
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('newRestaurant.html')


@app.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
  """Edit an existing restaurant"""
  if request.method == 'POST':
    # restaurant      = Restaurant(id = restaurant_id)
    # restaurant.name = request.form['name']
    # session.commit()

    for restaurant in restaurants:  
      if int(restaurant['id']) == restaurant_id:
        restaurant['name'] = request.form['name']

    return redirect(url_for('showRestaurants'))
  else:
    return render_template('editRestaurant.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
  """Delete an existing restaurant"""
  # restaurant = session.query(Restaurant).filter_by(id = id).one()
  for restaurant in restaurants:
    if int(restaurant['id']) == restaurant_id:
      restaurantToDelete = restaurant
      break

  if request.method == 'POST':
    # session.delete(restaurant)
    # session.commit()
    restaurants.remove(restaurantToDelete)
    return redirect(url_for('showRestaurants'))
  else:
    return render_template('deleteRestaurant.html', restaurant = restaurant)


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
  """Show the menu for a restaurant"""
  # restaurantToShow = session.query(Restaurant).filter_by(id = restaurant_id).one()
  # items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)

  for restaurant in restaurants:
    if int(restaurant['id']) == restaurant_id:
      restaurantToShow = restaurant
      break

  return render_template('menu.html', restaurant = restaurantToShow, items = items)


@app.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
  """Create a restaurant menu item"""
  if request.method == 'POST':
    # newItem = MenuItem(name = request.form['name'], description = request.form['description'], price = request.form['price'], course = request.form['course'], restaurant_id = restaurant_id)
    # session.add(newItem)
    # session.commit()
    items.append({'name':'Chilly Chicken', 'description':'Finger licking good!', 'price':'$0.99','course' :'Entree', 'id':'6'})
    return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
    return render_template('newMenuItem.html', restaurant_id = restaurant_id)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/', methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
  """Edit a restaurant menu item"""
  # editedItem = session.query(MenuItem).filter_by(id = menu_id).one()

  if request.method == 'POST':
    if request.form['name']:
      editedItem.name = request.form['name']
    if request.form['description']:
        editedItem.description = request.form['description']
    if request.form['price']:
        editedItem.price = request.form['price']
    if request.form['course']:
        editedItem.course = request.form['course']
    # session.add(editedItem)
    # session.commit()
    return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
  else:
    return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = menu_id, item = editedItem)


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/', methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
  """Delete a restaurant menu item"""
  # itemToDelete = session.query(MenuItem).filter_by(id = menu_id).one()

  if request.method == 'POST':
    # session.delete(itemToDelete)
    # session.commit()
    return redirect(url_for('showMenu', restaurant_id = restaurant_id))
  else:
    return render_template('deleteMenuItem.html', item = itemToDelete)


if __name__ == '__main__':
  app.debug    = True
  app.run(host = '0.0.0.0', port = 5000)