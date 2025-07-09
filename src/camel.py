from llama_cpp import Llama

class CamelBackend:
    def __init__(self, model_dir: str):
        self.llm = Llama(model_path=model_dir, chat_format="chatml")

    # GenTXT is a method to generate a basic text response.
    # Query is the input text, and tokens is the maximum number of tokens to generate.
    def gentxt(self, query: str, tokens: int, experimental_streaming: bool):
        # prompt optimized for Qwen
        prompt = f"""<|im_start|>system\nYou are a helpful assistant. Act witty and smart but remain efficient.<|im_end|>\n<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant"""

        # backend streaming
        if experimental_streaming == True:
            for chunk in self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=0.2, stream=True, stop=["<|im_end|>"]):
                token = chunk['choices'][0]['text']
                yield token
        else:
            response = self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=0.2, stream=False, stop="<|im_end|>")
            return response['choices'][0]['text']