from flask_restful import Api, Resource, reqparse,fields,marshal_with
from model import *
from datetime import datetime

api = Api()

section_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'image_url': fields.String
}
class Api_section(Resource):
    def get(self):
        all_sections = {}
        sections = Section.query.all()
        for sec in sections:
            s = [sec.name,sec.image_url]
            all_sections[sec.id] = s
        return all_sections
    

    def delete(self,id):
        section = Section.query.get(id)
        if section:
            db.session.delete(section)
            try:
                db.session.commit()
                return {'status': 'Section deleted successfully'}, 204
            except Exception as e:
                return {'status': 'something bad happened'},500
        else:
            return {'status': 'Section not found'}, 404
        

    @marshal_with(section_fields)    
    def put(self,id):
        section = Section.query.get(id)
        if section:
            parser = reqparse.RequestParser()
            parser.add_argument('name',type=str,required= True)
            parser.add_argument('image_url',type=str)
            args = parser.parse_args()

            section.name = args['name']
            section.image_url = args['image_url']
            try:
                db.session.commit()
                # return {'status': 'Section updated successfully'}, 200
                return section, 200
            except Exception as e:
                db.session.rollback()
                return {'status': "Something goes wrong"}, 500    
        else:
            return {'status': 'Section not found'}, 404
      
        
    @marshal_with(section_fields)    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',type=str,required= True)
        parser.add_argument('image_url',type=str)
        args = parser.parse_args()

        # Check if the section name is already taken
        existing_section = Section.query.filter_by(name=args['name']).first()
        if existing_section:
            return {'status': 'Section name already exists'}, 409
    
        sec = Section(name = args['name'],
                      image_url = args['image_url'])
        db.session.add(sec)
        try:
            db.session.commit()
            return sec,201
        except Exception as e:
            db.session.rollback()
            return {'status': "something goes wrong"}, 500
             
api.add_resource(Api_section,
                 "/api/all_sections", 
                 "/api/delete_section/<int:id>",
                 "/api/update_section/<int:id>",
                 "/api/create_section")


# #========================================== for products==============================
product_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'brand': fields.String,
    'manufacturing_date': fields.String(attribute=lambda x: x.manufacturing_date.isoformat() if x.manufacturing_date else None),
    'expiry_date': fields.String(attribute=lambda x: x.expiry_date.isoformat() if x.expiry_date else None),
    'price': fields.Float,
    'stock': fields.Integer,
    'image_url': fields.String,
    'section_id': fields.Integer
}


class Api_product(Resource):
    @marshal_with(product_fields)
    def get(self, product_id):
        product = Product.query.get(product_id)
        if not product:
            return {"status": "product not found"}, 404
        return product
        
    
    def delete(self,product_id):
        prod = Product.query.get(product_id)
        if prod:
            db.session.delete(prod)
            try:
                db.session.commit()
                return {'status': 'Product deleted successfully'}, 204
            except Exception as e:
                return {'status': 'Something bad happened'}, 500
        else:
            return {'status': 'Product not found'}, 404
        

    @marshal_with(product_fields)    
    def put(self,product_id):
        product = Product.query.get(product_id)
        if product:
            parser = reqparse.RequestParser()
            parser.add_argument('name', type=str)
            parser.add_argument('brand', type=str)
            parser.add_argument('manufacturing_date', type=str)
            parser.add_argument('expiry_date', type=str)
            parser.add_argument('price', type=float)
            parser.add_argument('stock', type=int)
            parser.add_argument('image_url', type=str)
            parser.add_argument('section_id', type=int)
            args = parser.parse_args()
        
            if args['name']:
                product.name = args['name']
            if args['brand']:
                product.brand = args['brand']
            if args['manufacturing_date']:
                print(type(args['manufacturing_date']))
                manufacturing_date = datetime.strptime(args['manufacturing_date'], '%Y-%m-%d').date()
                product.manufacturing_date = manufacturing_date
            if args['expiry_date']:
                expiry_date = datetime.strptime(args['expiry_date'], '%Y-%m-%d').date()
                product.expiry_date = expiry_date
            if args['price']:
                product.price = args['price']
            if args['stock']:
                product.stock = args['stock']
            if args['image_url']:
                product.image_url = args['image_url']
            if args['section_id']:
                product.section_id = args['section_id']
        
            try:
                db.session.commit()
                # return product,200
                return product, 200
            except Exception as e:
                db.session.rollback()
                return {'status': "Something goes wrong"}, 500    
        else:
            return {'status': 'Product not found'}, 404


    @marshal_with(product_fields)    
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('brand', type=str, required=True)
        parser.add_argument('manufacturing_date', type=str, required=True)
        parser.add_argument('expiry_date', type=str, required=True)
        parser.add_argument('price', type=float, required=True)
        parser.add_argument('stock', type=int, required=True)
        parser.add_argument('image_url', type=str)
        parser.add_argument('section_id', type=int, required=True)
        args = parser.parse_args()

        existing_product = Product.query.filter_by(name=args['name']).first()
        if existing_product:
            return {'status': 'Product name already exists'}, 409

        new_product = Product(
            name=args['name'],
            brand=args['brand'],
            manufacturing_date=datetime.strptime(args['manufacturing_date'], '%Y-%m-%d').date(),
            expiry_date=datetime.strptime(args['expiry_date'], '%Y-%m-%d').date(),
            price=args['price'],
            stock=args['stock'],
            image_url=args['image_url'],
            section_id=args['section_id']
        )
        db.session.add(new_product)
        try:
            db.session.commit()
            return new_product, 201
        except Exception as e:
            db.session.rollback()
            return {'status': "Something goes wrong"}, 500
    
api.add_resource(Api_product,
                 "/api/product/<int:product_id>",
                 "/api/delete_product/<int:product_id>",
                 "/api/update_product/<int:product_id>",
                 "/api/create_product")
