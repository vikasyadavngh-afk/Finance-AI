[app]
title = Finance AI
package.name = financeai
package.domain = com.vikas.financeai
source.dir = .
source.include_exts = py,json,md
version = 0.1.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[app:android]
android.permissions =
android.api = 33
android.minapi = 23
android.archs = arm64-v8a, armeabi-v7a
