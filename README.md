# Chi

![GitHub Repo stars](https://img.shields.io/github/stars/srcworks-software/Chi?style=for-the-badge)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/srcworks-software/Chi?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/srcworks-software/Chi?style=for-the-badge)
[![PyPI status](https://img.shields.io/pypi/status/ansicolortags.svg?style=for-the-badge)](https://pypi.python.org/project/chi-ai/)

#  Install

## 1. Install system dependencies

Chi uses GTK4 for its interface. These cannot be installed via pip and must come from your system package manager.

**Debian / Ubuntu**
```bash
sudo apt install python3-gi python3-gi-cairo gir1.2-gtk-4.0 libgtk-4-1
```

**Fedora**
```bash
sudo dnf install python3-gobject gtk4
```

**Arch**
```bash
sudo pacman -S python-gobject gtk4
```

## 2. Install Chi

It is recommended to use `pipx` to install Chi, as it keeps Chi and its dependencies isolated from your system Python.

```bash
pipx install chi-ai
```

Don't have pipx? Install it first:
```bash
pip install pipx
```

Or if you'd prefer plain pip:
```bash
pip install chi-ai
```

## 3. Run

```bash
chi-ai
```

# Features

This section describes (and shows how to use) all features in Chi.

## Model selection

Model selection is important, as Chi will require a specificed model to use in order to continue. Once selected, it will be saved in ```config.ini``` and you will not need to redo this process unless you are switching models.

In the settings menu of Chi, click "Open file", located underneath the text that says "Change your model. Upon clicking, a file dialog will appear, allowing you to look through your computer for a model to use. Note that it must be a ```.gguf``` model, optimized for LlaMA 3 style prompts.

After selecting a model, you will be able to use Chi in the "Chat" menu.

## Generation parameters

In the settings menu of Chi, you will notice two sliders. One controls generation tokens, and the other controls generation temperature. The following is a quick description of these parameters.

- **Tokens** are the maximum length of a response. The higher the number, the longer the response.
- **Temperature** is the 'creativity' of the model. A lower number means more logical, basic responses, while a higher number means higher creativity, at the sacrifice of some logic.

## Quick action buttons

In the chat section of Chi, you may notice three buttons. These buttons append a message at the end of an input, and can alter responses in more favorable ways. The translations to the prompt for each button is provided in the following.

- **Explain like I'm 5** -> Explain this in a way suitable for a 5 year-old.
- **Explain thoroughly** -> Explain this thoroughly with examples.
- **Explain efficiently** -> Explain this efficiently and concisely.

## Personality customization

In the settings section of Chi, there is an entry box to change the personality. You can write instructions and press enter to save them and apply them to the model. Your customizations are saved in ```config.ini``` so there is no worry regarding loss of settings.

# Want to contribute?

Read ```CONTRIBUTING.md``` for information regarding contribution. Any issues can go into the 'issues' section of the repository. 

# License

This project is licensed under the MIT License. See the ```LICENSE``` file for details.
