
Install The Following Modules:

1.Flask

2.Flask-Login

3.Flask-Admin

4.Flask-SQLALCHEMY

5.Flask-WTF

6.pymysql

7.Flask-Bcrypt


For Database,do the following steps:

Password should be 'password'

1.Create a database test on mysql;

2.Navigate to the flaskblog folder in project

3.Invoke Python and run the following:

from flaskblog import db

db.create_all()
