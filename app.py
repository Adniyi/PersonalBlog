from flask import Flask, render_template,request,redirect,url_for,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import LoginManager,login_required,current_user,login_user

app = Flask(__name__)
app.config['SECRET_KEY'] = "THIS IS MYSECRETEKEY"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///post.db"
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime(timezone=True), default=func.now())
    title = db.Column(db.String(120), nullable=False)
    header = db.Column(db.String(120), nullable=False)
    body = db.Column(db.Text, nullable=False)

with app.app_context():
    db.create_all()

name = "David"
password = "12345"




#User Section 
@app.route("/")
def index():
    posts = Posts.query.all()
    return render_template("index.html", posts=posts)


@app.route("/view/<int:id>")
def user_view(id):
    peptits = Posts.query.filter_by(id=id).first()
    return render_template("user_view.html", peptits = peptits)


# Adims Section
@app.route("/admin", methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        admin_name = request.form.get("admin-name")
        admin_password = request.form.get("admin-password")
        print(admin_name, admin_password)

        if name == admin_name and password == admin_password:
            return redirect(url_for('view'))
        else: 
            return render_template("admin.html")
    return render_template("admin.html")



@app.route("/admin/view")
def view():
    poes = Posts.query.all()
    return render_template("admin_view.html", poes=poes,  name=name)



@app.route("/admin/add", methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get("title")
        header = request.form.get("header")
        body = request.form.get("body")
        posts = Posts(title=title, header=header, body=body)
        db.session.add(posts)
        db.session.commit()

        return redirect(url_for('view'))

    return render_template("add.html")


@app.route("/base/<int:id>")
def base(id):
    postses = Posts.query.filter_by(id=id).first()
    return render_template("base.html", postses=postses)


#Editing Posts
@app.route("/admin/edit/<int:id>", methods=['GET', 'PATCH'])
def edit(id):
    post = Posts.query.get(id)
    if not post:
        return jsonify({'error': "No Post was found"}), 404
    
    if request.method == 'GET':
        # Render the edit form
        return render_template("edit.html", post=post)

    # Handle PATCH request
    data = request.get_json()
    if data is None:
        return jsonify({'error': "No data provided"}), 400

    post.title = data.get("title", post.title)
    post.header = data.get("header", post.header)
    post.body = data.get("body", post.body)

    db.session.commit()
    return jsonify({'message': 'Updated'})

# Deletes Posts
@app.route("/admin/delete/<int:id>")
def delete(id):
    powwing = Posts.query.filter_by(id=id).first()
    if not powwing:
        return "Post does not exist!"
    else:
        db.session.delete(powwing)
        db.session.commit()
        return redirect(url_for('view'))

if __name__=="__main__":
    app.run(debug=True)
