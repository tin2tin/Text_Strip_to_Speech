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

if os.name == 'nt':
    output_dir = r'C:\\tmp\\'
else:
    output_dir = r'/tmp/'


def sound_strip_from_text(tts, start_frame, accent_enum):

    top_level_domain = accents_domain[int(accent_enum)]
    language = accents_lang[int(accent_enum)]

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

    sequences = bpy.context.sequences
    if not sequences:
        addSceneChannel = 1
    else:
        channels = [s.channel for s in sequences]
        channels = sorted(list(set(channels)))
        empty_channel = channels[-1] + 1
        addSceneChannel = empty_channel

    #obj = bpy.ops.sequencer.sound_strip_add(filepath=output_name, frame_start=start_frame)
    obj = seq.sequences.new_sound(
        tts, filepath=output_name, channel=addSceneChannel, frame_start=start_frame)

    return obj
