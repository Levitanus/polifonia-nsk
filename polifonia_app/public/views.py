from . import bp
import typing as ty

from flask import render_template, request, url_for
from flask import flash, redirect, current_app, abort
from werkzeug import Response
from werkzeug.urls import url_parse

from .models import products, PaymentForm


@bp.route('/')
@bp.route('/index')
def index() -> str:
    return render_template('index.html', products=products)


@bp.route('/pay_rules')
def pay_rules() -> str:
    return render_template('pay_rules.html')


@bp.route(
    '/pay/<product_id>',
    # methods=['GET', 'POST'],
)
@bp.route('/payhalf/<product_id>')
def pay(product_id: str) -> str:
    product = products[product_id]
    form = PaymentForm(request.form)
    if "/payhalf/" in str(request):
        if not product.can_be_halfed:
            abort(403)
        value = product.price.value // 2
        comission = product.price.comission // 2
    else:
        value = product.price.value
        comission = product.price.comission
    form.sum.data = value
    form.service_name.data = f'{product.type_} {product.name}'
    return render_template('test_pay_widget.html',
                           product=product,
                           form=form,
                           comission=comission)
