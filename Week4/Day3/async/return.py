
import asyncio
# Learning: asyncio is a library to write concurrent code using the async/await syntax. It provides a way to run asynchronous tasks in Python.

async def add(a, b): # Learning: This is an asynchronous function that simulates adding two numbers with a delay. It takes two arguments, a and b, and returns their sum after a delay of 1 second.
    await asyncio.sleep(1) # Learning: asyncio.sleep() is a non-blocking sleep function that allows other tasks to run while waiting. It pauses the execution of the current task for the specified number of seconds without blocking the event loop.
    return a + b

async def main(): # Learning: This is the main asynchronous function that calls the add function and prints the result. It uses await to wait for the result of the add function before printing it.
    result = await add(10, 20) # Learning: The await keyword is used to wait for the result of the add function. It pauses the execution of the main function until the add function completes and returns its result.
    print("Result:", result)

asyncio.run(main()) # Learning: asyncio.run() is used to run the main async function and manage the event loop. It starts the event loop, runs the main function, and closes the loop when done.
