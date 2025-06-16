import reflex as rx
from .service.hunglin_page import hunglin_page, fnc_personas


app = rx.App()
app.add_page(hunglin_page)
# app.add_page(fnc_personas, route='/personas')

