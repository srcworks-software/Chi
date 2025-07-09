import gi
gi.require_version('Gtk', '4.0')
gi.require_version('Notify', '0.7')
from gi.repository import Gtk, GLib, Gio, Notify
import sys
from camel import CamelBackend as cb

Notify.init("Cyckle")
class gui(Gtk.Application):
    def __init__(self):
        super().__init__(
            application_id="org.sourceworks.app",
            flags=Gio.ApplicationFlags.NON_UNIQUE)
        GLib.set_application_name("Cyckle")
        self.instance = None
        self.val = 768

    def do_startup(self):
        Gtk.Application.do_startup(self)

    def do_activate(self):
        Notify.init("Cyckle")
        def send_notify(title, info):
            message = Notify.Notification.new(title, info, "dialog-information")
            message.set_urgency(Notify.Urgency.NORMAL)

        window = Gtk.ApplicationWindow(application=self)
        window.set_default_size(800, 600)

        # header
        header = Gtk.HeaderBar()
        title_label = Gtk.Label(label="Cyckle")
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
        boxmain = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)

        label = Gtk.Label(label="Welcome to the Camel demo!\n")
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

        def handler(entry):
            text = entry.get_text()
            if text.lower() == "quit":
                sys.exit(0)
            else:
                gen = self.instance.gentxt(text, tokens=self.val, experimental_streaming=True)
                send_notify("Response Status", "Response has been generated.")
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

        entry.connect("activate", handler)

        boxmain.append(scroll)
        boxmain.append(label)
        boxmain.append(entry)

        # settings page
        boxset = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10, margin_top=12, margin_bottom=12, margin_start=12, margin_end=12)

        # token selection
        tseltext = Gtk.Label(label="Generation tokens")
        tselscale = Gtk.Scale.new_with_range(Gtk.Orientation.HORIZONTAL, 1, 2048, 1)
        tselscale.set_value(768) # default
        tselscale.set_hexpand(True)
        tselscale.set_digits(0)

        def tsel_handler(scale):
            self.val = int(scale.get_value())
            tseltext.set_text(f"Generation tokens: {self.val}")

        tselscale.connect("value-changed", tsel_handler)

        # model changer
        mdlfile_label = Gtk.Label(label="Change your model")
        open_mdlfile = Gtk.Button(label="Open file")
        
        def open_mdlfile_handler(button):
            global instance, file_dir
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
                dialog.destroy()
            
            dialog.connect("response", on_resp)
            dialog.show()

        open_mdlfile.connect("clicked", open_mdlfile_handler)

        boxset.append(tseltext)
        boxset.append(tselscale)
        boxset.append(mdlfile_label)
        boxset.append(open_mdlfile)

        # stack pages
        stack.add_titled(child=boxmain, name="chat", title="Chat")
        stack.add_titled(child=boxset, name="settings", title="Settings")

        # stack layout
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        hbox.append(sidebar)
        hbox.append(stack)

        window.set_child(hbox)
        window.present()

app = gui()
exit_status = app.run(sys.argv)
sys.exit(exit_status)