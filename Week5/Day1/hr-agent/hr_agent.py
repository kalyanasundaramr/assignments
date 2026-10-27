
"""
HR Assistant Agent — Week 5, Day 1

Creates an AutoGen assistant that generates a job description
for a Junior Python Developer using OpenAI's GPT-4o-mini model.

Expected output:
    Job title followed by five numbered responsibilities.
"""

# Import the asyncio library to handle asynchronous operations in Python.
import asyncio

# Import the AssistantAgent class from the autogen_agentchat library to create an AI assistant agent.
from autogen_agentchat.agents import AssistantAgent

# Import the Console class from the autogen_agentchat library to handle console input and output for the agent.
from autogen_agentchat.ui import Console

# Import the OpenAIChatCompletionClient class from the autogen_ext.models.openai module to interact with the OpenAI API for chat completions.
from autogen_ext.models.openai import OpenAIChatCompletionClient

# Import the load_dotenv function from the dotenv library to load environment variables from a .env file.
from dotenv import load_dotenv 

# Load environment variables from a .env file to access the OpenAI API key and other configurations.
load_dotenv()

# Initialize the OpenAI chat completion client with the specified model and temperature.
model_client = OpenAIChatCompletionClient(
    model="gpt-4o-mini",# Use the GPT-4o-mini model for generating responses, which is a smaller and faster variant of the GPT-4 model.
    temperature=0.7, # Set the temperature to 0.7 to allow for some creativity in the generated responses while maintaining coherence.
)

agent = AssistantAgent( # Create an instance of the AssistantAgent class, which represents the HR assistant agent.
    name="hr_assistant", # Assign the name "hr_assistant" to the agent for identification purposes.
    model_client=model_client, # Use the previously initialized model_client to handle the agent's interactions with the OpenAI API.    
    system_message="You are an HR assistant.", # Provide a system message to define the agent's role and context as an HR assistant, guiding its responses accordingly.
)

async def main(): # Define the main asynchronous function that will run the HR assistant agent and handle the job description generation task.  
    try: # Use a try-finally block to ensure that the model client is properly closed after the task is completed, even if an error occurs during execution.
        await Console( 
            agent.run_stream(
                task=(
                    "Write a job description for a Junior Python Developer. "
                    "Format the response as exactly six lines: "
                    "the job title on the first line, followed by five numbered "
                    "lines from 1 to 5. Each numbered line must contain a complete, "
                    "meaningful job responsibility or qualification. "
                    "Do not include an introduction, conclusion, blank lines, "
                    "or placeholders."
                )
        ) 
)
    finally:
        await model_client.close()

if __name__ == "__main__": 
    asyncio.run(main()) 