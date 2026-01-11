from langchain_ollama import ChatOllama

# Initialize the model
# You don't need to provide a URL if Ollama is running on the same machine
llm = ChatOllama(
    model="gemma3:12b",
    temperature=0.2,
)

# Invoke the model
response = llm.invoke("Explain how a GPU works in one sentence.")

print(response.content)