from llama_cpp import Llama
from datetime import datetime

class CamelBackend:
    def __init__(self, model_dir: str):
        self.llm = Llama(model_path=model_dir, chat_format="chatml")

    # GenTXT is a method to generate a basic text response.
    # Query is the input text, and tokens is the maximum number of tokens to generate.
    def gentxt(self, query: str, tokens: int, temp: float, experimental_streaming: bool):
        # time of day
        current = datetime.now()
        current = current.strftime("%B %d")

        # prompt optimized for LlaMA 3
        system = f"""You are a helpful and precise assistant for answering questions. Answer in plaintext, not markdown."""
        prompt = f"""<|begin_of_text|><|start_header_id|>system<|end_header_id|>\nCutting Knowledge Date: December 2023\nToday Date: {current}\n{system}<|eot_id|><|start_header_id|>user<|end_header_id|>\n{query}<|eot_id|><|start_header_id|>assistant<|end_header_id|>"""

        # backend streaming
        if experimental_streaming == True:
            for chunk in self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=temp, stream=True, stop=["<|im_end|>"]):
                token = chunk['choices'][0]['text']
                yield token
        else:
            response = self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=temp, stream=False, stop="<|im_end|>")
            return response['choices'][0]['text']