import mysql.connector
import hashlib
import random

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
def db_get_casas():
	respuesta = []
	q1 = f'SELECT * FROM bosquetaoista_casa ORDER BY id'
	cursor.execute(q1)
	casas = cursor.fetchall()
	for casa in casas:
		q1 = f'SELECT CONCAT(apellido, ", ", nombre) FROM bosquetaoista_persona WHERE responsable_casa_id = {casa[0]} ORDER BY orden'
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
		# anf = ' / '.join([activos, noactivos, fallecidos])
		respuesta.append([casa[0], casa[1], casa[2], responsables, anf])
	return(respuesta)

def db_get_casa(id: int):
	q1 = f'SELECT * FROM bosquetaoista_casa WHERE id = {id}'
	cursor.execute(q1)
	casa = cursor.fetchone()
	return(casa)

def db_upd_casa(id: int, nombre: str, direccion: str):
	if (int(id) != 0):
		q1 =  f'UPDATE bosquetaoista_casa SET nombre="{nombre}", direccion="{direccion}" WHERE id={id}'
	else:
		q1 =  f'INSERT INTO bosquetaoista_casa VALUES (0, "{nombre}", "{direccion}")'
	cursor.execute(q1)
	conn.commit()
	return

def db_get_alumnos(id: int):
	q1 = f'SELECT nombre FROM bosquetaoista_casa WHERE id = {id}'
	cursor.execute(q1)
	casa = cursor.fetchone()
	q1 = f'SELECT CONCAT(apellido, ", ", nombre) FROM bosquetaoista_persona WHERE estado_id = 1 AND responsable_casa_id = {id}'
	cursor.execute(q1)
	resps = cursor.fetchall()
	responsables = ' // '.join([resp[0] for resp in resps])
	q1 = f'SELECT A.id, A.orden, CASE WHEN A.foto is NULL THEN "/bosquetaoista/nophoto.jpg" ELSE CONCAT("/fotos/",CONCAT("img_", A.apellido, "_", LPAD(A.orden, 4, "0"), ".jpg")) END, CONCAT(A.apellido, ", ", A.nombre), B.nombre FROM  bosquetaoista_persona A INNER JOIN bosquetaoista_grado B on B.id = A.grado_id WHERE A.estado_id = 1 AND A.casa_practica_id = {id}'
	cursor.execute(q1)
	alumnos = cursor.fetchall()
	return(casa, responsables, alumnos)

# personas
def db_get_persona(id):
	q1 = f'SELECT A.id, B.nombre as estado, A.orden, A.apellido, A.nombre, A.usuario, C.nombre as grado,  D.nombre as casa_practica, E.nombre as responsable_casa, A.direccion, A.localidad, A.codigo_postal, A.email, A.fechanacimiento, A.fechaingreso, A.fechaegreso, A.celular, F.nombre as tipodoc, A.nrodoc, A.clave, A.is_superuser, A.is_staff, CASE WHEN A.foto is NULL THEN "/bosquetaoista/nophoto.jpg" ELSE CONCAT("/fotos/",CONCAT("img_", A.apellido, "_", LPAD(A.orden, 4, "0"), ".jpg")) END as foto, CASE WHEN A.certificado is NULL THEN "/bosquetaoista/nocert.jpg" ELSE CONCAT("/certificados/", CONCAT("cer_", A.apellido, "_", LPAD(A.orden, 4, "0"), ".jpg")) END as certificado FROM bosquetaoista_persona A INNER JOIN bosquetaoista_tipoestado B on B.id = A.estado_id INNER JOIN bosquetaoista_grado C on C.id = A.grado_id INNER JOIN bosquetaoista_casa D on D.id = A.casa_practica_id LEFT JOIN bosquetaoista_casa E on E.id = A.responsable_casa_id LEFT JOIN bosquetaoista_tipodoc F on F.id = A.tipodoc_id WHERE A.id = {id}'
	cursor.execute(q1)
	persona = cursor.fetchone()
	q1 = 'SELECT * FROM bosquetaoista_tipoestado ORDER BY id'
	cursor.execute(q1)
	tipoestado = cursor.fetchall()
	return(persona, tipoestado)

def db_get_personas():
	q1 = 'SELECT A.id, A.orden, B.nombre as estado, CASE WHEN A.foto is NULL THEN "/bosquetaoista/nophoto.jpg" ELSE CONCAT("/fotos/", CONCAT("img_", A.apellido, "_", LPAD(A.orden, 4, "0"), ".jpg")) END as foto, CONCAT(A.apellido, ", ", A.nombre), C.nombre as grado, D.nombre as casapractica FROM bosquetaoista_persona A INNER JOIN bosquetaoista_tipoestado B on B.id = A.estado_id INNER JOIN bosquetaoista_grado C on C.id = A.grado_id INNER JOIN bosquetaoista_casa D on D.id = A.casa_practica_id WHERE A.estado_id = 1 ORDER BY A.orden'
	cursor.execute(q1)
	personas = cursor.fetchall()
	return(personas)

