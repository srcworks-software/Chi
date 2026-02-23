# Copyright (c) 2025-2026 Zane Apatoff and Sourceworks. 
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.

import gi
gi.require_version('Gtk', '4.0')
from gi.repository import Gtk, GLib, Gio
import sys
from camel import CamelBackend as cb
from configparser import ConfigParser as cfg
import random

class gui(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.sourceworks.app",
            flags=Gio.ApplicationFlags.NON_UNIQUE)
        GLib.set_application_name("Chi")
        
        self.val = 768  # default token count
        self.temp = 0.2
        self.prompt = None 
        self.instance = None

        # ini parser for model
        self.config = cfg()
        self.config.read('config.ini')
        mdl = self.config['settings']['mdl']
        if mdl != "":
            self.instance = cb(model_dir=mdl)
        if mdl == "":
            self.instance = None

        prompt = self.config['settings']['prompt']
        if prompt != "":
            self.prompt = prompt
        else:
            self.prompt = None

        temp = self.config['settings']['temp']
        if temp != "":
            self.temp = float(temp)
        else:
            self.temp = 0.2

        tokens = self.config['settings']['tokens']
        if tokens != "":
            self.val = int(tokens)
        else:
            self.val = 768

        self.prefix = ""  # Stores the quick action prompt template prefix

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        window = Gtk.ApplicationWindow(application=self)
        window.set_default_size(800, 600)

        # header
        header = Gtk.HeaderBar()
        title_label = Gtk.Label(label="Chi")
        header.set_title_widget(title_label)
        header.set_show_title_buttons(True)
        window.set_titlebar(header)

        # icons
        icon = Gtk.Image.new_from_file("assets/icon.svg")
        header.pack_start(icon)

        # stack
        stack = Gtk.Stack()
        stack.set_hexpand(True)
        stack.set_vexpand(True)
        stack.set_transition_type(Gtk.StackTransitionType.SLIDE_LEFT_RIGHT)

        sidebar = Gtk.StackSidebar()
        sidebar.set_stack(stack)
        sidebar.set_vexpand(True)
        sidebar.set_hexpand(False)

        # chat page
        boxmain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10,
                         margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)
        boxmain.add_css_class("card")

        label = Gtk.Label()
        # msg random setup
        msgs = [
            "Ready when you are.",
            "What's on your mind?",
            "Ask away!",
            "What's on the agenda today?"
        ]
        label.set_markup(f'<span font_size="32768"><i>{random.choice(msgs)}</i></span>\n')
        label.set_wrap(True)
        label.set_max_width_chars(50)
        label.set_selectable(True)
        label.set_hexpand(True)
        label.set_vexpand(True)

        scroll = Gtk.ScrolledWindow()
        scroll.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scroll.set_child(label)
        scroll.set_vexpand(True)
        scroll.set_hexpand(True)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter text here")
        entry.set_hexpand(True)

        # quick action box
        qactionbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        qactionbox.set_hexpand(True)
        qactionbox.add_css_class("linked")

        qaction_eli5 = Gtk.Button(label="Explain like I'm 5", hexpand=True)
        qaction_deep = Gtk.Button(label="Explain thoroughly", hexpand=True)
        qaction_effi = Gtk.Button(label="Explain efficiently", hexpand=True)

        qactionbox.append(qaction_eli5)
        qactionbox.append(qaction_deep)
        qactionbox.append(qaction_effi)

        # quick action handlers
        qaction_eli5.connect("clicked", lambda btn: self.set_prefix("Explain this in a simple way suitable for a 5-year-old."))
        qaction_deep.connect("clicked", lambda btn: self.set_prefix("Explain this thoroughly with examples."))
        qaction_effi.connect("clicked", lambda btn: self.set_prefix("Explain this efficiently and concisely."))

        # handle entry activate (pressing Enter)
        def handler(entry):
            text = entry.get_text()
            if text.strip() == "":
                return
            prompt_text = f"{self.prefix} {text}" if self.prefix else text
            if not self.instance:
                label.set_text("Please load a model first in the Settings tab.")
                label.add_css_class("error")
                return
            
            label.remove_css_class("error")

            gen = self.instance.gentxt(prompt_text, tokens=self.val, temp=self.temp, experimental_streaming=True, custom=self.prompt)
            stream_buffer = []

            def stream_gen():
                try:
                    token = next(gen)
                    stream_buffer.append(token)
                    label.set_text("".join(stream_buffer))
                    return True
                except StopIteration:
                    return False

            GLib.idle_add(stream_gen)
            entry.set_text("")
            self.prefix = ""  # reset prefix after sending

        entry.connect("activate", handler)
        boxmain.append(scroll)
        boxmain.append(entry)
        boxmain.append(qactionbox)

        # settings page
        boxset = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10,
                         margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)

        # slider box
        slbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        slbox.set_hexpand(True)
        slbox.add_css_class("linked")
        slbox.add_css_class("card")

        # token selection
        tseltext = Gtk.Label(label=f"Generation tokens: {self.val}")
        tselscale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 2048, 16)
        tselscale.set_value(768)  # default
        tselscale.set_hexpand(True)
        tselscale.set_digits(0)

        def tsel_handler(scale):
            self.val = int(scale.get_value())
            tseltext.set_text(f"Generation tokens: {self.val}")
            self.config.read('config.ini')
            self.config['settings']['tokens'] = str(self.val)
            with open('config.ini', 'w') as f:
                self.config.write(f)

        tselscale.connect("value-changed", tsel_handler)

        # temp selection
        temptext = Gtk.Label(label=f"Generation temperature: {self.temp}")
        tempscale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 0, 2, 0.1)
        tempscale.set_value(0.2)  # default
        tempscale.set_hexpand(True)
        tempscale.set_digits(0)

        def temp_handler(scale):
            self.temp = round(float(scale.get_value()), 1)
            temptext.set_text(f"Generation temperature: {self.temp}")
            self.config.read('config.ini')
            self.config['settings']['temp'] = str(self.temp)
            with open('config.ini', 'w') as f:
                self.config.write(f)

        tempscale.connect("value-changed", temp_handler)

        # model changer box
        mdlbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        mdlbox.set_hexpand(True)
        mdlbox.add_css_class("linked")
        mdlbox.add_css_class("card")        

        # model changer
        mdlfile_label = Gtk.Label(label="Change your model")
        mdlfile_label.set_hexpand(True)
        open_mdlfile = Gtk.Button(label="Open file")
        open_mdlfile.set_hexpand(True)
        open_mdlfile.add_css_class("suggested-action")

        def open_mdlfile_handler(button):
            dialog = Gtk.FileChooserNative.new(
                "Open Model File",
                window,
                Gtk.FileChooserAction.OPEN,
                "_Open",
                "_Cancel"
            )
            file_filter = Gtk.FileFilter()
            file_filter.set_name("GGUF files")
            file_filter.add_pattern("*.gguf")
            dialog.add_filter(file_filter)

            def on_resp(dialog, response):
                if response == Gtk.ResponseType.ACCEPT:
                    file_dir = dialog.get_file().get_path()
                    self.instance = cb(model_dir=file_dir)
                    self.config.read('config.ini')
                    self.config['settings']['mdl'] = file_dir
                    with open('config.ini', 'w') as f:
                        self.config.write(f)
                dialog.destroy()

            dialog.connect("response", on_resp)
            dialog.show()

        open_mdlfile.connect("clicked", open_mdlfile_handler)

        # legal blah blah
        lglext = Gtk.Label(label="Copyright (c) 2025-2026 Sourceworks and Zane Apatoff. Licensed under MIT.")
        lglext.add_css_class("dim-label")

        # prompt box
        pbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        pbox.set_hexpand(True)
        pbox.add_css_class("linked")
        pbox.add_css_class("card")

        # prompt customization
        ptext = Gtk.Label(label="Personality customization (optional)")
        ptext.set_hexpand(True)
        entryp = Gtk.Entry()
        entryp.set_placeholder_text("Enter customization here")
        entryp.set_hexpand(True)

        def custom_handler(entryp):
            self.prompt = entryp.get_text().strip()
            self.config.read('config.ini')
            self.config['settings']['prompt'] = self.prompt
            with open('config.ini', 'w') as f:
                self.config.write(f)
        
        # delete box
        delbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        delbox.set_hexpand(True)
        delbox.add_css_class("linked")
        delbox.add_css_class("card")

        # delete all configs
        delcfgtxt = Gtk.Label(label="Reset all settings to default")
        delcfgtxt.set_hexpand(True)
        delcfg = Gtk.Button(label="Reset")
        delcfg.set_hexpand(True)
        delcfg.add_css_class("destructive-action")

        def del_handler(button):
            self.config['settings']['mdl'] = ""
            self.config['settings']['prompt'] = ""
            self.config['settings']['temp'] = "0.2"
            self.config['settings']['tokens'] = "768"
            with open('config.ini', 'w') as f:
                self.config.write(f)
            self.instance = None
            self.prompt = None
            self.temp = 0.2
            self.val = 768
            entryp.set_text("")
            tselscale.set_value(768)
            tempscale.set_value(0.2)

        delcfg.connect("clicked", del_handler)
        entryp.connect("activate", custom_handler)
        slbox.append(tseltext)
        slbox.append(tselscale)
        slbox.append(temptext)
        slbox.append(tempscale)
        mdlbox.append(mdlfile_label)
        mdlbox.append(open_mdlfile)
        pbox.append(ptext)
        pbox.append(entryp)
        delbox.append(delcfgtxt)
        delbox.append(delcfg)
        boxset.append(slbox)
        boxset.append(mdlbox)
        boxset.append(pbox)
        boxset.append(delbox)
        boxset.append(lglext)

        # stack pages
        stack.add_titled(child=boxmain, name="chat", title="Chat")
        stack.add_titled(child=boxset, name="settings", title="Settings")

        # stack layout
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.append(sidebar)
        hbox.append(stack)

        window.set_child(hbox)
        window.present()

    def set_prefix(self, new_prefix):
        self.prefix = new_prefix
        print(f"Quick action prefix set: {self.prefix}")

def main():
    app = gui()
    exit_status = app.run(sys.argv)
    sys.exit(exit_status)

if __name__ == "__main__":
    main()