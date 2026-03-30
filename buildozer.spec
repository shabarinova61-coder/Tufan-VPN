[app]
# اسم التطبيق الظاهر على الموبايل
title = Tufan VPN
# اسم الحزمة (يجب أن يكون فريداً)
package.name = tufanvpn
package.domain = org.tufan
# مكان ملف main.py
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# المكتبات المطلوبة (بايثون + كيفي)
requirements = python3,kivy,kivymd,psutil

# إعدادات الأندرويد (تم ضبطها للتوافق مع سيرفر GitHub)
orientation = portrait
android.api = 31
android.minapi = 21
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a

# السماح للروبوت بالموافقة على رخص جوجل تلقائياً
android.accept_sdk_license = True

# أيقونة التطبيق (إذا كان لديك ملف png باسم icon)
# icon.filename = %(source.dir)s/icon.png

[buildozer]
log_level = 2
warn_on_root = 1



