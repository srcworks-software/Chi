# Copyright (c) 2025-2026 Zane Apatoff and Sourceworks. 
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.

from llama_cpp import Llama
from datetime import datetime
import psutil

class CamelBackend:
    def __init__(self, model_dir: str):
        if psutil.virtual_memory().available / (1024 ** 2) <= 6144:
            memstat = True
        else:
            memstat = False

        self.llm = Llama(model_path=model_dir, chat_format="chatml", low_mem=memstat, low_vram=memstat, use_mmap=True, thread_count=psutil.cpu_count(logical=True))

    # GenTXT is a method to generate a basic text response.
    # Query is the input text, and tokens is the maximum number of tokens to generate.
    def gentxt(self, query: str, tokens: int, temp: float, experimental_streaming: bool, custom: str):
        # time of day
        current = datetime.now()
        current = current.strftime("%B %d")

        # prompt optimized for LlaMA 3
        if custom == None or custom == "" or custom == " ":
            system = f"""You are a helpful and precise assistant for answering questions. Answer in plaintext, not markdown."""
        else:
            system = f"""{custom} Answer in plaintext, not markdown."""
        prompt = f"""<|start_header_id|>system<|end_header_id|>\nCutting Knowledge Date: December 2023\nToday Date: {current}\n{system}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        # backend streaming
        if experimental_streaming == True:
            for chunk in self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=temp, stream=True, stop=["<|im_end|>"]):
                token = chunk['choices'][0]['text']
                yield token
        else:
            response = self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=temp, stream=False, stop=["<|im_end|>"])
            return response['choices'][0]['text']