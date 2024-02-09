from GecoIntSite import app, db
from GecoIntSite.models import Utente, Film, Mylist
from datetime import time, date
from sqlalchemy import ForeignKey, Boolean, create_engine
import os.path

# Creiamo il database all'avvio del server solo se non ne esiste già uno.
if not(os.path.isfile('./site.db')):
	db.create_all()
	# Dopo aver creato il database, possiamo istanziare un engine che ci servirà
	# ad interfacciarci con esso.
	engine = create_engine('sqlite:///site.db')

	# Per rendere più comodi e iterabili i processi di inserimento dei primi dati di base,
	# creiamo delle classi che utilizzeremo come costruttori per ogni tabella, tranne che
	class UtenteDaInserire:
		def __init__(self, nome, cognome, email, password, annonascita, provincia, nazione, admin):
			self.nome = nome
			self.cognome = cognome
			self.email = email
			self.password = password
			self.annonascita = annonascita
			self.provincia = provincia
			self.nazione = nazione
			self.admin = admin

	class FilmDaInserire:
		def __init__(self, titolo, annoproduzione, regista, genere, durata, locandina, descrizione):
			self.titolo = titolo
			self.annoproduzione = annoproduzione
			self.regista = regista
			self.genere = genere
			self.durata = durata
			self.locandina = locandina
			self.descrizione = descrizione

	# classe per inseirmento books
	class BookDaInserire:
		def __init__(self,titolo,annoproduzione,autore,genere ,durata ,locandina,descrizione):
			self.titolo =titolo
			self.annoproduzione = annoproduzione
			self.autore = autore
			self.genere = genere
			self.durata = durata
			self.locandina = locandina
			self.descrizione =descrizione

	class ListaDaInserire:
		def __init__(self, idUser, idMedia):
			self.idUser = idUser
			self.idMedia = idMedia

	# Per utilizzare le classi-costruttori sopra descritte, inizializziamo delle liste con i dati da inserire
	# nelle varie tabelle. Poi, con un ciclo for, creiamo dinamicamente delle stringhe di query scorrendo
	# suddette liste e le eseguiamo.
	lista_utenti = [UtenteDaInserire("Filippo", "Cigana", "876887@stud.unive.it", "filippopassw", 1999, "Conegliano", "Italia", True), 
					UtenteDaInserire("Ettore", "Chinellato", "ettorechinellato@gmail.com", "ettorepassw", 1997, "Conegliano", "Italia", True), 
					UtenteDaInserire("Stefano", "Calzavara", "stefanocalzavara@email.com", "stefanopassw", 1985, "Roma", "Italia", False), 
					UtenteDaInserire("Alessandra", "Raffaetà", "alessandraraffaeta@email.com", "alessandrapassw", 1970, "Firenze", "Italia", False), 
					UtenteDaInserire("Marcello", "Pelillo", "marcellopelillo@email.com", "marcellopassw", 1966, "Milano", "Italia", False), 
					UtenteDaInserire("Alvise", "Spanò", "alvisespano@email.com", "alvisepassw", 1977, "Torino", "Italia", False), 
					UtenteDaInserire("Andrea", "Albarelli", "andreaalbarelli@email.com", "andreapassw", 1975, "Venezia", "Italia", False), 
					UtenteDaInserire("Andrea", "Marin", "andreamarin@email.com", "marinpassw", 1976, "Verona", "Italia", False),
					UtenteDaInserire("Denis", "Tomasella", "tomasella.denis@gmail.com", "miapassword", 1976, "Verona", "Italia", True)]


	for i in lista_utenti:
		ins_user = engine.execute('''INSERT INTO Utente (nome, cognome, email, password, annonascita, provincia, nazione, admin)
										VALUES (\'{}\', \'{}\', \'{}\', \'{}\', {}, \'{}\', \'{}\', {})'''.format(i.nome, i.cognome,
																									i.email, i.password, i.annonascita,
																									i.provincia, i.nazione, i.admin))

	lista_film = [FilmDaInserire("The Truman Show", 1998, "Peter Weir", "Commedia", 103, '/static/images/truman.jpg', "Descrizione"), 
					FilmDaInserire("Avatar", 2009, "James Cameron", "Fantascienza", 161, '/static/images/avatar.jpg', "Descrizione"), 
					FilmDaInserire("Transformers", 2007, "Michael Bay", "Azione", 142, '/static/images/trans.jpg', "Descrizione"), 
					FilmDaInserire("Avengers: Endgame", 2019, "Anthony & Joe Russo", "Azione", 181, '/static/images/avengers.jpg', "Descrizione"), 
					FilmDaInserire("Lord Of The Rings", 2001, "Peter Jackson", "Fantasy", 208, '/static/images/lordrings.jpg', "Descrizione"), 
					FilmDaInserire("Star Wars", 1977, "George Lucas", "Fantascienza", 121, '/static/images/starwars.jpg', "Descrizione"), 
					FilmDaInserire("Titanic", 1997, "James Cameron", "Dramma", 195, '/static/images/titanic.jpg', "Descrizione"), 
					FilmDaInserire("Matrix", 1999, "Andy & Larry Wachowsky", "Fantascienza", 136, '/static/images/matrix.jpg', "Descrizione"), 
					FilmDaInserire("Harry Potter", 2001, "Chris Columbus", "Fantasy", 159, '/static/images/harrypotter.jpg', "Descrizione"),
					FilmDaInserire("Pulp Fiction", 1994, "Quentin Tarantino", "Gangster", 154, '/static/images/pulp.jpg', "Descrizione"), 
					FilmDaInserire("Into The Wild", 2007, "Sean Penn", "Avventura", 148, '/static/images/intowild.jpg', "Descrizione"), 
					FilmDaInserire("Tron", 1982, "Steven Lisberger", "Fantascienza", 96, '/static/images/tron.jpg', "Descrizione")]
					
	for i in lista_film:
		ins_film = engine.execute('''INSERT INTO Film (titolo, annoproduzione, regista, genere, durata, locandina, descrizione)
										VALUES (\'{}\', {}, \'{}\', \'{}\', {}, \'{}\', \'{}\')'''.format(i.titolo, i.annoproduzione,
																									i.regista, i.genere, i.durata,
																									i.locandina, i.descrizione))
	
	lista_book = [ BookDaInserire("Abbastanza felice per morire",2021,"Mark Edwards","Thriller",300,"/static/images/Abbastanza felice per morire.jpeg",'Descrizione'),
					BookDaInserire("2700 ore di sole",2017,"Romy Gallo","Romanzo",200,"/static/images/2700 ore di sole (Italian Edition).jpeg",'Descrizione'),
					BookDaInserire("Ali d argento",2020,"Camilla Lackberg","Thriller",200,"/static/images/Ali dargento.jpeg",'Descrizione'),
					BookDaInserire("Dear Child",2020,"Romy Hausmann","Thriller",200,"/static/images/Dear Child_ The twisty thriller that starts where others end.jpeg",'Descrizione'),
					BookDaInserire("Il lungo ritorno",2020,"Elizabeth George","Thriller",200,"/static/images/Il lungo ritorno.jpeg",'Descrizione'),
					BookDaInserire("Le ragazze non devono parlare",2020,"Mary Higgins Clark","Romanzo",200,"/static/images/Le ragazze non devono parlare.jpeg",'Descrizione'),
					BookDaInserire("La casa delle voci",2019,"Donato Carrisi","Romanzo",200,"/static/images/La casa delle voci.jpeg",'Descrizione'),
					BookDaInserire("La tigre",2019,"Joël Dicker","Thriller",200,"/static/images/La tigre [Illustrazioni di David de las Heras].jpeg",'Descrizione'),
					BookDaInserire("Extravergine",2019,"Chiara Moscardelli","Romanzo",200,"/static/images/Extravergine.jpeg",'Descrizione'),
					BookDaInserire("Cambiare l acqua ai fiori",2019,"Valerie Perrin","Thriller",200,"/static/images/Cambiare l_acqua ai fiori.jpeg",'Descrizione'),
					BookDaInserire("Una ragazza cattiva",2018,"Alberto Beruffi","Romanzo",200,"/static/images/Una ragazza cattiva.jpeg",'Descrizione'),
					BookDaInserire("La prigioniera",2018,"Debra Jo Immergut","Romanzo",200,"/static/images/La prigioniera.jpeg",'Descrizione'),
					BookDaInserire("Punizione",2018,"Elizabeth George","Romanzo",200,"/static/images/Punizione.jpeg",'Descrizione')]
		

	for i in lista_book:
	    ins_book = engine.execute('''INSERT INTO Book (titolo, annoproduzione, autore, genere, durata, locandina, descrizione)
										VALUES (\'{}\', {}, \'{}\', \'{}\', {}, \'{}\', \'{}\')'''.format(i.titolo, i.annoproduzione,
																									i.autore, i.genere, i.durata,
																									i.locandina, i.descrizione))


	


	# lista_mylist = [ListaDaInserire(8,1),
	# 				ListaDaInserire(1,1)]
	 
	# for i in lista_mylist:
	# 	ins_mylist = engine.execute('''INSERT INTO Mylist (idUser, idMedia)
	# 									VALUES ({},{})'''.format(i.idUser, i.idMedia))
	
	# ins_mylist = engine.execute('''INSERT INTO Mylist (idUser, idMedia)
	#  									VALUES (8,1)''')



#Avvio dell'applicazione Flask
if __name__ == '__main__':
#    app.run(debug=True, host="127.0.0.1", port=8180)
	app.run(host='0.0.0.0', port=8180)