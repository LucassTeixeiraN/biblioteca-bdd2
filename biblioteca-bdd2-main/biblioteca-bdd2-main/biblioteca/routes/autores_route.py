from flask import render_template, request, redirect, url_for, Blueprint, jsonify
from core.database import db
from models.autor import Autor
from services.serialize_autor import serialize_autor

autores_bp = Blueprint('autores_bp', __name__)

@autores_bp.route('/autores', methods=['GET'])
def lista_autores():
    autores = Autor.query.all()
    autores_data = [serialize_autor(autor) for autor in autores]

    return jsonify(autores_data), 200