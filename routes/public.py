from flask import Blueprint, render_template, request, redirect, url_for, flash
import database

public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    db = database.obtener_conexion()
    destacados = db.execute('SELECT * FROM productos LIMIT 4').fetchall()
    db.close()
    return render_template('index.html', destacados=destacados)

@public_bp.route('/quienes-somos')
def quienes_somos():
    return render_template('quienes_somos.html')

@public_bp.route('/emprender')
def emprender():
    return render_template('emprender.html')