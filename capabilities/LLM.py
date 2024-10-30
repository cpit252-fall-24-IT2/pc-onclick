import sys
from groq import Groq

def send_message(groq_client, conversation_history, model):
    try:
        completion = groq_client.chat.completions.create(
            messages=conversation_history,
            model=model,
            max_tokens=1024
        )
        response = completion.choices[0].message.content
        return response
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == '__main__':
    groq_client = Groq(api_key="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")
    conversation_history = [
        {"role": "system", "content": "You are a helpful assistant with a cool and witty personality."},
        {"role": "user", "content": ""}
    ]
    model = "llama-3.2-90b-text-preview"
    
    response = send_message(groq_client, conversation_history, model)
    print("Response from LLM:", response)