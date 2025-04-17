from sqlalchemy import Column, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import declarative_base, relationship


Base = declarative_base()

class Shop(Base):
    __tablename__ = 'shops'

    shop_id = Column(Text, primary_key=True)
    region = Column(Text, nullable=False)
    address = Column(Text, nullable=False)


class Good(Base):
    __tablename__ = 'goods'

    articul = Column(Integer, primary_key=True)
    group = Column(Text, nullable=False)
    name = Column(Text, nullable=False)
    measure = Column(Integer, nullable=False)
    value = Column(Integer, nullable=False)
    cost = Column(Integer, nullable=False)


class Operation(Base):
    __tablename__ = 'operations'

    operation_id = Column(Integer, primary_key=True)
    date = Column(Text, nullable=False)
    shop_id = Column(Text, ForeignKey('shops.shop_id'), nullable=False)
    articul = Column(Integer, ForeignKey('goods.articul'), nullable=False)
    pacs_amount = Column(Integer, nullable=False)
    operation_type = Column(Text, nullable=False)
