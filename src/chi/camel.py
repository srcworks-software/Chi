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
            chat_format="chatml",
            low_mem=memstat,
            low_vram=memstat,
            use_mmap=True,
            n_threads=psutil.cpu_count(logical=False),  # physical cores only — logical/hyperthreaded cores hurt LLM perf
        )

    def gentxt(self, query: str, tokens: int, temp: float, experimental_streaming: bool, custom: str, md: bool, use_pipe_grammar: bool = False):
        current = datetime.now().strftime("%B %d")

        if md == False:
            if not custom or (isinstance(custom, str) and custom.isspace()):
                system = "You are a helpful and precise assistant for answering questions. Answer in plaintext, not markdown."
            else:
                system = f"{custom} Answer in plaintext, not markdown."
        else:
            if not custom or (isinstance(custom, str) and custom.isspace()):
                system = "You are a helpful and precise assistant for answering questions. Answer in markdown."
            else:
                system = f"{custom} Answer in markdown."
        prompt = (
            f"<|start_header_id|>system<|end_header_id|>\n"
            f"Cutting Knowledge Date: December 2023\nToday Date: {current}\n"
            f"{system}<|eot_id|>"
            f"<|start_header_id|>user<|end_header_id|>\n{query}<|eot_id|>"
            f"<|start_header_id|>assistant<|end_header_id|>"
        )

        grammar = PIPE_GRAMMAR if use_pipe_grammar else None

        if experimental_streaming:
            for chunk in self.llm(
                prompt=prompt,
                max_tokens=tokens,
                repeat_penalty=1.28,
                temperature=temp,
                stream=True,
                stop=["<|eot_id|>"],
                grammar=grammar,
            ):
                yield chunk['choices'][0]['text']
        else:
            response = self.llm(
                prompt=prompt,
                max_tokens=tokens,
                repeat_penalty=1.28,
                temperature=temp,
                stream=False,
                stop=["<|eot_id|>"],
                grammar=grammar,
            )
            return response['choices'][0]['text']