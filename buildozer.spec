[app]
title = Tufan VPN
package.name = tufanvpn
package.domain = org.tufan
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المكتبات المطلوبة لعمل الـ VPN واستقرار الواجهة
requirements = python3,kivy==2.3.0,kivymd,psutil,requests,urllib3

orientation = portrait

# --- التعديلات الجوهرية هنا لضمان النجاح ---
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# استخدام Gradle حديث لتجنب خطأ ANT المفقود الذي ظهر في سجلاتك
android.gradle_dependencies = 'com.android.tools.build:gradle:7.4.2'

android.accept_sdk_license = True

[buildozer]
log_level = 1
warn_on_root = 1
