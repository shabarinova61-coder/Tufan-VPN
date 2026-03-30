[app]
title = Tufan VPN
package.name = tufanvpn
package.domain = org.tufan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# تم إضافة requests و urllib3 لدعم اتصال الـ VPN
requirements = python3,kivy==2.3.0,kivymd,psutil,requests,urllib3

orientation = portrait
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
