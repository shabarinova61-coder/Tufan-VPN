[app]
title = Tufan VPN
package.name = tufanvpn
package.domain = org.tufan

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

version = 1.0

requirements = kivy==2.3.0,kivymd==1.1.1,requests,cython<3.0.0

orientation = portrait
fullscreen = 1

android.api = 33
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a

android.enable_androidx = True
android.accept_sdk_license = True

p4a.bootstrap = sdl2
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
