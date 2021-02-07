import typing as ty

from pathlib import Path

from transliterate import translit


class Product:
    def __init__(self,
                 type_: str,
                 pic: Path,
                 name: str,
                 price: str,
                 lifetime: ty.Optional[ty.Tuple[str, int]] = None,
                 comment: ty.Optional[str] = None) -> None:
        self.type_ = type_
        self.pic = Path('/static/images') / pic
        self.name = name
        self.price = price
        self.lifetime = lifetime
        self.comment = comment
        self.id_: str = translit(f'{type_} {name}', 'ru',
                                 True).replace(' ', '_')


ab4 = Product('Абонемент',
              Path('abonement4.png'),
              'на 4 занятия',
              "3 000",
              lifetime=("1 месяц", 1))
ab8 = Product('Абонемент',
              Path('abonement8.png'),
              'на 8 занятий',
              "5 200",
              lifetime=("1 месяц", 1))
ab24 = Product('Абонемент',
               Path('abonement24.png'),
               'на 24 занятия',
               "13 200",
               lifetime=("3 месяца", 1),
               comment='Возможна рассрочка по абонементу в'
               ' течение 2х месяцев: по 6 600₽')
products = {
    ab4.id_: ab4,
    ab8.id_: ab8,
    ab24.id_: ab24,
}
