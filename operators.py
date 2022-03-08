import os
import sys
from pathlib import Path
from datetime import date, datetime, timedelta
import importlib

import bpy
from bpy.types import Operator
from bpy_extras.io_utils import ImportHelper

from . import text_to_sound as tts
importlib.reload(tts)

global global_captions
global_captions = []

if os.name == 'nt':
    output_dir = r'C:\\tmp\\'
else:
    output_dir = r'/tmp/'


def refresh_strip_times():
    global global_captions

    for caption in global_captions:
        caption.update_timecode()

    global_captions.sort(
        key=lambda caption: caption.current_seconds, reverse=False)


def ensure_two_chars(number):

    string = str(number)

    if len(string) == 1:
        return '0' + string
    elif len(string) > 3:
        return string[0:3]
    else:
        return string


class Time():

    def __init__(self, hours=0, minutes=0, seconds=0, milliseconds=0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        self.milliseconds = milliseconds

    def time_to_frame(self):
        if self.hours == -1:
            return self.hours
        else:
            total_seconds = self.hours * 3600 + self.minutes * \
                60 + self.seconds + self.milliseconds/1000
        return total_seconds * bpy.context.scene.render.fps

    def frame_to_time(self, frames):
        td = timedelta(seconds=(frames / bpy.context.scene.render.fps))
        if (td.seconds/3600 >= 1):
            self.hours = int(td.seconds/3600)
        else:
            self.hours = 0
        if (td.seconds/60 >= 1):
            self.minutes = int(td.seconds/60)
        else:
            self.minutes = 0
        if (td.seconds >= 1):
            self.seconds = int(td.seconds)
        else:
            self.seconds = 0
        self.milliseconds = int(td.microseconds * 1000)
        return


class Caption():

    def __init__(self, cc_type, name, text, start_time, end_time, accent):
        self.rearrange = False
        self.cc_type = cc_type  # 0 : default, 1 : person, 2 : event
        self.accent = accent
        self.name = name
        self.text = text
        self.start_time = start_time
        self.end_time = end_time
        self.frame_start = start_time.time_to_frame()

        if self.frame_start != -1:
            self.sound_strip = tts.sound_strip_from_text(
                text, self.frame_start, self.accent)
        else:
            self.sound_strip = tts.sound_strip_from_text(text, 0, self.accent)

    def update_timecode(self):
        self.start_time.frame_to_time(self.sound_strip.frame_start)
        self.end_time.frame_to_time(self.sound_strip.frame_final_end)
        self.current_seconds = self.sound_strip.frame_start / bpy.context.scene.render.fps


class StripToSpeechOperator(bpy.types.Operator):
    """Convert selected text strips to speech"""
    bl_idname = 'text_to_speech.text_strip'
    bl_label = 'Convert Text Strips to Speech'
    bl_options = {'INTERNAL'}
    bl_description = "Turns selected text strips into audio strips"

    @classmethod
    def poll(cls, context):
        return context.scene and context.scene.sequence_editor

    def execute(self, context):
        global global_captions
        strips = context.selected_sequences
        for strip in strips:
            if strip.type == 'TEXT':
                if strip.text:
                    global_captions.append(
                        Caption(0, '', strip.text,
                                Time(
                                    0, 0, strip.frame_start / bpy.context.scene.render.fps, 0), Time(-1, -1, -1, -1),
                                context.scene.text_to_speech.accent_enumerator))

        self.report({'INFO'}, "FINISHED")
        return {'FINISHED'}
