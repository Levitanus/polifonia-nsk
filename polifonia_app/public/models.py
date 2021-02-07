import typing as ty

from pathlib import Path


class Product:

    def __init__(
        self,
        type_: str,
        pic: Path,
        name: str,
        price: str,
        lifetime: ty.Optional[ty.Tuple[str, int]] = None
    ) -> None:
        self.type_ = type_
        self.pic = Path('/static/images') / pic
        self.name = name
        self.price = price
        self.lifetime = lifetime


products = [
    Product(
        'Абонемент',
        Path('abonement4.png'),
        'на 4 занятия',
        "3 000",
        lifetime=("1 месяц", 1)
    ),
    Product(
        'Абонемент',
        Path('abonement8.png'),
        'на 8 занятия',
        "7 200",
        lifetime=("1 месяц", 1)
    ),
    Product(
        'Абонемент',
        Path('abonement24.png'),
        'на 24 занятия',
        "13 200",
        lifetime=("3 месяца", 1)
    ),
]
