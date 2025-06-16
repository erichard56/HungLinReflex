import reflex as rx
from sqlmodel import Field
from typing import Optional, List
from datetime import date

class Frase(rx.Model, table=True):
    id: int = Field(default=None, primary_key=True)
    frase: str
    detalle: str

class Persona(rx.Model, table=True):
	id: int = Field(default=None, primary_key=True)
	orden: Optional[int] = Field(default=0)
	nombre: str = Field(max_length=50)
	apellido: str = Field(max_length=50)
	usuario: Optional[str] = Field(default=None, max_length=50)
	direccion: Optional[str] | None = Field(max_length=50)
	localidad: Optional[str] | None = Field(max_length=50)
	codigo_postal: Optional[str] | None = Field(max_length=10)
	email: Optional[str] | None = Field(max_length=50)
	fechanacimiento: date
	fechaingreso: date					#10
	fechaegreso: Optional[date]
	celular: Optional[str] | None = Field(max_length=50)
	nrodoc: int = Field(default=0)
	casa_practica_id: int = Field(foreign_key='bosquetaoista_casa.id')
	grado_id: int | None = Field(default=None, foreign_key="bosquetaoista_grado.id")
	responsable_casa_id: int | None = Field(foreign_key='bosquetaoista_casa.id')
	tipodoc_id: int = Field(foreign_key='bosquetaoista_tipodoc.id')
	estado_id: int | None = Field(default=None, foreign_key="bosquetaoista_tipoestado.id")
	foto: Optional[str]
	certificado: Optional[str]			#20
	clave: Optional[str]
	is_superuser: Optional[int]
	is_staff: Optional[int]

class PersonasLista(rx.Model, table=False):
	id: int
	orden: int
	foto: str
	ayn: str
	grado: str
	casa: str


# Casa
class Casa(rx.Model, table=True):
	id: int = Field(default=None, primary_key=True)
	nombre: str = Field(max_length=200)
	direccion: str = Field(max_length=200)

class Grado(rx.Model, table=True):
	id: int = Field(default=None, primary_key=True)
	nombre: str = Field(max_length=20)



class CasasLista(rx.Model, table=False):
	id: int
	nombre: str
	direccion: str
	responsable: str
	anf: str
