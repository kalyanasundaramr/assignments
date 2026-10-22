
import asyncio
# Learning: asyncio is a library to write concurrent code using the async/await syntax. It provides a way to run asynchronous tasks in Python.  
async def say_hello():
    print("Hello!")
    await asyncio.sleep(2) # Learning: asyncio.sleep() is a non-blocking sleep function that allows other tasks to run while waiting. It pauses the execution of the current task for the specified number of seconds without blocking the event loop.
    print("Welcome to Async Python!")

asyncio.run(say_hello()) # Learning: asyncio.run() is used to run the main async function and manage the event loop.
