# This is a stripped down version of Mark Lagana's Text to Speech add-on.
# This version is only for converting text strips to speech.

from . import ui
from . import operators
import os
import sys
import bpy
import subprocess
import site
bl_info = {
    "name": "Text Strips to Speech",
    "author": "Mark Lagana, tintwotin",
    "version": (0, 1, 0),
    "blender": (3, 00, 0),
    "description": "Turns text strips into speech",
    "location": "Sequence Editor > Select Text Strip > Strip Menu > Convert to Speech",
    "warning": "",
    "tracker_url": "",
    "category": "Sequencer",
}
app_path = site.USER_SITE
if app_path not in sys.path:
    sys.path.append(app_path)
pybin = sys.executable  # bpy.app.binary_path_python # Use for 2.83

try:
    subprocess.call([pybin, "-m", "ensurepip"])
except ImportError:
    pass
try:
    import gtts
except ImportError:
    subprocess.check_call([pybin, "-m", "pip", "install", "gtts"])
try:
    import gtts
except ImportError:
    print("Installation of the Media Info module failed")


def panel_text_to_speech(self, context):
    strip = context.active_sequence_strip
    if strip.type == 'TEXT':
        layout = self.layout
        layout.separator()
        layout.operator('text_to_speech.text_strip', text='Convert to Speech')
        layout.prop_menu_enum(context.scene.text_to_speech,
                              'language_enumerator', text="Language")
        layout.prop_menu_enum(context.scene.text_to_speech,
                              'accent_enumerator', text="Accent")


classes = (
    ui.TextToSpeechSettings,
    operators.StripToSpeechOperator,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.text_to_speech = bpy.props.PointerProperty(
        type=ui.TextToSpeechSettings)
    bpy.types.SEQUENCER_MT_strip.append(panel_text_to_speech)


def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.text_to_speech
    bpy.types.SEQUENCER_MT_strip.remove(panel_text_to_speech)


if __name__ == '__main__':
    register()

