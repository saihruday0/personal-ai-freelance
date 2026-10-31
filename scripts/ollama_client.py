
import requests

# Ollama configuration
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL_NAME = "qwen3:8b"
TIMEOUT = 180


def ask_qwen(prompt, system_prompt=None):
    payload = {
        "model": MODEL_NAME,
        "messages": [],
        "stream": False,
        "format": "json",
        "options": {
            "temperature": 0.0
        }
    }

    if system_prompt:
        payload["messages"].append({
            "role": "system",
            "content": system_prompt
        })

    payload["messages"].append({
        "role": "user",
        "content": prompt
    })

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        result = response.json()
        answer = result.get("message", {}).get("content", "")

        if not answer:
            raise ValueError("Qwen returned an empty response.")

        return answer

    except requests.exceptions.Timeout:
        raise RuntimeError("Qwen request timed out.")

    except requests.exceptions.ConnectionError:
        raise RuntimeError("Could not connect to Ollama.")

    except requests.exceptions.RequestException as error:
        raise RuntimeError(f"Ollama API error: {error}")


if __name__ == "__main__":

    test_prompt = (
        "Explain what a website HTTP status code 200 means "
        "in two sentences."
    )

    print("Connecting to Qwen3:8B...")
    
    try:
        answer = ask_qwen(test_prompt)

        print("\nQwen Response:")
        print(answer)

    except RuntimeError as error:
        print("\nError:", error)
