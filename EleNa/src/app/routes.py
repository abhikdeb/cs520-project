from EleNa.src.app import app
from flask import render_template, flash, redirect, url_for
from EleNa.src.app.forms import LoginForm
from flask_googlemaps import GoogleMaps
from flask_googlemaps import Map


@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Test_User_1'}
    # 42.375755, -72.519789
    # 42.350887, -72.528246
    # 42.395215, -72.531281
    map_view = Map(
        identifier="map_view",
        lat=42.375755,
        lng=-72.519789,
        zoom=13,
        # markers=[
        #     {
        #         'icon': 'http://maps.google.com/mapfiles/ms/icons/red-dot.png',
        #         'lat': 42.350887,
        #         'lng': -72.528246,
        #         'infobox': "<b>Source</b>"
        #     },
        #     {
        #         'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
        #         'lat': 42.395215,
        #         'lng': -72.531281,
        #         'infobox': "<b>Destination</b>"
        #     }
        # ],
        style="height:500px;width:750px;margin:10;",
        center_on_user_location=False  # Need to check user preferences
    )

    return render_template('index.html', title='Home Page', user=user, map_view=map_view)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)
