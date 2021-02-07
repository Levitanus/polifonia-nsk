from flask_wtf import Form
from wtforms.fields import IntegerField
import typing as ty

from pathlib import Path

from transliterate import translit
from wtforms import (
    SubmitField,
    BooleanField,
    StringField,
    PasswordField,
    validators,
)


class Price:
    def __init__(self, price: int, rate: float = 3.3) -> None:
        self._value = price
        self._rate = rate

    @property
    def value(self) -> int:
        return int(self._value / (100 - self._rate) * 100)

    @property
    def comission(self) -> int:
        return self.value - self._value

    def __str__(self) -> str:
        return "{:,d}".format(self.value).replace(',', ' ')


class PaymentForm(Form):
    sum = IntegerField('Сумма к оплате', [validators.DataRequired()],
                       _name='sum')
    service_name = StringField('Название услуги', [validators.DataRequired()])
    client_id = StringField(
        'Представьтесь, пожалуйста '
        '(как угодно, главное - чтобы мы вас опознали)',
        [validators.DataRequired()])
    submit = SubmitField('К оплате')


class Product:
    def __init__(self,
                 type_: str,
                 pic: Path,
                 name: str,
                 price: int,
                 quantaty: ty.Optional[int] = None,
                 lifetime: ty.Optional[str] = None,
                 comment: ty.Optional[str] = None,
                 can_be_halfed: bool = False) -> None:
        self.type_ = type_
        self.pic = Path('/static/images') / pic
        self.name = name
        self.price = Price(price)
        self.quantaty = quantaty
        self.lifetime = lifetime
        self.comment = comment
        self.id_: str = translit(f'{type_} {name}', 'ru',
                                 True).replace(' ', '_')
        self.can_be_halfed = can_be_halfed


ab4 = Product(
    'Абонемент',
    Path('abonement4.png'),
    'на 4 занятия',
    3000,
    quantaty=4,
    lifetime="абонемент действителен 1 месяц, "
    "ещё месяц вы можете прогулять по уважительным причинам",
)
ab8 = Product(
    'Абонемент',
    Path('abonement8.png'),
    'на 8 занятий',
    5200,
    quantaty=8,
    lifetime="абонемент действителен 1 месяц, "
    "ещё месяц вы можете прогулять по уважительным причинам",
)
ab24 = Product(
    'Абонемент',
    Path('abonement24.png'),
    'на 24 занятия',
    13200,
    quantaty=24,
    lifetime="абонемент действителен 3 месяца, "
    "ещё месяц вы можете прогулять по уважительным причинам",
    comment='Возможна рассрочка по абонементу в'
    ' течение 2х месяцев: по 6 600₽',
    can_be_halfed=True,
)
products = {
    ab4.id_: ab4,
    ab8.id_: ab8,
    ab24.id_: ab24,
}
