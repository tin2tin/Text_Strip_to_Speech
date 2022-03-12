# This is a stripped down version of Mark Lagana's Text to Speech add-on.
# This version is only for converting text strips to speech.

from . import ui
from . import operators
import os
import sys
import bpy
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

try:
    import gtts

except ImportError:
    print("Installing gtts...")
    import subprocess
    import bpy
    import os
    from pathlib import Path

    if bpy.app.version < (2, 92, 0):
        py_exec = bpy.app.binary_path_python
        subprocess.call([str(py_exec), "-m", "ensurepip", "--user"])
        subprocess.call([str(py_exec), "-m", "pip",
                         "install", "--upgrade", "pip"])
        subprocess.call([str(py_exec), "-m", "pip",
                         "install", "--user", "gtts"])
    else:
        import sys
        py_exec = str(sys.executable)
        lib = os.path.join(Path(py_exec).parent.parent, "lib")
        subprocess.call([py_exec, "-m", "ensurepip", "--user"])
        subprocess.call([py_exec, "-m", "pip", "install", "--upgrade", "pip"])
        subprocess.call([py_exec, "-m", "pip", "install",
                         f"--target={str(lib)}", "gtts"])

        try:
            import gtts
        except PermissionError:
            print("To install, right click the Blender icon and run as Administrator")
        except:
            print("Error installing gtts")


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

