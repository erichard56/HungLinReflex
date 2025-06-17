import reflex as rx

def fnc_casas(casas) -> rx.Component:
	return rx.center(
		rx.box(
			# menu(),
			rx.heading('CASAS', margin_x='1vw', style={'color':'black'}),
			rx.table.root(
				rx.table.header(
					rx.table.row(
						rx.table.column_header_cell('Nombre', width='20vw', style={'color':'black'}),
						rx.table.column_header_cell('Dirección', width='25vw', style={'color':'black'}),
						rx.table.column_header_cell('Responsable', width='30vw', style={'color':'black'}),
						rx.table.column_header_cell('Alumnos (A/N/F)', width='10vw', style={'color':'black'}),
						rx.table.column_header_cell('Acciones', width='15vw', style={'color':'black'})
					)
				),
				rx.table.body(
					rx.foreach(casas, mostrar_casa),
				),
			),
			background_color ='#fff',
			width='70vw',
			height='auto',
			# margin_x='1vw',
			padding_bottom='1vw',
		),
		background_color ='#801316',
		width='100vw',
		height='auto'
	)

def mostrar_casa(casa) -> rx.Component:
	return rx.table.row(
		rx.table.cell(casa[1], style={'color':'black'}),
		rx.table.cell(casa[2], style={'color':'black'}),
		rx.table.cell(casa[3], style={'color':'black'}),
		rx.table.cell(casa[4], style={'color':'black'}),
		rx.table.cell(
			rx.hstack(
				rx.button(
					rx.icon(
						'pen'
					)
				),
				rx.link(
					rx.button(
						rx.icon(
							'users',
						),
						# on_click=HunglinState.get_casa_detalles(casalista[0]),
					),
					href='/casadetalleslista'
				),
			)
		)
	)
