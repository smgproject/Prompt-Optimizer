import requests
import json
import time

# Ollama API URL
OLLAMA_URL = "http://localhost:11434"
MODEL_NAME = "deepseek-r1:1.5b"  # Use the installed DeepSeek model

# Tone options for prompt optimization
TONE_CHOICES = {
    "academic": "Optimize the following prompt in a formal, academic tone suitable for scholarly work. Only improve the wording, making it more professional and scholarly. DO NOT answer or provide any additional explanation. Only return the optimized prompt.",
    "casual": "Optimize the following prompt in a casual and friendly tone. Make it more conversational and approachable. DO NOT answer or provide any additional explanation. Only return the optimized prompt.",
    "professional": "Optimize the following prompt in a professional business-like tone. Make the wording more formal and clear for corporate environments. DO NOT answer or provide any additional explanation. Only return the optimized prompt.",
    "creative": "Optimize the following prompt in a highly creative and artistic tone. Make it imaginative, expressive, and inspiring. DO NOT answer or provide any additional explanation. Only return the optimized prompt.",
    "technical": "Optimize the following prompt in a technical tone, full of precise language and jargon. It should be suitable for experts in the field, focusing on clarity and accuracy. DO NOT answer or provide any additional explanation. Only return the optimized prompt."
}

def check_connection():
    """Check if Ollama is running and list available models."""
    try:
        response = requests.get(f"{OLLAMA_URL}/api/tags")
        if response.status_code == 200:
            models = response.json().get("models", [])
            print("✅ Connected to Ollama successfully!")
            print("Available Models:", [model["name"] for model in models])

            if MODEL_NAME not in [m["name"] for m in models]:
                print(f"❌ Model '{MODEL_NAME}' not found. Make sure it's installed.")
                return False
            return True
        else:
            print("❌ Failed to connect:", response.text)
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Ollama server is not running. Start it with 'ollama serve'.")
        return False

def optimize_prompt(prompt, tone):
    """Optimize a given prompt based on selected tone, ensuring it only returns the optimized prompt."""
    tone_instruction = TONE_CHOICES.get(tone, "")
    optimization_prompt = (
        f"{tone_instruction}\n\n"
        f"Original Prompt: {prompt}\n\nOptimized Prompt:"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": optimization_prompt,
        "stream": False  # Set to True for streaming responses
    }
    headers = {"Content-Type": "application/json"}

    start_time = time.time()  # Start timing

    try:
        response = requests.post(f"{OLLAMA_URL}/api/generate", data=json.dumps(payload), headers=headers)
        end_time = time.time()  # End timing

        if response.status_code == 200:
            elapsed_time = round(end_time - start_time, 2)
            # Extract and clean up the output
            output_text = response.json().get("response", "").strip()
            # Ensure it only returns the optimized part, without extra explanations
            optimized_prompt = output_text.split("\n\nOptimized Prompt:")[-1].strip()
            return f"⏳ Optimization Time: {elapsed_time} sec\n\nOptimized Prompt:\n{optimized_prompt}"
        else:
            return f"❌ Error: {response.text}"
    except requests.exceptions.ConnectionError:
        return "❌ Ollama server is not running. Start it with 'ollama serve'."

if __name__ == "__main__":
    if check_connection():
        # User input for prompt and tone choice
        user_prompt = input("Enter a prompt to optimize: ")
        print("\nSelect the tone for optimization:")
        for key in TONE_CHOICES:
            print(f"- {key.capitalize()}: {TONE_CHOICES[key]}")
        
        user_tone = input("\nEnter your choice (academic/casual/professional/creative/technical): ").lower()

        if user_tone not in TONE_CHOICES:
            print("❌ Invalid tone choice. Please choose from academic, casual, professional, creative, or technical.")
        else:
            print("\n🤖 Optimizing your prompt...\n")
            optimized_output = optimize_prompt(user_prompt, user_tone)
            # Output only the optimized prompt without any thinking or explanation
            print("\nOptimized Prompt:\n", optimized_output)
