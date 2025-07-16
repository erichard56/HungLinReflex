import reflex as rx
import asyncio

from .db import db_get_usuario, db_get_casas, db_get_casa, db_upd_casa, db_get_frase, db_get_alumnos
from .db import db_get_personas, db_get_persona
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
	tipoestado: list[tuple]


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
				casa = db_upd_casa(form_data['id'], form_data['nombre'], form_data['direccion'])
				self.casas = db_get_casas()
				self.opc = 'cas'
			else:
				self.error = 'Falta nombre o direccion'
		if (self.error != ''):
			await self.handle_notify()

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
			print(self.casap, self.responsables, self.alumnos)
			self.opc = "cad"

	@rx.event(background=True)
	async def evt_casas(self):
		async with self:
			self.casas = db_get_casas()
			self.opc = "cas"

# eventos persona
	@rx.event(background=True)
	async def evt_personas(self):
		async with self:
			self.personas = db_get_personas()
			self.opc = "per"

	@rx.event(background=True)
	async def evt_persona_am(self, id):
		async with self:
			if (id != 0):
				self.persona, self.tipoestado = db_get_persona(id)
			else:
				self.persona = (0, '', '')
			self.opc = "pam"

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

def fnc_casa_alumno(alumno: list) -> rx.Component:
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
					# 	<tr>
					# 		<td style="width: 10px"></td>
					# 		<td>Estado:</td>
					# 		<td>
					# 			<select name="estado" style="width: 100px;">
					# 				{% for estado in estados %}
					# 					<option value="{{estado.id}}" 
					# 						{% if estado.id == persona.estado_id %} selected {% endif %}>{{estado.nombre}}</option>
					# 				{% endfor %}
					# 			</select>
					# 		</td>
					# 		<td>Orden:</td>
					# 		<td><input type="number" name="orden" value={{ persona.orden }} style="width: 100px;" required="" disabled></td>
					# 	</tr>
					rx.hstack(
						rx.card(
						rx.text('Estado: '),
						rx.input(placeholder=persona[1], type='text', default_value=persona[1], name='estado', style={'width':'200px'}),
						),
						rx.card(
						rx.text('Orden: '),
						rx.input(placeholder=persona[2], type='numeric', default_value=persona[2], name='orden', style={'width':'200px'}),
						)
					),
					# 	<tr>
					# 		<td style="width: 10px"></td>
					# 		<td>Apellido:</td>
					# 		<td><input type="text" name="apellido" value="{{ persona.apellido }}" style="width: 200px;" maxlength="100" required=""></td>
					# 		<td>Nombre:</td>
					# 		<td><input type="text" name="nombre" value="{{ persona.nombre }}" style="width: 200px;" maxlength="100" required=""></td>
					# 	</tr>
					rx.hstack(
						rx.hstack(
							rx.text('Apellido: '),
							rx.input(placeholder=persona[3], type='text', default_value=persona[3], name='apellido', style={'width':'200px'}),
							rx.text('Nombre: '),
							rx.input(placeholder=persona[4], type='text', default_value=persona[4], name='nombre', style={'width':'200px'}),
						)
					),
					# 	<tr>
					# 		<td style="width: 10px"></td>
					# 		<td>Usuario:</td>
					# 		<td><input type="text" name="usuario" value="{{ persona.usuario }}" style="width: 200px;" maxlength="50" 
					# 			{% if operador.is_superuser != 1 %} disabled {% endif %}></td>
					# 		<td>Grado:</td>
					# 		<td>
					# 			<select name="grado" style="width: 200px;">
					# 				{% for grado in grados %}
					# 					<option value="{{ grado.id }}" 
					# 						{% if grado.id == persona.grado_id %} selected {% endif %}>{{ grado.nombre }}</option>
					# 				{% endfor %}
					# 			</select>
					# 		</td>
					# 	</tr>
					rx.hstack(
						rx.text('Usuario: '),
						rx.input(placeholder=persona[5], type='text', default_value=persona[5], name='usuario', style={'width':'200px'}),
						rx.text('Grado: '),
						rx.input(placeholder=persona[6], type='text', default_value=persona[6], name='grado', style={'width':'200px'}),
					),
					# 	<tr>
					# 		<td style="width: 10px"></td>
					# 		<td>Casa Práctica:</td>
					# 		<td>
					# 			<select name="casa_practica" style="width: 200px;">
					# 				{% for casa in casas %}
					# 					<option value="{{ casa.id }}" 
					# 						{% if casa.id == persona.casa_practica_id %} selected {% endif %}>{{ casa.nombre }}</option>
					# 				{% endfor %}
					# 			</select>
					# 		</td>
					# 		<td>Responsable Casa:</td>
					# 		<td>
					# 			<select name="responsable_casa" style="width: 200px;">
					# 				<option value="0">----</option>
					# 				{% for casa in casas %}
					# 					<option value="{{ casa.id }}" 
					# 						{% if casa.id == persona.responsable_casa_id %} selected {% endif %}>{{ casa.nombre }}</option>
					# 				{% endfor %}
					# 			</select>
					# 		</td>
					# 	</tr>
					rx.hstack(
						rx.text('Casa de Practica: '),
						rx.input(placeholder=persona[7], type='text', default_value=persona[7], name='casa_practica', style={'width':'200px'}),
						rx.text('Responsable Casa: '),
						rx.input(placeholder=persona[8], type='text', default_value=persona[8], name='responsable_casa', style={'width':'200px'}),
					),

					# 	<tr>
					# 		<td style="width: 10px"></td>
					# 		<td>Direccion:</td>
					# 		<td><input type="text" name="direccion" value="{{ persona.direccion }}" style="width: 300px;" maxlength="100" required=""></td>
					# 		<td>Localidad:</td>
					# 		<td><input type="text" name="localidad" value="{{ persona.localidad }}" style="width: 300px;" maxlength="100" required=""></td>
					# 	</tr>
					rx.hstack(
						rx.text('Direccion: '),
						rx.input(placeholder=persona[9], type='text', default_value=persona[9], name='direccion', style={'width':'200px'}),
						rx.text('Localidad: '),
						rx.input(placeholder=persona[10], type='text', default_value=persona[10], name='localidad', style={'width':'200px'}),
					),

					# 	<tr>
					# 		<td style="width: 10px"></td>
					# 		<td>Código Postal:</td>
					# 		<td><input type="text" name="codigo_postal" value="{{ persona.codigo_postal }}" style="width: 200px;" maxlength="50" required=""></td>
					# 		<td>Email:</td>
					# 		<td><input type="email" name="email" value="{{ persona.email }}" style="width: 300px;" maxlength="100" required=""></td>
					# 	</tr>
					rx.hstack(
						rx.text('Codigo Postal: '),
						rx.input(placeholder=persona[11], type='text', default_value=persona[11], name='codigo_postal', style={'width':'200px'}),
						rx.text('e-mail: '),
						rx.input(placeholder=persona[12], type='text', default_value=persona[12], name='email', style={'width':'200px'}),
					),

		# 	<tr>
		# 		<td style="width: 10px"></td>
		# 		<td>Fecha Nacimiento:</td>
		# 		<td><input type="date" name="fechanacimiento" value="{{ persona.fechanacimiento }}" style="width: 200px;" maxlength="50" required=""></td>
		# 		<td>Fecha Ingreso:</td>
		# 		<td><input type="date" name="fechaingreso" value="{{ persona.fechaingreso }}" style="width: 200px;" maxlength="100" required=""></td>
		# 	</tr>
					rx.hstack(
						rx.text('Fecha de Nacimiento: '),
						rx.input(placeholder=persona[13], type='date', default_value=persona[13], name='fechanacimiento', style={'width':'200px'}),
						rx.text('Fecha de Ingreso: '),
						rx.input(placeholder=persona[14], type='date', default_value=persona[14], name='fechaingreso', style={'width':'200px'}),
					),





					rx.button('Confirmar', type='submit', style={'width':'100%'})
				),
				on_submit=State.handle_casa_am,
				reset_on_submit=True,
			)
		),
		width='100%',
		margin_y='2vw'
	)
		# 	<table>
		# 	<tr>
		# 		<td style="width: 10px"></td>
		# 		<td>Fecha Egreso:</td>
		# 		<td><input type="date" name="fechaegreso" value="{{ persona.fechaegreso }}" style="width: 200px;" maxlength="100"></td>
		# 	</tr>
		# 	<tr>
		# 		<td style="width: 10px"></td>
		# 		<td>Celular:</td>
		# 		<td><input type="text" name="celular" value="{{ persona.celular }}" style="width: 200px;" maxlength="50" required=""></td>
		# 		<td>Documento:</td>
		# 		<td>
		# 			<select name="tipodoc" style="width: 100px;">
		# 				<option value="0">----</option>
		# 				{% for tipodoc in tipodocs %}
		# 					<option value="{{ tipodoc.id }}" 
		# 						{% if tipodoc.id == persona.tipodoc_id %} selected {% endif %}>{{ tipodoc.nombre }}</option>
		# 				{% endfor %}
		# 			</select>
		# 			<input type="number" name="nrodoc" value="{{ persona.nrodoc }}" style="width: 100px;" maxlength="150" required="">
		# 		</td>
		# 	</tr>
		# 	<tr>
		# 		<td style="width: 10px"></td>
		# 		<td>Clave:</td>
		# 		<td><input type="text" name="clave" value="" style="width: 200px;" maxlength="50" 
		# 				{% if persona.id == 0 %} required {% endif %}></td>
		# 		<td>
		# 			<input type="checkbox" name="is_superuser" id="is_superuser_id" 
		# 					{% if persona.is_superuser == 1 %} checked {% endif %} 
		# 					{% if operador.is_superuser != 1 %} disabled {% endif %} >
		# 			<label for="is_superuser_id">Es Superusuario</label><br>
		# 			<input type="checkbox" name="is_staff" id="is_staff_id" {% if persona.is_staff %} checked {% endif %}>
		# 			<label for="is_staff_id">Es Staff</label><br>
		# 		</td>
		# 	</tr>
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
		# </table>

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
