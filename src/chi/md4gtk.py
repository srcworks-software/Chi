# Copyright (c) 2025-2026 Zane Apatoff and Sourceworks. 
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.

import re
from html import escape

class MarkdownToPango:
    def __init__(self, markdown_text):
        self.markdown_text = markdown_text
        self._code_blocks = []

    def convert(self):
        text = escape(self.markdown_text)

        # I do not understand how regex works.
        text = re.sub(r"```(\w*)\n(.*?)```", self._stash_code, text, flags=re.DOTALL)

        # Headers
        text = re.sub(r"^### (.*)$", r'<span size="large"><b>\1</b></span>', text, flags=re.MULTILINE)
        text = re.sub(r"^## (.*)$", r'<span size="x-large"><b>\1</b></span>', text, flags=re.MULTILINE)
        text = re.sub(r"^# (.*)$", r'<span size="xx-large"><b>\1</b></span>', text, flags=re.MULTILINE)

        # Bold
        text = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", text)
        text = re.sub(r"__(.+?)__", r"<b>\1</b>", text)

        # Italic 
        text = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<i>\1</i>", text)
        text = re.sub(r"(?<!_)_(?!_)(.+?)(?<!_)_(?!_)", r"<i>\1</i>", text)

        # Inline code
        text = re.sub(r"`(.+?)`", r'<span font_family="monospace" background="#2d2d2d">\1</span>', text)

        # Strikethrough
        text = re.sub(r"~~(.+?)~~", r"<s>\1</s>", text)

        # Vestigial, might be useful (coding, might add)
        for i, code in enumerate(self._code_blocks):
            block_markup = f'<span font_family="monospace" background="#1e1e1e" foreground="#dcdcdc">{code}</span>'
            text = text.replace(f"\x00CODEBLOCK{i}\x00", block_markup)

        return text

    def _stash_code(self, match):
        self._code_blocks.append(match.group(2))
        return f"\x00CODEBLOCK{len(self._code_blocks)-1}\x00"