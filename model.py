from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint,func
from flask_login import LoginManager,UserMixin,login_user,logout_user,current_user,login_required

db = SQLAlchemy()

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(), nullable=False, unique=True)
    image_url = db.Column(db.String())
    
    products = db.relationship('Product', backref='section', cascade='all, delete-orphan')

     


class Product(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    name = db.Column(db.String(),nullable = False)
    brand = db.Column(db.String(),nullable = False)
    manufacturing_date = db.Column(db.Date(), nullable = False)
    expiry_date = db.Column(db.Date(), nullable = False)
    price = db.Column(db.Float(),nullable = False)
    stock = db.Column(db.Integer,nullable = False)
    image_url = db.Column(db.String())
    # section_id = db.Column(db.Integer,db.ForeignKey("section.id"), nullable = False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id", ondelete="CASCADE"), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    username = db.Column(db.String(10), nullable=False, unique=True)
    password = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(20), nullable=False, unique=True)
    mobile = db.Column(db.Integer, nullable=False, unique=True)
    address = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(10),nullable = False)
    state = db.Column(db.String(15),nullable = False)
    pin = db.Column(db.Integer, nullable=False)

    __table_args__ = (
        db.Index('idx_user_username', username),
        db.Index('idx_user_email', email)
    )



class Cart(db.Model):
    id = db.Column(db.Integer(),primary_key = True)
    user_id = db.Column(db.Integer(),db.ForeignKey("user.id"))
    product_id = db.Column(db.Integer,db.ForeignKey("product.id"),nullable = False, unique = True)
    quantity = db.Column(db.Integer, default = 1)

    
class Order(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    order_date = db.Column(db.Date(), nullable = False)
    total_amount = db.Column(db.Float(),nullable = False)
    
    user = db.relationship('User',backref='order')
    
class Order_item(db.Model):
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    prod_name = db.Column(db.String(),nullable = False)
    brand = db.Column(db.String(),nullable = False)
    manufacturing_date = db.Column(db.Date(), nullable = False)
    expiry_date = db.Column(db.Date(), nullable = False)
    price = db.Column(db.Float(),nullable = False)
    quantity = db.Column(db.Integer,nullable = False)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'))
    
    Order = db.relationship('Order',backref='order_items')


class Admin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)



    