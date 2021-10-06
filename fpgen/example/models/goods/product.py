from fpgen.example.models.base import BaseIDModel
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    DateTime,
    Integer,
)
from sqlalchemy.orm import backref, relationship
from sqlalchemy_utils import CountryType


class Product(BaseIDModel):
    __tablename__ = "gds_product"
    
    name = Column(String)
    country_of_origin = Column(CountryType)
    expiration_time = Column(DateTime)
    category_id = Column(
        Integer,
        ForeignKey("gds_category.id", ondelete="SET NULL")
    )
    category = relationship(
        "Category", 
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('products', lazy='dynamic'),
        remote_side='Category.id'
    )
    unit_id = Column(
        Integer,
        ForeignKey("gds_unit.id", ondelete="SET NULL")
    )
    unit = relationship(
        "Unit",
        cascade="all, delete",
        passive_deletes=True,
        backref=backref('products', lazy='dynamic'),
        remote_side='Unit.id'
    )
