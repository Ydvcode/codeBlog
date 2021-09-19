from flask_pro import app
from flask import render_template,redirect, url_for, flash, get_flashed_messages
from flask_pro.Model import Base, User
from flask_pro.forms import RegisterForm, LoginForm
from flask_pro import db
from flask_login import login_user, logout_user, login_required
@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/flask')
@login_required
def flask_page():
    items = Base.query.all()
    return render_template('flask.html', items=items)

@app.route('/register', methods=['GET','POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = User(user_name=form.username.data,
                              email_address=form.email.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account Created Successfully! You are now logged in as {user_to_create.user_name}", category='Success')
        return redirect(url_for('login_page'))
    if form.errors != {}:
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user :{err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(user_name=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: { attempted_user.user_name}', category='Success')
            return redirect(url_for('flask_page'))

#    else:
#        flash('Username and Password are not match! Please Try Again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash('You have been Logged out', category='info')
    return redirect(url_for('home_page'))