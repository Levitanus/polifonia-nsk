from . import bp
import typing as ty

from flask import render_template, request, url_for
from flask import flash, redirect, current_app, abort
from werkzeug import Response
from werkzeug.urls import url_parse


@bp.route('/')
@bp.route('/index')
def index() -> str:
    return render_template('index.html')

