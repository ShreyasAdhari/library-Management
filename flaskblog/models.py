from flaskblog import db,login_manager,admin,bcrypt
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.sqla.view import func
from flask_login import UserMixin,current_user
import datetime

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):

    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(80),index=True,nullable=False)
    email = db.Column(db.String(120),unique=True,nullable=False)
    password = db.Column(db.String(120),nullable=False)
    books_taken = db.relationship('Transaction',backref="Email")

    def __repr__(self):
        return str(self.email)

    def is_accessible(self):
        return (current_user.name == 'admin' and current_user.is_authenticated)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))



class Transaction(db.Model):

    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(120),db.ForeignKey('user.email'),index=True,nullable=False)
    isbn = db.Column(db.String(20),db.ForeignKey('books.isbn'),nullable=False)
    book_name = db.Column(db.String(200),index=True,nullable=False)
    issue_date = db.Column(db.DateTime,default=datetime.datetime.now)
    due_date = db.Column(db.DateTime,default=lambda :(datetime.datetime.now() + datetime.timedelta(days=7)))
    returned = db.Column(db.Boolean,default=False)

    def is_accessible(self):
        return (current_user.name == 'admin' and current_user.is_authenticated)

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))








class Books(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(200), index=True, nullable=False)
    isbn = db.Column(db.String(20), index=True, nullable=False,unique=True)
    author = db.Column(db.String(120),index=True,nullable=False)
    books_isbn = db.relationship('Transaction', backref="ISBN")

    def __repr__(self):
        return self.isbn






class UserView(ModelView):
    column_exclude_list = ['password']
    form_columns = ['name','email','password']
    can_create = True
    can_edit = False
    can_delete = False
    column_searchable_list = ['email']

    def on_model_change(self, form, model, is_created):
        if is_created:
            model.password = bcrypt.generate_password_hash(model.password)


    def is_accessible(self):
        if current_user.is_authenticated :
            return current_user.name == 'admin'
        else: return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

class TransactionView(ModelView):
    can_create = True
    can_edit = False
    column_searchable_list = ['email']
    can_delete = False

    def is_accessible(self):
        if current_user.is_authenticated :
            return current_user.name == 'admin'
        else: return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))


class PendingView(ModelView):
    can_edit = False
    can_create = False
    column_editable_list = ['returned']
    can_delete = False
    column_searchable_list = ['email']


    def get_query(self):
        return self.session.query(self.model).filter(self.model.returned == False)

    def get_count_query(self):
        return self.session.query(func.count('*')).filter(self.model.returned == False)

    def is_accessible(self):
        if current_user.is_authenticated :
            return current_user.name == 'admin'
        else: return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))



class BookView(ModelView):
    can_edit = False
    form_columns = ['book_name','isbn','author']
    column_searchable_list = ['book_name']

    def is_accessible(self):
        if current_user.is_authenticated :
            return current_user.name == 'admin'
        else: return False

    def inaccessible_callback(self, name, **kwargs):
        # redirect to login page if user doesn't have access
        return redirect(url_for('login', next=request.url))

admin.add_view(UserView(User,db.session))
admin.add_view(TransactionView(Transaction,db.session,endpoint='first'))
admin.add_view(BookView(Books,db.session))
admin.add_view(PendingView(Transaction,db.session,'Pending',endpoint='second'))
