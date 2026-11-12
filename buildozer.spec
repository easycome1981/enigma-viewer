[app]

# (str) Title of your application
title = Enigma2 Viewer

# (str) Package name
package.name = enigmaviewer

# (str) Package domain (needed for android packaging)
package.domain = org.enigma

# (str) Source files where the let's go
source.dir = .

# (list) Source files to include
source.exts = py,png,jpg,kv,atlas

# (list) Application version
version = 0.1

# (list) Application requirements
requirements = python3,kivy,requests,pillow

# (str) Supported orientations
orientation = landscape

# (list) Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE

# (int) Target Android API
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (list) Android architectures to build for
android.archs = armeabi-v7a

# (bool) Fullscreen
fullscreen = 1

# (int) Log level (2 = detailed debug)
log_level = 2
