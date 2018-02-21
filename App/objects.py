#!/usr/bin/python

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	password = Column(String)
	holdings = relationship("Holding")
	transactions = relationship("Transaction")

	def __repr__(self):
		return "<User(id=%d, name='%s', password='%s')>" % (
				self.id, self.name, "".join(['*' for i in range(len(self.password))]))

class Currency(Base):
	__tablename__ = 'currencies'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	code = Column(String)

	def __repr__(self):
		return "<Currency(id=%d, name='%s', code='%s')>" % (
				self.id, self.name, self.code)

class Holding(Base):
	__tablename__ = 'holdings'

	id = Column(Integer, primary_key=True)
	user_id = Column(Integer, ForeignKey('users.id'))
	currency_id = Column(Integer, ForeignKey('currencies.id'))
	quantity = Column(Float)
	user = relationship("User", uselist=False) 
	currency = relationship("Currency", uselist=False)

	def __repr__(self):
		return "<Holding(user_id=%d, currency_id=%d, quantity='%d')>" % (
				self.user_id, self.currency_id, self.quantity)


class TransactionType(Base):
	__tablename__ = 'transaction_types'

	id = Column(Integer, primary_key=True)
	name = Column(Integer)

	def __repr__(self):
		return "<Transaction(id=%d, name=%s)>" % (self.id, self.name)

class Transaction(Base):
    __tablename__ = 'transactions'

    id = Column(Integer, primary_key=True)
    transaction_type_id = Column(Integer)
    amount = Column(Float)	
    user_id = Column(Integer, ForeignKey('users.id'))
    currency_id = Column(Integer, ForeignKey('currencies.id'))
    transaction_type_id = Column(Integer, ForeignKey('transaction_types.id'))
    user = relationship("User")
    transaction_type_name = relationship("TransactionType")
    currency = relationship("Currency")

    def __repr__(self):
        return "<Transaction(id=%d, user=%s, transaction_type_name=%s, currency=%s, amount='%d')>" % (self.id, self.user, self.transaction_type_name, self.currency, self.amount)



