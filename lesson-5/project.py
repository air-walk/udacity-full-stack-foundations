from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def allRestaurants():
  """Show all restaurants"""
  return "1 - All restaurants here..."


@app.route('/restaurant/new/')
def createRestaurant():
  """Create a new restaurant"""
  return "2 - Create a new restaurant here..."


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
  """Edit an existing restaurant"""
  return "3 - Edit an existing restaurant..."


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
  """Delete an existing restaurant"""
  return "4 - Delete an existing restaurant..."


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showRestaurantMenu(restaurant_id):
  """Show the menu for a restaurant"""
  return "5 - Show the menu for a restaurant..."


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def createRestaurantMenuItem(restaurant_id):
  """Create a restaurant menu item"""
  return "6 - Create a restaurant menu item..."


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editRestaurantMenuItem(restaurant_id, menu_id):
  """Edit a restaurant menu item"""
  return "7 - Edit a restaurant menu item..."


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteRestaurantMenuItem(restaurant_id, menu_id):
  """Delete a restaurant menu item"""
  return "8 - Delete a restaurant menu item..."


if __name__ == '__main__':
  app.debug    = True
  app.run(host = '0.0.0.0', port = 5000)