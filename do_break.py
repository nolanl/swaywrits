# SPDX-License-Identifier: GPL-2.0-only

import gi

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GLib

BUTTON_TEXT = "Time left in break: %s"

class BreakWindow(Gtk.Window):
    def __init__(self, duration):
        Gtk.Window.__init__(self, title="Swaywrits Breaktime")
        self.duration = duration

        self.time_left = self.duration
        self.focused = True

        self.set_border_width(8)
        self.set_resizable(False)
        self.set_default_size(640, 480)
        self.set_keep_above(True)

        self.connect("focus-in-event", self.on_focus_in)
        self.connect("focus-out-event", self.on_focus_out)
        GLib.timeout_add_seconds(1, self.tick)

        self.button = Gtk.Button(label=BUTTON_TEXT % self.time_left)
        self.button.connect("clicked", self.on_button_clicked)
        self.add(self.button)

    def on_focus_in(self, widget, event):
        if self.time_left > 0:
            self.button.get_style_context().remove_class("destructive-action")
            self.button.get_style_context().add_class("suggested-action")

            self.focused = True

    def on_focus_out(self, widget, event):
        if self.time_left > 0:
            self.button.get_style_context().remove_class("suggested-action")
            self.button.get_style_context().add_class("destructive-action")

            self.time_left = self.duration
            self.button.set_label(BUTTON_TEXT % self.time_left)
            self.focused = False

    def tick(self):
        if self.focused:
            self.time_left -= 1
            self.button.set_label(BUTTON_TEXT % self.time_left)
            if self.time_left == 0:
                self.button.get_style_context().remove_class("suggested-action")
                return False
        return True

    def on_button_clicked(self, widget):
        if self.time_left == 0:
            self.destroy()
            Gtk.main_quit()

def do_break(duration, force_break):
    while True:
        win = BreakWindow(duration)
        win.connect("destroy", Gtk.main_quit)
        win.show_all()
        Gtk.main()
        if not force_break or win.time_left <= 0:
            break

if __name__ == "__main__":
    do_break(10)
