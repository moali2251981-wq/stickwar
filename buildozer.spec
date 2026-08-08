[app]

title = Stick War Ultra
package.name = stickwarultra
package.domain = com.mohamed.stickwarultra
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy
orientation = landscape
fullscreen = 0
android.permissions = INTERNET

# الأسطر المهمة للحل:
android.api = 33
android.minapi = 21
android.build_tools_version = 33.0.2
android.ndk = 25b
android.accept_sdk_license_agreement = True

[buildozer]
log_level = 2
warn_on_root = 1
