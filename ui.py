import bpy


class TextToSpeechSettings(bpy.types.PropertyGroup):

    #    pitch : bpy.props.FloatProperty(
    #        name="Pitch",
    #        description="Control pitch",
    #        default=1.0,
    #        min=0.1,
    #        max=10.0)

    accent_enumerator: bpy.props.EnumProperty(
        name="",
        description="Accent options for speakers",
        items=[('0', "Australia", ""),
               ('1', "United Kingdom", ""),
               ('2', "Canada", ""),
               ('3', "India", ""),
               ('4', "Ireland", ""),
               ('5', "South Africa", ""),
               ('6', "French Canada", ""),
               ('7', "France", ""),
               ('8', "Brazil", ""),
               ('9', "Portugal", ""),
               ('10', "Mexico", ""),
               ('11', "Spain", ""),
               ('12', "Spain (US)", "")])
