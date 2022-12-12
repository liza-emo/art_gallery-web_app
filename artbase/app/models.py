# app/models.py

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Artist(db.Model):
    __tablename__ = 'artists'
    artistid=db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    artistName = db.Column(db.String(120), unique=True)
    age = db.Column(db.Integer, index=True)
    birthplace = db.Column(db.String(60), index=True)
    artwork = db.relationship('Artwork', backref='artist', cascade='save-update, merge, delete', lazy='dynamic')

    def __repr__(self):
         return '<Artist: {}>'.format(self.artistName)

Styles = db.Table('Styles',
                    db.Column('artistid', db.Integer, db.ForeignKey('artists.artistid', onupdate='cascade'), primary_key=True),
                    db.Column('styleid', db.Integer, db.ForeignKey('art_styles.styleid', onupdate='cascade'), primary_key=True))

class Art_Style(db.Model):
    __tablename__ = 'art_styles'
    styleid = db.Column(db.Integer, index=True, primary_key=True)
    styleName = db.Column(db.String(60), unique=True)
    Art_ists= db.relationship('Artist',secondary='Styles', backref=db.backref('artistStyle'), lazy='dynamic')

    def __repr__(self):
        return '{}'.format(self.styleName)

class Artwork(db.Model):
    __tablename__ = 'artworks'
    artworkid = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), unique=True)
    artType = db.Column(db.String(60))
    price = db.Column(db.Integer)
    yearMade = db.Column(db.Integer)
    creator = db.Column(db.Integer, db.ForeignKey('artists.artistid'))

    def __repr__(self):
        return '<Artwork: {}>'.format(self.title)


Categories = db.Table('Categories',
                        db.Column('artworkid', db.Integer, db.ForeignKey('artworks.artworkid', onupdate='cascade'), primary_key=True),
                        db.Column('categoryid', db.Integer, db.ForeignKey('art_categories.categoryid', onupdate='cascade'), primary_key=True))

class Art_Category(db.Model):

    __tablename__ = 'art_categories'
    categoryid = db.Column(db.Integer, primary_key=True)
    categoryName = db.Column(db.String(60), unique=True)
    artCategory = db.relationship('Artwork', secondary='Categories', backref=db.backref('categorisedArt'), lazy='dynamic')

    def __repr__(self):
        return '<Art_category: {}>'.format(self.categoryName)


artistPreference = db.Table('artistPreference',
                        db.Column('id', db.Integer, db.ForeignKey('customers.id', onupdate='cascade'), primary_key=True),
                        db.Column('artistid', db.Integer, db.ForeignKey('artists.artistid', onupdate='cascade'), primary_key=True))
categoryPreference = db.Table('categoryPreference',
                        db.Column('id', db.Integer, db.ForeignKey('customers.id', onupdate='cascade'), primary_key=True),
                        db.Column('categoryid', db.Integer, db.ForeignKey('art_categories.categoryid', onupdate='cascade'), primary_key=True))


class Customer(UserMixin, db.Model):
    """
    create a customer Table
    """
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    customerName = db.Column(db.String(60))
    address = db.Column(db.String(60))
    expenditure = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128))
    preferredArtists = db.relationship('Artist', secondary='artistPreference', backref=db.backref('artistPreferred'), lazy='dynamic')
    preferredCategory = db.relationship('Art_Category', secondary='categoryPreference', backref=db.backref('categoryPreferred'), lazy='dynamic')
    is_admin = db.Column(db.Boolean, default=False)
    @property
    def password(self):
        """
        Prevent pasword from being accessed
        """
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        """
        Set password to a hashed password
        """
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        """
        Check if hashed password matches actual password
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Customer: {}>'.format(self.customerName)

# Set up user_loader
@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))