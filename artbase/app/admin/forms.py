# app/admin/forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from ..models import Art_Style, Artist, Customer, Art_Category, Artwork

class CategoryForm(FlaskForm):
	"""
	Form for admin to add or edit a category
	"""
	categoryid = IntegerField('categoryid', validators=[DataRequired()])
	categoryName = StringField('categoryName', validators=[DataRequired()])
	submit = SubmitField('Submit')


class ArtworkForm(FlaskForm):
	artworkid = IntegerField('artworkid', validators=[DataRequired()])
	title = StringField('title', validators=[DataRequired()])
	artType = StringField('artType', validators=[DataRequired()])
	price = IntegerField('price', validators=[DataRequired()])
	yearMade = IntegerField('yearMade', validators=[DataRequired()])
	creator = QuerySelectField(query_factory=lambda: Artist.query.all(), get_label="artistName")
	art_Category = QuerySelectField(query_factory=lambda: Art_Category.query.all(),
										get_label="categoryName")
	submit = SubmitField('Submit')


class StyleForm(FlaskForm):
    """
    Form for admin to add or edit a style
    """
    styleid = StringField('styleid', validators=[DataRequired()])
    styleName = StringField('styleName', validators=[DataRequired()])
    submit = SubmitField('Submit')

class ArtistForm(FlaskForm):
	#for admin to add artist
	artistid = IntegerField('Artistid', validators=[DataRequired()])
	email = StringField('Email', validators=[DataRequired()])
	artistName = StringField('Artist Name', validators=[DataRequired()])
	age = IntegerField('Age', validators=[DataRequired()])
	birthplace = StringField('Birthplace', validators=[DataRequired()])

	style = QuerySelectField(query_factory=lambda: Art_Style.query.all(),
	                   	get_label="styleName", allow_blank=True)
	submit = SubmitField('Submit')

class AssignCustomerForm(FlaskForm):
	#edit expenditure and preferences
	# expenditure = IntegerField('expenditure', validators=[DataRequired()])
	preferredArtist = QuerySelectField(query_factory=lambda: Artist.query.all(),
	                   	get_label="artistName", allow_blank=True)
	preferredCategories = QuerySelectField(query_factory=lambda: Art_Category.query.all(),
	                   	get_label="categoryName", allow_blank=True)
	submit = SubmitField('Submit')

class EditCustomerForm(FlaskForm):
	expenditure = IntegerField('expenditure', validators=[DataRequired()])
	submit = SubmitField('Submit')
