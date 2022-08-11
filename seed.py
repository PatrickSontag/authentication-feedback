"""Seed file to make sample data for db"""
from models import User, Feedback, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# Add data to tables
nate = User.register("natethegreat", "tickles", "nnickerson@dundermifflin.com", "Nate", "Nickerson")
charles = User.register("chuck99", "jakeandcharles", "charles@99.com", "Charles", "Boyle")
ron = User.register("RonSwanson", "password", "RonSwanson@Pawnee.gov", "Ron", "Swanson")

f1 = Feedback(title="Ryan vs Ravi", content="I've never met Ravi personally, but I'm gonna go ahead and say just having known you a short while, Brian, that I prefer Ravi.  And again, I've never even met the guy.", username="natethegreat")
f2 = Feedback(title="Influence", content="I've never been a bad influence on anyone.", username="chuck99")
f3 = Feedback(title="Hello", content="All the eggs and bacon.", username="RonSwanson")
f4 = Feedback(title="Gloves", content="Thanks Daryl.", username="natethegreat")

# Add users to db session and commit
db.session.add(nate)
db.session.add(charles)
db.session.add(ron)

db.session.commit()

# Add feedback to db session and commit
db.session.add(f1)
db.session.add(f2)
db.session.add(f3)
db.session.add(f4)

db.session.commit()
