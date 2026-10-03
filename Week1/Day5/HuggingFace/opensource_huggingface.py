from transformers import AutoTokenizer, AutoModelForCausalLM


MODEL_PATH = "./models/qwen-0.5b"

print("Loading model...")

# Load tokenizer
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

# Load model
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    dtype="auto"
)

print("Model loaded successfully!")
print("Type 'exit' to quit.\n")


while True:

    question = input("You: ")

    if question.lower() == "exit":
        print("Goodbye!")
        break

    messages = [
        {
            "role": "user",
            "content": question
        }
    ]

    # Convert chat message to tokens
    inputs = tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_tensors="pt"
    )

    # Generate response
    outputs = model.generate(
        inputs["input_ids"],
        max_new_tokens=150
    )

    # Remove the original question from the output
    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True
    )

    print("\nAI:", response)
    print()