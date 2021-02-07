from . import bp
import typing as ty

from flask import render_template, request, url_for
from flask import flash, redirect, current_app, abort
from werkzeug import Response
from werkzeug.urls import url_parse

from .models import products


@bp.route('/')
@bp.route('/index')
def index() -> str:
    return render_template('index.html', products=products)


@bp.route('/pay_rules')
def pay_rules() -> str:
    return render_template('pay_rules.html')


@bp.route('/pay/<product_id>', methods=['GET', 'POST'])
def pay(product_id: str) -> str:
    product = products[product_id]
    return render_template('test_pay_widget.html', product=product)
