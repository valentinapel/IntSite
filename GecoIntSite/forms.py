from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, validators, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from GecoIntSite.models import Utente


# I seguenti form derivano dalla libreria WTForms, e verranno usati per le route di:
# registrazione, login, ricerca di un film, prenotazione dei posti a sedere, 
# modifica di una proiezione, modifica della descrizione di un film, aggiunta di un
# nuovo film.

class RegistrationForm(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    cognome = StringField('Cognome', validators=[DataRequired()])
    nazione = StringField('Nazione', validators=[DataRequired()])
    provincia = StringField('Provincia', validators=[DataRequired()])
    annonascita = IntegerField('Anno di nascita', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confermapassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_email(self, email):
        utente = Utente.query.filter_by(email=email.data).first()
        if utente:
            raise ValidationError('Esiste già un account associato a questa email.')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    login = SubmitField('Login')

class RicercaForm(FlaskForm):
    ricerca = StringField('Cerca Film', validators=[DataRequired()])
    cerca = SubmitField('Cerca')

#class PrenotazioneForm(FlaskForm):  !delete form!!

class DescrizioneForm(FlaskForm):
    descrizione = TextAreaField('Descrizione', validators=[DataRequired(), validators.Length(max=150)])
    conferma = SubmitField('Conferma')

class NewFilmForm(FlaskForm):
    titolo = StringField('Titolo', validators=[DataRequired()])
    regista = StringField('Regista', validators=[DataRequired()])
    genere = StringField('Genere', validators=[DataRequired()])
    anno = IntegerField('Anno', validators=[DataRequired()])
    descrizione = TextAreaField('Descrizione', validators=[DataRequired(), validators.Length(max=150)])
    durata = IntegerField('Durata', validators=[DataRequired()])
    aggiungi = SubmitField('Aggiungi')

class NewBookForm(FlaskForm):
    titolo = StringField('Titolo', validators=[DataRequired()])
    autore = StringField('Autore', validators=[DataRequired()])
    genere = StringField('Genere', validators=[DataRequired()])
    anno = IntegerField('Anno', validators=[DataRequired()])
    descrizione = TextAreaField('Descrizione', validators=[DataRequired(), validators.Length(max=150)])
    aggiungi = SubmitField('Aggiungi')

""" class NewSongForm(FlaskForm):
    titolo = StringField('Titolo', validators=[DataRequired()])
    artista = StringField('artista', validators=[DataRequired()])
    genere = StringField('Genere', validators=[DataRequired()])
    anno = IntegerField('Anno', validators=[DataRequired()])
    descrizione = TextAreaField('Descrizione', validators=[DataRequired(), validators.Length(max=150)])
    durata = IntegerField('Durata', validators=[DataRequired()])
    aggiungi = SubmitField('Aggiungi') """