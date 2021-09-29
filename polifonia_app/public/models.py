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

    def __init__(self, price: int, rate: float = 0) -> None:
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
    sum = IntegerField(
        'Сумма к оплате', [validators.DataRequired()], _name='sum'
    )
    service_name = StringField('Название услуги', [validators.DataRequired()])
    clientid = StringField(
        'Представьтесь, пожалуйста '
        '(как угодно, главное - чтобы мы вас опознали)',
        [validators.DataRequired()]
    )
    submit = SubmitField('К оплате')


_links_template = """\
<a href="{link}">{desc}</a>
"""


class Product:

    def __init__(
        self,
        type_: str,
        pic: Path,
        name: str,
        price: int,
        quantaty: ty.Optional[int] = None,
        lifetime: ty.Optional[str] = None,
        comment: ty.Optional[str] = None,
        can_be_halfed: bool = False,
        links: ty.Dict[str, str] = {},
        can_be_paid: bool = True
    ) -> None:
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
        self.links: str = ', '.join(
            [_links_template.format(link=l, desc=d) for d, l in links.items()]
        )
        self.can_be_paid = can_be_paid


ab4 = Product(
    'Абонемент',
    Path('abonement4.png'),
    'на 4 занятия',
    4000,
    quantaty=4,
    lifetime="абонемент действителен 1 месяц, "
    "ещё месяц вы можете прогулять по уважительным причинам",
)
ab4_student = Product(
    'Абонемент',
    Path('abonement4.png'),
    'на 4 занятия (студенческий, групповой)',
    2400,
    quantaty=4,
    lifetime="абонемент действителен 1 месяц, "
    "ещё месяц вы можете прогулять по уважительным причинам",
)
ab8 = Product(
    'Абонемент',
    Path('abonement8.png'),
    'на 8 занятий',
    7200,
    quantaty=8,
    lifetime="абонемент действителен 1 месяц, "
    "ещё месяц вы можете прогулять по уважительным причинам",
)
ab24 = Product(
    'Абонемент',
    Path('abonement24.png'),
    'на 16 занятий',
    12800,
    quantaty=16,
    lifetime="абонемент действителен 2 месяца, "
    "ещё месяц вы можете прогулять по уважительным причинам",
)
lesson = Product(
    'Урок',
    Path('lesson.png'),
    'очный',
    1200,
    can_be_halfed=True,
    comment="пробное занятие — половина стоимости"
)
lesson_online = Product(
    'Урок',
    Path('lesson_online.png'),
    'онлайн',
    1000,
)
song = Product(
    'Сведение',
    Path('mix_song.png'),
    'голос + фонограмма',
    2000,
    comment='Сведение ансамблей и прочих нетипичных'
    ' случаев лучше обговорить отдельно)',
    links={'примеры': 'https://disk.yandex.ru/d/uw-OtVsBuZh2QA?w=1'}
)
arrangement = Product(
    'Аранжировка',
    Path('arrangement.png'),
    'под ключ',
    4000,
    comment='цена указана за минуту готовой фонограммы',
    links={
        'примеры': 'https://audiomack.com/levitanus',
        'ещё примеры': 'https://soundcloud.com/levitanus/sets'
    },
    can_be_paid=False,
)
rent = Product(
    'Аренда',
    Path('rent.png'),
    'для уроков и репетиций',
    200,
    comment='цена указана за час',
)
products = {
    ab4.id_: ab4,
    ab4_student.id_: ab4_student,
    ab8.id_: ab8,
    ab24.id_: ab24,
    lesson.id_: lesson,
    lesson_online.id_: lesson_online,
    song.id_: song,
    arrangement.id_: arrangement,
    rent.id_: rent,
}
