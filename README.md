# Grocery Store Web Application

## Introduction

This is a multi-user web application designed for buying and selling groceries. Users can browse and purchase various products from different sections, while administrators have the ability to create new sections and manage products. The application was developed as part of the requirements for a BS in Data Science and Application.

## Description

The Grocery Store web application consists of two interfaces: one for users and one for administrators.

### User Interface

- Users can search for products based on various criteria such as categories, product name, price, and expiry date.
- They can add products to their shopping carts and proceed to place orders.
- Users can view their full profiles, update their information, and review past orders.
- User registration and password reset functionalities are also available.

### Admin Interface

- Administrators can search for products based on name, quantity, expiry date, and categories.
- They have the authority to create, update, and delete product categories and manage products.
- Admins can also register new users and reset user passwords.

## Technology Stack

- Python Flask: Used for application logic.
- Jinja2: Responsible for HTML template generation.
- Bootstrap: Provides styling and a responsive user interface.
- SQLite and SQLAlchemy: Used for data storage and object-relational mapping.
- Flask Login: Implements user login functionality.
- Flask Restful: Enables the creation of API endpoints.
- Flask Session: Stores admin login data in session.
- Bcrypt: Used for password hashing.

## Database Schema

The application's database includes the following tables and their attributes:

- `section (id, name, image_url)`
- `product (id, name, brand, manufacturing_date, expiry_date, price, stock, image_url, section_id)`
- `user (id, name, username, password, email, mobile, address, city, state, pin)`
- `cart (id, user_id, product_id, quantity)`
- `order (id, user_id, order_date, total_amount)`
- `order_item (id, product_name, brand, manufacturing_date, expiry_date, price, quantity, order_id)`
- `admin (id, username, name, password, email)`

## API

API endpoints were created using the Flask-Restful library for the `section` and `product` tables to perform CRUD operations.

## References

- [Flask Documentation](https://flask.palletsprojects.com/en/2.3.x/)
- [Flask-Restful Documentation](https://flask-restful.readthedocs.io/en/latest/)
- [Flask-SQLAlchemy Documentation](https://flask-sqlalchemy.palletsprojects.com/en/3.0.x/)
- [Flask-Login Documentation](https://flask-login.palletsprojects.com/en/0.5.x/)
- [OpenAI ChatGPT](https://chat.openai.com)
- [Bootstrap](https://getbootstrap.com/)


