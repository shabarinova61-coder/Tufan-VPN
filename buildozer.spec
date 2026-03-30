[app]
title = Tufan VPN
package.name = tufanvpn
package.domain = org.tufan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

requirements = python3,kivy==2.3.0,kivymd,psutil,requests,urllib3,certifi

orientation = portrait
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25c
android.archs = arm64-v8a, armeabi-v7a

# تفعيل الأفرع الرسمية لضمان وجود مجلد python-for-android
p4a.branch = master
android.enable_androidx = True
android.accept_sdk_license = True
android.gradle_dependencies = 'com.android.tools.build:gradle:7.4.2'

[buildozer]
log_level = 1
warn_on_root = 1
