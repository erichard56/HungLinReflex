import reflex as rx
from enum import Enum
import asyncio

from .db import db_get_usuario, db_get_frase
from .db import db_get_personas_lista, db_get_persona, db_get_persona_caps, db_get_persona_extras, db_get_persona_detalle_extra, db_put_persona_detalle_extra, db_persona_detalle_extra_delete, db_put_persona
from .db import db_get_estados, db_get_casas, db_get_grados
from .db import db_get_tipoextras, db_get_docs
# from .db import db_get_casas_lista, db_get_casa, db_put_casa, db_del_casa, db_get_cg_alumnos
# from .db import db_get_grados_lista, db_get_grado, db_put_grado
# from .db import db_get_persona
# # , db_get_grados, db_get_casas, 
# # from .db import db_get_personas, db_get_persona, , db_put_persona 
# # from .db import , 
from .notify import notify_component

from rxconfig import config


class State(rx.State):
	opc: str = "img"
	form_data: dict = {}
	error: str = ''

	nombre: str = ''
	is_superuser: int
	is_staff: int

	# solo para uso de seleccion en pagina personas
	select_casas_total: list
	select_estados_total: list
	select_grados_total: list

	selected_casa: str = 'Todas'
	selected_estado: str = 'Activo'
	selected_grado: str = 'Todos'

	# solo para uso de tablas que no cambian
	select_casas: list
	select_docs: list
	select_estados: list
	select_grados: list
	select_tipocursantes: list

	selected_doc: str = 'DNI'
	selected_tipocursante: str


#########

	personas: list[tuple]
	# estados: list
	# casas: list
	# grados: list
	# docs: list


	persona: tuple
	persona_id: int
	caps: list[tuple]
	extras: list[tuple]
	tipoextras: list
	extra_id: int
	extra: tuple

	# casas_lista: list[list]
	# casa: tuple
	# responsables: str

	# gradox: list[list]
	# grado: list
	# grados_lista: list


	# alumnos: list[tuple]




	# casas
	# casap: tuple
	# persona: tuple
	# tipoestados: list
	# tipoestado: str
	# casaspr: list
	# tipodocs: list
	# tipodoc: str
	# casa1: str
	# extra: tuple
	# casa_practica: str

	@rx.event()
	def cargar_tablas(self):
		self.select_docs: db_get_docs()
		self.select_tipocursantes: db_get_tipocursantes()


# handle's
	@rx.event()
	async def handle_notify(self):
		async with self:
			await asyncio.sleep(2)
			self.error = ''

	@rx.event(background=True)
	async def handle_ingresar(self, form_data: dict):
		async with self:
			self.form_data = form_data
			if (form_data['usuario'] and form_data['clave']):
				persona = db_get_usuario(form_data['usuario'], form_data['clave'])
				if (persona):
					self.nombre = persona[2].split()[0]
					self.is_superuser = persona[22]
					self.is_staff = persona[23]
				else:
					self.error = 'No existe el usuario'
			else:
				self.error = 'Falta usuario o clave'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def evt_select_estado(self, value):
		async with self:
			self.selected_estado = value

	@rx.event(background=True)
	async def evt_select_casa(self, value):
		async with self:
			self.selected_casa = value

	@rx.event(background=True)
	async def evt_select_grado(self, value):
		async with self:
			self.selected_grado = value

	# @rx.event(background=True)
	# async def handle_casa_am(self, form_data: dict):
	# 	async with self:
	# 		self.form_data = form_data
	# 		if (form_data['nombre'] and form_data['direccion']):
	# 			db_put_casa(form_data['id'], form_data['nombre'], form_data['direccion'])
	# 			self.casas_lista = db_get_casas_lista()
	# 			self.opc = 'cas'
	# 		else:
	# 			self.error = 'Falta nombre o direccion'
	# 	if (self.error != ''):
	# 		await self.handle_notify()

	@rx.event(background=True)
	async def handle_persona_am(self, form_data: dict):
		async with self:
			form_persona = form_data
			persona = db_put_persona(form_data)
			self.personas = db_get_personas_lista('', self.selected_estado, self.selected_casa, self.selectedgrado)
			self.opc = 'per'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def handle_personas(self, form_data: dict):
		async with self:
			self.select_casas_total = db_get_casas('T')
			self.select_estados_total = db_get_estados('T')
			self.select_grados_total = db_get_grados('T')
			self.personas = db_get_personas_lista(form_data['busq'], self.selected_estado, self.selected_casa, self.selected_grado)
			self.opc = 'per'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def handle_persona_detalle_extra_am(self, form_data: dict):
		async with self:
			db_put_persona_detalle_extra(form_data)
			self.persona = db_get_persona(form_data['persona_id'])
			self.caps = db_get_persona_caps(form_data['persona_id'])
			self.extras = db_get_persona_extras(form_data['persona_id'])
			self.tipoextras = db_get_tipoextras()
			self.opc = 'pde'
		if (self.error != ''):
			await self.handle_notify()

# 	@rx.event()
# 	def evt_tipoestado(self, value: str):
# 		self.tipoestado = value

# 	@rx.event()
# 	def evt_grado(self, value: str):
# 		self.grado = value


# eventos casas
	# @rx.event(background=True)
	# async def evt_casas_lista(self):
	# 	async with self:
	# 		self.casas_lista = db_get_casas_lista()
	# 		self.opc = "cas"

	# @rx.event(background=True)
	# async def evt_casa_am(self, id):
	# 	async with self:
	# 		self.casa = db_get_casa(id)
	# 		self.opc = "cam"

	# @rx.event(background=True)
	# async def evt_del_casa(self, casa_id):
	# 	async with self:
	# 		db_del_casa(casa_id)
	# 		self.casas_lista = db_get_casas_lista()
	# 		self.opc = "cas"

	# @rx.event(background=True)
	# async def evt_cg_alumnos(self, id):
	# 	async with self:
	# 		self.responsables, self.alumnos = db_get_cg_alumnos(id, 0)
	# 		self.opc = "cg"


# eventos persona
	@rx.event(background=True)
	async def evt_personas(self):
		async with self:
			self.select_casas_total = db_get_casas('T')
			self.select_estados_total = db_get_estados('T')
			self.select_grados_total = db_get_grados('T')
			self.selected_estado = 'Activo'
			self.selected_casa = 'Todas'
			self.selected_grado = 'Todos'
			self.personas = db_get_personas_lista('', self.selected_estado, self.selected_casa, self.selected_grado)
			self.opc = "per"

	@rx.event(background=True)
	async def evt_persona_am(self, id):
		async with self:
			self.persona = db_get_persona(int(id))
			self.select_estados = db_get_estados()
			self.select_grados = db_get_grados()
			self.select_casas = db_get_casas()
			self.select_docs = db_get_docs()
			self.selected_estado = self.persona[1]
			self.selected_grado = self.persona[6]
			self.selected_casa = self.persona[7]
			self.selected_doc = self.persona[17]
			self.opc = "pam"

	@rx.event(background=True)
	async def evt_persona_detalle_extra_delete(self, persona_id, extra_id):
		async with self:
			db_persona_detalle_extra_delete(persona_id, extra_id)
			self.persona = db_get_persona(persona_id)
			self.caps = db_get_persona_caps(persona_id)
			self.extras = db_get_persona_extras(persona_id)
			self.tipoextras = db_get_tipoextras()
			self.opc = 'pde'

	@rx.event(background=True)
	async def evt_persona_detalle(self, id):
		async with self:
			self.persona = db_get_persona(id)
			self.caps = db_get_persona_caps(id)
			self.extras = db_get_persona_extras(id)
			self.tipoextras = db_get_tipoextras()
			self.opc = 'pde'

	@rx.event(background=True)
	async def evt_persona_detalle_extras_am(self, ids: list):
		async with self:
			self.persona_id, self.extra_id = ids
			if (self.extra_id > 0):
				self.extra = db_get_persona_detalle_extra(self.extra_id)
				self.opc = 'pde'
			else:
				self.extra = ()
			self.opc = 'pdxam'

# eventos grados
	# @rx.event(background=True)
	# async def evt_grados_lista(self):
	# 	async with self:
	# 		self.gradox = db_get_grados_lista()
	# 		self.opc = "gra"

	# @rx.event(background=True)
	# async def evt_grado_detalle(self, grado_id):
	# 	async with self:
	# 		self.responsables, self.alumnos = db_get_cg_alumnos(0, grado_id)
	# 		self.opc = "cg"
			
	# @rx.event(background=True)
	# async def evt_grado_am(self, id):
	# 	async with self:
	# 		self.grado = db_get_grado(id)
	# 		self.opc = "gam"

	# @rx.event(background=True)
	# async def handle_grado_am(self, form_data: dict):
	# 	async with self:
	# 		self.form_data = form_data
	# 		if (form_data['nombre']):
	# 			db_put_grado(form_data['id'], form_data['nombre'])
	# 			self.grados_lista = db_get_grados_lista()
	# 			self.opc = 'gra'
	# 		else:
	# 			self.error = 'Falta nombre'
	# 	if (self.error != ''):
	# 		await self.handle_notify()

# eventos varios
	@rx.event(background=True)
	async def evt_salir(self):
		async with self:
			self.nombre = ''
			self.is_superuser = 0
			self.is_staff = 0
			self.opc = 'img'


#################
def index() -> rx.Component:
	return rx.container(
		rx.container(
			rx.vstack(
				rx.hstack(
					rx.image(src='/bosquetaoista/bosquetaoista.jpg'),
					rx.card(
						rx.cond(
							State.nombre == '',
							fnc_ingresar(),
							fnc_adentro(State.nombre),
						)
					)
				),
				rx.cond(
					State.nombre != '',
					fnc_menu(),
				),
				rx.match(
					State.opc,
					('img', fnc_imagen()),

					# ('cas', fnc_casas_lista(State.casas_lista)),
					# ('cam', fnc_casa_am(State.casa)),
					# ('cg', fnc_cg_alumnos(State.responsables, State.alumnos)),

					('per', fnc_personas(State.personas, State.select_estados_total, State.select_casas_total, State.select_grados_total)),
					('pam', fnc_persona_am(State.persona, State.select_estados, State.select_casas, State.select_docs)),
					('pde', fnc_persona_detalle(State.persona, State.caps, State.extras)),
					('pdxam', fnc_persona_detalle_extra_am(State.persona_id, State.extra_id, State.extra, State.tipoextras)),

					# ('gra', fnc_grados_lista(State.gradox)),
					# ('gam', fnc_grado_am(State.grado)),
				),
				spacing="5",
				justify_x="center",
				min_height="85vh",
			),
			rx.cond(
				State.error != '',
				notify_component(State.error, 'shield_alert', 'yellow'),
			),
			style={'background_color':'#ffffff'},
		),
		style={'background_color':'#801316'},
	)

#################
def fnc_adentro(nombre) -> rx.Component:
	return rx.box(
		rx.hstack(
			rx.text('Hola ', nombre, '!!!'),
			rx.button(rx.icon('angry'), 'Salir', on_click=State.evt_salir),
		),
	)

################# Casas

# def fnc_casa_row(casa: list) -> rx.Component:
# 	return rx.table.row(
# 		rx.table.cell(casa[1], vertical_align='middle'),
# 		rx.table.cell(casa[2], vertical_align='middle'),
# 		rx.table.cell(casa[3], vertical_align='middle'),
# 		rx.table.cell(casa[4], vertical_align='middle'),
# 		rx.table.cell(
# 			rx.hstack(
# 				rx.button(rx.icon('pencil'), on_click=State.evt_casa_am(casa[0])),
# 				rx.button(rx.icon('users'), on_click=State.evt_cg_alumnos(casa[0])),
# 				fnc_del_confirmation(casa[0], State.evt_del_casa),
# 			)
# 		)
# 	)

# def fnc_casas_lista(casas_lista) -> rx.Component:
# 	return rx.box(
# 		rx.card(
# 			rx.heading('CASAS', align='center'),
# 			rx.heading(
# 				rx.button(rx.icon('plus'), 'CASA'), 
# 				align='right', 
# 				on_click=State.evt_casa_am(0)
# 			),
# 		),
# 		rx.card(
# 			rx.table.root(
# 				rx.table.row(
# 					rx.table.column_header_cell('Nombre'),
# 					rx.table.column_header_cell('Direccion'),
# 					rx.table.column_header_cell('Responsable'),
# 					rx.table.column_header_cell('Alumnos (A/N/F)'),
# 					rx.table.column_header_cell('Acciones'),
# 				),
# 				rx.table.body(
# 					rx.foreach(casas_lista, fnc_casa_row),
# 				),
# 			),
# 		)
# 	)

# def fnc_casa_am(casa) -> rx.Component:
# 	return rx.center(
# 		rx.box(
# 			rx.card(
# 				rx.cond(
# 					casa[0] == 0,
# 					rx.text('NUEVA CASA', weight="bold", align='center'),
# 					rx.text('MODIFICACION CASA', weight="bold", align='center')
# 				),
# 			),
# 			rx.card(
# 				rx.form(
# 					rx.vstack(
# 						rx.input(value=casa[0], type='text', name='id', style={'width':'0px', 'height':'0px'}),
# 						rx.hstack(
# 							rx.text('Nombre: '),
# 							rx.input(type='text', default_value=casa[1], name='nombre', style={'width':'200px'}),
# 						),
# 						rx.hstack(
# 							rx.text('Dirección: '),
# 							rx.input(type='text', default_value=casa[2], name='direccion', style={'width':'200px'}),
# 						),
# 						rx.button('Confirmar', type='submit', style={'width':'100%'})
# 					),
# 					on_submit=State.handle_casa_am,
# 					reset_on_submit=True,
# 				)
# 			)
# 		),
# 		width='100%',
# 		margin_y='2vw'
# 	)

# def fnc_cg_alumno(alumno) -> rx.Component:
# 	return rx.table.row(
# 		rx.table.cell(alumno[1], vertical_align='middle'),
# 		rx.table.cell(rx.image(alumno[2], width='100%', high='auto')),
# 		rx.table.cell(alumno[3], vertical_align='middle'),
# 		rx.table.cell(alumno[4], vertical_align='middle'),
# 		rx.table.cell(alumno[5], vertical_align='middle'),
# 		rx.table.cell(
# 			rx.hstack(
# 				rx.button(rx.icon('pencil')), #, on_click=State.evt_casa_am(casa[0])),
# 				rx.button(rx.icon('notebook-text'), on_click=State.evt_persona_detalles(alumno[0])),
# 			)
# 		),
# 		width='100%',
# 	)

# def fnc_cg_alumnos(responsables, alumnos) -> rx.Component:
# 	return rx.box(
# 		rx.cond(
# 			responsables,
# 			rx.card(rx.text('RESPONSABLE(S) ', responsables, size='5', align='center')),
# 		),
# 		rx.card(
# 			rx.text('ALUMNOS', align='left'),
# 			rx.table.root(
# 				rx.table.row(
# 					rx.table.column_header_cell('Orden', width='10%'),
# 					rx.table.column_header_cell('Foto', width='10%'),
# 					rx.table.column_header_cell('Apellido y Nombre', width='40%'),
# 					rx.table.column_header_cell('Grado', width='20%'),
# 					rx.table.column_header_cell('Casa de Practica', width='20%'),
# 					rx.table.column_header_cell('Acciones', width='10%'),
# 				),
# 				rx.table.body(
# 					rx.foreach(alumnos, fnc_cg_alumno),
# 				),
# 			),
# 		)
# 	)



################# Grados
# def fnc_grado(grado: list) -> rx.Component:
# 	return rx.table.row(
# 		rx.table.cell(grado[1]),
# 		rx.table.cell(grado[2]),
# 		rx.table.cell(grado[3]),
# 		rx.table.cell(
# 			rx.hstack(
# 				rx.button(rx.icon('pencil'), on_click=State.evt_grado_am(grado[0])),
# 				rx.button(rx.icon('users'), on_click=State.evt_grado_detalle(grado[0])),
# 			)
# 		)
# 	)

# def fnc_grados_lista(grados) -> rx.Component:
# 	return rx.box(
# 			rx.card(
# 				rx.heading('GRADOS', align='center'),
# 				rx.text(
# 					rx.button(rx.icon('plus'), 'GRADOS'), 
# 					align='right', 
# 					on_click=State.evt_grado_am(0)
# 				),
# 			),
# 				rx.card(

# 		rx.table.root(
# 			rx.table.row(
# 				rx.table.column_header_cell('Nombre', width='50%'),
# 				rx.table.column_header_cell('Activos', width='15%'),
# 				rx.table.column_header_cell('No Activos', width='15%'),
# 				rx.table.column_header_cell('Acciones', width='10%'),
# 			),
# 			rx.table.body(
# 				rx.foreach(grados, fnc_grado),
# 			),
# 		),
# 		),
# 		width='100%'
# 	)

# def fnc_grado_alumno(alumno) -> rx.Component:
# 	return rx.table.row(
# 		rx.table.cell(alumno[1]),
# 		rx.table.cell(
# 			rx.hstack(
# 				rx.image(alumno[2], width='10%', high='auto'), 
# 				alumno[3]
# 			),
# 		),
# 		rx.table.cell(alumno[4]),
# 		rx.table.cell(
# 			rx.hstack(
# 				rx.button(rx.icon('pencil')), #, on_click=State.evt_casa_am(casa[0])),
# 				rx.button(rx.icon('users')) #, on_click=State.evt_casa_detalle(casa[0])),
# 			)
# 		),
# 		width='100%'
# 	)

# def fnc_grado_alumnos(grado, alumnos) -> rx.Component:
# 	return rx.box(
# 		rx.card(
# 			rx.text('GRADO ', grado, size='6', align='center'),
# 		),
# 		rx.card(
# 			rx.text('ALUMNOS', align='left'),
# 			rx.table.root(
# 				rx.table.row(
# 					rx.table.column_header_cell('Orden', width='10%'),
# 					rx.table.column_header_cell('Apellido y Nombre', width='50%'),
# 					rx.table.column_header_cell('Casa de Practica', width='30%'),
# 					rx.table.column_header_cell('Acciones', width='10%'),
# 				),
# 				rx.table.body(
# 					rx.foreach(alumnos, fnc_grado_alumno),
# 				),
# 			),
# 		)
# 	)

# def fnc_grado_am(grado) -> rx.Component:
# 	return rx.center(
# 		rx.box(
# 			rx.card(
# 				rx.cond(
# 					grado[0] == 0,
# 					rx.text('NUEVO GRADO', weight="bold", align='center'),
# 					rx.text('MODIFICACION GRADO', weight="bold", align='center')
# 				),
# 			),
# 			rx.card(
# 				rx.form(
# 					rx.vstack(
# 						rx.input(value=grado[0], type='text', name='id', style={'width':'0px', 'height':'0px'}),
# 						rx.hstack(
# 							rx.text('Nombre: '),
# 							rx.input(type='text', default_value=grado[1], name='nombre', style={'width':'200px'}),
# 						),
# 						rx.button('Confirmar', type='submit', style={'width':'100%'})
# 					),
# 					on_submit=State.handle_grado_am,
# 					reset_on_submit=True,
# 				)
# 			)
# 		),
# 		width='100%',
# 		margin_y='2vw'
# 	)


################# Personas

def fnc_persona_am(persona: list, estados, casas, docs) -> rx.Component:
	return rx.box(
		rx.card(
			rx.cond(
				persona[0] == 0,
				rx.heading('NUEVA PERSONA', weight="bold", align='center'),
				rx.heading('MODIFICACION PERSONA', weight="bold", align='center')
			),
			rx.form(
				rx.table.root(
					rx.table.header(
						rx.table.row(
							rx.table.column_header_cell(width='50%', height='0vw'),
							rx.table.column_header_cell(width='50%', height='0vw'),
						),
					),
					rx.table.body(
						rx.input(value=persona[0], type='text', name='id', style={'width':'0px', 'height':'0px'}),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('*Estado: '),
									rx.select(estados, default_value=persona[1], value=persona[1], name='estado'),
								),
							),
							rx.table.cell(
								rx.hstack(
									rx.text('Orden: '),
									rx.input(type='number', default_value=persona[2], name='orden', style={'width':'50px'}),
								)
							),
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('*Apellido: '),
									rx.input(type='text', default_value=persona[3], name='apellido', required=True, style={'width':'200px'}),
								),
							),
							rx.table.cell(
								rx.hstack(
									rx.text('*Nombre: '),
									rx.input(type='text', default_value=persona[4], name='nombre', required=True, style={'width':'200px'}),
								)
							),
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Usuario: '),
									rx.cond(
										State.is_superuser != 1,
										rx.input(type='text', default_value=persona[5], name='usuario', disabled=True, style={'width':'200px'}),
										rx.input(type='text', default_value=persona[5], name='usuario', style={'width':'200px'}),
									),
								)
							),
							rx.table.cell(
								rx.hstack(
									rx.text('*Grado: '),
									rx.select(State.select_grados, default_value=persona[6], name='grado', required=True),
								),
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('*Casa de Practica: '),
									rx.select(casas, default_value=persona[7], name='casapractica', required=True), 
								),
							),
							rx.table.cell(
								rx.hstack(
									rx.text('Responsable Casa: '),
									rx.cond(
										persona[8],
										rx.select(casas, default_value=persona[8], name='responsablecasa', required=False), 
										rx.select(casas, default_value=None, name='responsablecasa', required=False), 
									)
								),
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Direccion: '),
									rx.input(type='text', default_value=persona[9], name='direccion', style={'width':'200px'}),
								)
							),
							rx.table.cell(
								rx.hstack(
									rx.text('Localidad: '),
									rx.input(type='text', default_value=persona[10], name='localidad', style={'width':'200px'}),
								)
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Codigo Postal: '),
									rx.input(type='text', default_value=persona[11], name='codigo_postal', style={'width':'200px'}),
								)
							),
							rx.table.cell(
								rx.hstack(
									rx.text('e-mail: '),
									rx.input(type='text', default_value=persona[12], name='email', style={'width':'200px'}),
								)
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Fecha de Nacimiento: '),
									rx.input(type='date', default_value=persona[13], name='fechanacimiento', style={'width':'200px'}),
								)
							),
							rx.table.cell(
								rx.hstack(
									rx.text('Fecha de Ingreso: '),
									rx.input(type='date', default_value=persona[14], name='fechaingreso', style={'width':'200px'}),
								)
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Fecha de Egreso: '),
									rx.input(type='text', default_value=persona[15], name='fechaegreso', style={'width':'200px'}),
								),
							),
							rx.table.cell(),		# para completar el row()
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Celular: '),
									rx.input(type='text', default_value=persona[16], name='celular', style={'width':'200px'}),
								)
							),
							rx.table.cell(
								rx.hstack(
									rx.text('Documento: '),
									rx.select(docs, default_value=persona[17], name='tipodoc'), 
									rx.input(type='text', default_value=persona[18], name='nrodoc', style={'width':'200px'}),
								)
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.text('Clave: '),
									rx.input(type='password', default_value=persona[19], name='clave', style={'width':'200px'}),
								)
							),
							rx.table.cell(
								rx.vstack(
									rx.hstack(
										rx.checkbox(name='is_superuser', label='Superusuario? ', default_checked=persona[20]),
										rx.text('SuperUsuario'),
										rx.checkbox(name='is_staff', label='Staff? ', default_checked=persona[21]),
										rx.text('Staff'),
									),
								)
							)
						),
						rx.table.row(
							rx.table.cell(
								rx.hstack(
									rx.vstack(
										rx.hstack(
											rx.text('Foto'),
											rx.image(src=persona[22], width='160px', high='auto'),
											# rx.checkbox(name='eliminar_foto', label='Eliminar'),
											# rx.text('Eliminar'),
										),
										rx.input(type='file', name='foto', accept='image/*'),
									),
								),
							),
							rx.table.cell(
								rx.hstack(
									rx.vstack(
										rx.hstack(
											rx.text('Certificado'),
											rx.image(src=persona[23], width='150px', high='auto'),
											# rx.checkbox(name='eliminar_cert', label='Eliminar', justify_y='50px'),
											# rx.text('Eliminar'),
										),
										rx.input(type='file', name='certificado', accept='image/*'),
									),
								),
							),
						),
					)
				),
				rx.button('Confirmar', type='submit', style={'width':'100%'}),
				on_submit=State.handle_persona_am,
				reset_on_submit=True,
			)
		),
		width='100%',
		margin_y='1vw',
	)

def fnc_persona(persona: list) -> rx.Component:
	return rx.table.row(
		rx.table.cell(persona[1], vertical_align="middle"),
		rx.table.cell(persona[2], vertical_align="middle"),
		rx.table.cell(rx.image(persona[3], width='100%', high='auto')), 
		rx.table.cell(persona[4], vertical_align="middle"),
		rx.table.cell(persona[5], vertical_align="middle"),
		rx.table.cell(persona[6], vertical_align="middle"),
		rx.table.cell(
			rx.hstack(
				rx.button(rx.icon('pencil'), on_click=State.evt_persona_am(persona[0])),
				rx.button(rx.icon('notebook-text'), on_click=State.evt_persona_detalle(persona[0])),
			),
		),
	)

def fnc_personas(personas, estados, casas, grados) -> rx.Component:
	return rx.box(
		rx.card(
			rx.hstack(
				rx.form(
					rx.hstack(
						rx.input(placeholder='Buscar...', type='text', name='busq'),
						rx.select(estados, name='estado', defaut_value=State.selected_estado, on_change=State.evt_select_estado),
						rx.select(casas, name='casa', default_value=State.selected_casa, on_change=State.evt_select_casa),
						rx.select(grados, name='grado', default_value=State.selected_grado, on_change=State.evt_select_grado),
						rx.button(rx.icon('search'), 'Buscar', type='submit'),
					),
					on_submit=State.handle_personas,
					reset_on_submit=True,
				),
				rx.button(rx.icon('plus'), 'PERSONA', align='right', on_click=State.evt_persona_am(0)),
			),
		),

		rx.card(
			rx.table.root(
				rx.table.row(
					rx.table.column_header_cell('Orden', width='5%'),
					rx.table.column_header_cell('Estado', width='10%'),
					rx.table.column_header_cell('Foto', width='10%'),
					rx.table.column_header_cell('Apellido y Nombre', width='25%'),
					rx.table.column_header_cell('Grado', width='10%'),
					rx.table.column_header_cell('Casa de Practica', width='10%'),
					rx.table.column_header_cell('Acciones', width='10%'),
				),
				rx.table.body(
					rx.foreach(personas, fnc_persona),
				),
			),
		),
	)

def fnc_persona_detalle_cap(cap) -> rx.Component:
	return rx.table.row(
		rx.table.cell(cap[0]),
		rx.table.cell(cap[1]),
		rx.table.cell(cap[2]),
		rx.table.cell(cap[3]),
		rx.table.cell(cap[4]),
	)

def fnc_persona_detalle_extra_am(persona_id: int, extra_id: int, extras: list, tipoextras) -> rx.Component:
	return rx.box(
		rx.center(
			rx.vstack(
				rx.card(
					rx.cond(
						extra_id,
						rx.heading('MODIFICACION EXTRA', weight="bold", align='center'),
						rx.heading('NUEVO EXTRA', weight="bold", align='center'),
					),
					width='100%'
				),
				rx.card(
					rx.form(
						rx.input(value=persona_id, name='persona_id', width='0%', height='0px'),
						rx.input(value=extra_id, name='extra_id', width='0%', height='0px'),
						rx.vstack(
							rx.select(tipoextras, default_value=extras[0], value=extras[0], name='extra', width='100%'),
							rx.input(default_value=extras[1], type='text', name='cmntx', width='100%'),
						),
						rx.button('Confirmar', type='submit', style={'width':'100%'}, margin_y='1vw'),
						on_submit=State.handle_persona_detalle_extra_am,
						reset_on_submit=True,
					),
					width='100%'
				),
			),
		),
		width='100%',
		margin_y='1vw',
	)

def fnc_persona_detalle_extra(extra) -> rx.Component:
	return rx.table.row(
		rx.table.cell(
			rx.text(extra[2], width='100%'),
		),
		rx.table.cell(
			rx.text(extra[3]),
		),
		rx.table.cell(
			rx.hstack(
				rx.button(rx.icon('pencil'), on_click=State.evt_persona_detalle_extras_am([extra[0], extra[1]])),
				rx.alert_dialog.root(
					rx.alert_dialog.trigger(rx.button(rx.icon('trash'))),
					rx.alert_dialog.content(
						rx.hstack(
							rx.alert_dialog.description('Seguro ????'),
							rx.flex(
								rx.alert_dialog.cancel(rx.button('Cancel')),
								rx.alert_dialog.action(rx.button('Ok'), on_click=State.evt_persona_detalle_extra_delete(extra[0], extra[1])),
								spacing = '3',
							),
						)
					),
				)
			)
		)
	)

def fnc_persona_detalle(persona: list, caps: list, extras: list) -> rx.Component:
	return rx.box(
		rx.card(
			rx.heading(persona[3], ', ', persona[4], weight="bold", align='center'),
		),
		rx.card(
			rx.table.root(
				rx.table.header(
					rx.table.row(
						rx.table.column_header_cell('Imagen', width='40%', height='0vw'),
						rx.table.column_header_cell('Datos', width='60%', height='0vw'),
					),
				),
				rx.table.body(
					rx.table.row(
						rx.table.cell(
							rx.vstack(
								rx.image(src=persona[22], width='100%', high='auto'),
								rx.image(src=persona[23], width='100%', high='auto'),
							)
						),
						rx.table.root(
							rx.table.header(
								rx.table.row(
									rx.table.column_header_cell(width='50%', height='0vw'),
									rx.table.column_header_cell(width='50%', height='0vw'),
								),
							),
							rx.table.body(
								rx.table.row(
									rx.table.cell('Orden'),
									rx.table.cell(persona[2])
								),
								rx.table.row(
									rx.table.cell('Estado'),
									rx.table.cell(persona[1]),
								),
								rx.table.row(
									rx.table.cell('Grado: '),
									rx.table.cell(persona[6]),
								),
								rx.table.row(
									rx.table.cell('Casa de Práctica'),
									rx.table.cell(persona[7]),
								),
								rx.cond(
									persona[8],
									rx.table.row(
										rx.table.cell('Responsable Casa'),
										rx.table.cell(persona[8]),
									),
								),
								rx.table.row(
									rx.table.cell('Dirección'),
									rx.table.cell(persona[9]),
								),
								rx.table.row(
									rx.table.cell('Localidad'),
									rx.table.cell(persona[10]),
								),
								rx.table.row(
									rx.table.cell('Código Postal'),
									rx.table.cell(persona[11]),
								),
								rx.table.row(
									rx.table.cell('Email'),
									rx.table.cell(persona[12]),
								),
								rx.table.row(
									rx.table.cell('Fecha de Nacimiento'),
									rx.table.cell(persona[13]),
								),
								rx.table.row(
									rx.table.cell('Fecha de Ingreso'),
									rx.table.cell(persona[14]),
								),
								rx.cond(
									persona[15],
									rx.table.row(
										rx.table.cell('Fecha de Egreso'),
										rx.table.cell(persona[15]),
									),
								),
								rx.table.row(
									rx.table.cell('Celular'),
									rx.table.cell(persona[16]),
								),
								rx.table.row(
									rx.table.cell('Documento'),
									rx.table.cell(persona[17], ' ', persona[18]),
								),
								rx.cond(
									persona[5],
									rx.table.row(
										rx.table.cell('Usuario'),
										rx.table.cell(
											persona[5],
											rx.cond(
												persona[20] == 1,
												' *Superuser* ',
												''
											),
											rx.cond(
												persona[21] == 1,
												' *Staff*',
												''
											)
										),
									),
								),
							),
						),
					)
				),
			)
		),

		rx.card(
			rx.heading('CURSOS / ACTIVIDADES / PRACTICAS', weight="bold", align='center'),
		),
		rx.card(
			rx.table.root(
				rx.table.header(
					rx.table.row(
						rx.table.column_header_cell('Tipo', width='10%', height='0vw'),
						rx.table.column_header_cell('Nombre', width='25%', height='0vw'),
						rx.table.column_header_cell('Fecha', width='15%', height='0vw'),
						rx.table.column_header_cell('Orador', width='30%', height='0vw'),
						rx.table.column_header_cell('Estado', width='10%', height='0vw'),
					),
				),
				rx.table.body(
					rx.foreach(caps, fnc_persona_detalle_cap)
				),
			),
		),

		rx.card(
			rx.heading('INFORMACION EXTRA', weight="bold", align='center'),
			rx.heading(
				rx.button(rx.icon('plus'), 'Nuevo', on_click=State.evt_persona_detalle_extras_am([persona[0], 0])), align='right'
			),
		),
		rx.card(
			rx.table.root(
				rx.table.header(
					rx.table.row(
						rx.table.column_header_cell('Tipo', width='25%'),
						rx.table.column_header_cell('Comentario', width='65%'),
						rx.table.column_header_cell('Acciones', width='10%'),
					),
				),
				rx.table.body(
					rx.foreach(extras, fnc_persona_detalle_extra)
				),
			),
		),
		width='100%',
		margin_y='1vw',
	)




################## Varios
def fnc_imagen() -> rx.Component:
	frase, detalle = db_get_frase()
	return rx.box(
		rx.image(src='/bosquetaoista/EscuelaTaoistaHungLin.jpg'),
		rx.center(
			rx.card(
				rx.text(frase, size='6', align = 'center'),
				rx.text(detalle, size='4', align = 'center'),
			),
			padding_y='1vw',
			width='100%'
		),
	)

def fnc_ingresar() -> rx.Component:
	return rx.form(
		rx.hstack(
			rx.vstack(
				rx.input(placeholder='Usuario', type='text', name='usuario'),
				rx.input(placeholder='Clave', type='password', name='clave'),
			),
			rx.button(rx.icon('smile'), 'Ingresar', type='submit'),
		),
		on_submit=State.handle_ingresar,
		reset_on_submit=True,
	)

def fnc_menu() -> rx.Component:
	return rx.center(
		rx.box(
			rx.hstack(
				rx.button(rx.icon('users-round'), 'Personas', on_click=State.evt_personas()),
				rx.button(rx.icon('calendar-days'), 'Agenda'),
				rx.button(rx.icon('ticket'), 'Eventos'),
				rx.button(rx.icon('house'), 'Casas'), #, on_click=State.evt_casas_lista()),
				rx.button(rx.icon('graduation-cap'), 'Grados'), #, on_click=State.evt_grados_lista()),
				rx.button(rx.icon('list'), 'Tipo Eventos'),
				rx.button(rx.icon('list'), 'Extras'),
			),
		),
		width='100%',
	)

def fnc_del_confirmation(casa_id, fnc) -> rx.Component:
	return rx.box(
		rx.alert_dialog.root(
			rx.alert_dialog.trigger(rx.button(rx.icon('trash'))),
			rx.alert_dialog.content(
				rx.hstack(
					rx.alert_dialog.description('Seguro ????'),
					rx.flex(
						rx.alert_dialog.cancel(rx.button('Cancel')),
						rx.alert_dialog.action(rx.button('Ok'), on_click=fnc(casa_id)),
						spacing = '3',
					),
				)
			),
		)
	)



#################
app = rx.App()
app.add_page(index)
