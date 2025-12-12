from typing import Any, Callable

routes: dict[str, Callable[... ,Any]] = {}

def route(path: str):
    def register_route(func):
        routes[path] = func
        return func
    return register_route

# /shipment/12701
@route("/shipment/{id}")
def get_shipment(id):
    return "Shipment<1001, in transit>"

request: str = ""

while request != "quit":
    request = input(">  ")
    
    if request in routes:
        response = routes[request]()
        print(response, end="\n\n")
    else :
        print("not seen")