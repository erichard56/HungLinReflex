import mysql.connector
import hashlib
import random
import uuid

conn = mysql.connector.connect(user='hunglin', 
								host='127.0.0.1', 
								database='hunglin', 
								password='Rafaela4840')
cursor = conn.cursor()

def db_get_frase():
	q1 = 'SELECT COUNT(*) FROM bosquetaoista_frase'
	cursor.execute(q1)
	cant = cursor.fetchone()[0]
	n = random.randint(1, cant)
	q1 = f'SELECT * FROM bosquetaoista_frase WHERE id = {n}'
	cursor.execute(q1)
	frase = cursor.fetchone()
	return(frase[1], frase[2])

def db_get_usuario(usuario, clave):
	q1 = f'SELECT * FROM bosquetaoista_persona WHERE usuario = "{usuario}"'
	cursor.execute(q1)
	persona = cursor.fetchone()
	if (persona):
		if (hashlib.sha256(clave.encode('utf-8')).hexdigest() == persona[21]):
			return(persona)
	return(persona)


# casas
def db_get_casas_lista():
	respuesta = []
	q1 = f'SELECT * FROM bosquetaoista_casa ORDER BY id'
	cursor.execute(q1)
	casas = cursor.fetchall()
	for casa in casas:
		q1 = f'SELECT CONCAT(TRIM(apellido), ", ", TRIM(nombre)) FROM bosquetaoista_persona WHERE responsable_casa_id = {casa[0]} ORDER BY orden'
		cursor.execute(q1)
		resps = cursor.fetchall()
		responsables = ' // '.join([resp[0] for resp in resps])
		q1 = f'SELECT COUNT(*) FROM bosquetaoista_persona WHERE casa_practica_id = {casa[0]} and estado_id = 1'
		cursor.execute(q1)
		activos = cursor.fetchone()[0]
		q1 = f'SELECT COUNT(*) FROM bosquetaoista_persona WHERE casa_practica_id = {casa[0]} and estado_id = 2'
		cursor.execute(q1)
		noactivos = cursor.fetchone()[0]
		q1 = f'SELECT COUNT(*) FROM bosquetaoista_persona WHERE casa_practica_id = {casa[0]} and estado_id = 3'
		cursor.execute(q1)
		fallecidos = cursor.fetchone()[0]
		anf = ' / '.join([str(activos), str(noactivos), str(fallecidos)])
		respuesta.append([casa[0], casa[1], casa[2], responsables, anf])
	return(respuesta)

def db_get_casa(id: int):
	if (int(id) > 0):
		q1 = f'SELECT * FROM bosquetaoista_casa WHERE id = {id}'
		cursor.execute(q1)
		casa = cursor.fetchone()
	else:
		casa = (0, None, None)
	return(casa)

def db_put_casa(id: int, nombre: str, direccion: str):
	if (int(id) != 0):
		q1 =f'UPDATE bosquetaoista_casa SET nombre="{nombre}", direccion="{direccion}" WHERE id={id}'
	else:
		q1 = f'INSERT INTO bosquetaoista_casa VALUES (0, "{nombre}", "{direccion}")'
	cursor.execute(q1)
	conn.commit()
	return

def db_del_casa(casa_id):
	q1 = f'DELETE FROM bosquetaoista_casa WHERE id = {casa_id}'
	cursor.execute(q1)
	conn.commit()


# personas
def db_get_persona(id):
	if (int(id) != 0):
		q1 = f'SELECT A.id, B.nombre as estado, A.orden, A.apellido, A.nombre, A.usuario, C.nombre as grado, D.nombre as casa_practica, E.nombre as responsable_casa, A.direccion, A.localidad, A.codigo_postal, A.email, A.fechanacimiento, A.fechaingreso, A.fechaegreso, A.celular, F.nombre as tipodoc, A.nrodoc, A.clave, A.is_superuser, A.is_staff, CASE WHEN A.foto is NULL OR A.foto = "" THEN "/bosquetaoista/nophoto.jpg" ELSE foto END as foto, CASE WHEN A.certificado is NULL or A.certificado = "" THEN "/bosquetaoista/nocert.png" ELSE certificado END as certificado FROM bosquetaoista_persona A INNER JOIN bosquetaoista_tipoestado B on B.id = A.estado_id INNER JOIN bosquetaoista_grado C on C.id = A.grado_id LEFT JOIN bosquetaoista_casa D on D.id = A.casa_practica_id LEFT JOIN bosquetaoista_casa E on E.id = A.responsable_casa_id LEFT JOIN bosquetaoista_tipodoc F on F.id = A.tipodoc_id WHERE A.id = {id}'
		cursor.execute(q1)
		persona = cursor.fetchone()
	else:
		persona = (0, 'Activo', 0, '', '', '', 'Alumno', '', '', '', '', '', '', None, None, None, '', 'DNI', 0, '', 0, 0, '', '')
	return(persona)

def db_get_persona_caps(id):
	q1 = f' SELECT C.nombre, B.nombre, A.fecha, CONCAT(TRIM(D.apellido), ", ", TRIM(D.nombre)),  F.nombre FROM bosquetaoista_agenda A INNER JOIN bosquetaoista_evento B ON B.id = A.evento_id INNER JOIN bosquetaoista_tipoevento C on C.id = B.tipo_id INNER JOIN bosquetaoista_persona D on D.id = A.orador_id INNER JOIN bosquetaoista_cursante E ON E.persona_id = {id} INNER JOIN bosquetaoista_tipocursante F ON F.id = E.tipocursante_id'
	cursor.execute(q1)
	caps = cursor.fetchall()
	return(caps)

def db_get_persona_extras(id):
	q1 = f'SELECT A.persona_id, A.id, B.nombre, a.comentario FROM hunglin.bosquetaoista_personaextra A INNER JOIN bosquetaoista_tipoextra B on B.id = A.tipoextra_id WHERE A.persona_id = {id} ORDER BY B.nombre'
	cursor.execute(q1)
	extras = cursor.fetchall()
	return(extras)

def db_get_persona_detalle_extra(id: int):
	q1 = f'SELECT B.nombre, A.comentario FROM hunglin.bosquetaoista_personaextra A INNER JOIN bosquetaoista_tipoextra B ON B.id = A.tipoextra_id WHERE A.id = {id}'
	cursor.execute(q1)
	extra = cursor.fetchall()[0]
	return(extra)

def db_put_persona_detalle_extra(form_data: dict):
	persona_id = form_data['persona_id']
	extra_id = form_data['extra_id']
	extrax = form_data['extra']
	cmntx = form_data['cmntx']
	q1 = f'SELECT * from bosquetaoista_tipoextra WHERE nombre = \"{extrax}\"'
	cursor.execute(q1)
	tipoextra = cursor.fetchone()
	if (form_data['extra_id'] == '0'):
		q1 = f'INSERT INTO bosquetaoista_personaextra (id, comentario, persona_id, tipoextra_id) VALUES (0, "{cmntx}", {persona_id}, {tipoextra[0]})'
	else:
		q1 = f'UPDATE bosquetaoista_personaextra SET comentario = "{cmntx}", persona_id = {persona_id}, tipoextra_id = {tipoextra[0]} WHERE id = {extra_id}'
	cursor.execute(q1)
	conn.commit()

def db_persona_detalle_extra_delete(persona_id, extra_id):
	q1 = f'DELETE FROM bosquetaoista_personaextra WHERE persona_id = {persona_id} AND id = {extra_id}'
	cursor.execute(q1)
	conn.commit()

def db_get_personas_lista(busq, estado, casa, grado):
	q1 = 'SELECT A.id, A.orden, B.nombre as estado, CASE WHEN A.foto is NULL OR A.foto = "" THEN "/bosquetaoista/nophoto.jpg" ELSE foto END as foto, CONCAT(TRIM(A.apellido), ", ", TRIM(A.nombre)), C.nombre as grado, D.nombre as casapractica FROM bosquetaoista_persona A INNER JOIN bosquetaoista_tipoestado B on B.id = A.estado_id INNER JOIN bosquetaoista_grado C on C.id = A.grado_id LEFT JOIN bosquetaoista_casa D on D.id = A.casa_practica_id WHERE '
	if (len(busq)):
		q1 += f' A.nombre LIKE "%{busq}%" OR A.apellido LIKE "%{busq}%" AND '
	if (estado != 'Todos'):
		q2 = f'SELECT * FROM bosquetaoista_tipoestado WHERE nombre = "{estado}"'
		cursor.execute(q2)
		estado_id = cursor.fetchone()[0]
		q1 += f' A.estado_id = {estado_id} AND'
	if (casa != 'Todas'):
		q2 = f'SELECT * FROM bosquetaoista_casa WHERE nombre = "{casa}"'
		cursor.execute(q2)
		casa_id = cursor.fetchone()[0]
		q1 += f' A.casa_practica_id = {casa_id} AND'
	if (grado != 'Todos'):
		q2 = f'SELECT * FROM bosquetaoista_grado WHERE nombre = "{grado}"'
		cursor.execute(q2)
		grado_id = cursor.fetchone()[0]
		q1 += f' A.grado_id = {grado_id} AND'
	q1 += ' 1 = 1 ORDER BY A.orden'
	cursor.execute(q1)
	personas = cursor.fetchall()
	return(personas)

def db_put_persona(pers):

	is_superuser = False
	is_staff = False

	id = pers['id']

	qins = f'INSERT INTO bosquetaoista_persona (id'
	valores = '(0 '
	qupd = f'UPDATE bosquetaoista_persona SET id = {id}'

	for key, value in pers.items():
		match key:
			case 'estado':
				q1 = f'SELECT * FROM bosquetaoista_tipoestado WHERE nombre = "{value}"'
				cursor.execute(q1)
				estado = cursor.fetchone()[0]
				qins += f', estado_id'
				valores += f', {estado}'
				qupd += f', estado_id = {estado}'

			case 'orden':
				if (int(id) != 0):
					orden = pers['orden']
				else:
					q1 = f'SELECT MAX(orden) from bosquetaoista_persona'
					cursor.execute(q1)
					orden = int(cursor.fetchone()[0]) + 1
				qins += f', orden '
				valores += f', {orden}'
				qupd += f', orden = {orden}'

			case 'grado':
				q1 = f'SELECT * FROM bosquetaoista_grado WHERE nombre = "{value}"'
				cursor.execute(q1)
				grado = cursor.fetchone()[0]
				qins += f', grado_id'
				valores += f', {grado}'
				qupd += f', grado_id = {grado}'

			case 'casapractica':
				q1 = f'SELECT * FROM bosquetaoista_casa WHERE nombre = "{value}"'
				cursor.execute(q1)
				casa = cursor.fetchone()[0]
				qins += f', casa_practica_id'
				valores += f', {casa}'
				qupd += f', casa_practica_id = {casa}'

			case 'responsablecasa':
				if (value != ''):
					q1 = f'SELECT * FROM bosquetaoista_casa WHERE nombre = "{value}"'
					cursor.execute(q1)
					responsablecasa = cursor.fetchone()[0]
					qins += f', responsable_casa_id'
					valores += f', {responsablecasa}'
					qupd += f', responsable_casa_id = {responsablecasa}'

			case 'fechanacimiento':
				fnac = pers['fechanacimiento']
				if (len(fnac) > 0):
					qins += f', fechanacimiento'
					valores += f', \"{fnac}\"'
					qupd += f', fechanacimiento = \"{fnac}\"'

			case 'fechaingreso':
				fing = pers['fechaingreso']
				if (len(fing) > 0):
					qins += f', fechaingreso'
					valores += f', \"{fing}\"'
					qupd += f', fechaingreso = \"{fing}\"'

			case 'fechaegreso':
				fegr = pers['fechaegreso']
				if (len(fegr) > 0):
					qins += f', fechaegreso'
					valores +=' f, \"{fegr}\"'
					qupd += f', fechaegreso = \"{fegr}\"'

			case 'tipodoc':
				q1 = f'SELECT * FROM bosquetaoista_tipodoc WHERE nombre = "{value}"'
				cursor.execute(q1)
				tipodoc = cursor.fetchone()[0]
				qins += f', tipodoc_id'
				valores += f', {tipodoc}'
				qupd += f', tipodoc_id = {tipodoc}'

			case 'clave':
				## falta codificar
				if (len(pers['clave']) > 0):
					clavecod = pers['clave']
					qins += f', clave'
					valores += f', \"{clavecod}\"'
					qupd += f', clave = \"{clavecod}\"'

			case 'is_superuser':
				is_superuser = True

			case 'is_staff':
				is_staff = True

			case 'foto':
				if (len(pers['foto']) > 0):
					foto = 'images/' + str(uuid.uuid4()) + '.jpg'
					with open('./assets/' + foto, 'wb') as f:
						f.write(pers['foto'])
					qins += f', foto'
					valores += f', "{foto}"'
					qupd += f', foto = "{foto}"'

			case 'certificado':
				if (len(pers['certificado']) > 0):
					cert = 'certificados/' + str(uuid.uuid4()) + '.jpg'
					with open('./assets/' + cert, 'wb') as f:
						f.write(pers['certificado'])
					qins += f', certificado'
					valores += f', "{cert}"'
					qupd += f', certificado = "{cert}"'

			case _:
				if (key in ['apellido', 'nombre', 'usuario', 'direccion', 'localidad', 'codigopostal', 'email', 'celular', 'nrodoc', 'codigo_postal']):
					qins += f', {key}'
					valores += f', TRIM(\"{value}\")'
					qupd += f', {key} = TRIM(\"{value}\")'


	qins += f', is_superuser'
	valores += ', 1' if is_superuser else ', 0'
	qins += f', is_staff'
	valores += f', 1' if is_staff else ', 0'
	qins += f') VALUES {valores} )'

	qupd += f', is_superuser = 1' if is_superuser else f', is_superuser = 0'
	qupd += f', is_staff = 1' if is_staff else f', is_staff = 0'
	qupd += f' WHERE id = {id}'

	if (int(id) == 0):
		cursor.execute(qins)
	else:
		cursor.execute(qupd)
	conn.commit()

	return


# agendas
# def db_get_eve_lista():
# 	q1 = f'SELECT nombre FROM bosquetaoista_tipoevento ORDER BY nombre'
# 	cursor.execute(q1)
# 	eves = cursor.fetchall()
# 	return(eves)

def db_get_agendas_lista():
	q1 = f'SELECT A.evento_id, A.orador_id, B.nombre, A.fecha, CONCAT(TRIM(C.apellido), ", ", TRIM(C.nombre)) FROM bosquetaoista_agenda A INNER JOIN bosquetaoista_evento B ON B.id = A.evento_id INNER JOIN bosquetaoista_persona C ON C.id = A.orador_id ORDER BY A.fecha'
	cursor.execute(q1)
	eventos = cursor.fetchall()
	return(eventos)

def db_get_agenda(id: int):
	if (int(id) > 0):
		q1 = f'SELECT A.evento_id, B.nombre, A.fecha, CONCAT(TRIM(C.apellido), ", ", TRIM(C.nombre)) FROM bosquetaoista_agenda A INNER JOIN bosquetaoista_evento B ON B.id = A.evento_id INNER JOIN bosquetaoista_persona C ON C.id = A.orador_id WHERE A.id =  {id}'
		cursor.execute(q1)
		evento = cursor.fetchone()
	else:
		evento = (0, 0, None, None, None)
	return(evento)

def db_get_oradores():
	q1 = 'SELECT CONCAT(TRIM(apellido), ", ", TRIM(nombre)) FROM bosquetaoista_persona WHERE estado_id = 1 ORDER BY apellido, nombre'
	cursor.execute(q1)
	oradores = [orador[0] for orador in cursor.fetchall()]
	return(oradores)

def db_put_agenda(id: int, nombre: str, descripcion: str):
	if (int(id) != 0):
		q1 =f'UPDATE bosquetaoista_evento SET nombre="{nombre}", descripcion="{descripcion}" WHERE id={id}'
	else:
		q1 = f'INSERT INTO bosquetaoista_evento VALUES (0, "{nombre}", "{descripcion}")'
	# cursor.execute(q1)
	# conn.commit()
	return

def db_del_agenda(agenda_id):
	q1 = f'DELETE FROM bosquetaoista_evento WHERE id = {agenda_id}'
	# cursor.execute(q1)
	# conn.commit()
	return


# eventos
def db_get_eve_lista():
	q1 = f'SELECT nombre FROM bosquetaoista_tipoevento ORDER BY nombre'
	cursor.execute(q1)
	eves = [ev[0] for ev in cursor.fetchall()]
	return(eves)

def db_get_evt_lista():
	q1 = f'SELECT nombre FROM bosquetaoista_evento ORDER BY nombre'
	cursor.execute(q1)
	evts = [ev[0] for ev in cursor.fetchall()]
	return(evts)



def db_get_eventos_lista():
	q1 = f'SELECT A.id, B.nombre, A.nombre, A.descripcion FROM hunglin.bosquetaoista_evento A INNER JOIN bosquetaoista_tipoevento B on B.id = A.tipo_id ORDER BY A.id'
	cursor.execute(q1)
	eventos = cursor.fetchall()
	return(eventos)

def db_get_evento(id: int):
	if (int(id) > 0):
		q1 = f'SELECT A.id, B.nombre, A.nombre, A.descripcion FROM hunglin.bosquetaoista_evento A INNER JOIN bosquetaoista_tipoevento B on B.id = A.tipo_id WHERE A.id =  {id}'
		cursor.execute(q1)
		evento = cursor.fetchone()
	else:
		evento = (0, None, None, None)
	return(evento)

def db_put_evento(id: int, nombre: str, descripcion: str):
	if (int(id) != 0):
		q1 =f'UPDATE bosquetaoista_evento SET nombre="{nombre}", descripcion="{descripcion}" WHERE id={id}'
	else:
		q1 = f'INSERT INTO bosquetaoista_evento VALUES (0, "{nombre}", "{descripcion}")'
	cursor.execute(q1)
	conn.commit()
	return

def db_del_evento(evento_id):
	q1 = f'DELETE FROM bosquetaoista_evento WHERE id = {tipoextra_id}'
	cursor.execute(q1)
	conn.commit()


# grados
def db_get_grados_lista():
	q1 = f'SELECT * FROM bosquetaoista_grado ORDER BY id'
	cursor.execute(q1)
	grados = cursor.fetchall()
	res = []
	for grado in grados:
		q1 = f'SELECT COUNT(*) FROM bosquetaoista_persona WHERE grado_id = {grado[0]} AND estado_id = 1'
		cursor.execute(q1)
		activos = cursor.fetchone()[0]
		q1 = f'SELECT COUNT(*) FROM bosquetaoista_persona WHERE grado_id = {grado[0]} AND estado_id = 2'
		cursor.execute(q1)
		noactivos = cursor.fetchone()[0]
		res.append([grado[0], grado[1], activos, noactivos])
	return(res)

def db_get_grado(id):
	if (int(id) > 0):
		q1 = f'SELECT * FROM bosquetaoista_grado WHERE id = {id}'
		cursor.execute(q1)
		grado = cursor.fetchone()
	else:
		grado = [0, '']
	return grado

def db_put_grado(id: int, nombre: str):
	if (int(id) != 0):
		q1 =f'UPDATE bosquetaoista_grado SET nombre="{nombre}" WHERE id={id}'
	else:
		q1 = f'INSERT INTO bosquetaoista_grado VALUES (0, "{nombre}")'
	cursor.execute(q1)
	conn.commit()
	return

def db_del_grado(grado_id):
	q1 = f'DELETE FROM bosquetaoista_grado WHERE id = {grado_id}'
	cursor.execute(q1)
	conn.commit()


# extras
def db_get_tipoextras_lista():
	q1 = f'SELECT * FROM bosquetaoista_tipoextra ORDER BY id'
	cursor.execute(q1)
	tipoextras = cursor.fetchall()
	return(tipoextras)

def db_get_tipoextra(id: int):
	if (int(id) > 0):
		q1 = f'SELECT * FROM bosquetaoista_tipoextra WHERE id = {id}'
		cursor.execute(q1)
		tipoextra = cursor.fetchone()
	else:
		tipoextra = (0, None, None)
	return(tipoextra)

def db_put_tipoextra(id: int, nombre: str, descripcion: str):
	if (int(id) != 0):
		q1 =f'UPDATE bosquetaoista_tipoextra SET nombre="{nombre}", descripcion="{descripcion}" WHERE id={id}'
	else:
		q1 = f'INSERT INTO bosquetaoista_tipoextra VALUES (0, "{nombre}", "{descripcion}")'
	cursor.execute(q1)
	conn.commit()
	return

def db_del_tipoextra(tipoextra_id):
	q1 = f'DELETE FROM bosquetaoista_tipoextra WHERE id = {tipoextra_id}'
	cursor.execute(q1)
	conn.commit()


# tipoeventos
def db_get_tipoeventos_lista():
	q1 = f'SELECT nombre FROM bosquetaoista_tipoevento ORDER BY id'
	cursor.execute(q1)
	tipoeventos = cursor.fetchall()
	return(tipoeventos)

def db_get_tipoevento(id: int):
	if (int(id) > 0):
		q1 = f'SELECT * FROM bosquetaoista_tipoevento WHERE id = {id}'
		cursor.execute(q1)
		tipoevento = cursor.fetchone()
	else:
		tipoevento = (0, None, None)
	return(tipoevento)

def db_put_tipoevento(id: int, nombre: str, descripcion: str):
	if (int(id) != 0):
		q1 =f'UPDATE bosquetaoista_tipoevento SET nombre="{nombre}", descripcion="{descripcion}" WHERE id={id}'
	else:
		q1 = f'INSERT INTO bosquetaoista_tipoevento VALUES (0, "{nombre}", "{descripcion}")'
	cursor.execute(q1)
	conn.commit()
	return

def db_del_tipoevento(evento_id):
	q1 = f'DELETE FROM bosquetaoista_tipoevento WHERE id = {evento_id}'
	cursor.execute(q1)
	conn.commit()



# misc
def db_get_estados(todos: str=''):
	q1 = 'SELECT nombre FROM bosquetaoista_tipoestado ORDER BY id'
	cursor.execute(q1)
	estados = [tp[0] for tp in cursor.fetchall()]
	if (len(todos) > 0):
		estados.insert(0, 'Todos')
	return(estados)

def db_get_casas(todos: str=''):
	q1 = f'SELECT nombre FROM bosquetaoista_casa ORDER BY id'
	cursor.execute(q1)
	casas = [casa[0] for casa in cursor.fetchall()]
	if (len(todos) > 0):
		casas.insert(0, 'Todas')
	return(casas)

def db_get_grados(todos: str=''):
	q1 = 'SELECT nombre FROM bosquetaoista_grado ORDER BY id'
	cursor.execute(q1)
	grados = [grado[0] for grado in cursor.fetchall()]
	if (len(todos) > 0):
		grados.insert(0, 'Todos')
	return(grados)

def db_get_docs():
	q1 = 'SELECT nombre FROM bosquetaoista_tipodoc ORDER BY id'
	cursor.execute(q1)
	docs = [doc[0] for doc in cursor.fetchall()]
	return(docs)

def db_get_tipoextras():
	q1 = 'SELECT nombre FROM bosquetaoista_tipoextra ORDER BY nombre'
	cursor.execute(q1)
	tipoextras = [tp[0] for tp in cursor.fetchall()]
	return(tipoextras)
