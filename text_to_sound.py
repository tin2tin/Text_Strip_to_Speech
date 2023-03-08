from pathlib import Path
#from gtts import gTTS
import os
import time
import re
import bpy
#from bpy import context

accents_domain = ["com.au", "co.uk", "ca", "us", "co.in", "ie",
                  "co.za", "ca", "fr", "com.br", "pt", "com.mx", "es", "us"]
accents_lang = ["en", "en", "en", "en", "en", "en",
                "en", "fr", "fr", "pt", "pt", "es", "es", "es"]
language_lang = [("af"), ("sq"), ("ar"), ("hy"), ("bn"), ("bs"), ("bg"), ("my"), ("ca"), ("zh-CN"), ("zh-TW"), ("hr"), ("cs"), ("da"), ("nl"), ("en"), ("eo"), ("et"), ("tl"), ("fi"), ("fr"), ("de"), ("el"), ("gu"), ("hi"), ("hu"), ("is"), ("id"), ("it"), ("ja"), ("jw"), ("kn"), ("km"), ("ko"), ("la"), ("lv"), ("mk"), ("ms"), ("ml"), ("mr"), ("ne"), ("no"), ("pl"), ("pt"), ("ro"), ("ru"), ("sr"), ("si"), ("sk"), ("es"), ("su"), ("sw"), ("sv"), ("ta"), ("te"), ("th"), ("tr"), ("uk"), ("ur"), ("vi"), ("cy")]


if os.name == 'nt':
    output_dir = r'C:\\tmp\\'
else:
    output_dir = r'/tmp/'

def clean_filename(string):
    """
    Sanitize a string to be used as a filename.
    """
    string = string.replace(':', '_').replace('/', '_').replace('\x00', '_')

    string = re.sub('[\n\\\*><?\"|\t]', '', string)
    string = string.strip()
    string = string[:10]

    return string

def sound_strip_from_text(tts, start_frame, language_enum, accent_enum, chan):
    try:
        from gtts import gTTS
    except ModuleNotFoundError:
        import site
        import subprocess
        import sys
        app_path = site.USER_SITE
        if app_path not in sys.path:
            sys.path.append(app_path)
        pybin = sys.executable  # bpy.app.binary_path_python # Use for 2.83

        print("Ensuring: pip")
        try:
            subprocess.call([pybin, "-m", "ensurepip"])
        except ImportError:
            pass
        print("Installing: gTTS module")
        subprocess.check_call([pybin, "-m", "pip", "install", "gtts"])
        try:
            from gtts import gTTS
        except ModuleNotFoundError:
            print("Installation of the gTTS module failed")

    top_level_domain = accents_domain[int(accent_enum)]
    # language = accents_lang[int(accent_enum)]
    language = language_lang[int(language_enum)-1]

    if os.name == 'nt':
        output_name = output_dir + '\\' + clean_filename(tts) + \
            time.strftime("%Y%m%d-%H%M%S") + ".mp3"
    else:
        output_name = output_dir + '/' + clean_filename(tts) + \
            time.strftime("%Y%m%d-%H%M%S") + ".mp3"

    ttmp3 = gTTS(text=tts, lang=language, tld=top_level_domain, slow=False)
    ttmp3.save(output_name)

    context = bpy.context
    scene = context.scene

    if not scene.sequence_editor:
        scene.sequence_editor_create()
    seq = scene.sequence_editor

    obj = seq.sequences.new_sound(
        tts, filepath=output_name, channel=chan, frame_start=int(start_frame))

    return obj
