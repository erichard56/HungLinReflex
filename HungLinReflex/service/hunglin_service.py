import reflex as rx
import icecream as ic
from typing import List
from ..models.hunglin_models import Frase, Persona, PersonasLista, CasasLista
from ..repository.hunglin_repository import get_frase, chk_usuario, get_casas, \
        get_casa_detalles, get_personas, get_persona_detalles

def get_frase_service() -> Frase:
    frase = get_frase()
    return(frase)


def chk_usuario_service(usuario: str, clave: str) -> Persona:
    persona = chk_usuario(usuario, clave)
    return(persona)

def get_personas_service(id: int, busq: str, estado_id: int) -> List[PersonasLista]:
    personas = get_personas(id, busq, estado_id)
    return(personas)

def get_persona_detalles_service(id: int)-> list[list]:
    detalles, eventos, extras = get_persona_detalles(id)
    return(detalles, eventos, extras)


def get_casas_service() -> List[CasasLista]:
    casaslista = get_casas()
    return(casaslista)

def get_casa_detalles_service(id: int):
    personas = get_casa_detalles(id)
    return(personas)

