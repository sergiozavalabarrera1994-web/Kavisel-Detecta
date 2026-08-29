from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock
from kivy.graphics import Color, Rectangle
import random, time, platform

# COLORES OFICIALES
COLOR_ALERTA_MAX = (0.90, 0.20, 0.20, 1)
COLOR_ALERTA_MEDIA = (0.95, 0.70, 0.20, 1)
COLOR_SEGURO = (0.20, 0.80, 0.30, 1)
COLOR_FONDO = (0.05, 0.05, 0.15, 1)
COLOR_TEXTO = (1, 1, 1, 1)

# BASE DE SEÑALES — TODAS LAS PRIORIDADES
SENALES = [
    {'id':'dron','nombre':'DRON','icono':'🚁','color':COLOR_ALERTA_MAX,'prioridad':1,'desc':'Señal de dron detectada — ALERTA MÁXIMA'},
    {'id':'pdi','nombre':'POLICÍA DE INVESTIGACIONES','icono':'🔫','color':COLOR_ALERTA_MAX,'prioridad':1,'desc':'Unidad de investigación detectada — ALERTA MÁXIMA'},
    {'id':'carabineros','nombre':'CARABINEROS','icono':'🚓','color':COLOR_ALERTA_MAX,'prioridad':1,'desc':'Fuerza policial detectada — ALERTA MÁXIMA'},
    {'id':'bomberos','nombre':'BOMBEROS','icono':'🚒','color':COLOR_ALERTA_MEDIA,'prioridad':2,'desc':'Cuerpo de bomberos detectado'},
    {'id':'ambulancia','nombre':'AMBULANCIA','icono':'🚑','color':COLOR_ALERTA_MEDIA,'prioridad':2,'desc':'Servicio médico detectado'},
    {'id':'emergencia','nombre':'SERVICIO DE EMERGENCIA','icono':'📡','color':COLOR_ALERTA_MEDIA,'prioridad':2,'desc':'Red de emergencia detectada'},
    {'id':'radio','nombre':'RADIO COMERCIAL','icono':'📻','color':COLOR_SEGURO,'prioridad':3,'desc':'Señal comercial detectada'},
    {'id':'telefonia','nombre':'RED TELEFÓNICA','icono':'📶','color':COLOR_SEGURO,'prioridad':3,'desc':'Red telefónica detectada'}
]

class FondoBox(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        with self.canvas.before: Color(*COLOR_FONDO); self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._upd, pos=self._upd)
    def _upd(self, inst, val): self.rect.size = self.size; self.rect.pos = self.pos

class Principal(Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.activo = False
        layout = FondoBox(orientation='vertical', padding=20, spacing=15)
        layout.add_widget(Label(text='🛡️ KAVISEL DETECTA', font_size=28, bold=True, color=COLOR_TEXTO, size_hint_y=0.15))
        self.estado = Label(text='⏳ Sistema en espera...', font_size=18, color=(0.8,0.8,0.8,1), size_hint_y=0.2)
        layout.add_widget(self.estado)
        self.lista = Label(text='Sin señales detectadas', font_size=14, color=(0.7,0.7,0.7,1), markup=True, size_hint_y=0.45)
        layout.add_widget(self.lista)
        btns = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=0.2)
        self.btn_ini = Button(text='▶️ INICIAR', font_size=16, background_color=(0.2,0.7,0.3,1), on_press=self.iniciar)
        self.btn_fin = Button(text='⏹️ DETENER', font_size=16, background_color=(0.8,0.2,0.2,1), on_press=self.detener, disabled=True)
        btns.add_widget(self.btn_ini); btns.add_widget(self.btn_fin)
        layout.add_widget(btns)
        layout.add_widget(Label(text='Creado por Sergio Zavala Barrera', font_size=11, color=(0.4,0.4,0.5,1), size_hint_y=0.1))
        self.add_widget(layout)
    def iniciar(self, inst):
        self.activo = True; self.btn_ini.disabled = True; self.btn_fin.disabled = False
        self.estado.text = '🔍 Escaneando...'; self.estado.color = (0.95,0.8,0.2,1)
        Clock.schedule_interval(self._escaneo, 2.5)
    def detener(self, inst):
        self.activo = False; self.btn_ini.disabled = False; self.btn_fin.disabled = True
        self.estado.text = '⏳ Escaneo detenido'; self.estado.color = (0.8,0.8,0.8,1)
        Clock.unschedule(self._escaneo)
    def _escaneo(self, dt):
        if not self.activo: return
        if random.randint(1,100) <= 35:
            s = random.choice(SENALES); h = time.strftime('%H:%M:%S')
            r,g,b = s['color'][:3]
            nuevo = f'[color={r},{g},{b},1]{s["icono"]} [b]{s["nombre"]}[/b] — {h}\n{s["desc"]}\n[/color]\n'
            self.lista.text = nuevo + self.lista.text
            if s['prioridad'] == 1:
                self.estado.text = f'🚨 ALERTA MÁXIMA: {s["nombre"]}'
            elif s['prioridad'] == 2:
                self.estado.text = f'⚠️ DETECTADO: {s["nombre"]}'
            else:
                self.estado.text = f'📡 Detectado: {s["nombre"]}'
            self.estado.color = s['color']

class KaviselDetectaApp(App):
    title = 'Kavisel Detecta'
    icon = 'kavisel_icon'
    def build(self):
        sm = ScreenManager(); sm.add_widget(Principal(name='principal')); return sm

if __name__ == '__main__':
    KaviselDetectaApp().run()
