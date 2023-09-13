from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_session import Session
from model import *
from datetime import datetime
import os,re 
from werkzeug.utils import secure_filename
import bcrypt


# Create a Flask app
app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocery_app.sqlite3'
app.config['SECRET_KEY'] = "Msaligs_project"
app.config['SESSION_TYPE'] = 'filesystem'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = "its all about privacy to send flash"
UPLOAD_FOLDER = 'static'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Function to check if a file has an allowed extension
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Initialize the Flask-Session extension
Session(app)

# Initialize the login manager
login_manager = LoginManager()
login_manager.init_app(app)

# Initialize the database
db.init_app(app)
app.app_context().push()

# for api initialisation
from resources import *
from flask_cors import CORS

api.init_app(app)
CORS(app)


import bcrypt

def hash_password(password):
    # Generate a salt
    salt = bcrypt.gensalt()

    # Hash the password using the salt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)

    return hashed_password

def check_password(input_password, hashed_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), hashed_password)


# ===============================================================================================
# ============================form input validation==============================================
def validate_name(name):
    name = name.strip()
    # Check if the name contains only alphabetic characters and spaces
    if not all(char.isalpha() or char.isspace() for char in name):
        return False
    
    # Check if the name length is within a reasonable range (e.g., 2 to 50 characters)
    if len(name) < 5 or len(name) > 35:
        return False
    
    return True


def validate_username(username):
    # Add your validation logic for username here
    if not (4 <= len(username) <= 10) or not re.match('^[a-zA-Z0-9_]*$', username) :
        return False
    return True

def validate_password(password):
    # Add your validation logic for password here
    if not (6 <= len(password) <= 20) or not password.isalnum():
        return False
    return True

def validate_email(email):
    # Use a regular expression pattern for basic email format validation
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    if re.match(pattern, email):
        return True
    else:
        return False

def validate_mobile(mobile):
    #validation logic for mobile here
    if not mobile.isdigit() or len(mobile) < 10 or  len(mobile) >13:
        return False
    return True

def validate_city(city):
    # Validation logic for state using regular expression
    pattern = r'^[a-zA-Z\s]{1,25}$'
    
    if re.match(pattern, city):
        return True
    else:
        return False

def validate_state(state):
    # Validation logic for state using regular expression
    pattern = r'^[a-zA-Z\s]{1,25}$'
    
    if re.match(pattern, state):
        return True
    else:
        return False


def validate_pin(pin):
    # Remove any spaces or non-digit characters
    pin = ''.join(filter(str.isdigit, pin))
    
    # Check if the PIN code is 6 digits long
    if len(pin) != 6:
        return False
    
    return True





# Load a user from the database using the user ID stored in the session
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Registration route
@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == 'POST':
        # Extract user registration details from the form
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pin = request.form.get('pin')

        
        if  not validate_name(name):
            flash("Name can be alphabet only and between 5 ,35 charcater.", "warning")
            return render_template("registration.html")

        # Validate username format
        if not validate_username(username):
            flash("Username must be between 4 and 10 characters and contain only letters, numbers, and underscores.", "warning")
            return render_template("registration.html")
        
        # Validate password 
        if not validate_password(password):
            flash("Password must be between 6 and 20 characters and can only contain alphabet and numbers.", "warning")
            return render_template("registration.html")
        
        # Validate eamil
        if not validate_email(email):
            flash("Invalid Email address.", "warning")
            return render_template("registration.html")

        # Validate mobile number format
        if not validate_mobile(mobile):
            flash("Invalid mobile number .", "warning")
            return render_template("registration.html")
        
        # Validate city
        if not validate_city(city):
            flash("Invalid city name .", "warning")
            return render_template("registration.html")
        
        # Validate state
        if not validate_state(state):
            flash("Invalid state name .", "warning")
            return render_template("registration.html")
        
        # Validate pin
        if not validate_pin(pin):
            flash("Invalid PIN number .", "warning")
            return render_template("registration.html")
        
        username_check = User.query.filter_by(username = username).first()
        email_check = User.query.filter_by(email = email).first()
        mobile_check = User.query.filter_by(mobile = mobile).first()

        if username_check:
            flash(f" Username '{username}' already exist","danger")
            return render_template("registration.html")
        
        if email_check:
            flash(f" Email '{email}' already exist","danger")
            return render_template("registration.html")
        
        if mobile_check:
            flash(f" Mobile '{mobile}' already exist","danger")
            return render_template("registration.html")


        # Create and add user to the database
        user = User(name=name, username=username, password=hash_password(password), email=email, mobile=mobile, address=address, city=city, state=state, pin=pin)
        db.session.add(user)
        try:
            db.session.commit()
            flash("You have registered successfully, please login to continue!", "success")
            return redirect('login')
        except Exception as e:
            db.session.rollback()
            flash("Unable to register. Please check your details and try again.", "danger")
            return render_template("registration.html")

    return render_template('registration.html')

# Update profile route
@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        # Update user details in the database
        user = User.query.get(current_user.id)

        name = request.form.get('name')
        email = request.form.get('email')
        mobile = request.form.get('mobile')
        address = request.form.get('address')
        city = request.form.get('city')
        state = request.form.get('state')
        pin = request.form.get('pin')

# validation of data
        if  not validate_name(name):
            flash("Name can be alphabet only and between 5 ,35 charcater.", "warning")
            return render_template('update_profile.html', user=current_user)
        
        # Validate eamil
        if not validate_email(email):
            flash("Invalid Email address.", "warning")
            return render_template('update_profile.html', user=current_user)

        # Validate mobile number format
        if not validate_mobile(mobile):
            flash("Invalid mobile number .", "warning")
            return render_template('update_profile.html', user=current_user)
        
        # Validate city
        if not validate_city(city):
            flash("Invalid city name .", "warning")
            return render_template('update_profile.html', user=current_user)
        
        # Validate state
        if not validate_state(state):
            flash("Invalid state name .", "warning")
            return render_template('update_profile.html', user=current_user)
        
        # Validate pin
        if not validate_pin(pin):
            flash("Invalid PIN number .", "warning")
            return render_template('update_profile.html', user=current_user)
        
        if user.email != email:
            email_check = User.query.filter_by(email = email).first()
            if email_check:
                flash(f" Email '{email}' already exist","danger")
                return render_template('update_profile.html', user=current_user)

        if user.mobile != int(mobile):
            mobile_check = User.query.filter_by(mobile = mobile).first()
            if mobile_check:
                flash(f" Mobile '{mobile}' already exist","danger")
                return render_template('update_profile.html', user=current_user)

        user.name = name
        user.email = email
        user.mobile = int(mobile)
        user.address = address
        user.city = city
        user.state = state
        user.pin = pin

        try:
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect('user_card')
        except Exception as e:
            flash("Something went wrong while updating profile, please Try again!")
            return render_template('update_profile.html', user=current_user)

    return render_template('update_profile.html', user=current_user)

# User login route
@app.route('/login', methods=['GET', 'POST'])
def user_login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate username format
        if not validate_username(username):
            flash("Username is not correct.", "warning")
            return render_template('login.html')
        
        # Validate password 
        if not validate_password(password):
            flash("Password is not correct.", "warning")
            return render_template('login.html')
        
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password(password,user.password):
            # if user.password == password:
                login_user(user)
                flash("Logged in  successfully!", "success")
                # return redirect(url_for('index'))
                return redirect(request.referrer)
            else:
                flash("Wrong password", 'danger')
                return render_template('login.html')
        else:
            flash("Wrong username", 'danger')
            return render_template('login.html')

    cartItems = Cart.query.all()
    return render_template('login.html', cartItems=cartItems)

# User logout route
@app.route('/logout')
@login_required
def user_logout():
    logout_user()
    flash("Logged out  successfully!", "info")
    return redirect('/')

# Forgot password route
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        new_password = request.form.get('new_password')
        

        # Validate username format
        if not validate_username(username):
            flash("Username is not correct.", "warning")
            return render_template('forgot_password.html')
        
        # Validate eamil
        if not validate_email(email):
            flash("Invalid Email address.", "warning")
            return render_template('forgot_password.html')
        
        # Validate password 
        if not validate_password(new_password):
            flash("Password must be between 6 and 20 characters and can only contain alphabet and numbers.", "warning")
            return render_template('forgot_password.html')

        user = User.query.filter_by(email=email).first()
        if user and (user.username == username):
            user.password = hash_password(new_password)
            try:
                db.session.commit()
                flash("Password reset successfully, Please login now!", 'success')
                return redirect('login')
            except:
                flash("Ops! Unable to reset, please try again", 'danger')
                return render_template('forgot_password.html')
        else:
            flash("You have entered invalid details", 'danger')
            return render_template('forgot_password.html')
    return render_template('forgot_password.html')

# Home page route
@app.route('/', methods=['GET', 'POST'])
def index():
    sections = Section.query.all()
    cartItems = []

    if current_user.is_authenticated:
        cartItems = Cart.query.all()

    return render_template('index.html', sections=sections, cartItems=cartItems)


# #####################################################################################
#######################################################################################
@app.route('/products/<int:id>', methods=['GET', 'POST'])
def products(id):
    # Display products based on section ID chosen by the user
    products = Product.query.filter_by(section_id=id).all()
    products = sorted(products, key=lambda product: product.id, reverse=True)
    section = Section.query.get(id)
    cartItems = Cart.query.all()
    return render_template('products.html', products=products, section_name=section.name, cartItems=cartItems)


@app.before_request
def before_request():
    # Check if the user is not authenticated and the current endpoint requires login
    if not current_user.is_authenticated and request.endpoint in ['addtocart']:
        # Redirect the user to the login page
        return redirect(url_for('user_login'))


@app.route('/addtocart', methods=['POST'])
@login_required
def addtocart():
    if request.method == 'POST':
        # Get product and quantity for adding to cart
        product_id = request.form.get('prod_id')
        quantity = int(request.form.get('quantity'))

        # validating quantity 
        if quantity <1:
            flash("something is wrong with quantity", 'warning')

        # Fetching the product details
        prod = Product.query.get(product_id)

        # Check if product is already in cart
        cart = Cart.query.filter_by(user_id=current_user.id, product_id=product_id).first()

        if cart:
            # If the product is already in the cart, update the quantity
            prod.stock += cart.quantity
            cart.quantity = quantity
            prod.stock -= quantity 

        else:
            # If the product is not in the cart, create a new cart entry
            cart = Cart(user_id=current_user.id, product_id=product_id, quantity=quantity)
            prod.stock -= quantity 
            db.session.add(cart)


        try:
            db.session.commit()

            flash("Item added to cart successfully", "success")
            return redirect( url_for('index'))
            # return redirect(request.referrer)
        except Exception as e:
            flash("Something went wrong", "warning")
            return redirect(request.referrer or url_for('index'))


@app.route('/remove/<int:id>', methods=['GET', 'POST'])
@login_required
def remove(id):
    item = Cart.query.get(id)

    if item is not None:
        # Updating the stock
        prod = Product.query.get(item.product_id)
        prod.stock = prod.stock + item.quantity

        db.session.delete(item)
        try:
            db.session.commit()
            flash("Product removed successfully", "info")
            return redirect(request.referrer or url_for('index'))
        except Exception as e:
            flash("Somewhere something went wrong!")
            return redirect(request.referrer or url_for('index'))
    else:
        return "Item not found in the cart."


@login_required
def get_cart_details():
    products = []
    total_amount = 0
    cart_items = Cart.query.all()
    for item in cart_items:
        prod = Product.query.get(item.product_id)
        products.append((prod, item.quantity, item.id))
        total_amount += prod.price * item.quantity

    return products, cart_items, total_amount


@app.route('/cart_details', methods=['GET', 'POST'])
def cart_details():
    products, cart_items, total_amount = get_cart_details()
    user = User.query.get(current_user.id)
    return render_template('cart_details.html',user =user, products=products, cartItems=cart_items, total_amount=total_amount)


@app.route('/place_order', methods=['GET', 'POST'])
@login_required
def place_order():
    cart_items = Cart.query.all()
    products, cart_items, total_amount = get_cart_details()

    order = Order(user_id=current_user.id,
                  order_date=datetime.now(),
                  total_amount=total_amount)
    db.session.add(order)
    try:
        db.session.commit()
        for item in cart_items:
            prod = Product.query.get(item.product_id)
            order_item = Order_item(prod_name=prod.name, brand=prod.brand,
                                    manufacturing_date=prod.manufacturing_date,
                                    expiry_date=prod.expiry_date,
                                    price=prod.price, quantity=item.quantity,
                                    order_id=order.id)
            db.session.delete(item)
            db.session.add(order_item)
        try:
            db.session.commit()
            flash("Order placed successfully!", "success")
            return redirect(url_for('index'))
        except Exception as e:
            msg = "There is a problem with your account while placing the order"
            return render_template("error.html", error=msg)

    except Exception as e:
        msg = "There is a problem while placing the order"
        return render_template("error.html", error=msg)


@app.route('/order_history', methods=['GET', 'POST'])
@login_required
def order_history():
    orders = Order.query.filter_by(user_id=current_user.id).all()
    orders = sorted(orders, key=lambda order: order.id, reverse=True)
    return render_template('order_history.html', orders=orders)


@app.route('/order_history_details/<int:id>', methods=['GET', 'POST'])
@login_required
def order_history_details(id):
    order_item = Order_item.query.filter_by(order_id=id).all()
    return render_template('order_history_details.html', order_items=order_item)


@app.route('/user_card', methods=['GET'])
@login_required
def user_card():
    user = User.query.get(current_user.id)
    return render_template('user_card.html', user=user)

@app.route('/search', methods = ['POST'])
def search():
    if request.method == 'POST':
        search_criteria = request.form.get('search_criteria')

        if search_criteria == 'product_name':
            q = request.form.get('product_name_input')
            if q.isalpha():
                query = "%" + q + "%"
                flash("product with name :" +q,"info")
                results = Product.query.filter(Product.name.like(query)).all()
            else:
                flash("Please enter correct string",'warning')
                return redirect(request.referrer)

        elif search_criteria == 'price':
            max_price = request.form.get('price_input')
            if max_price.isnumeric() and float(max_price) >0:
                flash("product with maximum price :" +max_price,"info")
                results = Product.query.filter(Product.price < max_price).all()
            else:
                flash("Please enter correct Price",'warning')
                return redirect(request.referrer)

        elif search_criteria == 'expire_after':
            date = datetime.strptime(request.form.get('expire_after_input'), '%Y-%m-%d').date()
            flash("product with expiry date :" +str(date),"info")
            results = Product.query.filter(Product.expiry_date >= date).all()

        return render_template('products.html', products=results, search = True)


# admin section   ##########################################################################

@app.route('/admin_search', methods=['GET', 'POST'])
def admin_search():
    admin_id = session.get('admin_id')
    if admin_id:
        if request.method == 'POST':
            search_criteria = request.form.get('search_criteria')

            if search_criteria == 'product_name':
                q = request.form.get('product_name_input')
                if q.isalnum():
                    query = "%" + q + "%"
                    flash("Product with name :" +q,"info")
                    results = Product.query.filter(Product.name.like(query)).all()
                else:
                    flash("Please enter correct string",'warning')
                    return redirect(request.referrer)
            elif search_criteria == 'stock':
                stock_input = request.form.get('stock_input')
                if stock_input == '100plus':
                    stock = "more than Rs 100"
                    results = Product.query.filter(Product.stock > 100).all()
                elif stock_input == '100minus':
                    stock = "less than Rs 100"
                    results = Product.query.filter(Product.stock < 100).all()
                elif stock_input == '10minus':
                    stock = "less than Rs 10"
                    results = Product.query.filter(Product.stock < 10).all()
                elif stock_input == 'out_of_stock':
                    stock = "0"
                    results = Product.query.filter(Product.stock == 0).all()
                flash("product with stock " +stock,"info")

            elif search_criteria == 'expire_before':
                date = datetime.strptime(request.form.get('expire_before_input'), '%Y-%m-%d').date()
                flash("product that expire before "+str(date),"info")
                results = Product.query.filter(Product.expiry_date <= date).all()

            return render_template('admin_search.html', products=results)

    flash('Please login first', 'info')
    return redirect('admin_login')


@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    admin_id = session.get('admin_id')
    if admin_id:
        return redirect(url_for('admin_section'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Validate username format
        if not validate_username(username):
            flash("Username is not correct.", "warning")
            return render_template('admin_login.html')
        
        # Validate password 
        if not validate_password(password):
            flash("Password is not correct.", "warning")
            return render_template('admin_login.html')

        admin = Admin.query.filter_by(username=username).first()

        if admin and check_password(password,admin.password):
            session['admin_id'] = admin.id
            flash("Admin logged in successfully", "success")
            return redirect(url_for('admin_section'))

        else:
            flash("Invalid credentials", "danger")
            return render_template('admin_login.html')

    return render_template('admin_login.html')


@app.route('/admin_logout')
def admin_logout():
    session.pop('admin_id', None)
    return redirect(url_for('index'))


@app.route('/admin_registration', methods=['GET', 'POST'])
def admin_registration():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        email = request.form.get('email')
        
        if  not validate_name(name):
            flash("Name can be alphabet only and between 5 ,35 charcater.", "warning")
            return render_template("admin_registration.html")

        # Validate username format
        if not validate_username(username):
            flash("Username must be between 4 and 10 characters and contain only letters, numbers, and underscores.", "warning")
            return render_template("admin_registration.html")
        
        # Validate password 
        if not validate_password(password):
            flash("Password must be between 6 and 20 characters and can only contain alphabet and numbers.", "warning")
            return render_template("admin_registration.html")
        
        # Validate eamil
        if not validate_email(email):
            flash("Invalid Email address.", "warning")
            return render_template("admin_registration.html")

        username_check = Admin.query.filter(func.lower(Admin.username) == username.lower()).first()
        email_check = Admin.query.filter(func.lower(Admin.email) == email.lower()).first()

        
        if username_check:
            flash(f" Username '{username}' already exist","warning")
            return render_template("admin_registration.html")
        if email_check:
            flash(f" Email '{email}' already exist","warning")
            return render_template("admin_registration.html")
        
        admin = Admin(name=name, username=username, password=hash_password(password), email=email)
        db.session.add(admin)
        try:
            db.session.commit()
            flash("Admin registered successfully. Please login now!", 'success')
            return redirect('admin_login')
        except Exception as e:
            flash("Something went wrong. Please try again!", "danger")
            return render_template('admin_registration.html')

    return render_template('admin_registration.html')


@app.route('/admin_forgot_password', methods=['GET', 'POST'])
def admin_forgot_password():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        new_password = request.form.get('new_password')

        # Validate username format
        if not validate_username(username):
            flash("Username is not correct", "warning")
            return render_template("registration.html")
        
        # Validate eamil
        if not validate_email(email):
            flash("Invalid Email address.", "warning")
            return render_template("registration.html")
        
        # Validate password 
        if not validate_password(new_password):
            flash("Password must be between 6 and 20 characters and can only contain alphabet and numbers.", "warning")
            return render_template("registration.html")

        admin = Admin.query.filter_by(email=email).first()

        if admin and (admin.username == username):
            admin.password = hash_password(new_password)

            try:
                db.session.commit()
                flash("Password reset successfully. Please login now!", 'success')
                return redirect('admin_login')
            except:
                flash("Unable to reset password. Please try again.", 'danger')
                return render_template('admin_forgot_password.html')

        else:
            flash("Invalid details entered.", 'danger')
            return render_template('admin_forgot_password.html')

    return render_template('admin_forgot_password.html')


@app.route('/admin_section', methods=['GET', 'POST'])
def admin_section():
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        sections = Section.query.all()
        return render_template('admin_sections.html', sections=sections)
    else:
        return redirect(url_for('admin_login'))


@app.route('/new_section', methods=['GET', 'POST'])
def new_section():
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)

        if request.method == 'POST':
            name = request.form.get('name')
            image = request.files.get('image')

            if image and allowed_file(image.filename):
                image_filename = secure_filename(image.filename)
                image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
                image.save(image_path)
                section = Section(name=name, image_url=image_filename)
                db.session.add(section)

                try:
                    db.session.commit()
                    flash("New category added successfully!", "success")
                    return redirect(url_for('admin_section'))
                except Exception as e:
                    msg = "Problem while creating a new section"
                    return render_template("error.html", error=msg)

        return render_template('new_section.html')
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_section/<int:id>', methods=['GET', 'POST'])
def delete_section(id):
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        section = Section.query.get(id)
        db.session.delete(section)

        try:
            db.session.commit()
            flash("Category deleted successfully!", "danger")
            return redirect(url_for('admin_section'))
        except Exception as e:
            msg = "Problem while deleting the section"
            return render_template("error.html", error=msg)

    return redirect(url_for('admin_login'))


@app.route('/update_section/<int:id>', methods=['GET', 'POST'])
def update_section(id):
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        section = Section.query.get(id)

        if request.method == 'POST':
            section.name = request.form.get('name')

            try:
                db.session.commit()
                flash("Section updated successfully!", "info")
                return redirect(url_for('admin_section'))
            except Exception as e:
                msg = "Problem while updating the section"
                return render_template("error.html", error=msg)

        return render_template('update_section.html', section=section)
    else:
        return redirect(url_for('admin_login'))

@app.route('/section_details/<int:id>', methods=['GET', 'POST'])
def section_details(id):
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        section = Section.query.get(id)
        products = Product.query.filter_by(section_id=id).all()
        return render_template('section_details.html', products=products, section=section)
    else:
        return redirect(url_for('admin_login'))


@app.route('/update_product/<int:id>', methods=['GET', 'POST'])
def update_product(id):
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        product = Product.query.get(id)

        if request.method == 'POST':
            name = request.form.get('name')
            brand = request.form.get('brand')
            manufacturing_date = datetime.strptime(request.form.get('manufacturing_date'), '%Y-%m-%d').date()
            expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date()
            price = request.form.get('price')
            stock = request.form.get('stock')
            section_id = request.form.get('section')

            if manufacturing_date >= expiry_date:
                flash("expiry date can not be before the manufacuring date",'warning')
                return render_template('add_product.html', section_id=id)
            
            if int(stock) <0:
                flash("Invalid stock",'warning')
                return render_template('add_product.html', section_id=id)
            
            if float(price) <1.0:
                flash("Invalid Price",'warning')
                return render_template('add_product.html', section_id=id)

            product.name = name
            product.brand = brand
            product.manufacturing_date = manufacturing_date
            product.expiry_date = expiry_date
            product.price =float(price)
            product.stock = int(stock)
            product.section_id = section_id

            try:
                db.session.commit()
                flash("Product has been updated successfully!", "info")
                return redirect(url_for('section_details', id=product.section_id, _external=True))
            except Exception as e:
                flash("There is a problem while updating the product", "danger")
                return render_template("update_product.html")
        else:
            sections = Section.query.all()
            return render_template('update_product.html', product=product, sections=sections)
    else:
        return redirect(url_for('admin_login'))


@app.route('/delete_product/<int:id>', methods=['GET', 'POST'])
def delete_product(id):
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)
        product = Product.query.get(id)

        db.session.delete(product)
        try:
            db.session.commit()
            flash("Product has been deleted successfully!", "danger")
            return redirect(url_for('section_details', id=product.section_id, _external=True))
        except Exception as e:
            msg = "There is a problem while deleting the product"
            return render_template("error.html", error=msg)
    else:
        return redirect(url_for('admin_login'))


@app.route('/add_product/<int:id>', methods=['GET', 'POST'])
def add_product(id):
    admin_id = session.get('admin_id')
    if admin_id:
        admin = Admin.query.get(admin_id)

        if request.method == 'POST':
            name = request.form.get('name')
            brand = request.form.get('brand')
            manufacturing_date = datetime.strptime(request.form.get('manufacturing_date'), '%Y-%m-%d').date()
            expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d').date()
            price = float(request.form.get('price'))
            stock = int(request.form.get('stock'))

            if manufacturing_date >= expiry_date:
                flash("expiry date can not be before the manufacuring date",'warning')
                return render_template('add_product.html', section_id=id)
            
            if stock <0:
                flash("Invalid stock",'warning')
                return render_template('add_product.html', section_id=id)
            
            if price <1:
                flash("Invalid Price",'warning')
                return render_template('add_product.html', section_id=id)

            new_product = Product(
                name=name,
                brand=brand,
                manufacturing_date=manufacturing_date,
                expiry_date=expiry_date,
                price=price,
                stock=stock,
                section_id=id
            )
            db.session.add(new_product)
            try:
                db.session.commit()
                flash("New Product added successfully!", "success")
                return redirect(url_for('section_details', id=id, _external=True))
            except Exception as e:
                msg = "There is a problem while adding the new product"
                return render_template("error.html", error=msg)
        else:
            return render_template('add_product.html', section_id=id)
    else:
        return redirect(url_for('admin_login'))

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
