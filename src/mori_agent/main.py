import requests

OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "qwen3:4b"


def chat():
    messages = []

    print("Mori Agent is ready!")
    print("Type 'exit' to quit.\n")

    while True:
        user_input = input("You: ").strip()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        if not user_input:
            continue

        messages.append({
            "role": "user",
            "content": user_input
        })

        try:
            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL,
                    "messages": messages,
                    "stream": False
                },
                timeout=120
            )

            response.raise_for_status()

            result = response.json()
            assistant_message = result["message"]["content"]

            messages.append({
                "role": "assistant",
                "content": assistant_message
            })

            print(f"\nMori: {assistant_message}\n")

        except requests.RequestException as error:
            print(f"\nConnection error: {error}\n")
            messages.pop()


if __name__ == "__main__":
    chat()