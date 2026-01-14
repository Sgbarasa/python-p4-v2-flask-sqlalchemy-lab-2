from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()


class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

    # relationships
    reviews = relationship('Review', back_populates='customer', cascade='all, delete-orphan')

    # association proxy
    items = association_proxy('reviews', 'item')

    # serialization rules
    serialize_rules = ('-reviews.customer',)

    def __repr__(self):
        return f"<Customer {self.id}, {self.name}>"


class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)

    # relationships
    reviews = relationship('Review', back_populates='item', cascade='all, delete-orphan')

    # serialization rules
    serialize_rules = ('-reviews.item',)

    def __repr__(self):
        return f"<Item {self.id}, {self.name}, {self.price}>"


class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String)

    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))

    # relationships
    customer = relationship('Customer', back_populates='reviews')
    item = relationship('Item', back_populates='reviews')

    # serialization rules
    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __repr__(self):
        return f"<Review {self.id}>"
