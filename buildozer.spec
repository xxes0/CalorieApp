[app]
title = CalorieCalc
package.name = caloriecalc
package.domain = org.vasil

source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,atlas,tflite,json,db

version = 1.0.0

requirements = python3,kivy==2.3.1,kivymd==1.2.0,pillow,numpy,plyer,pyjnius

orientation = portrait
fullscreen = 0

android.permissions = CAMERA,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
