from . import bp
import typing as ty

from flask import render_template, request, url_for
from flask import flash, redirect, current_app, abort
from werkzeug import Response
from werkzeug.urls import url_parse

from .models import products, PaymentForm

import telebot
from . import telegram_bot_parcer as data_parcer
from threading import Thread

channel = -1001586470274
channel = "@polifoniaBotTest"


class MenuItem:

    def __init__(self, text: str, route: str) -> None:
        self.text = text
        self.route = bp.url_defaults(route)


menu_items = [
    MenuItem('главная', '/'),
    MenuItem('контактная информация', '/about_us'),
]


@bp.route('/')
@bp.route('/index')
def index() -> str:
    return render_template(
        'index.html', products=products, menu_items=menu_items
    )


@bp.route('/about_us')
def about_us() -> str:
    return render_template('about_us.html', menu_items=menu_items)


@bp.route('/pay_rules')
def pay_rules() -> str:
    return render_template('pay_rules.html', menu_items=menu_items)


@bp.route(
    '/pay/<product_id>',
    methods=['GET', 'POST'],
)
@bp.route('/payhalf/<product_id>')
def pay(product_id: str) -> str:
    try:
        product = products[product_id]
    except KeyError:
        abort(404)
    if not product.can_be_paid:
        abort(404)
    form = PaymentForm(request.form)
    if request.method == 'POST':
        raise Exception(request.form)
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
    return render_template(
        'test_pay_widget.html',
        product=product,
        form=form,
        comission=comission,
        menu_items=menu_items
    )


def process_webhook(data):
    bot = telebot.TeleBot("1925166479:AAE0uwMEPNO3H9mJ2LYq39HaTxYFm7_0ULc")
    # bot.send_message(channel, str(data))
    try:
        if info := data_parcer.allert_if_new_lesson(data):
            bot.send_message(channel, info, parse_mode="HTML")
        else:
            bot.send_message(channel, f"unsuccessful: {str(info)}")
    except Exception as e:
        bot.send_message(channel, e)


@bp.route("/QD9OfEzZnjv3gYYDtg2k9p1xph0LMORMS", methods=['GET', 'POST'])
def webhook():
    data = request.get_json()
    t = Thread(target=process_webhook, args=(data, ))
    t.start()
    return 'Hello from polifonia-nsk.ru!!'
