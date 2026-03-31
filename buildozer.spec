[app]
title = Tufan VPN
package.name = tufanvpn
package.domain = org.tufan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المتطلبات الأساسية فقط لضمان النجاح
requirements = python3,kivy==2.3.0,kivymd,requests

orientation = portrait
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# منع التحديثات اليدوية التي تستهلك المساحة
android.skip_update = True
android.accept_sdk_license = True
android.enable_androidx = True

[buildozer]
log_level = 1
warn_on_root = 1
