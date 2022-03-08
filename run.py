import os

dir = r"/home/magag/text_to_speech/__init__.py"

if os.name == 'nt':
    dir = r"C:\Users\marco\blender-text-to-speech"

exec(compile(open(dir).read(), dir, 'exec'))