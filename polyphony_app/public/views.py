from . import bp
import typing as ty

from flask import render_template, request, url_for
from flask import flash, redirect, current_app, abort
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug import Response
from werkzeug.urls import url_parse

from ..users import models as md
from ..app import db


@bp.route('/')
@bp.route('/index')
def index() -> str:
    return render_template('index.html')


@bp.route('/create_admin/<token>')
def create_admin(token):
    if token == current_app.config['CREATE_ADMIN_TOKEN']:
        if md.User.query.filter(md.User.username == 'admin').first():
            flash('oooOPS, admin exists already')
            abort(403)
        u = md.User(
            username='admin',
            email='admin@admin.admin',
            password=current_app.config['CREATE_ADMIN_PASSWORD']
        )
        u.add_to_group(md.UserGroup.admin)
        db.session.add(u)
        db.session.commit()
        flash('admin created')
        return redirect('/')
    abort(403)
