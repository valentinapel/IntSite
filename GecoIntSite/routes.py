from pickletools import string1
from traceback import print_list
from typing import overload
from flask import Flask, render_template, url_for, flash, redirect, request, session 
from GecoIntSite import app, db
from GecoIntSite.models import Utente, Film, Mylist
from GecoIntSite.forms import RegistrationForm, LoginForm, RicercaForm, DescrizioneForm, NewFilmForm
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import create_engine
from werkzeug.utils import secure_filename
import os

# Configurazione della UPLOAD FOLDER per il caricamento di immagini e della SECRET_KEY
app.config['UPLOAD_FOLDER'] = '/static/images'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
engine = create_engine('sqlite:///site.db')  # ENGINE CON IL QUALE CI INTERFACCEREMO A site.db


# HOME PAGE: se l'utente è loggato con priorità di admin, compaiono anche i film senza proiezioni
# e delle opzioni di gestione dei film.
@app.route("/")
@app.route("/home")
def home():
    if current_user.is_authenticated and current_user.admin == True:
        films = engine.execute('''SELECT * FROM Film''')
        Books=engine.execute('''SELECT * FROM Book''')  
        return render_template('home.html', films = films, Books= Books)

    if current_user.is_authenticated == True:
    
        querymylist = '''SELECT DISTINCT f.*
                         FROM Film f INNER JOIN Mylist m
                         WHERE f.id = m.idMedia AND m.idUser = \'{}\'
                        '''.format(current_user.id)
               
        films = engine.execute(querymylist)
        querymylist = '''SELECT DISTINCT b.*
                         FROM book b INNER JOIN Mylist m
                         WHERE b.id = m.idMedia AND m.idUser = \'{}\'
                        '''.format(current_user.id)
        Books=engine.execute(querymylist)                
     
    else:
        films = engine.execute('''SELECT * FROM Film''')
        # queryFilmList = '''SELECT DISTINCT * 
        #                           FROM Film f 
        #                '''             
        # gestisco i Libri
        Books=engine.execute('''SELECT * FROM Book''')                       
    return render_template('home.html', films = films, Books=Books)

# Aggiungi film/media alla lista
@app.route("/addonmylist/<int:media_id>")
def addonmylist(media_id):
    queryaddmedia = '''INSERT INTO Mylist(idUser, idMedia)
                            VALUES ({}, {})'''.format(current_user.id, media_id)
    engine.execute(queryaddmedia)
    return redirect(url_for('home'))

# @app.route("/addonmylist/<int:media_id>")
# def addonmylist(media_id):    
#     queryaddmedia = '''INSERT INTO Mylist(idUser, idMedia)
#                             VALUES ({}, {})'''.format(current_user.id, media_id)
#     engine.execute(queryaddmedia)
#     #if request.method == 'POST':
#     if form != None:
#         return cercafilm(form)
#         #return cercafilm(request.form['form'])
#     else:
#         return redirect(url_for('home'))
    #return redirect(url_for('cerca.html', form = form))
    #return render_template('filmtrovati.html', filmtrovati = filmtrovati)
    
# Elimina film/media alla lista
@app.route("/removeonmylist/<int:media_id>")
def removeonmylist(media_id):
    querydeletemedia = '''DELETE FROM Mylist
                          WHERE Mylist.idMedia = {} AND Mylist.idUser = \'{}\''''.format(media_id, current_user.id)
    engine.execute(querydeletemedia)
    return redirect(url_for('home'))



# REGISTRAZIONE: prima di aggiungere un utente, dobbiamo controllare che l'email non sia già stata utilizzata.
# A questo punto, possiamo reindirizzarlo alla schermata di login.
@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    registerquery = '''INSERT INTO Utente(nome, cognome, nazione, provincia, annonascita, email, password, admin)
                       VALUES (\'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', \'{}\', False)'''.format(form.nome.data, form.cognome.data, form.nazione.data, form.provincia.data,
                                                                        form.annonascita.data, form.email.data, form.password.data)
    if form.validate_on_submit():
        engine.execute(registerquery)
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# LOGIN: controlliamo se l'email inserita esiste nel database, quindi verifichiamo che la password ad essa
# associata sia corretta. In tal caso, l'utente verrà reindirizzato all'area riservata oppure al pannello
# di controllo nel caso si tratti di un amministratore. 
@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm() 
    loginquery = "SELECT * FROM Utente WHERE email = \'{}\'".format(form.email.data)
    utente = engine.execute(loginquery).first()
    if format(form.email.data)=='None':
        myerror=''
    else :
        myerror=0
    if utente and (utente.password == form.password.data):
    # Siccome utente non è compatibile con la funzione login_user() perché
    # non eredita "db.Model" e "UserMixin", creiamo dinamicamente un oggetto della
    # classe Utente per risolvere i problemi di compatibilità tra librerie.
        login_user(Utente(utente.id, utente.nome, utente.cognome, utente.annonascita,
                     utente.nazione, utente.provincia, utente.email, utente.password,
                     utente.admin))
        session['utente_id'] = utente.id   #salva in utente_id l'id dell utente
        if utente.admin:
            return render_template('adminhome.html')
        else:
            next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        else:
            return redirect(url_for('home'))
    else:
        return render_template('login.html', form=form,myerror=myerror,mydata=format(form.email.data))

# LOGOUT: l'utente effettua la disconnessione e viene reindirizzato alla home page come guest.
@app.route("/logout")
def logout():
    logout_user()
    session.pop('utente_id', None) # distrugge la sessione al log out
    return redirect(url_for('home'))

# AREA RISERVATA: dal momento che l'area riservata mostra informazioni sull'utente e sulle prenotazioni
# da esso effettuate, le ricaviamo effettuando le sottostanti query.
@app.route('/areariservata')
@login_required
def areariservata():
    queryutente = "SELECT * FROM Utente WHERE id = \'{}\'".format(current_user.id)
    utente = engine.execute(queryutente).first()

    return render_template('areariservata.html', utente = utente)

# CERCAFILM: L'utente può digitare un genere, un titolo o un regista e la query restituisce tutti
# i film con risultati compatibili.
@app.route("/cercafilm", methods=['GET', 'POST'])
def cercafilm():
    form = RicercaForm()
    return cercafilm(form)

def cercafilm(form):
    if form.validate_on_submit():
        flag=0
        valoreimmesso = form.ricerca.data

        if current_user.is_authenticated == True:
            querytrovati = '''SELECT DISTINCT * 
                            FROM Film f
                            LEFT JOIN Mylist m ON f.id = m.idMedia
                            WHERE f.titolo LIKE \'{}\'
                                OR f.genere LIKE \'{}\'
                                OR f.regista LIKE \'{}\'
                                AND m.idUser = \'{}\' OR m.idUser = Null
                                '''.format(valoreimmesso, valoreimmesso, valoreimmesso, current_user.id)                         
        else:
            querytrovati = '''SELECT DISTINCT * 
                         FROM Film
                         WHERE titolo LIKE \'{}\'
                            OR genere LIKE \'{}\'
                            OR regista LIKE \'{}\''''.format(valoreimmesso, valoreimmesso, valoreimmesso)
                        
        filmtrovati = engine.execute(querytrovati)
        flag=len(filmtrovati.fetchall()) # verifico il numero delle righe
        filmtrovati = engine.execute(querytrovati)
        if flag > 0:  # verifico ese estraggo almeno una riga
            return render_template('filmtrovati.html', filmtrovati = filmtrovati)
#        return render_template('filmtrovati.html', filmtrovati = filmtrovati, form = form)
        else:
            return render_template('cercafilm.html', form = form)
    return render_template('cercafilm.html', form = form)

# ADMINHOME: Pannello di controllo dell'amministratore
@app.route("/adminhome")
def adminhome():
    return render_template('adminhome.html')

@app.route("/statistiche")
def statistiche():
    etamed = engine.execute('''SELECT AVG(2020-annonascita) 
                               FROM Utente''').first()
    etamed = "{:.1f}".format(etamed[0])

    return render_template('statistiche.html', etamed = etamed) 


# GESTIONEUSER: In questa pagina verrà visualizzata una lista degli utenti in tre diversi ordini
# in base alla modalità scelta: modalità 1 = ordine di cognome, modalità 2 = ordine di ID,
# modalità 3 = ordine di biglietti comprati.
@app.route("/gestioneuser/<int:modalita>")
def gestioneuser(modalita):
    if modalita == 1:
        #engine.execute('''DROP VIEW IF EXISTS UtenteBiglietti''')
        userordinealfa = engine.execute('''SELECT *
                                           FROM Utente 
                                           ORDER BY cognome, nome ASC''')
        return render_template('gestioneuser.html', userordinealfa = userordinealfa, modalita = modalita)
    
    if modalita == 2:
        #engine.execute('''DROP VIEW IF EXISTS UtenteBiglietti''')
        userordineid = engine.execute('''SELECT *
                                         FROM Utente
                                         ORDER BY id ASC''')
        return render_template('gestioneuser.html', userordineid = userordineid, modalita = modalita)
    
    if modalita == 3:
        print("@app.route(/gestioneuser/<int:modalita 3 fail")
        raise ValueError("route modalita 3")


# GESTIONEFILM: In questa route l'amministratore può gestire i film, visualizzati in ordine
# alfabetico di titolo. Tra le opzioni esiste quella di eliminare un film, che però è 
# utilizzabile solamente se non ci sono prenotazioni effettuate per quel film.
@app.route("/gestionefilm")
def gestionefilm():
    films = engine.execute('''SELECT * FROM Film ORDER BY titolo''')
    queryconpren = engine.execute('''SELECT DISTINCT f.titolo
                                       FROM Film f ''')
    listafilmconpren = []
    for f in queryconpren:
        listafilmconpren.append("{}".format(f.titolo))
        print(f.titolo in listafilmconpren)
    print(listafilmconpren)

    return render_template('gestionefilm.html', films = films, lista = listafilmconpren)


# PROMUOVIUTENTE: Promuove l'utente selezionato a ruolo di admin, poi reindirizza l'utente alla
# pagina di gestione utenti in ordine alfabetico
@app.route("/promuoviutente/<int:idutente>")
def promuoviutente(idutente):
    queryupdate = '''UPDATE Utente
                     SET admin = True
                     WHERE id = {}'''.format(idutente)
    engine.execute(queryupdate)
    userordinealfa = engine.execute('''SELECT *
                                       FROM Utente 
                                       ORDER BY cognome ASC''')
    return render_template('gestioneuser.html', userordinealfa = userordinealfa, modalita = 1)

@app.route("/confermapromozione/<int:idutente>")
def confermapromozione(idutente):
    queryutente = '''SELECT * FROM Utente WHERE id = {}'''.format(idutente)
    utente = engine.execute(queryutente).first()
    return render_template('confermapromozione.html', utente = utente)


# RIMUOVIUTENTE: Oltre a rimuovere l'utente, si dovranno rimuovere le relative prenotazioni
# e i posti prenotati nelle diverse mappe.
@app.route("/rimuoviutente/<int:idutente>")
def rimuoviutente(idutente):  
    with engine.connect() as connection:
        # Tutte le prenotazioni che l'utente ha effettuato:
        queryselectpren = '''SELECT *
                             FROM Prenotazione WHERE id_utente = {}'''.format(idutente)
        prens = connection.execute(queryselectpren)

        for pren in prens:
            queryproid = '''SELECT * FROM Proiezione WHERE id = {}'''.format(pren.proiezione_id)
            pro = connection.execute(queryproid).first()

            postiliberati = 0
            
            # Controlliamo ogni posto a sedere nella Mappaposti relativa alla proiezione: se l'id 
            # dell'utente corrisponde a quello del posto, questo posto viene liberato e si effettua
            # il +1 su "postiliberati". Ciò serve ad evitare che vengano liberati anche tutti gli
            # altri posti prenotati da altri utenti.            
            for f in range(1, 5):
                for c in range(1, 11):
                    queryperunposto = '''SELECT fila{}col{} FROM Mappaposti WHERE proiezione_id = {}'''.format(f, c, pro.id)
                    filacolcorrente = connection.execute(queryperunposto).first()
                    if filacolcorrente[0] == idutente:  # .first() ritorna una lista, in questo caso
                                                        # un singleton, quindi con filacolcorrente[0]
                                                        # accediamo all'effettivo valore int
                        postiliberati += 1
                        # Per liberare il posto inseriamo i valore NULL all'interno della filaXcolX nella mappa.
                        queryupdate = '''UPDATE Mappaposti
                                         SET fila{}col{} = NULL 
                                         WHERE proiezione_id = {}'''.format(f, c, pro.id)
                        connection.execute(queryupdate)
                            

            # Aggiorniamo i posti rimasti aggiungendo quelli appena liberati.
            queryupdateposti = '''UPDATE Proiezione
                                  SET posti_rimasti = posti_rimasti + {}
                                  WHERE id = {}'''.format(postiliberati, pro.id)
            connection.execute(queryupdateposti)

            # Eliminiamo la prenotazione.
            querydeletepren = '''DELETE FROM Prenotazione
                                 WHERE id = {}'''.format(pren.id)
            connection.execute(querydeletepren)

        # Ora possiamo eliminare l'utente
        querydelete = '''DELETE FROM Utente
                         WHERE id = {}'''.format(idutente)
        connection.execute(querydelete)

    # Redirect alla pagina di gestione utenti in ordine alfabetico
    userordinealfa = engine.execute('''SELECT *
                                       FROM Utente 
                                       ORDER BY cognome ASC''')
    return render_template('gestioneuser.html', userordinealfa = userordinealfa, modalita = 1)


@app.route("/confermarimuoviutente/<int:idutente>")
def confermarimuoviutente(idutente):
    queryutente = '''SELECT * FROM Utente WHERE id = {}'''.format(idutente)
    utente = engine.execute(queryutente).first()
    return render_template('confermarimuoviutente.html', utente = utente)

# CANCELLAPRENUTENTE: Elimina tutte le proiezioni effettuate da quell'utente.
# Route praticamente identica a RIMUOVIUTENTE, ma che si limita a rimuoverne le
# proiezioni, senza eliminare l'utente.
@app.route("/cancellaprenutente/<int:idutente>")
def cancellaprenutente(idutente):
    with engine.connect() as connection:
        queryselectpren = '''SELECT *
                             FROM Prenotazione WHERE id_utente = {}'''.format(idutente)
        prens = connection.execute(queryselectpren)
        
        for pren in prens:
            queryproid = '''SELECT * FROM Proiezione WHERE id = {}'''.format(pren.proiezione_id)
            pro = connection.execute(queryproid).first()

            postiliberati = 0
            
            # Controlliamo ogni posto a sedere nella Mappaposti relativa alla proiezione: se l'id 
            # dell'utente corrisponde a quello del posto, questo posto viene liberato e si effettua
            # il +1 su "postiliberati". Ciò serve ad evitare che vengano liberati anche tutti gli
            # altri posti prenotati da altri utenti.            
            for f in range(1, 5):
                for c in range(1, 11):
                    queryperunposto = '''SELECT fila{}col{} FROM Mappaposti WHERE proiezione_id = {}'''.format(f, c, pro.id)
                    filacolcorrente = connection.execute(queryperunposto).first()
                    if filacolcorrente[0] == idutente:  # .first() ritorna una lista, in questo caso
                                                        # un singleton, quindi con filacolcorrente[0]
                                                        # accediamo all'effettivo valore int
                        postiliberati += 1
                        # Per liberare il posto inseriamo i valore NULL all'interno della filaXcolX nella mappa.
                        queryupdate = '''UPDATE Mappaposti
                                         SET fila{}col{} = NULL 
                                         WHERE proiezione_id = {}'''.format(f, c, pro.id)
                        connection.execute(queryupdate)
                            

            # Aggiorniamo i posti rimasti aggiungendo quelli appena liberati.
            queryupdateposti = '''UPDATE Proiezione
                                  SET posti_rimasti = posti_rimasti + {}
                                  WHERE id = {}'''.format(postiliberati, pro.id)
            connection.execute(queryupdateposti)

            # Eliminiamo la prenotazione.
            querydeletepren = '''DELETE FROM Prenotazione
                                 WHERE id = {}'''.format(pren.id)
            connection.execute(querydeletepren)

    userordinealfa = engine.execute('''SELECT *
                                           FROM Utente 
                                           ORDER BY cognome ASC''')
    return render_template('gestioneuser.html', userordinealfa = userordinealfa, modalita = 1)


# NUOVOFILM: Route dalla quale si possono aggiungere nuovi film compilando il form "NewFilmForm".
@app.route("/nuovofilm", methods=['GET', 'POST'])
def nuovofilm():
    form = NewFilmForm()
    if form.validate_on_submit():
        # C'è anche l'opzione di allegare un'immagine per la locandina del film. Se non viene caricata, 
        # viene rimpiazzata automaticamente con un'immagine grigia.
        filepath = "/static/images/grigio.jpg"
        file = request.files['file']
        fileName = secure_filename(file.filename)
        if fileName != "": # Se non è stata caricata nessuna immagine, non modifico il filepath che
                           # rimane ".../grigio.jpg"
            file.save("GecoIntSite/static/images/" + fileName)
            filepath = "/static/images/{}".format(fileName)
        # Verifichiamo che non esista già un film con lo stesso titolo per non 
        # violare il vincolo di integrità UNIQUE.
        querycontrollafilm = '''SELECT * FROM Film WHERE titolo = \'{}\''''.format(form.titolo.data)
        controllafilm = engine.execute(querycontrollafilm).first()
        if controllafilm != None:
            return render_template('nuovofilm.html', form = form)
            
        # Se non esiste un film con lo stesso titolo, possiamo aggiungerlo
        queryinsert = '''INSERT INTO Film(titolo, regista, genere, annoproduzione, durata, descrizione, locandina)
                         VALUES ("{}", \'{}\', \'{}\', {}, {}, \'{}\', \'{}\')'''.format(form.titolo.data, form.regista.data, form.genere.data, 
                                                                                    form.anno.data, form.durata.data, form.descrizione.data, filepath)
        engine.execute(queryinsert)
        return redirect(url_for('gestionefilm'))
    return render_template('nuovofilm.html', form = form)



# MODIFICADESCRIZIONE: Modifica la descrizione di un film tramite il form "DescrizioneForm"
@app.route("/modificadescrizione/<id_film>", methods=['GET', 'POST'])
def modificadescrizione(id_film):
    form = DescrizioneForm()
    if form.validate_on_submit():
        queryupdate = '''UPDATE Film
                         SET descrizione = \'{}\'
                         WHERE id = {}'''.format(form.descrizione.data, id_film)
        engine.execute(queryupdate)
        return redirect(url_for('home'))

    # Prerempiamo la textarea con la descrizione corrente del film
    queryselect = '''SELECT * FROM Film WHERE id = {}'''.format(id_film)
    film = engine.execute(queryselect).first()
    form.descrizione.data = film.descrizione
    return render_template('modificadescrizione.html', form = form, film = film)


# ELIMINAFILM: Elimina il film selezionato e le sue proiezioni.
@app.route("/eliminafilm/<int:film_id>")
def eliminafilm(film_id):
    querydeletefilm = "DELETE FROM Film WHERE id = {}".format(film_id)
    engine.execute(querydeletefilm)
    return redirect(url_for('gestionefilm'))

@app.route("/confermaeliminafilm/<int:film_id>")
def confermaeliminafilm(film_id):
    queryfilm = '''SELECT * FROM Film WHERE id = {}'''.format(film_id)
    film = engine.execute(queryfilm).first()
    return render_template('confermaeliminafilm.html', film = film)

#page debug tomasella
@app.route("/test")
def mytest():    
    return render_template('mytest.html')

# gestione handle page
@app.errorhandler(404)
def page_not_found (e):
    return render_template('404.html')

@app.route("/cercabook", methods=['GET', 'POST'])
def cercabook():
    form = RicercaForm()
    return cercabook(form)
  # return render_template('cercabook.html')

def cercabook(form):
    mytype=0
    flag=0
    if form.validate_on_submit():
        valoreimmesso = form.ricerca.data

        if current_user.is_authenticated == True:
            querytrovati = '''SELECT DISTINCT * 
                            FROM Book f
                            LEFT JOIN Mylist m ON f.id = m.idMedia
                            WHERE f.titolo LIKE \'{}\'
                                OR f.genere LIKE \'{}\'
                                OR f.autore LIKE \'{}\'
                                AND m.idUser = \'{}\' OR m.idUser = Null
                                '''.format(valoreimmesso, valoreimmesso, valoreimmesso, current_user.id)                         
        else:
            querytrovati = '''SELECT DISTINCT * 
                         FROM Book
                         WHERE upper(titolo) LIKE \'{}\'
                            OR upper(genere) LIKE \'{}\'
                            OR autore LIKE \'{}\''''.format(valoreimmesso, valoreimmesso, valoreimmesso)
                        
        booktrovati = engine.execute(querytrovati)
        #return render_template('booktrovati.html', booktrovati = booktrovati)
        flag=len(booktrovati.fetchall()) # verifico il numero delle righe
 
        booktrovati = engine.execute(querytrovati)
        #print("denis")
        #print('total rows before ',flag)
 
        if (flag) >0:
            print('total rows ',flag)
            return render_template('booktrovati.html', booktrovati = booktrovati)
        else:
            return render_template('cercabook.html', form = form)
     #nel caso di problemi di form ritorna il rigo sotto       
    return render_template('cercabook.html', form = form)
   