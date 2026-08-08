[app]
title = Stick War Ultra
package.name = stickwarultra
package.domain = com.mohamed.stickwarultra
source.dir =.
source.include_exts = py,png,jpg,kv,atlas,json
version = 1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 0
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.ndk = 25b
android.accept_sdk_license_agreement = True

[buildozer]
log_level = 2

# استخدم API رقم 33 أو 34
android.api = 33

# حدد إصدار Build-Tools مستقر بصراحة
android.build_tools_version = 33.0.2

# حدد إصدار NDK مناسب
android.ndk = 25b
