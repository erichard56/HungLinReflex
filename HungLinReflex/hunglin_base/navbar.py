import reflex as rx
import icecream as ic

# from ..service.hunglin_page import HunglinState





def navbar_icons_item(icon: str, text: str, url: str) -> rx.Component:
	return rx.link(
		rx.hstack(
			rx.icon(icon),
			rx.text(text, size="4", weight="medium"),
		),
		href=url,
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
					rx.text( 'Hola ', nombre, ' !!'),
					rx.text('Inicie conexion')
				),
				rx.cond(
					nombre,
					rx.link(nombre, rx.button(rx.icon('angry'), 'Salir'), href='/'),
					rx.link(
						nombre, 
						rx.button(
							rx.icon(
								'door-open'), 
								'Login',
								# on_click=HunglinState.set_login
							), 
						href='/login'
					),
				),
				align_items='center',
			),
		),
		rx.cond(
			nombre,
			rx.hstack(
				rx.flex(
					navbar_icons_item("users", "Personas", "/#"),
					navbar_icons_item("home", "Agenda", "/#"),
					navbar_icons_item("home", "Eventos", "/#"),
					navbar_icons_item("house-plus", "Casas", "/#"),
					navbar_icons_item("home", "Grados", "/#"),
					navbar_icons_item("home", "Tipo Eventos", "/#"),
					navbar_icons_item("home", "Extras", "/#"),
					spacing="5",
				),
				margin_x='2vw',
				bg=rx.color("accent", 3),
			),
		),
		text_align='center',
		justify='center',
	)
