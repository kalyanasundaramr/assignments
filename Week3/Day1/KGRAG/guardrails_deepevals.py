import os
from dotenv import load_dotenv
from nemoguardrails import RailsConfig, LLMRails
from deepeval.test_case import LLMTestCase
from deepeval.metrics import AnswerRelevancyMetric

# Load environment variables from .env file
load_dotenv()

# Verify key is present
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in .env file.")

def run_guarded_pipeline():
    # Step 1: Define NeMo Guardrails configuration
    yaml_config = """
    models:
      - type: main
        engine: openai
        model: gpt-4o-mini
    """
    
    colang_config = """
    define user express greeting
        "hello"
        "hi"

    define bot express greeting
        "Hello! How can I securely assist you today?"

    define flow greeting
        user express greeting
        bot express greeting
    """

    # Initialize NeMo Guardrails
    config = RailsConfig.from_content(
        yaml_content=yaml_config,
        colang_content=colang_config
    )
    rails = LLMRails(config)

    # Step 2: Pass user input through the guardrails pipeline
    user_query = "Hello, can you help me write a secure web scraper?"
    print(f"User Input: {user_query}")

    response = rails.generate(messages=[{"role": "user", "content": user_query}])
    guarded_output = response["content"]
    print(f"Guarded LLM Output: {guarded_output}\n")

    # Step 3: Run DeepEval evaluation
    test_case = LLMTestCase(
        input=user_query,
        actual_output=guarded_output
    )

    metric = AnswerRelevancyMetric(threshold=0.7)
    metric.measure(test_case)

    print("--- DeepEval Results ---")
    print(f"Relevancy Score: {metric.score}")
    print(f"Evaluation Reason: {metric.reason}")
    print(f"Test Passed: {metric.is_successful()}")

if __name__ == "__main__":
    run_guarded_pipeline()