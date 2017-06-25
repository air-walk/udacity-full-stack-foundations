from flask import Flask

app = Flask(__name__)


@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
  """Show all restaurants"""
  return "This page will show all of my restaurants"


@app.route('/restaurant/new/')
def newRestaurant():
  """Create a new restaurant"""
  return "This page will be for making a new restaurant"


@app.route('/restaurant/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
  """Edit an existing restaurant"""
  return "This page will be editing restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
  """Delete an existing restaurant"""
  return "This page will be for deleting restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/')
@app.route('/restaurant/<int:restaurant_id>/')
def showMenu(restaurant_id):
  """Show the menu for a restaurant"""
  return "This page is the menu for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/new/')
def newMenuItem(restaurant_id):
  """Create a restaurant menu item"""
  return "This page is for making a new menu item for restaurant %s" % restaurant_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit/')
def editMenuItem(restaurant_id, menu_id):
  """Edit a restaurant menu item"""
  return "This page is for editing menu item %s" % menu_id


@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete/')
def deleteMenuItem(restaurant_id, menu_id):
  """Delete a restaurant menu item"""
  return "This page is for deleting menu item %s" % menu_id


if __name__ == '__main__':
  app.debug    = True
  app.run(host = '0.0.0.0', port = 5000)