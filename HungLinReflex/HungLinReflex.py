import reflex as rx
import asyncio

from .db import db_get_usuario, db_get_casas_full, db_get_casa, db_put_casa, db_get_frase, db_get_alumnos
from .db import db_get_personas, db_get_persona, db_get_tipoestados, db_get_grados, db_get_casas, db_get_tipodocs
from .db import db_put_persona
from .notify import notify_component

from rxconfig import config


class State(rx.State):
	opc: str = "img"
	form_data: dict = {}
	nombre: str = ''
	is_superuser: int
	is_staff: int
	error: str = ''
	casas: list[list]
	casa: tuple
	casap: tuple
	responsables: str
	alumnos: list[tuple]
	personas: list[tuple]
	persona: tuple
	tipoestados: list
	tipoestado: str
	grados: list
	grado: str
	casaspr: list
	tipodocs: list
	tipodoc: str
	casa1: str
	uploaded_files: list[str] = []

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
	async def handle_casa_am(self, form_data: dict):
		async with self:
			self.form_data = form_data
			if (form_data['nombre'] and form_data['direccion']):
				casa = db_put_casa(form_data['id'], form_data['nombre'], form_data['direccion'])
				self.casas = db_get_casas_full()
				self.opc = 'cas'
			else:
				self.error = 'Falta nombre o direccion'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event(background=True)
	async def handle_persona_am(self, form_data: dict):
		async with self:
			form_persona = form_data
			persona = db_put_persona(form_data)
			self.personas = db_get_personas()
			self.opc = 'per'
		if (self.error != ''):
			await self.handle_notify()

	@rx.event()
	def evt_tipoestado(self, value: str):
		self.tipoestado = value

	@rx.event()
	def evt_grado(self, value: str):
		self.grado = value


# eventos casas
	@rx.event(background=True)
	async def evt_casa_am(self, id):
		async with self:
			if (id != 0):
				self.casa = db_get_casa(id)
			else:
				self.casa = (0, '', '')
			self.opc = "cam"

	@rx.event(background=True)
	async def evt_casa_detalle(self, id):
		async with self:
			self.casap, self.responsables, self.alumnos = db_get_alumnos(id)
			self.opc = "cad"

	@rx.event(background=True)
	async def evt_casas(self):
		async with self:
			self.casas = db_get_casas_full()
			self.opc = "cas"

# eventos persona
	@rx.event(background=True)
	async def evt_persona_am(self, id):
		async with self:
			if (id != 0):
				self.persona = db_get_persona(id)
			else:
				self.persona = (0, '', '')
			self.opc = "pam"

	@rx.event(background=True)
	async def evt_personas(self):
		async with self:
			self.personas = db_get_personas()
			self.opc = "per"

	@rx.event(background=True)
	async def evt_persona_am(self, id):
		async with self:
			if (id != 0):
				self.persona = db_get_persona(id)
				print(self.persona)
			else:
				self.persona = (0, '', '')

			self.tipoestados = db_get_tipoestados()
			self.tipoestado = self.persona[1]
			self.grados = db_get_grados()
			self.grado = self.persona[6]
			self.casaspr = db_get_casas()
			self.casa1 = self.persona[7]
			self.tipodocs = db_get_tipodocs()
			self.tipodoc = self.persona[17]
			self.opc = "pam"

	@rx.event
	async def handle_foto(self, files: list[rx.UploadFile]):
		for file in files:
			data = await file.read()
			path = rx.get_upload_dir() / file.name
			# with path.open('wb') as f:
			# 	f.write(data)

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
		rx.vstack(
			rx.hstack(
				rx.image(src='/bosquetaoista/bosquetaoista.jpg'),
				rx.cond(
					State.nombre == '',
					fnc_ingresar(),
					fnc_adentro(),
				)
			),
			rx.cond(
				State.nombre != '',
				fnc_menu(),
			),
			
			rx.match(
				State.opc,
				('img', fnc_imagen()),
				('cas', fnc_casas()),
				('cam', fnc_casa_am(State.casa)),
				('cad', fnc_casa_alumnos(State.alumnos)),
				('per', fnc_personas(State.personas)),
				('pam', fnc_persona_am(State.persona)),
			),
			spacing="5",
			justify_x="center",
			min_height="85vh",
		),
		rx.cond(
			State.error != '',
			notify_component(State.error, 'shield_alert', 'yellow'),
		),
		# style={'background_color':'#801316'},
	)

#################
def fnc_adentro() -> rx.Component:
	return rx.box(
		rx.hstack(
			rx.text('Hola ', State.nombre, '!!!'),
			rx.button(rx.icon('angry'), 'Salir', on_click=State.evt_salir),
		),
	)

#################
def fnc_casa(casa: list) -> rx.Component:
	return rx.table.row(
		rx.table.cell(casa[1]),
		rx.table.cell(casa[2]),
		rx.table.cell(casa[3]),
		rx.table.cell(casa[4]),
		rx.table.cell(
			rx.hstack(
				rx.button(rx.icon('pencil'), on_click=State.evt_casa_am(casa[0])),
				rx.button(rx.icon('users'), on_click=State.evt_casa_detalle(casa[0])),
			)
		)
	)

def fnc_casas() -> rx.Component:
	return rx.card(
		rx.text(
			rx.button(rx.icon('plus'), 'CASAS'), 
			align='right', 
			on_click=State.evt_casa_am(0)
		),
		rx.table.root(
			rx.table.row(
				rx.table.column_header_cell('Nombre'),
				rx.table.column_header_cell('Direccion'),
				rx.table.column_header_cell('Responsable'),
				rx.table.column_header_cell('Alumnos (A/N/F)'),
				rx.table.column_header_cell('Acciones'),
			),
			rx.table.body(
				rx.foreach(State.casas, fnc_casa),
			),
		),
	)

def fnc_casa_am(casa) -> rx.Component:
	return rx.center(
		rx.card(
			rx.cond(
				casa[0] == 0,
				rx.text('NUEVA CASA', weight="bold", align='center'),
				rx.text('MODIFICACION CASA', weight="bold", align='center')
			),
			rx.form(
				rx.vstack(
					rx.box(
						rx.input(value=casa[0],  type='text', name='id', style={'width':'0px', 'height':'0px'}),
					),
					rx.input(placeholder=casa[1], type='text', default_value=casa[1], name='nombre', style={'width':'200px'}),
					rx.input(placeholder=casa[2], type='text', default_value=casa[2], name='direccion', style={'width':'200px'}),
					rx.button('Confirmar', type='submit', style={'width':'100%'})
				),
				on_submit=State.handle_casa_am,
				reset_on_submit=True,
			)
		),
		width='100%',
		margin_y='2vw'
	)

def fnc_casa_alumno(alumno) -> rx.Component:
	return rx.table.row(
		rx.table.cell(alumno[1]),
		rx.table.cell(
			rx.hstack(
				rx.image(alumno[2], width='10%', high='auto'), 
				alumno[3]
			),
		),
		rx.table.cell(alumno[4]),
		rx.table.cell(
			rx.hstack(
				rx.button(rx.icon('pencil')), #, on_click=State.evt_casa_am(casa[0])),
				rx.button(rx.icon('users')), #, on_click=State.evt_casa_detalle(casa[0])),
			)
		),
		width='100%'
	)

def fnc_casa_alumnos(alumnos) -> rx.Component:
	return rx.card(
		rx.text('CASA ', State.casap, size='6', align='center'),
		rx.divider(),
		rx.text('RESPONSABLE(S) ', State.responsables, size='5', align='center'),
		rx.divider(),
		rx.text('ALUMNOS', align='left'),
		rx.table.root(
			rx.table.row(
				rx.table.column_header_cell('Orden'),
				rx.table.column_header_cell('Apellido y Nombre'),
				rx.table.column_header_cell('Grado'),
				rx.table.column_header_cell('Acciones'),
			),
			rx.table.body(
				rx.foreach(State.alumnos, fnc_casa_alumno),
			),
		),
	)

#################

def fnc_persona_am(persona: list) -> rx.Component:
	return rx.center(
		rx.card(
			rx.card(
				rx.cond(
					persona[0] == 0,
					rx.text('NUEVA PERSONA', weight="bold", align='center'),
					rx.text('MODIFICACION PERSONA', weight="bold", align='center')
				),
				margin_bottom='2vw',
			),


			rx.form(
				rx.box(
					rx.input(value=persona[0],  type='text', name='id', style={'width':'0px', 'height':'0px'}),
				),
				rx.vstack(
					rx.hstack(
						rx.text('Estado: '),
						rx.select(State.tipoestados, default_value=persona[1], name='estado'), 
						rx.text('Orden: '),
						rx.input(placeholder=persona[2], type='number', default_value=persona[2], name='orden', style={'width':'50px'}),
					),
					rx.hstack(
						rx.hstack(
							rx.text('Apellido: '),
							rx.input(placeholder=persona[3], type='text', default_value=persona[3], name='apellido', style={'width':'200px'}),
							rx.text('Nombre: '),
							rx.input(placeholder=persona[4], type='text', default_value=persona[4], name='nombre', style={'width':'200px'}),
						)
					),
					rx.hstack(
						rx.text('Usuario: '),
						rx.cond(
							State.is_superuser != 1,
								rx.input(placeholder=persona[5], type='text', default_value=persona[5], name='usuario', disabled=True, style={'width':'200px'}),
								rx.input(placeholder=persona[5], type='text', default_value=persona[5], name='usuario', style={'width':'200px'}),
						),
						rx.text('Grado: '),
						rx.select(State.grados, default_value=persona[6], name='grado'),
					),
					rx.hstack(
						rx.text('Casa de Practica: '),
						rx.select(State.casaspr, default_value=persona[7], name='casapractica'), 
						rx.text('Responsable Casa: '),
						rx.cond(
							persona[8],
							rx.select(State.casaspr, default_value=persona[8], name='responsablecasa', required=False), 
							rx.select(State.casaspr, default_value=None, name='responsablecasa', required=False), 

						)
					),
					rx.hstack(
						rx.text('Direccion: '),
						rx.input(placeholder=persona[9], type='text', default_value=persona[9], name='direccion', style={'width':'200px'}),
						rx.text('Localidad: '),
						rx.input(placeholder=persona[10], type='text', default_value=persona[10], name='localidad', style={'width':'200px'}),
					),
					rx.hstack(
						rx.text('Codigo Postal: '),
						rx.input(placeholder=persona[11], type='text', default_value=persona[11], name='codigo_postal', style={'width':'200px'}),
						rx.text('e-mail: '),
						rx.input(placeholder=persona[12], type='text', default_value=persona[12], name='email', style={'width':'200px'}),
					),
					rx.hstack(
						rx.text('Fecha de Nacimiento: '),
						rx.input(placeholder=persona[13], type='date', default_value=persona[13], name='fechanacimiento', style={'width':'200px'}),
						rx.text('Fecha de Ingreso: '),
						rx.input(placeholder=persona[14], type='date', default_value=persona[14], name='fechaingreso', style={'width':'200px'}),
					),
					rx.hstack(
						rx.text('Fecha de Egreso: ', persona[15]),
						rx.cond(
							persona[15],
							rx.input(placeholder=persona[15], type='date', default_value=persona[15], name='fechaegreso', style={'width':'200px'}),
							rx.input(placeholder=persona[15], type='date', name='fechaegreso', style={'width':'200px'}),
						),
						rx.input(placeholder=persona[15], type='date', default_value=persona[15], name='fechaegreso', style={'width':'200px'}),
					),
					rx.hstack(
						rx.text('Celular: '),
						rx.input(placeholder=persona[16], type='text', default_value=persona[16], name='celular', style={'width':'200px'}),
						rx.text('Documento: '),
						rx.select(State.tipodocs, default_value=persona[17], name='tipodoc'), 
						rx.input(placeholder=persona[18], type='text', default_value=persona[18], name='nrodoc', style={'width':'200px'}),
					),
					rx.hstack(
						rx.text('Clave: '),
						rx.input(placeholder=persona[19], type='password', default_value=persona[19], name='clave', style={'width':'200px'}),
						rx.checkbox(name='is_superuser', label='Superusuario? ', default_checked=persona[20]),
						rx.text('SuperUsuario? '),
						rx.checkbox(name='is_staff', label='Staff? ', default_checked=persona[21]),
						rx.text('Staff? '),
					),

		# 	<tr>
		# 		<td style="width: 10px"></td>
		# 		<td>
		# 			{% if imagenes[0] %}
		# 				<img src={{ imagenes[0] }} height='50' width='50' />
		# 			{% else %}
		# 				<img src="{{ url_for('static', filename='bosquetaoista/nophoto.jpg') }}" height='50' width='50' />
		# 			{% endif %}
		# 			<label for="id_foto">Foto:</label>
		# 		</td>
		# 		<td>
		# 			<!-- Actual: <a href="/media/images/err_hX7dirl.jpg">{ { persona.foto }}</a> -->
		# 			<input type="checkbox" name="foto_delete" id="foto_delete_id">
		# 			<label for="foto_delete_id">Eliminar</label><br>
		# 			<!-- Modificar: -->
		# 			<input type="file" name="foto" accept="image/*" id="id_foto">
		# 		</td>
		# 		<td>
		# 			{% if imagenes[1] %}
		# 				<img src={{ imagenes[1] }} height='50' width='50' />
		# 			{% else %}
		# 				<img src="{{ url_for('static', filename='bosquetaoista/nocert.png') }}"" height='50' width='50' />
		# 			{% endif %}
		# 			<label for="id_certificado">Certif.:</label>
		# 		</td>
		# 		<td>
		# 			<!-- Actual: <a href="/media/images/err_hX7dirl.jpg">{ { persona.certificado }}</a> -->
		# 			<input type="checkbox" name="cert_delete" id="cert_delete_id">
		# 			<label for="cert_delete_id">Eliminar</label><br>
		# 			<!-- Modificar: -->
		# 			<input type="file" name="certificado" accept="image/*" id="id_certificado">
		# 		</td>
		# 	</tr>
					rx.hstack(
						rx.hstack(
							rx.vstack(
								rx.hstack(
									rx.upload(
										rx.image(src=persona[22], width='150px', high='auto'), 
										rx.text('Click para cambiar'), id='upload_foto', name='foto'
									)
								),
								rx.hstack(
									rx.text('Foto'),
									rx.checkbox(name='eliminar_foto', label='Eliminar'),
									rx.text('Eliminar'),
								),
								# rx.button('Nueva Foto', on_click=State.handle_foto(rx.upload_files(upload_id='upload'))),
							),
						),
						rx.hstack(
							rx.vstack(
								rx.hstack(
									rx.upload(
										rx.image(src=persona[23], width='150px', high='auto'), 
										rx.text('Click para cambiar'), id='upload_cert', name='foto'
									)
								),
								rx.hstack(
									rx.text('Certificado'),
										rx.checkbox(name='eliminar_cert', label='Eliminar'),
										rx.text('Eliminar'),
									),
								),
						),
					),
					rx.button('Confirmar', type='submit', style={'width':'100%'})
				),
				on_submit=State.handle_persona_am,
				reset_on_submit=True,
			)
		),
		width='100%',
		margin_y='1vw',
	)


def fnc_persona(persona: list) -> rx.Component:
	return rx.table.row(
		rx.table.cell(persona[1]),
		rx.table.cell(persona[2]),
		rx.table.cell(
			rx.hstack(
				rx.image(persona[3], width='20%', high='auto'), 
				persona[4]
			),
		),
		rx.table.cell(persona[5]),
		rx.table.cell(persona[6]),
		rx.table.cell(
			rx.vstack(
				rx.hstack(
					rx.button(rx.icon('pencil'), on_click=State.evt_persona_am(persona[0])),
					rx.button(rx.icon('users')), #, on_click=State.evt_persona_detalle(persona[0])),
				),
				rx.hstack(
					rx.button(rx.icon('users')), #, on_click=State.evt_persona_detalle(persona[0])),
					rx.button(rx.icon('users')), #, on_click=State.evt_persona_detalle(persona[0])),
				)
			)
		)
	)

def fnc_personas(personas) -> rx.Component:
	return rx.card(
		rx.text(
			rx.button(rx.icon('plus'), 'PERSONA'), 
			align='right', 
			on_click=State.evt_persona_am(0)
		),
		rx.table.root(
			rx.table.row(
				rx.table.column_header_cell('Orden'),
				rx.table.column_header_cell('Estado'),
				rx.table.column_header_cell('Apellido y Nombre'),
				rx.table.column_header_cell('Grado'),
				rx.table.column_header_cell('Casa de Practica'),
				rx.table.column_header_cell('Acciones'),
			),
			rx.table.body(
				rx.foreach(personas, fnc_persona),
			),
		),
	)

#################
def fnc_imagen() -> rx.Component:
	frase, detalle = db_get_frase()
	return rx.box(
		rx.image(src='/bosquetaoista/EscuelaTaoistaHungLin.jpg'),
		rx.center(
			rx.box(
				rx.text(frase, size='6'),
				rx.text(detalle, size='4'),
				padding_y='1vw'
			),
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
				rx.button(rx.icon('house'), 'Casas', on_click=State.evt_casas()),
				rx.button(rx.icon('graduation-cap'), 'Grados'),
				rx.button(rx.icon('list'), 'Tipo Eventos'),
				rx.button(rx.icon('list'), 'Extras'),
			),
		),
		width='100%',
	)



#################
app = rx.App()
app.add_page(index)
