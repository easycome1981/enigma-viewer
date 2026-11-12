[app]

title = Enigma2 Viewer
package.name = enigmaviewer
package.domain = org.enigma

source.dir = .
source.exts = py,png,jpg,kv,atlas

version = 0.1

requirements = python3,kivy,requests,pillow

orientation = landscape
fullscreen = 1

android.permissions = INTERNET,ACCESS_NETWORK_STATE

android.api = 33
android.minapi = 24
android.ndk = 25b
android.archs = armeabi-v7a

log_level = 2
