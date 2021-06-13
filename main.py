from flask import Flask,Flask, render_template,redirect,url_for
from flask import render_template,url_for,flash,redirect,request,Blueprint
from flask_login import login_user, current_user, logout_user, login_required

from forms import RegistrationForm, AddEntryForm
from models import db
from models import User, Entry
from forms import RegistrationForm,LoginForm,UpdateUserForm

from flask import Flask

import os
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash

app=Flask(__name__)

app.config['SECRET_KEY']='mysecret'
# SQLDATABASE SECTION
basedir=os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db=SQLAlchemy(app)
Migrate(app,db)

###########login configurations######################

login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)



class User(db.Model,UserMixin):
     __tablename__ = 'users'
     id = db.Column(db.Integer,primary_key=True)

     username = db.Column(db.String(64),unique=True,index=True)
     password_hash = db.Column(db.String(128))

     categorys = db.relationship('Entry',backref='owner',lazy=True)

     def __init__(self,username,password):

        self.username = username
        self.password_hash = generate_password_hash(password)

     def check_password(self,password):
        return check_password_hash(self.password_hash,password)

     def __repr__(self):
        return f"Username {self.username}"

class Entry(db.Model):

    users = db.relationship(User)

    id = db.Column(db.Integer,primary_key=True)

    category=db.Column(db.String(140),nullable=False)
    site_name = db.Column(db.String(140), unique=True,nullable=False)
    s_uname= db.Column(db.String(140), nullable=False)
    s_pwd=db.Column(db.String(140),nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self,category,site_name,s_uname,s_pwd,user_id):
        self.category=category
        self.site_name=site_name
        self.s_uname=s_uname
        self.s_pwd=s_pwd
        self.user_id = user_id

    def __repr__(self):
        return f"   {self.site_name}   , {self.s_uname}  ,  {self.s_pwd}     "





@app.route('/',methods=['GET','POST'])
def login():

    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user is not None and user.check_password(form.password.data)  :

            login_user(user)
            flash('Log in Success!')
            # next = request.args.get('next')
            #
            # if next ==None or not next[0]=='/':
            #     next = url_for('login')
            #
            # return redirect(next)
            # return redirect(url_for('add_entry'))
            return redirect(url_for('list_categories'))
            # return render_template('hi.html', username=form.username.data)

        elif user is None:

            return render_template('invalid_user.html', username=form.username.data)
            #
            #
        elif not user.check_password(form.password.data):
            return render_template('incorrect_password.html')


    return render_template('login.html',form=form)

@app.route('/register',methods=['GET','POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data,
                    password=form.password.data)

        db.session.add(user)
        db.session.commit()
        flash('Thanks for registration!')
        return redirect(url_for('login'))

    return render_template('register.html',form=form)




@app.route('/list_entries')
@login_required
def list_entries():
    entries= Entry.query.filter_by(user_id=current_user.id)
    return render_template('entry_list.html', entries=entries)

@app.route('/list_categories')
@login_required
def list_categories():
    # cats= Entry.query.filter_by(user_id=current_user.id,category=form)
    rows=db.session.query(Entry.category.distinct()).filter_by(user_id=current_user.id).all()
    cats = [i[0] for i in rows]
    return render_template('cat_list_home.html', cats=cats)

@app.route('/chosen_category/<val>')
@login_required
def chosen_category(val):
    # cats= Entry.query.filter_by(user_id=current_user.id,category=form)
    # cats=db.session.query(Entry.category.distinct()).filter_by(user_id=current_user.id).all()

    list_cat = Entry.query.filter_by(user_id=current_user.id, category=val)

    return render_template('chosen_cat.html', cat=val,list_cat=list_cat)
#
@app.route('/item_view/<item>')
@login_required
def item_view(item):
    return render_template('view_pwd.html', item=item)



@app.route('/del_entry/<site_name>/<uname>/<pwd>',methods=['GET','POST'])
@login_required
def del_entry(site_name,uname,pwd):
        print((uname))
        print((site_name))
        print((pwd))
        print(current_user.id)

        sn= site_name.replace(" ", "")
        un=uname.replace(" ", "")
        pw=pwd.replace(" ", "")

        entry_to_be_del = Entry.query.filter_by(user_id=current_user.id,site_name=sn,s_uname=un,s_pwd=pw).first()
        print(entry_to_be_del)


        if entry_to_be_del is not None:
            db.session.delete(entry_to_be_del)
            db.session.commit()
            flash('Entry has been deleted')
            return redirect(url_for('list_categories'))


        # else:
        #     return render_template('/invalid.html',id=id)


        item=site_name+", "+uname+", "+pwd
        return render_template('view_pwd.html',item=item)


# @app.route('/item_view/<item>')
# @login_required
# def item_view(item):
#     site_name=request.args.get('username')
#     return render_template('view_pwd.html', site_name=site_name)


@app.route('/add_entry',methods=['GET','POST'])
@login_required
def add_entry():
    form = AddEntryForm()
    if form.validate_on_submit():
        pwd_table_entry= Entry(category=form.category.data,
                    site_name=form.sitename.data,
                    s_uname=form.u_name.data,
                    s_pwd=form.u_pwd.data,
                    user_id=current_user.id
                            )
        db.session.add(pwd_table_entry)
        db.session.commit()
        return redirect(url_for("list_categories"))
    return render_template('add_entries.html', form=form)

# @app.route('/cat_list/<cat>',methods=['GET','POST'])
# @login_required
# def cat_list(cat):
#
#         list_cat= Entry.query.filter_by(user_id=current_user.id,category=cat)
#
#
#         return render_template('categories_final.html',list_cat=list_cat)



#
#
# # logout
@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("login"))

#
# # account (update UserForm)
# @app.route("/redirect")
# def redirect_url(default='index'):
#         return request.args.get('next') or \
#                request.referrer or \
#                url_for(default)

@app.route('/users_data')
@login_required
def users_list():
    users=User.query.all()

    return render_template('list.html',users=users)

#
# @users.route('/account',methods=['GET','POST'])
# @login_required
# def account():
#
#     form = UpdateUserForm()
#     if form.validate_on_submit():
#
#         if form.picture.data:
#             username = current_user.username
#             pic = add_profile_pic(form.picture.data,username)
#             current_user.profile_image = pic
#
#         current_user.username = form.username.data
#         current_user.email = form.email.data
#         db.session.commit()
#         flash('User Account Updated!')
#         return redirect(url_for('users.account'))
#
#     elif request.method == "GET":
#         form.username.data = current_user.username
#         form.email.data = current_user.email
#
#     profile_image = url_for('static',filename='profile_pics/'+current_user.profile_image)
#     return render_template('account.html',profile_image=profile_image,form=form)








if __name__ == '__main__':
    app.run(debug=True)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
