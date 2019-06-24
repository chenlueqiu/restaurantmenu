
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

# create
myFristRestaurant = Restaurant(name = "Pizza Palace")
session.add(myFristRestaurant)
session.commit()
session.query(Restaurant).all()

cheesepizza = MenuItem(name = "Cheese Pizza", 
                       description = "Very good!",
                       course = "Entree",
                       price = "$8.99",
                       restaurant = myFristRestaurant)
session.add(cheesepizza)
session.commit()
session.query(MenuItem).all()

# read
firstResult = session.query(Restaurant).first()
firstResult.name
firstResult.id

allRestaurants = session.query(Restaurant).all()
len(allRestaurants)
for restaurant in allRestaurants:
    print(restaurant.name)

allRestaurants[10].name = 'a'
session.add(allRestaurants[10])
session.commit()

items = session.query(MenuItem).all()
for item in items:
    print(item.name)
session.query(MenuItem).count()

d = session.query(MenuItem).filter_by(name = "ddddd").one()
d.course


veggieBurgers = session.query(MenuItem).filter_by(name = "Veggie Burger")
for veggieBurger in veggieBurgers:
    print(veggieBurger.id)
    print(veggieBurger.name)
    print(veggieBurger.price)
    print(veggieBurger.restaurant.name)
    print('\n')

# update
UrbanVeggieBurger = session.query(MenuItem).filter_by(id = 2).one()
UrbanVeggieBurger.price = "$2.99"
session.add(UrbanVeggieBurger)
session.commit()

# delete
spinach = session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()
print(spinach.restaurant.name)
session.delete(spinach) 
session.commit()
session.query(MenuItem).filter_by(name = 'Spinach Ice Cream').one()


pvh = session.query(Restaurant).filter_by(name = 'Peters Vege House2').one()
print(pvh.name)
session.delete(pvh) 
session.commit()


# wipe out the database
all_restaurants = session.query(Restaurant).all()
for r in all_restaurants:
    session.delete(r)
    session.commit()
    
all_menus = session.query(MenuItem).all()
for m in all_menus:
    session.delete(m)
    session.commit()





