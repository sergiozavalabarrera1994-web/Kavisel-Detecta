[app]
title = KaviselDetecta
package.name = kaviseldetecta
package.domain = org.kavisel
source.dir = .
source.include_exts = py,png,jpg
version = 1.0.0
orientation = portrait
icon.filename = kavisel_icon.png
author = Sergio Zavala Barrera
homepage = 
description = Detección de radiofrecuencias — alertas de proximidad y seguridad

# REQUISITOS COMPATIBLES
requirements = python3,kivy==2.2.1

# ============== ANDROID ==============
android.permissions = INTERNET, ACCESS_FINE_LOCATION, ACCESS_COARSE_LOCATION, RECORD_AUDIO, BLUETOOTH, BLUETOOTH_ADMIN
android.api = 33
android.ndk = 25b
android.sdk = 24
android.arch = arm64-v8a
android.buildtools = 33.0.0
android.accepts_license = True
android.minapi = 21

# ============== iOS / APPLE ==============
ios.platform = ios
ios.arch = arm64
ios.minimum_version = 15.0
ios.xcode_version = 15.0

# GENERAL
log_level = 2
warn_on_root = 0
android.allow_backup = True
android.use_aapt2 = True
