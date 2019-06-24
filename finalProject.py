#!/usr/bin/env python

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

app = Flask(__name__)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# temporary variables 
#Fake Restaurants
restaurant = {'name': 'The CRUDdy Crab', 'id': '1'}
restaurants = [{'name': 'The CRUDdy Crab', 'id': '1'}, {'name':'Blue Burgers', 'id':'2'},{'name':'Taco Hut', 'id':'3'}]

#Fake Menu Items
items = [ {'name':'Cheese Pizza', 'description':'made with fresh cheese', 'price':'$5.99','course' :'Entree', 'id':'1'}, {'name':'Chocolate Cake','description':'made with Dutch Chocolate', 'price':'$3.99', 'course':'Dessert','id':'2'},{'name':'Caesar Salad', 'description':'with fresh organic vegetables','price':'$5.99', 'course':'Entree','id':'3'},{'name':'Iced Tea', 'description':'with lemon','price':'$.99', 'course':'Beverage','id':'4'},{'name':'Spinach Dip', 'description':'creamy dip with fresh spinach','price':'$1.99', 'course':'Appetizer','id':'5'} ]
item =  {'name':'Cheese Pizza','description':'made with fresh cheese','price':'$5.99','course' :'Entree'}

@app.route('/')
@app.route('/restaurants/')
def showRestaurants():
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurants/new/')
def newRestaurant():
    return render_template('newrestaurant.html')

@app.route('/restaurants/<int:restaurant_id>/edit/')
def editRestaurant(restaurant_id):
    return render_template(
            'editrestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/delete/')
def deleteRestaurant(restaurant_id):
    return render_template(
            'deleterestaurant.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/')
@app.route('/restaurants/<int:restaurant_id>/menu/')
def showMenu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)

    return render_template('menu.html', restaurant=restaurant, items=items)

'''
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
    #restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id).all()
    return jsonify(MenuItems=[i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON') 
def restaurantMenuItemJSON(restaurant_id, menu_id):
    item = session.query(MenuItem).filter_by(
        restaurant_id=restaurant_id, id=menu_id).one()
    return jsonify(MenuItem=item.serialize)
'''

@app.route('/restaurants/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def newMenuItem(restaurant_id):
    if request.method == 'POST':
        newItem = MenuItem(name=request.form['name'], restaurant_id=restaurant_id)
        session.add(newItem)
        session.commit()
        flash('new menu item created!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    elif request.method == 'GET':
        return render_template('newmenuitem.html', restaurant_id=restaurant_id)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/edit',
           methods=['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
        session.add(editedItem)
        session.commit()
        flash('menu item edited!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        # USE THE RENDER_TEMPLATE FUNCTION BELOW TO SEE THE VARIABLES YOU
        # SHOULD USE IN YOUR EDITMENUITEM TEMPLATE
        return render_template(
            'editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, item=editedItem)

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/delete/', 
           methods=['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
    ItemToDelete = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        session.delete(ItemToDelete)
        session.commit()
        flash('menu item deleted!')
        return redirect(url_for('restaurantMenu', restaurant_id=restaurant_id))
    else:
        return render_template(
            'deletemenuitem.html', item=ItemToDelete)

if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000, threaded = False) 



















