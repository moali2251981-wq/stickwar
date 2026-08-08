[app]

# (str) Title of your application
title = Stick War Ultra

# (str) Package name
package.name = stickwarultra

# (str) Package domain (needed for android/ios packaging)
package.domain = com.mohamed.stickwarultra

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include
source.include_exts = py,png,jpg,kv,atlas

# (str) Application versioning
version = 1.0

# (list) Application requirements
requirements = python3,kivy

# (str) Supported orientation (landscape, portrait or all)
orientation = landscape

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET

# (int) Target Android API
android.api = 33

# (int) Minimum API required
android.minapi = 21

# (str) Android build tools version
android.build_tools_version = 33.0.2

# (str) Android NDK version
android.ndk = 25b

# (bool) Accept SDK license agreement
android.accept_sdk_license_agreement = True


[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# (int) Display warning if buildozer is run as root
warn_on_root = 1
