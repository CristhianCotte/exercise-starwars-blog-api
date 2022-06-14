from email.policy import default
from enum import unique
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False)
    favorites = db.relationship('Favorite', backref="user", uselist=True)

    # is_active = db.Column(db.Boolean(), unique=False, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.id

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
        }

class Nature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nature_name = db.Column(db.String(250))
    nature_people = db.relationship('People', backref="nature", uselist=True)
    nature_planet = db.relationship('Planet', backref="nature", uselist=True)
    nature_favorite = db.relationship('Favorite', backref="nature", uselist=True)

    def __repr__(self):
        return '<Nature %r>' % self.nature_name

    def serialize(self):
        return {
			"natureName": self.natureName,
			#do not serialize the password, it's a security breach
		}

class Favorite(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    favorite_name = db.Column(db.String(250), nullable=False)
    favorite_uid = db.Column(db.Integer, nullable=False)
    favorite_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))
    __table_args__ = (db.UniqueConstraint(
	"user_id","favorite_name","favorite_uid", "favorite_nature",
	name="debe_tener_una_sola_coincidencia"
    ),)


    def __repr__(self): 
        return '<Favorite %r>' % self.id

    def serialize(self):
        return {
			"favorite_name": self.favorite_name,
			"favorite_nature":self.favorite_nature,
            "favorite_uid":self.favorite_uid,
            "user_id":self.user_id
			#do not serialize the password, it's a security breach
		}




# class Favorites(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
#     planet_id = db.Column(db.Integer, db.ForeignKey("planet.id"), nullable=False)
#     people_id = db.Column(db.Integer, db.ForeignKey("people.id"), nullable=False)
#     planet = db.relationship("Planet", backref="favorites", uselist=False)
#     people = db.relationship("People", backref="favorites", uselist=False)
#     __tables_args__ =(db.UniqueConstraint(
#         "user_id",
#         "planet_id",
#         "people_id",
#         name = "debe_tener_un_solo_favorito"
#     ),)

#     def __repr__(self):
#         return '<Favorites %r>' % self.id

#     def serialize(self):
#         return {
#             "id": self.id,
#             "user_id": self.user_id,
#             "planet_id": self.planet_id,
#             "people_id": self.people_id,
#         }

class People(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    people_name = db.Column(db.String(250), unique=True)
    people_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))

    def __repr__(self):
        return '<People %r>' % self.uid

    def serialize(self):
        return {
            "people_name": self.people_name,
			"people_nature":self.people_nature,
            "people_uid":self.uid,
            # "hair_color": self.hair_color,
            # "eyes_color": self.eyes_color
        }

class Planet(db.Model):
    uid = db.Column(db.Integer, primary_key=True)
    planet_name = db.Column(db.String(250), unique=True)
    planet_nature = db.Column(db.Integer, db.ForeignKey("nature.id"))
    population = db.Column(db.String(250), nullable=False)
    terrain = db.Column(db.String(250), nullable=False)
    
    def __repr__(self):
        return '<Planet %r>' % self.uid

    def serialize(self):
        return {
            "planet_name": self.planet_name,
			"planet_nature":self.planet_nature,
            "planet_uid":self.uid,
            "population": self.population,
            "terrain": self.terrain
                }