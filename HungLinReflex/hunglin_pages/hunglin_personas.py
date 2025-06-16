import reflex as rx
import icecream as ic
from ..service.hunglin_page import HunglinState

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

def fnc_personas_detalles(detalles: tuple, eventos: list, extras: list) -> rx.Component:
	return rx.box(
		rx.heading(
			detalles[0], size='7'
		),
		fnc_detalles(detalles),
		rx.spacer(),
		fnc_eventos(eventos),
		rx.spacer(),
		fnc_extras(extras),
	)


def fnc_detalles_row(titulo: str, valor1: str, valor2: str = None) -> rx.Component:
	return rx.table.row(
		rx.table.cell(rx.text(titulo)),
		rx.cond(
			valor2 is None,
			rx.table.cell(rx.text(valor1)),
			rx.table.cell(rx.text(valor1, ' ', valor2))
		)
	),



def fnc_detalles(detalles: tuple) -> rx.Component:
	return rx.table.root(
		rx.table.header(
			rx.table.row(
				rx.table.column_header_cell('Imagen', width='50vw', style={'color':'black'}),
				rx.table.column_header_cell('Datos', width='50vw', style={'color':'black'}),
			),
		),
		rx.table.body(
			rx.table.row(
				rx.table.cell(
					rx.vstack(
						rx.image(
							src=detalles[15],
							width="25vw",
							height="auto",
						),
						rx.image(
							src=detalles[16],
							width="25vw",
							height="auto",
						),
						margin='6vw',
						padding='0vw',
					),
				),
				rx.table.cell(
					rx.table.root(
						rx.table.body(
							fnc_detalles_row('Orden', detalles[2]),
							fnc_detalles_row('Estado', detalles[3]),
							fnc_detalles_row('Grado', detalles[4]),
							fnc_detalles_row('Casa de Practica', detalles[5]),
							fnc_detalles_row('Responsable de Casa', detalles[6]),
							fnc_detalles_row('Dirección', detalles[7]),
							fnc_detalles_row('Localidad', detalles[8]),
							fnc_detalles_row('e-mail', detalles[9]),
							fnc_detalles_row('Fecha de Nacimiento', detalles[10]),
							fnc_detalles_row('Fecha de Ingreso', detalles[11]),
							fnc_detalles_row('Fecha de Egreso', detalles[12]),
							fnc_detalles_row('Documento', detalles[13], detalles[14]),
							fnc_detalles_row('Privilegios', detalles[17]),
						),
					)
				)
			)
		)
	),



def eventos_row(eventos) -> rx.Component:
	return rx.table.row(
			rx.table.cell(eventos[0]),
			rx.table.cell(eventos[1]),
			rx.table.cell(eventos[2]),
			rx.table.cell(eventos[3]),
			rx.table.cell(eventos[4]),
		)


def fnc_eventos(eventos: list):
	return rx.box(
		rx.heading('CURSOS / ACTIVIDADES / PRACTICAS'),
		rx.table.root(
			rx.table.header(
				rx.table.row(
					rx.table.column_header_cell('Tipo', width='20vw', style={'color':'black'}),
					rx.table.column_header_cell('Nombre', width='20vw', style={'color':'black'}),
					rx.table.column_header_cell('Fecha', width='10vw', style={'color':'black'}),
					rx.table.column_header_cell('Orador', width='30vw', style={'color':'black'}),
					rx.table.column_header_cell('Estado', width='20vw', style={'color':'black'}),
				),
			),
			rx.table.body(
				rx.foreach(eventos, eventos_row)
			),
		),
	)


def extra_row(extra) -> rx.Component:
	return rx.table.row(
		rx.table.cell(extra[0]),
		rx.table.cell(extra[1]),
	)


def fnc_extras(extras: list):
	return rx.box(
		rx.heading('INFORMACION EXTRA'),
		rx.table.root(
			rx.table.header(
				rx.table.row(
					rx.table.column_header_cell('Tipo', width='30vw', style={'color':'black'}),
					rx.table.column_header_cell('Comentario', width='70vw', style={'color':'black'}),
				),
			),
			rx.table.body(
				rx.foreach(extras, extra_row)
			),
		),
	)
