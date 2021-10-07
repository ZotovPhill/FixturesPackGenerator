from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Text, Integer
from fpgen.example.models.base import BaseIDModel


class Category(BaseIDModel):
    __tablename__ = "gds_category"

    name = Column(String)
    description = Column(Text)
    numeric_code = Column(Integer)
