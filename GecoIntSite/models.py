from GecoIntSite import app, db, login_manager
from datetime import date, time
from flask_login import UserMixin
from sqlalchemy import ForeignKey

# Funzionalità di gestione delle sessioni utente
@login_manager.user_loader
def load_user(utente_id):
	return Utente.query.get(int(utente_id))

# In questo file creiamo tutti i modelli, ovvero le tabelle del database.

class Utente(db.Model, UserMixin):
	# Costruttore aggiunto per la creazione dinamica di un utente da loggare per 
	# problemi di compatibilità tra librerie, si veda /GecoIntSite/routes.py linea 56
	def __init__(self, id, nome, cognome, email, password, annonascita, provincia, nazione, admin):
		self.id = id
		self.nome = nome
		self.cognome = cognome
		self.email = email
		self.password = password
		self.annonascita = annonascita
		self.provincia = provincia
		self.nazione = nazione
		self.admin = admin
	id = db.Column(db.Integer, primary_key=True)
	nome = db.Column(db.String, nullable=False)
	cognome = db.Column(db.String, nullable=False)
	email = db.Column(db.String, nullable=False, unique=True)
	password = db.Column(db.String, nullable=False)
	annonascita = db.Column(db.Integer, nullable=False)
	provincia = db.Column(db.String, nullable=False)
	nazione = db.Column(db.String, nullable=False)
	admin = db.Column(db.Boolean, nullable=False, default = False)

	def __repr__(self):
		return f"Utente('{self.id}', '{self.nome}', '{self.cognome}', '{self.annonascita}', '{self.nazione}', '{self.provincia}', '{self.email}', '{self.password}')"

class Film(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titolo = db.Column(db.String, unique=True, nullable=False)
	annoproduzione = db.Column(db.Integer, nullable=False)
	regista = db.Column(db.String, nullable=False)
	genere = db.Column(db.String, nullable=False)
	durata = db.Column(db.Integer, nullable=False)
	locandina = db.Column(db.String, nullable=False, default='/static/images/grigio.jpg') 
	descrizione = db.Column(db.String, default = 'Descrizione di questo bellissimo film')

class Mylist(db.Model):
	idUser = db.Column(db.Integer, primary_key=True)
	idMedia = db.Column(db.Integer, primary_key=True)
	#Status = db.Column(db.enum =[read/watched, in progress]) 
	#like = db.Column(db.Boolean, nullable=True)
	# id = db.Column(db.Integer, primary_key=True)

class Book(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titolo = db.Column(db.String, unique=True, nullable=False)
	annoproduzione = db.Column(db.Integer, nullable=False)
	autore = db.Column(db.String, nullable=False)
	genere = db.Column(db.String, nullable=False)
	durata = db.Column(db.Integer, nullable=False)
	locandina = db.Column(db.String, nullable=False, default='/static/images/grigio.jpg') 
	descrizione = db.Column(db.String, default = 'Descrizione di questo bellissimo libro')

""" class Song(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	titolo = db.Column(db.String, unique=True, nullable=False)
	annoproduzione = db.Column(db.Integer, nullable=False)
	artista = db.Column(db.String, nullable=False)
	genere = db.Column(db.String, nullable=False)
	durata = db.Column(db.Integer, nullable=False)
	locandina = db.Column(db.String, nullable=False, default='/static/images/grigio.jpg') 
	descrizione = db.Column(db.String, default = 'Descrizione di questo bellissima canzone') """

