from flask import render_template, Blueprint, logging
from BuchananTutoringBackEnd import app


logs_app = Blueprint('Logs', __name__)

@logs_app.route('/<page>')
def log(page):
    logging.lo

