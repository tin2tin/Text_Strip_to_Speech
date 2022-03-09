from pathlib import Path
from gtts import gTTS
import os
import time

import bpy
#from bpy import context

accents_domain = ["com.au", "co.uk", "com", "ca", "co.in", "ie",
                  "co.za", "ca", "fr", "com.br", "pt", "com.mx", "es", "com"]
accents_lang = ["en", "en", "en", "en", "en", "en",
                "en", "fr", "fr", "pt", "pt", "es", "es", "es"]
language_lang = [("af"), ("sq"), ("ar"), ("hy"), ("bn"), ("bs"), ("bg"), ("my"), ("ca"), ("zh-CN"), ("zh-TW"), ("hr"), ("cs"), ("da"), ("nl"), ("en"), ("eo"), ("et"), ("tl"), ("fi"), ("fr"), ("de"), ("el"), ("gu"), ("hi"), ("hu"), ("is"), ("id"), ("it"), ("ja"), ("jw"), ("kn"), ("km"), ("ko"), ("la"), ("lv"), ("mk"), ("ms"), ("ml"), ("mr"), ("ne"), ("no"), ("pl"), ("pt"), ("ro"), ("ru"), ("sr"), ("si"), ("sk"), ("es"), ("su"), ("sw"), ("sv"), ("ta"), ("te"), ("th"), ("tr"), ("uk"), ("ur"), ("vi"), ("cy")]


if os.name == 'nt':
    output_dir = r'C:\\tmp\\'
else:
    output_dir = r'/tmp/'


def sound_strip_from_text(tts, start_frame, language_enum, accent_enum, chan):

    top_level_domain = accents_domain[int(accent_enum)]
    # language = accents_lang[int(accent_enum)]
    language = language_lang[int(language_enum)-1]

    if os.name == 'nt':
        output_name = output_dir + '\\' + tts + \
            time.strftime("%Y%m%d-%H%M%S") + ".mp3"
    else:
        output_name = output_dir + '/' + tts + \
            time.strftime("%Y%m%d-%H%M%S") + ".mp3"

    ttmp3 = gTTS(text=tts, lang=language, tld=top_level_domain)
    ttmp3.save(output_name)

    context = bpy.context
    scene = context.scene

    if not scene.sequence_editor:
        scene.sequence_editor_create()
    seq = scene.sequence_editor

    #obj = bpy.ops.sequencer.sound_strip_add(filepath=output_name, frame_start=start_frame)
    obj = seq.sequences.new_sound(
        tts, filepath=output_name, channel=chan, frame_start=start_frame)

    return obj
