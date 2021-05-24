from app.forms import LoginForm, PostForm
from app import app
from flask import render_template,flash,redirect
from app.forms import LoginForm
from flask import url_for
from flask_login import current_user,login_user
from flask_login import logout_user
from app.models import Post, User
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from app.forms import RegistrationForm
from app import db
from datetime import datetime
from app.forms import EditProfile_form
from app.forms import EmptyForm

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    page=request.args.get('page',1,type=int)
    posts =current_user.followed_posts().paginate(page,app.config["POSTS_PER_PAGE"],False)
    next_url=url_for('index',page=posts.next_num) if posts.has_next else None
    prev_url=url_for('index',page=posts.prev_num) if posts.has_prev else None
    return render_template("index.html", title='Home Page', form=form,
                           posts=posts.items,next_url=next_url,prev_url=prev_url)
    
    
@app.route('/login',methods=["GET","POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            
            flash("invalid username or password")
            return redirect(url_for('login'))
        login_user(user,remember=form.remember_me.data)
        next_page=request.args.get("next")
        if not next_page or url_parse(next_page).netloc !='':
            next_page=url_for('index')
        return redirect(url_for('index'))
    return render_template('login.html',title="sign IN", form=form)
    r#eturn redirect(url_for())
    
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data,email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("congars for registration")
        return redirect(url_for('login'))
    return render_template('register.html',title="register",form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts=[
        {"author":user,"body":"Test post #1"},
        {"author":user,"body":"Test poset #2"}
    ]
    form=EmptyForm()
    return render_template("user.html",user=user,posts=posts,form=form)


@app.before_request
def before_reques():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.utcnow()
        db.session.commit()
        
@app.route("/edit_profile",methods=["GET","POST"])
@login_required
def edit_profile():
    form=EditProfile_form(current_user.username)
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash("your changes has been saved")
        return redirect(url_for("edit_profile"))
    elif request.method=="GET":
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
        return render_template("edit_profile.html",title="edit profile",
                               form=form)

@app.route("/follow/<username>",methods=["POST"])
@login_required
def follow(username):
    form=EmptyForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=username).first()
        if user is None:
            flash(f"User {username} not found")
            return redirect(url_for("index"))
        if user==current_user:
            flash("you cannot follow yourself !!")
            return redirect(url_for("user",username=username))
        current_user.follow(user)
        db.session.commit()
        flash(f"you are following {username}")
        return redirect(url_for("user",username=username))
    else:
        return redirect(url_for("index"))
    
@app.route('/unfollow/<username>',methods=["POST"])
@login_required
def unfollow(username):
    form=EmptyForm()
    if form.validate_on_submit():
        user=User.query.filter_by(username=username).first()
        if user is None:
            flash(f"user {username} not found")
            return redirect(url_for("index"))
        if user==current_user:
            flash("you cannot unfollow or follow yourself")
            return redirect(url_for("user",username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash(f"you are not following {username} ")
        return redirect(url_for("user",username=username))
    else:
        return redirect(url_for("index"))
    
    
@app.route('/explore')
@login_required
def explore():
    page=request.args.get("page",1,type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(page,app.config["POSTS_PER_PAGE"],False)
    next_url=url_for('explore',page=posts.next_num) if posts.has_next else None
    prev_url=url_for("explore",page=posts.prev_num) if posts.has_prev else None
    return render_template('index.html', title='Explore', posts=posts.items,
                          next_url=next_url,prev_url=prev_url )

