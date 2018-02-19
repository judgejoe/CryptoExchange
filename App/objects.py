#!/usr/bin/python

from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class User(Base):
	__tablename__ = 'users'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	pubkey = Column(String)
	holdings = relationship("Holding")#, back_populates="user")
	transactions = relationship("Transaction")#, back_populates="user")

	def __repr__(self):
		return "<User(id=%d, name='%s', pubkey='%s')>" % (
				self.id, self.name, self.pubkey)

class Currency(Base):
	__tablename__ = 'currencies'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	code = Column(String)
	#holding = relationship("Holding", back_populates="currency")

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


class Transaction(Base):
	__tablename__ = 'transactions'

	id = Column(Integer, primary_key=True)
	transaction_type = Column(Integer)
	quantity = Column(Float)	
	exchange_rate = Column(Float)
	user_id = Column(Integer, ForeignKey('users.id'))
	currency_id = Column(Integer, ForeignKey('currencies.id'))
	quantity = Column(Float)
	user = relationship("User", back_populates="transactions")

	def __repr__(self):
		return "<Transaction(id=%d, user=%s, transaction_type=%d, currency_id=%d, quantity='%d')>" % (
				self.id, self.user, self.transaction_type, self.currency_id, self.quantity)



