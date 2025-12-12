from typing import Any


class City:
    def __init__(self, name, location):
        self.name= name
        self.location = location

text: str ='value'
number : int|float =12
optional: str | None

optional = "value"

digits: list[int] =[1, 2, 3, 4, 5]

table_5:tuple[int, ...]=(5, 10, 15, 20, 25)

Taipei = City('Taipei',205544)
city_temp: tuple[City, float] = ("City", 20.5) 

shipment :dict[str, Any]={
    "content": 'wooden table',
    "id" : 10545,
    "weight":1.2,
    "status" : "in transit",
}

def root(num: int | float, exp: float | None= .5)-> float:
    return pow(num, .5)

root_25 =root(25)root_25 =root(25)