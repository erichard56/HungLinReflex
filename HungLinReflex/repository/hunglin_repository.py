import reflex as rx
from icecream import ic
from ..models.hunglin_models import Frase, Persona, PersonasLista, Casa, CasasLista, Grado
from ..repository.hunglin_connect_db import connect
from typing import Optional, List
import random
import hashlib

# frase
def get_frase() -> Frase:
	conn, cursor = connect()
	q1 = 'select count(*) from bosquetaoista_frase'
	cursor.execute(q1)
	cant = cursor.fetchone()
	n = random.randint(1, cant[0])
	q1 = f'select * from bosquetaoista_frase where id = {n}'
	cursor.execute(q1)
	frase = cursor.fetchone()
	return(frase)

# personas
def chk_usuario(usuario: str, clave: str) -> Persona:
	conn, cursor = connect()
	q1 = f'select * from bosquetaoista_persona where usuario = "{usuario}"'
	cursor.execute(q1)
	persona = cursor.fetchone()
	if (persona):
		if (hashlib.sha256(clave.encode('utf-8')).hexdigest() == persona[21]):
			return(persona)
		else:
			return(None)
	return(None)

def get_personas(id: int, busq: str, id_estado: int) -> list[PersonasLista]:
	conn, cursor = connect()

	q1 = f'select A.id, A.orden, CASE WHEN A.foto IS NULL then "/bosquetaoista/nophoto.jpg" ELSE CONCAT("/fotos/img_", A.apellido, "_", LPAD(A.orden, 4, "0"), "_low.jpg") END as foto,  CONCAT(A.apellido, ", ", A.nombre), B.nombre, C.nombre from bosquetaoista_persona A, bosquetaoista_grado B, bosquetaoista_casa C WHERE B.id = A.grado_id AND C.id = A.casa_practica_id '
	if (id != 0):
		q1 += f' AND A.estado_id = {id} '

	if (busq != ''):
		q1 += f'AND (A.nombre like "*{busq}*" or A.apellido like "*{busq}*") '

	if (id_estado != 0):
		q1 += f' AND A.estado_id = {id_estado} '
	
	q1 += ' ORDER BY A.estado_id, A.orden'
	cursor.execute(q1)
	personas = cursor.fetchall()
	return(personas)


def get_persona_detalles(id: int):
	conn, cursor = connect()

	q1 = f'select CONCAT(A.apellido, ", ", A.nombre), A.id, A.orden, B.nombre AS estado,  C.nombre AS grado, D.nombre AS casa_practica, "---" as responsable_casa, A.direccion, A.localidad, A.email, A.fechanacimiento, A.fechaingreso, A.fechaegreso, E.nombre as tipodoc, A.nrodoc, CASE WHEN A.foto IS NULL then "/bosquetaoista/nophoto.jpg" ELSE CONCAT("/fotos/img_", A.apellido, "_", LPAD(A.orden, 4, "0"), "_low.jpg") END as foto, CASE WHEN A.certificado IS NULL then "/bosquetaoista/nocert.png" ELSE CONCAT("/certificados/cer_", A.apellido, "_", LPAD(A.orden, 4, "0"), ".jpg") END AS cert, CONCAT("**", IF (A.is_superuser = 1, "Superuser**", ""), IF (A.is_staff = 1, "Staff**", "")) as privilegios FROM bosquetaoista_persona A, bosquetaoista_tipoestado B, bosquetaoista_grado C, bosquetaoista_casa D, bosquetaoista_tipodoc E WHERE A.id = {id} AND A.responsable_casa_id IS NULL AND B.id = A.estado_id AND C.id = A.grado_id AND D.id = A.casa_practica_id AND E.id = A.tipodoc_id union select CONCAT(A.apellido, ", ", A.nombre), A.id, A.orden, B.nombre AS estado,  C.nombre AS grado, D.nombre AS casa_practica, F.nombre as responsable_casa, A.direccion, A.localidad, A.email, A.fechanacimiento, A.fechaingreso, A.fechaegreso, E.nombre as tipodoc, A.nrodoc, CASE WHEN A.foto IS NULL then "/bosquetaoista/nophoto.jpg" ELSE CONCAT("/fotos/img_", A.apellido, "_", LPAD(A.orden, 4, "0"), "_low.jpg") END as foto, CASE WHEN A.certificado IS NULL then "/bosquetaoista/nocert.png" ELSE CONCAT("/certificados/cer_", A.apellido, "_", LPAD(A.orden, 4, "0"), ".jpg") END AS cert, CONCAT("**", IF (A.is_superuser = 1, "Superuser**", ""), IF (A.is_staff = 1, "Staff**", "")) as privilegios FROM bosquetaoista_persona A, bosquetaoista_tipoestado B, bosquetaoista_grado C, bosquetaoista_casa D, bosquetaoista_tipodoc E, bosquetaoista_casa F WHERE A.id = {id} AND B.id = A.estado_id AND C.id = A.grado_id AND D.id = A.casa_practica_id AND E.id = A.tipodoc_id and F.id = A.responsable_casa_id ' 
	cursor.execute(q1) 
	persona_detalles = cursor.fetchone()

	q1 = f'SELECT D.nombre, C.nombre, B.fecha, CONCAT(E.apellido, ", ", E.nombre), F.nombre FROM bosquetaoista_cursante A, bosquetaoista_agenda B, bosquetaoista_evento C, bosquetaoista_tipoevento D, bosquetaoista_persona E, bosquetaoista_tipocursante F WHERE A.persona_id = {id} AND B.id = A.agenda_id AND c.id = B.evento_id AND D.id = C.tipo_id AND E.id = B.orador_id AND F.id = A.tipocursante_id'
	cursor.execute(q1)
	eventos = cursor.fetchall()

	q1 = f'SELECT B.nombre, A.comentario FROM bosquetaoista_personaextra A, bosquetaoista_tipoextra B where A.persona_id = {id} and B.id = A.tipoextra_id'
	cursor.execute(q1)
	extras = cursor.fetchall()

	return(persona_detalles, eventos, extras)


#### Casas
def get_casas() -> List[CasasLista]:
	conn, cursor = connect()
	q1 = 'select * from bosquetaoista_casa ORDER BY id'
	cursor.execute(q1)
	casas = cursor.fetchall()

	casaslista = []
	for casa in casas:
		q1 = f'SELECT * FROM bosquetaoista_persona WHERE responsable_casa_id = {casa[0]}'
		cursor.execute(q1)
		personas = cursor.fetchall()
		resps = ' // '.join(', '.join([resp[3], resp[2]]) for resp in personas)

		q1 = f'SELECT COUNT(*) from bosquetaoista_persona WHERE casa_practica_id = {casa[0]} AND estado_id = 1'
		cursor.execute(q1)
		activos = cursor.fetchone()

		q1 = f'SELECT COUNT(*) from bosquetaoista_persona WHERE casa_practica_id = {casa[0]} AND estado_id = 2'
		cursor.execute(q1)
		noactivos = cursor.fetchone()

		q1 = f'SELECT COUNT(*) from bosquetaoista_persona WHERE casa_practica_id = {casa[0]} AND estado_id = 3'
		cursor.execute(q1)
		fallecidos = cursor.fetchone()

		anf = ' / '.join([ str(activos[0]), str(noactivos[0]), str(fallecidos[0])])
		tmp: CasasLista = ( casa[0], casa[1], casa[2], resps, anf )
		casaslista.append(tmp)
	return(casaslista)



def get_casa_detalles(id: int):
	conn, cursor = connect()

	q1 = f'SELECT nombre, direccion FROM bosquetaoista_casa where id = {id}'
	cursor.execute(q1)
	casa =  cursor.fetchone()
	casa = ' - '.join([casa[1], casa[2]])

	q1 = f'SELECT B.nombre, concat(A.apellido, A.nombre) FROM bosquetaoista_persona A, bosquetaoista_grado B WHERE A.responsable_casa_id = {id} AND B.id = A.grado_id'
	cursor.execute(q1)
	resps = cursor.fetchall()
	responsables = [' - '.join([resp[0], resp[1]]) for resp in resps]

	# for resp in resps:
	# 	tmp = {'grado': grado.nombre, 'nombre': resp.nombre, 'apellido': resp.apellido}
	# 	responsables.append(tmp)

	# alumnos = []
	# personas = session.query(models.Persona).filter(models.Persona.casa_practica_id==id).all()
	# for persona in personas:
	# 	grado = session.get(models.Grado, persona.grado_id)
	# 	tmp = { 'id': persona.id, 'orden': persona.orden, 'foto': persona.foto, 
	# 					'nombre': persona.nombre, 'apellido': persona.apellido, 
	# 					'grado': grado.nombre }
	# 	if (persona.foto is not None):
	# 		pass
	# 	alumnos.append(tmp)
	# todos = { 'casa': casa, 'responsables':responsables, 'alumnos':alumnos }
	return(casa, responsables)

#######



def get_persona(id: int) -> Persona:
	conn, cursor = connect()
	q1 = f'select * from bosquetaoista_persona WHERE id = {id}'
	cursor.execute(q1)
	persona = cursor.fetchone()
	return(persona)

def get_grado(id: int) -> Grado:
	conn, cursor = connect()
	q1 = f'select * from bosquetaoista_grado WHERE id = {id}'
	cursor.execute(q1)
	grado = cursor.fetchone()
	return(grado)


def get_casa(id: int) -> Casa:
	conn, cursor = connect()
	q1 = f'select * from bosquetaoista_casa WHERE id = {id}'
	cursor.execute(q1)
	casa = cursor.fetchone()
	return(casa)



def get_casa_detalles(id: int):
	conn, cursor = connect()

	q1 = f'SELECT nombre, direccion FROM bosquetaoista_casa where id = {id}'
	cursor.execute(q1)
	casa =  cursor.fetchone()
	casa = ' - '.join([casa[1], casa[2]])

	q1 = f'SELECT B.nombre, concat(A.apellido, A.nombre) FROM bosquetaoista_persona A, bosquetaoista_grado B WHERE A.responsable_casa_id = {id} AND B.id = A.grado_id'
	cursor.execute(q1)
	resps = cursor.fetchall()
	responsables = [' - '.join([resp[0], resp[1]]) for resp in resps]

	# for resp in resps:
	# 	tmp = {'grado': grado.nombre, 'nombre': resp.nombre, 'apellido': resp.apellido}
	# 	responsables.append(tmp)

	# alumnos = []
	# personas = session.query(models.Persona).filter(models.Persona.casa_practica_id==id).all()
	# for persona in personas:
	# 	grado = session.get(models.Grado, persona.grado_id)
	# 	tmp = { 'id': persona.id, 'orden': persona.orden, 'foto': persona.foto, 
	# 					'nombre': persona.nombre, 'apellido': persona.apellido, 
	# 					'grado': grado.nombre }
	# 	if (persona.foto is not None):
	# 		pass
	# 	alumnos.append(tmp)
	# todos = { 'casa': casa, 'responsables':responsables, 'alumnos':alumnos }
	return(casa, responsables)




# def get_personas_lista(estado_id: int, busq: str, id: int):

# 	titulo = []
# 	personaslista = []

# 	conn, cursor = connect()
# 	if (int(id) == 0):
# 		if (estado_id == 0 and busq == '*'):
# 			q1 = 'select * from bosquetaoista_persona ORDER BY estado_id, orden'
# 			cursor.execute(q1)
# 			personas = cursor.fetchall()

# 		elif (estado_id == 0 and busq != '*'):
# 			q1 = f'select * from bosquetaoista_persona WHERE nombre like "*{busq}*" or apellido like "*{busq}*" ORDER BY estado_id, orden'
# 			# print('11 ', q1)
# 			cursor.execute(q1)
# 			personas = cursor.fetchall()

# 		elif (estado_id != 0 and busq == '*'):
# 			q1 = f'select * from bosquetaoista_persona WHERE estado_id = {estado_id} ORDER BY orden'
# 			# print('12 ', q1)
# 			cursor.execute(q1)
# 			personas = cursor.fetchall()

# 		else:
# 			q1 = f'select * from bosquetaoista_persona WHERE estado_id = {estado_id} or nombre like "*{busq}*" or apellido like "*{busq}*" ORDER BY orden'
# 			# print('13 ', q1)
# 			cursor.execute(q1)
# 			personas = cursor.fetchall()

# 		# titulo = [ casapractica[1], casapractica[2], grado[1], ', '.join([per[3], per[2]]) ]

# 		for pers in personas:
# 			q1 = f'select * from bosquetaoista_grado WHERE id = {pers[15]}'
# 			# print('14 ', q1)
# 			cursor.execute(q1)
# 			grado = cursor.fetchone()
# 			q1 = f'select * from bosquetaoista_tipoestado WHERE id = {pers[18]}'
# 			# print('15 ', q1)
# 			cursor.execute(q1)
# 			estado = cursor.fetchone()
# 			q1 = f'select * from bosquetaoista_casa WHERE id = {pers[14]}'
# 			# print('16 ', q1)
# 			cursor.execute(q1)
# 			casapractica = cursor.fetchone()
# 			tmp = [ pers[0], pers[1], pers[2], estado[1], pers[18], 
# 		  			pers[2], pers[3], grado[1], casapractica[2] ]
# 			personaslista.append(tmp)

# 	else:
# 		q1 = f'select * from bosquetaoista_persona WHERE id = {id}'
# 		# print('17 ', q1)
# 		cursor.execute(q1)
# 		per = cursor.fetchone()
# 		q1 = f'select * from bosquetaoista_grado WHERE id = {per[15]}'
# 		# print('18 ', q1)
# 		cursor.execute(q1)
# 		grado = cursor.fetchone()
# 		q1 = f'select * from bosquetaoista_tipoestado WHERE id = {per[18]}'
# 		# print('19 ', q1)
# 		cursor.execute(q1)
# 		estado = cursor.fetchone()
# 		q1 = f'select * from bosquetaoista_casa WHERE id = {per[14]}'
# 		# print('20 ', q1)
# 		cursor.execute(q1)
# 		casapractica = cursor.fetchone()
# 		if (per[19] is None):
# 			foto = ''
# 		else:
# 			foto = f'/fotos/img_{per[3]}_' + str(per[1]).zfill(4) + '.jpg'
# 		titulo = [ casapractica[1], casapractica[2], grado[1], ', '.join([per[3], per[2]]) ]
# 		if (per[16] is not None):
# 			q1 = f'select * from bosquetaoista_persona WHERE casa_practica_id = {per[16]} AND id != {per[0]} AND estado_id = {per[18]} ORDER BY orden'
# 			# print('20 ', q1)

# 			cursor.execute(q1)
# 			pers = cursor.fetchall()
# 			for per in pers:
# 				q1 = f'select * from bosquetaoista_grado WHERE id = {per[15]}'
# 				# print('21 ', q1)
# 				cursor.execute(q1)
# 				grado = cursor.fetchone()
# 				q1 = f'select * from bosquetaoista_tipoestado WHERE id = {per[18]}'
# 				# print('22 ', q1)
# 				cursor.execute(q1)
# 				estado = cursor.fetchone()
# 				q1 = f'select * from bosquetaoista_casa WHERE id = {per[14]}'
# 				# print('23 ', q1)
# 				cursor.execute(q1)
# 				casapractica = cursor.fetchone()
# 				if (per[19] is None):
# 					foto = ''
# 				else:
# 					foto = f'/fotos/img_{per[3]}_' + str(per[1]).zfill(4) + '.jpg'
# 				tmp = [ per[0], per[1], foto, ', '.join([per[2], per[3]]), grado[1] ]
# 				personaslista.append(tmp)

# 	print('titulo ', titulo)
# 	print('personaslista ', personaslista)
# 	return(titulo, personaslista)
