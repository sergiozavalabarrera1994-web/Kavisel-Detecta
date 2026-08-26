[app]
title = Kavisel Detecta
package.name = kaviseldetecta
package.domain = org.kavisel
source.dir = .
version = 1.4
icon.filename = %(source.dir)s/icon.png

requirements = python3, kivy==2.3.0, kivymd==1.2.0, plyer==2.1.0

android.api = 33
android.ndk = 25b
android.sdk = 24
android.arch = arm64-v8a
android.minapi = 21
android.permissions = ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, INTERNET, ACCESS_WIFI_STATE, POST_NOTIFICATIONS, VIBRATE, WAKE_LOCK

orientation = portrait
fullscreen = 0
