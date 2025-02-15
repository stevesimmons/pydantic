from typing import Optional, Union

from typing_extensions import Literal

from pydantic import BaseModel

class Dessert(BaseModel):
    kind: str

class Pie(Dessert):
    kind: Literal['pie']
    flavor: Optional[str]

class ApplePie(Pie):
    flavor: Literal['apple']

class PumpkinPie(Pie):
    flavor: Literal['pumpkin']

class Meal(BaseModel):
    dessert: Union[ApplePie, PumpkinPie, Pie, Dessert]

print(type(Meal(dessert={'kind': 'pie', 'flavor': 'apple'}).dessert).__name__)
#> ApplePie
print(type(Meal(dessert={'kind': 'pie', 'flavor': 'pumpkin'}).dessert).__name__)
#> PumpkinPie
print(type(Meal(dessert={'kind': 'pie'}).dessert).__name__)
#> Pie
print(type(Meal(dessert={'kind': 'cake'}).dessert).__name__)
#> Dessert
