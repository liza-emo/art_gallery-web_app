# app/admin/views.py

from flask import abort, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import admin
from forms import CategoryForm, StyleForm, ArtistForm, ArtworkForm, AssignCustomerForm, EditCustomerForm
from .. import db
from ..models import Art_Style, Artist, Customer, Art_Category, Artwork

def check_admin():
    """
    Prevent non-admins from accessing the page
    """
    if not current_user.is_admin:
        abort(403)

# art_category Views

@admin.route('/art_categories', methods=['GET', 'POST'])
@login_required
def list_art_categories():
    """
    List all art_categories
    """
    check_admin()

    art_categories = Art_Category.query.all()

    return render_template('admin/art_categories/art_categories.html',
                           art_categories=art_categories, title="Art_Categories")


@admin.route('/art_categories/add', methods=['GET', 'POST'])
@login_required
def add_art_category():
    """
    Add a art_category to the database
    """
    check_admin()

    add_art_category = True

    form = CategoryForm()
    if form.validate_on_submit():
        art_category = Art_Category(categoryid=form.categoryid.data,
                            categoryName=form.categoryName.data)
        try:
            # add art_category to the database
            db.session.add(art_category)
            db.session.commit()
            flash('You have successfully added a new art_category.')
        except:
            # in case art_category name already exists
            flash('Error: art_category name already exists.')

        # redirect to art_categories page
        return redirect(url_for('admin.list_art_categories'))

    # load art_category template
    return render_template('admin/art_categories/art_category.html', action="Add",
                           add_art_category=add_art_category, form=form,
                           title="Add Art_Category")


@admin.route('/art_categories/edit/<int:categoryid>', methods=['GET', 'POST'])
@login_required
def edit_art_category(categoryid):
    """
    Edit a art_category
    """
    check_admin()

    add_art_category = False

    art_category = Art_Category.query.get_or_404(categoryid)
    form = CategoryForm(obj=art_category)
    if form.validate_on_submit():
        art_category.categoryid = form.categoryid.data
        art_category.categoryName = form.categoryName.data
        db.session.commit()
        flash('You have successfully edited the art_category.')

        # redirect to the art_categories page
        return redirect(url_for('admin.list_art_categories'))

    form.categoryid.data = art_category.categoryid
    form.categoryName.data = art_category.categoryName
    return render_template('admin/art_categories/art_category.html', action="Edit",
                           add_art_category=add_art_category, form=form,
                           art_category=art_category, title="Edit Art_Category")


@admin.route('/art_categories/delete/<int:categoryid>', methods=['GET', 'POST'])
@login_required
def delete_art_category(categoryid):
    """
    Delete a art_category from the database
    """
    check_admin()

    art_category = Art_Category.query.get_or_404(categoryid)
    db.session.delete(art_category)
    db.session.commit()
    flash('You have successfully deleted the art_category.')

    # redirect to the art_categories page
    return redirect(url_for('admin.list_art_categories'))

    return render_template(title="Delete Art_Category")

# Art_Style Views

@admin.route('/art_styles')
@login_required
def list_art_styles():
    check_admin()
    """
    List all art_styles
    """
    art_styles = Art_Style.query.all()
    return render_template('admin/art_styles/art_styles.html',
                           art_styles=art_styles, title='Art_Styles')

@admin.route('/art_styles/add', methods=['GET', 'POST'])
@login_required
def add_art_style():
    """
    Add a art_style to the database
    """
    check_admin()

    add_art_style = True

    form = StyleForm()
    if form.validate_on_submit():
        art_style = Art_Style(styleid=form.styleid.data,
                    styleName=form.styleName.data)

        try:
            # add art_style to the database
            db.session.add(art_style)
            db.session.commit()
            flash('You have successfully added a new art_style.')
        except:
            # in case art_style styleName already exists
            flash('Error: art_style styleName already exists.')

        # redirect to the art_styles page
        return redirect(url_for('admin.list_art_styles'))

    # load art_style template
    return render_template('admin/art_styles/art_style.html', add_art_style=add_art_style,
                           form=form, title='Add Art_Style')


@admin.route('/art_styles/edit/<int:styleid>', methods=['GET', 'POST'])
@login_required
def edit_art_style(styleid):
    """
    Edit a art_style
    """
    check_admin()

    add_art_style = False

    art_style = Art_Style.query.get_or_404(styleid)
    form = StyleForm(obj=art_style)
    if form.validate_on_submit():
        art_style.styleName = form.styleName.data
        art_style.styleid = form.styleid.data
        db.session.add(art_style)
        db.session.commit()
        flash('You have successfully edited the art_style.')

        # redirect to the art_styles page
        return redirect(url_for('admin.list_art_styles'))

    form.styleid.data = art_style.styleid
    form.styleName.data = art_style.styleName
    return render_template('admin/art_styles/art_style.html', add_art_style=add_art_style,
                           form=form, title="Edit Art_Style")


@admin.route('/art_styles/delete/<int:styleid>', methods=['GET', 'POST'])
@login_required
def delete_art_style(styleid):
    """
    Delete a art_style from the database
    """
    check_admin()

    art_style = Art_Style.query.get_or_404(styleid)
    db.session.delete(art_style)
    db.session.commit()
    flash('You have successfully deleted the art_style.')

    # redirect to the art_styles page
    return redirect(url_for('admin.list_art_styles'))

    return render_template(title="Delete Art_Style")




    # artist views

#artist views
@admin.route('/artists')
@login_required
def list_artists():
    check_admin()
    """
    List all artists
    """
    artists = Artist.query.all()
    return render_template('admin/artists/artists.html',
                           artists=artists, title='Artists')


@admin.route('/artists/add', methods=['GET', 'POST'])
@login_required
def add_artist():
    """
    Add a artist to the database
    """
    check_admin()

    add_artist = True

    form = ArtistForm()
    if form.validate_on_submit():
        artist = Artist(artistid=form.artistid.data,
                        email=form.email.data,
                        artistName=form.artistName.data,
                        age=form.age.data,
                        birthplace=form.birthplace.data)
        style=form.style.data
        style.Art_ists.append(artist)

        try:
            # add artist to the database
            db.session.add(artist)
            db.session.commit()
            flash('You have successfully added a new artist.')
        except:
            # in case artist name already exists
            flash('Error: artist name already exists.')

        # redirect to the artists page
        return redirect(url_for('admin.list_artists'))

    # load artist template
    return render_template('admin/artists/artist.html', add_artist=add_artist,
                           form=form, title='Add Artist')


@admin.route('/artists/edit/<int:artistid>', methods=['GET', 'POST'])
@login_required
def edit_artist(artistid):
    """
    Edit a artist
    """
    check_admin()

    add_artist = False

    artist = Artist.query.get_or_404(artistid)
    form = ArtistForm(obj=artist)
    if form.validate_on_submit():
        artist.artistid=form.artistid.data
        artist.email=form.email.data
        artist.artistName=form.artistName.data
        artist.age=form.age.data
        artist.birthplace=form.birthplace.data

        style=form.style.data
        style.Art_ists.append(artist)
        try:
            db.session.add(artist)
            db.session.commit()
            flash('You have successfully edited the artist.')
        except:
            # in case artist name already exists
            flash('Error: artist name already exists.')


        # redirect to the artists page
        return redirect(url_for('admin.list_artists'))

    form.artistid.data = artist.artistid
    form.email.data = artist.email
    form.artistName.data = artist.artistName
    form.age.data = artist.age
    form.birthplace.data = artist.birthplace
    return render_template('admin/artists/artist.html', add_artist=add_artist,
                           form=form, title="Edit Artist")


@admin.route('/artists/delete/<int:artistid>', methods=['GET', 'POST'])
@login_required
def delete_artist(artistid):
    """
    Delete a artist from the database
    """
    check_admin()

    artist = Artist.query.get_or_404(artistid)
    db.session.delete(artist)
    db.session.commit()
    flash('You have successfully deleted the artist.')

    # redirect to the artists page
    return redirect(url_for('admin.list_artists'))

    return render_template(title="Delete Artist")

# artwork views

@admin.route('/artworks', methods=['GET', 'POST'])
@login_required
def list_artworks():
    """
    List all artworks
    """
    check_admin()

    artworks = Artwork.query.all()

    return render_template('admin/artworks/artworks.html',
                           artworks=artworks, title="Artworks")


@admin.route('/artworks/add', methods=['GET', 'POST'])
@login_required
def add_artwork():
    """
    Add a artwork to the database
    """
    check_admin()

    add_artwork = True

    form = ArtworkForm()
    if form.validate_on_submit():
        creator=form.creator.data
        artwork = Artwork(artworkid=form.artworkid.data,
                                title=form.title.data,
                                artType=form.artType.data,
                                price=form.price.data,
                                yearMade=form.yearMade.data,
                                artist=creator)
        art_Category=form.art_Category.data
        art_Category.artCategory.append(artwork)
        try:
            #add artwork to the database
            db.session.add(artwork)
            db.session.commit()
            flash('You have successfully added a new artwork.')
        except:
            # in case artwork name already exists
            flash('Error: artwork name already exists.')

        # redirect to artworks page
        return redirect(url_for('admin.list_artworks'))

    # load artwork template
    return render_template('admin/artworks/artwork.html', action="Add",
                           add_artwork=add_artwork, form=form,
                           title="Add Artwork")


@admin.route('/artworks/edit/<int:artworkid>', methods=['GET', 'POST'])
@login_required
def edit_artwork(artworkid):
    """
    Edit a artwork
    """
    check_admin()

    add_artwork = False

    artwork = Artwork.query.get_or_404(artworkid)
    form = ArtworkForm(obj=artwork)
    if form.validate_on_submit():        
        artwork.artworkid=form.artworkid.data
        artwork.title=form.title.data
        artwork.artType=form.artType.data
        artwork.price=form.price.data
        artwork.yearMade=form.yearMade.data
        artwork.artist=form.creator.data

        art_Category=form.art_Category.data
        if art_Category:
            art_Category.artCategory.append(artwork) 
            db.session.commit()
            flash('You have successfully edited the artwork.')

        # redirect to the artworks page
        return redirect(url_for('admin.list_artworks'))
    form.artworkid.data=artwork.artworkid
    form.title.data=artwork.title
    form.artType.data=artwork.artType
    form.price.data=artwork.price
    form.creator.data=artwork.artist
    return render_template('admin/artworks/artwork.html', action="Edit",
                           add_artwork=add_artwork, form=form,
                           artwork=artwork, title="Edit Artwork")


@admin.route('/artworks/delete/<int:artworkid>', methods=['GET', 'POST'])
@login_required
def delete_artwork(artworkid):
    """
    Delete a artwork from the database
    """
    check_admin()

    artwork = Artwork.query.get_or_404(artworkid)
    db.session.delete(artwork)
    db.session.commit()
    flash('You have successfully deleted the artwork.')

    # redirect to the artworks page
    return redirect(url_for('admin.list_artworks'))

    return render_template(title="Delete Artwork")



@admin.route('/customers')
@login_required
def list_customers():
    """
    List all customers
    """
    check_admin()

    customers = Customer.query.all()
    return render_template('admin/customers/customers.html',
                           customers=customers, title='Customers')


@admin.route('/customers/assign/<int:id>', methods=['GET', 'POST'])
@login_required
def assign_customer(id):
    """
    Assign a artist and a art_category to an customer
    """
    check_admin()
    edit_customer = True
    customer = Customer.query.get_or_404(id)

    # prevent admin from being assigned a artist or art_category
    if customer.is_admin:
        abort(403)

    form = AssignCustomerForm(obj=customer)
    if form.validate_on_submit():

        preferredArtist = form.preferredArtist.data
        preferredArtist.artistPreferred.append(customer)
        preferredCategories = form.preferredCategories.data
        preferredCategories.categoryPreferred.append(customer)
        db.session.add(customer)
        db.session.commit()
        flash('You have successfully assigned a artist and art_category.')

        # redirect to the art_categories page
        return redirect(url_for('admin.list_customers'))

    return render_template('admin/customers/customer.html',edit_customer=edit_customer,
                           customer=customer, form=form,
                           title='Assign Customer')

    
@admin.route('/customers/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_customer(id):

    check_admin()

    customer = Customer.query.get_or_404(id)
    form = EditCustomerForm(obj=customer)
    if form.validate_on_submit(): 
        customer.expenditure = form.expenditure.data
        db.session.commit()
        flash('You have successfully edited the customer.')

        # redirect to the customers page
        return redirect(url_for('admin.list_customers'))
    form.expenditure.data=customer.expenditure

    return render_template('admin/customers/customer.html', action="Edit", form=form,
                           customer=customer, title="Edit Artwork")
