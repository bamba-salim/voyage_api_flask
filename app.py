#  tuto: https://github.com/CoreyMSchafer/code_snippets/tree/master/Python/Flask_Blog

from flask import Flask, render_template, url_for, app, request
from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf
from flask_bootstrap import Bootstrap
import requests
import json
import urllib.parse

app = Flask(__name__)
Bootstrap(app)
app.config['SECRET_KEY'] = 'DontTellAnyone'

###################################################################
# V2 de Navjot :

# Definition des parametres de l'API
API_URL = 'https://restcountries.eu/rest/v2'


def response(query_string, logger=None):

    r = requests.get(API_URL + query_string)

    if 200 <= r.status_code <= 299:

        try:
            countries_info = r.json()
            return countries_info

        except:
            return None

    elif r.status_code == 400:
        logger.error(r.request.url)

# Afficher tout les pays


def find_all():
    countries_info = response("/all/")
    return countries_info

# Trouver les informations d'un pays en fonction de son nom


def find_by_name(name):
    countries_info = response("/name/" + name)
    return countries_info

# Trouver un pays en fonction d'une langue


def find_lang(language):

    countries_info = response("/lang/" + language)
    return countries_info

# Trouver un pays en fonction de sa capital


def find_by_capital(capital_name):

    countries_info = response("/capital/" + capital_name)
    return countries_info

# Chercher les pays en fonction des continents


def find_by_region(region_name):

    countries_info = response("/region/" + region_name)
    return countries_info


# Chercher les pays en fonction de la monnaie locale
def find_by_currency(currency):

    countries_info = response("/currency/" + currency)
    return countries_info


# Numéro unique pour chaque pays. Constitué de 2 à 4 chiffres
def find_by_callingcode(code_num):

    countries_info = response("/callingcode/" + code_num)
    return countries_info

# Gérer l'erreur 404


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


test_nom = find_by_name('france')
test_language = find_lang('fr')
test_capitale = find_by_capital('paris')
test_monaie = find_by_currency('eur')
test_region = find_by_region('fr')

###################################################################
# https://github.com/SteinRobert/python-restcountries/blob/master/restcountries/base.py

###################################################################

# Formulaire :


class myForm(Form):
    pays = StringField("Saisissez le nom  d'un pays :",
                       validators=[InputRequired()])
    #langue = StringField('Langue', validators=[InputRequired()])
    #capital = StringField('Capital', validators=[InputRequired()])


# Routes :
@app.route("/pays", methods=['POST'])
def pays():
    pays_name_form = request.form["pays"]
    pays_name_api = find_by_name(pays_name_form)
    
    name = pays_name_api[0]['name']
    pays = pays_name_api[0]['translations']['fr']
    monnaies = pays_name_api[0]['currencies'][0]['name']
    region = pays_name_api[0]['region']
    languages = ', '.join(pays_name_api[0]['languages'][0]['name'])
    drapeaux = pays_name_api[0]['flag']
    habitants = pays_name_api[0]['population']
    print(languages)  # ToDo : formattez les langages en 1 ligne
    return render_template('pays.html', title=pays, name=name,  pays=pays, monnaies=monnaies, region=region, languages=languages, drapeaux=drapeaux, habitants=habitants, pays_name_form=pays_name_form, pays_name_api=pays_name_api)


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', test_nom=test_nom, test_language=test_language, test_capitale=test_capitale, test_monaie=test_monaie, test_region=test_region)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route('/research', methods=['GET', 'POST'])
def research():
    form = myForm()
    if form.validate_on_submit():
        return 'Form Successfully Submitted!'
    return render_template('research.html', form=form)


@app.route("/404")
def quatcentquat():
    return render_template('404.html', title='404')


# Run :
if __name__ == '__main__':
    app.run(debug=True)
