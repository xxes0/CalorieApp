[app]
title = CalorieCalc
package.name = caloriecalc
package.domain = org.vasil

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,tflite,json,db

version = 1.0.0

requirements = hostpython3==3.11.5,python3==3.11.5,kivy==2.3.1,kivymd==1.2.0,pillow,plyer,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 31
android.minapi = 24
android.archs = arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
