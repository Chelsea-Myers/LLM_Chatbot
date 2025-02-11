from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load the pre-trained DialoGPT model and tokenizer
model_name = "microsoft/DialoGPT-medium"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Initialize the chat history
chat_history_ids = None

# Define the function to generate responses with sampling techniques and conversation history
def generate_response(input_text, chat_history_ids):
    # Tokenize the input text
    new_input_ids = tokenizer.encode(input_text + tokenizer.eos_token, return_tensors="pt")
    
    # Append the new user input tokens to the chat history
    if chat_history_ids is not None:
        bot_input_ids = torch.cat([chat_history_ids, new_input_ids], dim=-1)
    else:
        bot_input_ids = new_input_ids

    # Create attention mask
    attention_mask = torch.ones(bot_input_ids.shape, dtype=torch.long)

    # Generate a response with sampling
    with torch.no_grad():
        chat_history_ids = model.generate(
            bot_input_ids,
            attention_mask=attention_mask,
            max_length=1000, 
            pad_token_id=tokenizer.eos_token_id,
            do_sample=True,   
            temperature=0.7,  
            top_k=50,         
            top_p=0.95        
        )

    # Decode the generated response
    response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
    return response, chat_history_ids

# Create the chat funtion
def chat():
    print("Start chatting with the bot (type 'exit' to stop)!")
    chat_history_ids = None
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        response, chat_history_ids = generate_response(user_input, chat_history_ids)
        print(f"Bot: {response}")

if __name__ == "__main__":
    chat()



