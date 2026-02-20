# Chi

![GitHub Repo stars](https://img.shields.io/github/stars/srcworks-software/Chi?style=for-the-badge)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/srcworks-software/Chi?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/srcworks-software/Chi?style=for-the-badge)

# Install

> For key details, please refer to ```CONTRIBUTING.md```.

To install Chi, simply paste in this command:

```bash
git clone https://github.com/srcworks-software/Chi.git
cd chi/src
pip install requirements.txt
```

Then, run it using

```bash
python3 app.py
```

## Dependencies

To install required dependencies on Debian, paste in the following command:

```bash
sudo apt update && sudo apt install python3-full
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