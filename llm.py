from typing import Literal

class LLM:
    def __init__(self, provider: Literal["ollama"] = "ollama"):
        if provider == "ollama":
            from langchain_ollama import ChatOllama

            self.model = ChatOllama(
                model="gemma3:12b",
                temperature=0.2,
                validate_model_on_init=True,
            )
        # elif provider == "openai":
        #     try:
        #         from langchain_openai import ChatOpenAI
        #     except ImportError:
        #         raise ImportError(
        #             "langchain_openai is not installed. Please install it with 'uv add '"
        #         )
        #     self.model = ChatOpenAI(
        #         model_name="gpt-4",
        #         temperature=0.2,
        #     )
        else:
            raise ValueError(f"Unsupported LLM provider: {provider}")

    def explain_gpu(self):
        structured_llm = self.model.with_structured_output(
            {
                "type": "object",
                "properties": {
                    "content": {
                        "type": "string",
                        "description": "A concise explanation of how a GPU works.",
                    },
                    "topic": {
                        "type": "string",
                        "description": "The main topic of the explanation.",
                    },
                },
                "required": ["content", "topic"],
            }
        )

        response = structured_llm.invoke("Explain how a GPU works in one sentence.")
        return response


# Initialize the model
# You don't need to provide a URL if Ollama is running on the same machine
llm = ChatOllama(
    model="gemma3:12b",
    temperature=0.2,
    validate_model_on_init=True,
)

structured_llm = llm.with_structured_output(
    {
        "type": "object",
        "properties": {
            "content": {
                "type": "string",
                "description": "A concise explanation of how a GPU works.",
            },
            "topic": {
                "type": "string",
                "description": "The main topic of the explanation.",
            },
        },
        "required": ["content", "topic"],
    }
)

# Invoke the model
response = structured_llm.invoke("Explain how a GPU works in one sentence.")

print(response)
