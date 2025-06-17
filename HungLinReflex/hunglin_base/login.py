import reflex as rx
from ..service.hunglin_page import HunglinState



# class LoginState(rx.State):
# 	login: bool = False
# 	usuario: str

# 	@rx.event(background=True)
# 	async def set_usuario(self, usuario):
# 		async with self:
# 			self.usuario = usuario

# 	@rx.event(background=True)
# 	async def set_clave(self, clave):
# 		async with self:
# 			self.clave = clave

	# @rx.event(background=True)
	# async def ingresar(self):
	# 	async with self:
	# 		persona = chk_usuario_service(self.usuario, self.clave)
	# 		if (persona is not None):
	# 			self.nombre = persona[2].split(' ')[0]
	# 			self.is_superuser = persona[22]
	# 			self.is_staff = persona[23]
	# 			self.login = True


def fnc_login() -> rx.Component:
	return rx.box(
		rx.center(
			rx.vstack(
				rx.image(
					src='/bosquetaoista/hunglin.ico',
					width='16vw',
				),
				rx.input(
					placeholder='Usuario',
					type='text',
					width='16vw',
					on_change=HunglinState.set_usuario,
				),
				rx.input(
					placeholder='Clave',
					type='password',
					width='16vw',
					on_change=HunglinState.set_clave,
				),
				rx.button(
					'Ingresar',
					width='16vw',
				)
			)
		),
		background_color ='#801316',
		width='22vw',
		height='auto',
		margin_x='39vw',
		margin_top='2vw',
		style={ 'padding':'2vw' }
	)
