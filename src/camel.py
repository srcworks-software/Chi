from llama_cpp import Llama

class CamelBackend:
    def __init__(self, model_dir: str):
        self.llm = Llama(model_path=model_dir, chat_format="chatml")

    # GenTXT is a method to generate a basic text response.
    # Query is the input text, and tokens is the maximum number of tokens to generate.
    def gentxt(self, query: str, tokens: int, temp: float, experimental_streaming: bool):
        # prompt optimized for Qwen
        prompt = f"""<|im_start|>system\nYou are a clever, witty assistant who responds like a human in casual conversation. Avoid reminding the user that you’re an AI unless they specifically ask. Mirror the user's tone and keep responses efficient. Do not use markdown in your responses. Instead, use plaintext.<|im_end|>\n<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant"""

        # backend streaming
        if experimental_streaming == True:
            for chunk in self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=temp, stream=True, stop=["<|im_end|>"]):
                token = chunk['choices'][0]['text']
                yield token
        else:
            response = self.llm(prompt=prompt, max_tokens=tokens, repeat_penalty=1.28, temperature=temp, stream=False, stop="<|im_end|>")
            return response['choices'][0]['text']