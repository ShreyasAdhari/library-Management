from flask import Flask,render_template,redirect,url_for,flash,request
from flaskblog.forms import LoginForm,RegForm
from flaskblog import app,bcrypt,db
from flaskblog.models import User,Transaction
from flask_login import login_user,logout_user,current_user,login_required

@app.route('/',methods=['GET','POST'])
def home():

    if current_user.is_authenticated:

        if current_user.name=='admin':
            return redirect('/admin')

        return redirect(url_for('account'))

    form = RegForm()

    if form.validate_on_submit():
        u = User(name=form.name.data,email=form.email.data,password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'))
        db.session.add(u)
        db.session.commit()
        flash('Account Created Successfully !')

    return render_template('home.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():

    if current_user.is_authenticated:

        if current_user.name=='admin':
            return redirect('/admin')

        return redirect(url_for('account'))

    form = LoginForm()

    if form.validate_on_submit():

        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user)

            if current_user.name == 'admin':
                return redirect('/admin')

            next_page = request.args.get('next')
            return redirect(url_for(next_page[1:])) if next_page else redirect(url_for('account'))

        else : flash('Username or Password is Incorrect.')





    return render_template('login.html' ,form=form)


@app.route('/account')
@login_required
def account():
    if current_user.name == 'admin':
        return redirect('/admin')

    return render_template('account.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/issued_user')
@login_required
def issued_user():
    if current_user.name == 'admin':
        return redirect('/admin')

    books_issued = Transaction.query.filter_by(email=current_user.email).all()

    return render_template('issued_user.html',books_issued=books_issued)


@app.route('/pending_user')
@login_required
def pending_user():

    if current_user.name == 'admin':
        return redirect('/admin')

    books_pending = Transaction.query.filter_by(email=current_user.email).filter_by(returned=False).all()

    return render_template('pending_user.html',books_pending = books_pending)

