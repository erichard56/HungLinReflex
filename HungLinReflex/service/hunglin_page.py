import reflex as rx
from icecream import ic
# from ..hunglin_base.navbar import navbar
# from ..hunglin_base.login import fnc_login
# from ..models.hunglin_models import Frase, Persona, Casa, CasasLista
from ..models.hunglin_models import Frase, PersonasLista
# from ..service.hunglin_service import , \
# 		, get_casa_detalles_service
from ..service.hunglin_service import get_frase_service, chk_usuario_service, \
		get_personas_service, get_persona_detalles_service, get_casas_service
# from ..hunglin_base import definiciones
from ..hunglin_pages.hunglin_personas import fnc_personas_detalles
from ..hunglin_pages.hunglin_casas import fnc_casas
from rxconfig import config


class HunglinState(rx.State):
	opcion: str = 'Im'
	frase: str = ''
	detalle: str = ''
	usuario: str
	clave: str
	is_superuser: int = 0
	is_staff: int = 0
	nombre: str = ''
	personas: list[tuple]
	detalles: tuple
	eventos: list[tuple]
	extras: list[tuple]
	casas: list[tuple]
	titulo: list[tuple]
	casa: str = ''
	responsablescasa: tuple

# opciones
	@rx.event(background=True)
	async def set_opcion(self, opc: str, id: int):
		async with self:
			self.opcion = opc
			if (opc == 'Im'):
				self.nombre = ''
			elif (opc == 'Pe'):
				self.personas = get_personas_service(id, '', 1)
			elif (opc == 'PeD'):
				self.detalles, self.eventos, self.extras = get_persona_detalles_service(id)
			elif (opc == 'Ca'):
				self.casas = get_casas_service()



# get_frase
	@rx.event(background=True)
	async def get_frase(self):
		async with self:
			frase = get_frase_service()
			self.frase = frase[1]
			self.detalle = frase[2]

# Ingresar
	@rx.event(background=True)
	async def set_usuario(self, usuario):
		async with self:
			self.usuario = usuario

	@rx.event(background=True)
	async def set_clave(self, clave):
		async with self:
			self.clave = clave

	@rx.event(background=True)
	async def ingresar(self):
		async with self:
			persona = chk_usuario_service(self.usuario, self.clave)
			if (persona is not None):
				self.nombre = persona[2].split(' ')[0]
				self.is_superuser = persona[22]
				self.is_staff = persona[23]
				self.opcion = "*"


# personas
	@rx.event(background=True)
	async def get_personas(self, id: int, busq: str, id_estado: int):
		async with self:
			personas = get_personas_service(id, busq, id_estado)
			return(personas)


	# @rx.event(background=True)
	# async def get_casas_lista(self):
	# 	async with self:
	# 		self.casaslista = get_casas_lista_service()


	# @rx.event(background=True)
	# async def get_casa_detalles(self, id):
	# 	async with self:
	# 		self.casa, self.responsables = get_casa_detalles_service(id)


# opciones
# @rx.event(background=True)
#async 
def fnc_set_opcion(opc: str, id: int):
	# async with self:
	HunglinStateopcion = opc
	if (opc == 'Im'):
		HunglinState.nombre = ''
	elif (opc == 'Pe'):
		HunglinState.personas = get_personas_service(id, '', 1)
	elif (opc == 'PeD'):
		HunglinState.detalles, HunglinState.eventos, HunglinState.extras = get_persona_detalles_service(id)
	elif (opc == 'Ca'):
		HunglinState.casas = get_casas_service()


@rx.page(route='/', on_load=HunglinState.get_frase)
def hunglin_page() -> rx.Component:
	return rx.box (
		navbar(HunglinState.nombre),
		rx.match(
			HunglinState.opcion,
			('Im', fnc_imagen()),
			('In', fnc_ingresar()),
			('Pe', fnc_personas()),
			('PeD', fnc_personas_detalles(HunglinState.detalles, HunglinState.eventos, HunglinState.extras)),
			('Ca', fnc_casas(HunglinState.casas)),
			('*' , fnc_imagen()),
		),
		show_frase(),
		text_align='center',
		justify='center',
		width='80vw'
	)

def show_frase() -> rx.Component:
	return rx.center(
		rx.vstack(
			rx.text(
				HunglinState.frase, 
				style={ 'color':'white' },
				size='5',
				# align='center', as_='div',
				width='70vw'
			),
			rx.text(
				HunglinState.detalle, 
				style={ 'color':'white' },
				size='4',
				align='center', as_='div',
				width='70vw'
			),
			margin_x='6vw',
			background_color ='#801316',
		),
	)

def fnc_imagen() -> rx.Component:
	return	rx.center(
		rx.image(
			src=rx.asset('bosquetaoista/EscuelaTaoistaHungLin.jpg'),
			width='70vw',
			margin_y='1vw',
		),
	)




####### navbar

def navbar_icons_item(icon: str, text: str, opc: str) -> rx.Component:
	return rx.button(
		rx.icon(icon), 
		text, 
		on_click=HunglinState.set_opcion(opc, 0)
	)


def navbar(nombre: str) -> rx.Component:
	return rx.container(
		rx.vstack(
			rx.hstack(
				rx.image(
					src="/bosquetaoista/bosquetaoista.jpg",
					width="30vw",
					height="auto",
					margin='1vw',
					padding='0vw',
				),
				rx.cond(
					nombre,
					rx.hstack(
						rx.text( 'Hola ', nombre, ' !!'),
						rx.button(
							rx.icon('angry'), 
							'Salir',
							on_click=HunglinState.set_opcion('Im', 0)
						)
					),
					rx.hstack(
						rx.text('Inicie conexion'),
						rx.button(
							rx.icon('smile'),
							'Ingresar',
							on_click=HunglinState.set_opcion('In', 0)
						)
					),
				),
				align_items='center',
			),
		),
		rx.cond(
			nombre,
			rx.hstack(
				rx.flex(
					# rx.button(
					# 	rx.icon('users'), 'Personas', on_click=HunglinState.set_opcion('Pe')
					# ),
					navbar_icons_item("users", "Personas", "Pe"),
					navbar_icons_item("home", "Agenda", "Ag"),
					navbar_icons_item("home", "Eventos", "Ev"),
					navbar_icons_item("house-plus", "Casas", "Ca"),
					navbar_icons_item("home", "Grados", "Gr"),
					navbar_icons_item("home", "Tipo Eventos", "Te"),
					navbar_icons_item("home", "Extras", "Ex"),
					spacing="5",
				),
				margin_x='1vw',
				bg=rx.color("accent", 3),
			),
		),
		text_align='center',
		justify='center',
	)


###### fnc_ingresar
def fnc_ingresar() -> rx.Component:
	return rx.box(
		rx.center(
			rx.vstack(
				rx.input(
					placeholder='Usuario',
					type='text',
					on_change=HunglinState.set_usuario,
				),
				rx.input(
					placeholder='Clave',
					type='password',
					on_change=HunglinState.set_clave,
				),
				rx.button(
					'Ingresar',
					on_click=HunglinState.ingresar,
				),
			),
			padding='2vw'
		),
		background_color ='#801316',
		width='22vw',
		height='auto',
		margin_x='30vw',
		margin_y='2vw',
	)


# personas
# @rx.page(route='/personas', on_load=HunglinState.get_personas(0, '', 1))
def fnc_personas() -> rx.Component:
	return rx.box(
		rx.box(
			rx.vstack( 
				rx.heading(
					'Personas',
					margin_x='4vw', 
					size='6', 
					style={'color':'black'},
				),
			),
			rx.text(' '),
			rx.table.root(
				rx.table.header(
					rx.table.row(
						rx.table.column_header_cell('Orden', width='10vw', style={'color':'black'}),
						rx.table.column_header_cell('Apellido y Nombre', width='50vw', style={'color':'black'}),
						rx.table.column_header_cell('Grado', width='20vw', style={'color':'black'}), 
						rx.table.column_header_cell('Casa Práctica', width='30vw', style={'color':'black'}), 
						rx.table.column_header_cell('Acciones', width='10vw', style={'color':'black'})
					)
				),
				rx.table.body(
					rx.foreach(HunglinState.personas, mostrar_persona),
					rx.text(' '),				
				),
			),
			background_color ='#fff',
			width='80vw',
			height='auto',
			margin_x='2vw',
			padding_bottom='1vw',
			padding_left='4vw'
		),
		# background_color ='#801316',
		width='100vw',
		height='auto'
	)

def mostrar_persona(persona) -> rx.Component:
	return rx.table.row(
		rx.table.cell(
			persona[1], 
			style={'color':'black'}
		),
		rx.table.cell(
			rx.hstack(
				rx.image(
					src=persona[2],
					width='4vw',
				),
				persona[3], 
				style={'color':'black'}
			),
		),
		rx.table.cell(
			rx.hstack(
				persona[4], 
				style={'color':'black'}
			),
		),
		rx.table.cell(
			rx.hstack(
				persona[5], 
				style={'color':'black'}
			),
		),
		rx.table.cell(
			rx.hstack(
				rx.button(
					rx.icon('pen')
				),
				rx.button(
					rx.icon('receipt-text'),
					on_click=HunglinState.set_opcion('PeD', persona[0])
				),
				rx.link(
					rx.button(
						rx.icon(
							'notebook-pen',
						),
					),
					href='/personaslista'
				),
				rx.link(
					rx.button(
						rx.icon(
							'receipt-text',
						),
					),
					href='/personaslista'
				),
				
		# 		rx.button(
		# 			rx.icon(
		# 				'users'
		# 			)
		# 		)
			)
		)
	)


# def fnc_personas_detalles() -> rx.Component:
# 	return rx.box(
# 		rx.heading(
# 			'---',
# 			HunglinState.detalles,
# 			'---',
# 			HunglinState.eventos,
# 			'---',
# 			HunglinState.extras,
# 			'---',
# 		),
# 		rx.table.root(
# 			rx.table.header(
# 				rx.table.row(
# 					rx.table.column_header_cell('Imagen', width='50vw', style={'color':'black'}),
# 					rx.table.column_header_cell('Datos', width='50vw', style={'color':'black'}),
# 				),
# 			),
# 			rx.table.body(
# 				rx.table.row(
# 					rx.table.cell(
# 						rx.vstack(
# 							rx.image(
# 								src=HunglinState.detalles[15],
# 								width="20vw",
# 								height="auto",
# 							),
# 							rx.image(
# 								src=HunglinState.detalles[16],
# 								width="20vw",
# 								height="auto",
# 							),
# 							margin='6vw',
# 							padding='0vw',
# 						),
# 					),
# 					rx.table.cell(
# 						rx.table.root(
# 							# rx.table.header(
# 							# 	rx.table.row(
# 							# 		rx.table.column_header_cell('Dato', width='60vw', style={'color':'black'}),
# 							# 		rx.table.column_header_cell('Valor', width='40vw', style={'color':'black'}),
# 							# 	),
# 							# ),
# 							rx.table.body(
# 								rx.table.row(
# 									rx.table.cell(rx.text('Orden ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[2])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Estado ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[3])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Grado ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[4])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Casa de Práctica ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[5])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Responsable de Casa ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[6])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Dirección ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[7])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Localidad ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[8])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('e-mail ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[9])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Fecha de Nacimiento ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[10])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Fecha de Ingreso ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[11])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Fecha de Egreso ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[12])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Documento ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[13], ' ', HunglinState.detalles[14])),
# 								),
# 								rx.table.row(
# 									rx.table.cell(rx.text('Privilegios ')),
# 									rx.table.cell(rx.text(HunglinState.detalles[17])),
# 								),
# 							),
# 						)
# 					)
# 				)
# 			)
# 		),
# 		margin='6vw'
# 	)
