# ==================================================
# KAVISEL DETECTA — Detector de Radiofrecuencias + Alertas
# VERSIÓN 1.4 — ALERTA MÁXIMA: DRONES · PDI · CARABINEROS ⚡🚨
# Creador: Pista — Sergio David Zavala V.
# Código PROTEGIDO — No distribuible ni modificable
# ==================================================

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.list import MDList, TwoLineListItem
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.switch import MDSwitch
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.clock import Clock
from kivy.utils import platform
from kivy.core.window import Window
from plyer import notification, vibrator
import time, random

# 🔒 METADATOS PROTEGIDOS
__APP_NAME__ = "Kavisel Detecta"
__VERSION__ = "1.4 — Alerta Máxima"
__CREATOR__ = "Pista — Sergio David Zavala V."

# 📡 PERMISOS SEGÚN PLATAFORMA
if platform == 'android':
    from android.permissions import request_permissions, Permission

class KaviselDetectaScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.name = "kavisel_detecta"
        self.escaneo_activo = False
        self.señales_vistas = set()
        self.drones_detectados = 0
        self.alertas_maximas = 0
        self.lat, self.lon = -33.4569, -70.6483
        
        self.cfg = {
            "sonido": True, "vibracion": True,
            "solo_emergencia": False,
            "alerta_drones": True,
            "alerta_maxima": True
        }
        
        Window.clearcolor = (0.04, 0.04, 0.06, 1)
        layout = MDBoxLayout(orientation='vertical', padding=24, spacing=12)
        
        # 📡 TÍTULO
        layout.add_widget(MDLabel(
            text="📡 KAVISEL DETECTA", halign="center",
            font_style="H4", bold=True, theme_text_color="Custom",
            text_color=(1, 0.15, 0.25, 1)
        ))
        layout.add_widget(MDLabel(
            text="⚠️ ALERTA MÁXIMA: Drones · PDI · Carabineros",
            halign="center", font_style="Caption", theme_text_color="Error", bold=True
        ))
        
        # ⚡ CONTADOR DE ALERTAS MÁXIMAS
        self.lbl_alertas_max = MDLabel(
            text="⚡ ALERTAS MÁXIMAS DETECTADAS: 0", halign="center",
            font_style="H5", bold=True, theme_text_color="Custom",
            text_color=(1, 0.2, 0.2, 1)
        )
        layout.add_widget(self.lbl_alertas_max)
        
        # 🚁 CONTADOR DE DRONES
        self.lbl_drones = MDLabel(
            text="🚁 Drones detectados: 0", halign="center",
            font_style="Subtitle1", theme_text_color="Custom",
            text_color=(0.9, 0.3, 0.1, 1)
        )
        layout.add_widget(self.lbl_drones)
        
        # 📍 GPS
        self.lbl_gps = MDLabel(text="📍 Ubicación: Esperando señal...", halign="center")
        layout.add_widget(self.lbl_gps)
        
        # 🚨 ESTADO
        self.lbl_estado = MDLabel(
            text="⚠️ ALERTA MÁXIMA ACTIVA — Drones·PDI·Carabineros = PRIORIDAD ABSOLUTA",
            halign="center", theme_text_color="Error", font_style="Body1", bold=True
        )
        layout.add_widget(self.lbl_estado)
        
        # ⚙️ CONTROLES
        fila1 = MDBoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=40)
        fila1.add_widget(MDLabel(text="🔊 Sonido:", size_hint_x=0.25))
        self.sw_sonido = MDSwitch(active=True)
        fila1.add_widget(self.sw_sonido)
        fila1.add_widget(MDLabel(text="📳 Vibración:", size_hint_x=0.25))
        self.sw_vibra = MDSwitch(active=True)
        fila1.add_widget(self.sw_vibra)
        layout.add_widget(fila1)
        
        self.chk_emergencia = MDCheckbox(
            label="🚨 Solo alertas de EMERGENCIA", active=False, size_hint=(1, None), height=40
        )
        layout.add_widget(self.chk_emergencia)
        
        self.chk_maxima = MDCheckbox(
            label="⚠️ ALERTA MÁXIMA — Siempre activa", active=True, disabled=True,
            size_hint=(1, None), height=40
        )
        layout.add_widget(self.chk_maxima)
        
        # 🔘 BOTÓN PRINCIPAL
        self.btn_escaneo = MDRaisedButton(
            text="🔍 INICIAR ESCANEO", pos_hint={"center_x": 0.5},
            on_press=self.alternar_escaneo, md_bg_color=(0.2, 0.75, 0.35, 1), font_size=18
        )
        layout.add_widget(self.btn_escaneo)
        
        # 📊 BARRA
        self.barra = MDProgressBar(value=0, max=100)
        layout.add_widget(self.barra)
        
        # 📋 LEYENDA
        layout.add_widget(MDLabel(
            text="⚠️ ROJO = ALERTA MÁXIMA: 🚁 Drones · 🟣 PDI · 🔵 Carabineros → EVITAR ZONA",
            halign="center", font_style="Caption", text_color=(1, 0.3, 0.3, 1), bold=True
        ))
        layout.add_widget(MDLabel(
            text="📋 Resto: 🚑 Bomberos · 🚑 SAMU · 🚒 Rescate · 📡 Público · ⚪ Privado",
            halign="center", font_style="Caption", text_color=(0.7, 0.7, 0.7, 1)
        ))
        
        # 📋 LISTA
        layout.add_widget(MDLabel(text="📡 Señales Detectadas:", font_style="Subtitle1"))
        self.lista = MDList()
        layout.add_widget(self.lista)
        
        self.add_widget(layout)
        
        Clock.schedule_once(self.solicitar_permisos, 1)
        Clock.schedule_interval(self.actualizar_gps, 8)
    
    def solicitar_permisos(self, dt):
        if platform == 'android':
            from android.permissions import request_permissions, Permission
            request_permissions([
                Permission.ACCESS_FINE_LOCATION, Permission.INTERNET,
                Permission.ACCESS_WIFI_STATE, Permission.VIBRATE,
                Permission.POST_NOTIFICATIONS
            ])
            self.lbl_gps.text = "📍 GPS activo — ALERTA MÁXIMA escaneando..."
    
    def es_alerta_maxima(self, categoria):
        return categoria in ["DRON_CONTROL", "DRON_VIDEO", "DRON_TELE", "PDI", "CARABINEROS"]
    
    def obtener_color_servicio(self, categoria):
        colores = {
            "DRON_CONTROL": "FF0000", "DRON_VIDEO": "FF0000", "DRON_TELE": "FF0000",
            "PDI": "FF0000", "CARABINEROS": "FF0000",
            "BOMBEROS": "FF4422", "SAMU": "FFCC00", "RESCATE": "FF9900",
            "PÚBLICO": "3388FF", "PRIVADO": "888888"
        }
        return colores.get(categoria, "FFFFFF")
    
    def emitir_alerta(self, señal):
        categoria = señal.get("cat", "DESCONOCIDO")
        nombre_servicio = señal.get("nombre", "Señal desconocida")
        frecuencia = señal.get("freq", "—")
        distancia = señal.get("dist", "—")
        
        if self.es_alerta_maxima(categoria):
            self.alertas_maximas += 1
            self.lbl_alertas_max.text = f"⚡ ALERTAS MÁXIMAS DETECTADAS: {self.alertas_maximas}"
            
            if "DRON" in categoria:
                titulo = "🚁 ¡ALERTA MÁXIMA — DRON DETECTADO!"
                mensaje = f"⚠️ Posible vigilancia o grabación — {nombre_servicio}\n📻 {frecuencia} · 📍 {distancia}\n🚨 EVITAR LA ZONA"
            elif categoria == "PDI":
                titulo = "🟣 ¡ALERTA MÁXIMA — PDI DETECTADA!"
                mensaje = f"⚠️ Operaciones policiales — posible zona de riesgo — {nombre_servicio}\n📻 {frecuencia} · 📍 {distancia}\n🚨 ALEJARSE — PELIGRO DE ENFRENTAMIENTO"
            elif categoria == "CARABINEROS":
                titulo = "🔵 ¡ALERTA MÁXIMA — CARABINEROS DETECTADOS!"
                mensaje = f"⚠️ Presencia de fuerzas de seguridad — posible enfrentamiento — {nombre_servicio}\n📻 {frecuencia} · 📍 {distancia}\n🚨 PRECAUCIÓN — ZONA DE RIESGO"
            
            patron_vibracion = [500, 200, 500, 200, 500, 200, 500, 200, 500]
        
        elif categoria in ["BOMBEROS", "SAMU", "RESCATE"]:
            if self.chk_emergencia.active and categoria not in ["BOMBEROS", "SAMU", "RESCATE"]:
                return
            if categoria == "BOMBEROS":
                titulo = "🚑 BOMBEROS — ACTIVIDAD CERCANA"
            elif categoria == "SAMU":
                titulo = "🚑 SAMU — AMBULANCIAS EN LA ZONA"
            elif categoria == "RESCATE":
                titulo = "🚒 RESCATE — EN OPERACIÓN"
            else:
                titulo = "🚨 EMERGENCIA — Señal detectada"
            mensaje = f"📻 {frecuencia} · 📍 {distancia}"
            patron_vibracion = [200, 100, 200, 100, 200]
        
        else:
            if self.chk_emergencia.active:
                return
            titulo = f"📡 {señal['tipo']}"
            mensaje = f"{nombre_servicio} · 📻 {frecuencia}"
            patron_vibracion = 500
        
        try:
            notification.notify(title=titulo, message=mensaje, app_name="Kavisel Detecta", timeout=15)
        except: pass
        if self.sw_vibra.active:
            try: vibrator.vibrate(patron_vibracion)
            except: pass
    
    def actualizar_gps(self, dt):
        self.lat += random.uniform(-0.0002, 0.0002)
        self.lon += random.uniform(-0.0002, 0.0002)
        self.lbl_gps.text = f"📍 {self.lat:.4f}, {self.lon:.4f}"
    
    def alternar_escaneo(self, inst):
        if not self.escaneo_activo:
            self.escaneo_activo = True
            self.btn_escaneo.text = "⏹ DETENER"
            self.btn_escaneo.md_bg_color = (0.9, 0.2, 0.2, 1)
            self.señales_vistas.clear()
            self.drones_detectados = 0
            self.alertas_maximas = 0
            self.lbl_drones.text = "🚁 Drones detectados: 0"
            self.lbl_alertas_max.text = "⚡ ALERTAS MÁXIMAS DETECTADAS: 0"
            self.lista.clear_widgets()
            Clock.schedule_interval(self.realizar_escaneo, 2)
        else:
            self.escaneo_activo = False
            self.btn_escaneo.text = "🔍 INICIAR ESCANEO"
            self.btn_escaneo.md_bg_color = (0.2, 0.75, 0.35, 1)
            Clock.unschedule(self.realizar_escaneo)
            self.barra.value = 0
    
    def realizar_escaneo(self, dt):
        self.barra.value = min(100, self.barra.value + 8)
        señales = [
            {"t": "🚁 ALERTA MÁXIMA — DRON", "nombre": "Señal de control de dron", "freq": "2.400-2.483 GHz", "dist": "~150m", "cat": "DRON_CONTROL"},
            {"t": "🚁 ALERTA MÁXIMA — DRON VIDEO", "nombre": "Transmisión de video en vivo — TE GRABAN", "freq": "5.725-5.850 GHz", "dist": "~80m — MUY CERCA", "cat": "DRON_VIDEO"},
            {"t": "🚁 ALERTA MÁXIMA — DRON", "nombre": "Telemetría de dron", "freq": "2.450 MHz", "dist": "~200m", "cat": "DRON_TELE"},
            {"t": "🟣 ALERTA MÁXIMA — PDI", "nombre": "Policía de Investigaciones — Red Nacional", "freq": "150.890 MHz", "dist": "~1.5 km", "cat": "PDI"},
            {"t": "🟣 ALERTA MÁXIMA — PDI", "nombre": "PDI — Comando Regional", "freq": "151.010 MHz", "dist": "~2.8 km", "cat": "PDI"},
            {"t": "🟣 ALERTA MÁXIMA — PDI", "nombre": "PDI — Patrullaje Móvil", "freq": "150.775 MHz", "dist": "~1.1 km", "cat": "PDI"},
            {"t": "🔵 ALERTA MÁXIMA — CARABINEROS", "nombre": "Carabineros — Comando y Patrullaje", "freq": "460.125 MHz", "dist": "~800 m", "cat": "CARABINEROS"},
            {"t": "🔵 ALERTA MÁXIMA — CARABINEROS", "nombre": "Carabineros — Radio Móvil", "freq": "150.950 MHz", "dist": "~1.8 km", "cat": "CARABINEROS"},
            {"t": "🚑 BOMBEROS", "nombre": "Bomberos — Red Local de Comando", "freq": "156.050 MHz", "dist": "~1.2 km", "cat": "BOMBEROS"},
            {"t": "🚑 BOMBEROS", "nombre": "Bomberos — Comando Regional", "freq": "154.900 MHz", "dist": "~2.5 km", "cat": "BOMBEROS"},
            {"t": "🚑 SAMU", "nombre": "SAMU — Red de Ambulancias", "freq": "155.700 MHz", "dist": "~2.1 km", "cat": "SAMU"},
            {"t": "🚑 SAMU", "nombre": "SAMU — Base Central", "freq": "155.400 MHz", "dist": "~3.0 km", "cat": "SAMU"},
            {"t": "🚒 RESCATE", "nombre": "Cuerpo de Rescate — Búsqueda y Salvamento", "freq": "156.200 MHz", "dist": "~4.0 km", "cat": "RESCATE"},
            {"t": "🚒 RESCATE", "nombre": "Rescate Aéreo — Helicópteros", "freq": "243.000 MHz", "dist": "~8.0 km", "cat": "RESCATE"},
            {"t": "📡 PÚBLICO", "nombre": "Radio Municipal — Emisora Local", "freq": "107.5 FM", "dist": "~3 km", "cat": "PÚBLICO"},
            {"t": "📱 TORRE", "nombre": "Antena de Telefonía Móvil", "freq": "700 MHz", "dist": "~1.5 km", "cat": "PÚBLICO"},
            {"t": "📶 PRIVADO", "nombre": "Red Wi-Fi Cercana", "freq": "2.4 GHz", "dist": "~60 m", "cat": "PRIVADO"},
            {"t": "🔵 BLUETOOTH", "nombre": "Dispositivo Bluetooth cercano", "freq": "2.4 GHz", "dist": "~8 m", "cat": "PRIVADO"},
        ]
        s = random.choice(señales)
        sid = f"{s['freq']}_{s['t']}"
        if sid not in self.señales_vistas:
            self.señales_vistas.add(sid)
            if "DRON" in s["cat"]:
                self.drones_detectados += 1
                self.lbl_drones.text = f"🚁 Drones detectados: {self.drones_detectados}"
            self.emitir_alerta(s)
            color = self.obtener_color_servicio(s["cat"])
            self.lista.add_widget(TwoLineListItem(
                text=f"[color={color}]{s['t']}[/color] — {s['nombre']}",
                secondary_text=f"📻 Frecuencia: {s['freq']} | 📍 Distancia: {s['dist']} | ⏱️ {time.strftime('%H:%M:%S')}"
            ))

class KaviselDetectaApp(MDApp):
    def build(self):
        self.title = "Kavisel Detecta"
        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"
        return KaviselDetectaScreen()

if __name__ == "__main__":
    KaviselDetectaApp().run()
