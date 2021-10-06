from sqlalchemy.sql.schema import Column
from sqlalchemy import String, Text
from fpgen.example.models.base import BaseIDModel


class Unit(BaseIDModel):
    __tablename__ = "gds_unit"

    name = Column(String)
    description = Column(Text)
