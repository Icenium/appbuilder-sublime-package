import sublime_plugin
from .event import Event

on_sublime_view_loaded = Event()

class SublimeEventsListener(sublime_plugin.EventListener):
    def on_load(self, view):
        global on_sublime_view_loaded
        on_sublime_view_loaded(view)