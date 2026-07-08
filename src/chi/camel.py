# Copyright (c) 2025-2026 Zane Apatoff and Sourceworks. 
# Licensed under the MIT License.
# See LICENSE file in the project root for full license text.

from llama_cpp import Llama, LlamaGrammar
from datetime import datetime
import psutil

PIPE_GRAMMAR = LlamaGrammar.from_string(r"""
root ::= line+
line ::= ("T|" | "C|") [^\n]* "\n"
""")

class CamelBackend:
    def __init__(self, model_dir: str):
        mem_mb = psutil.virtual_memory().available / (1024 ** 2)
        memstat = mem_mb <= 6144

        self.llm = Llama(
            model_path=model_dir,
            low_mem=memstat,
            low_vram=memstat,
            use_mmap=True,
            n_threads=psutil.cpu_count(logical=False),  # physical cores only — logical/hyperthreaded cores hurt LLM perf
            n_ctx=int(512*(psutil.virtual_memory().available / (1024 **3)))
        )

    def gentxt(self, query: str, tokens: int, temp: float, experimental_streaming: bool, custom: str, use_pipe_grammar: bool = False):
        current = datetime.now().strftime("%B %d")

        if not custom or (isinstance(custom, str) and custom.isspace()):
            system = "Answer in markdown."
        else:
            system = f"{custom} Answer in markdown."

        messages = [
    {
        "role": "system",
        "content": f"Today Date: {current}\n{system}"
    },
    {
        "role": "user",
        "content": query
    }
]

        grammar = PIPE_GRAMMAR if use_pipe_grammar else None

        if experimental_streaming:
            for chunk in self.llm.create_chat_completion(
                messages=messages,
                max_tokens=tokens,
                repeat_penalty=1.28,
                temperature=temp,
                stream=True,
                stop=["<|eot_id|>"],
                grammar=grammar,
            ):
                content = chunk["choices"][0]["delta"].get("content")
                if content:
                    yield content