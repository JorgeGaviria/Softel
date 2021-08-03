from flask import g, render_template, redirect, url_for, flash, Blueprint, request, session
from werkzeug.exceptions import abort
from project.db import get_db

bp = Blueprint('public',__name__,url_prefix='/')

@bp.route('/')
def home():
   return render_template('public/home.html')