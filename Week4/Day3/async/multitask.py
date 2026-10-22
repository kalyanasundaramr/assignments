
import asyncio
# Learning: asyncio is a library to write concurrent code using the async/await syntax. It provides a way to run asynchronous tasks in Python.
async def task(name, seconds): # Learning: This is an asynchronous function that simulates a task taking a certain amount of time.
    print(f"{name} started")
    await asyncio.sleep(seconds) # Learning: asyncio.sleep() is a non-blocking sleep function that allows other tasks to run while waiting. It pauses the execution of the current task for the specified number of seconds without blocking the event loop.
    print(f"{name} completed after {seconds} seconds")

async def main(): # Learning: This is the main asynchronous function that runs multiple tasks concurrently using asyncio.gather().
    await asyncio.gather( # Learning: asyncio.gather() is used to run multiple asynchronous tasks concurrently. It takes multiple awaitable objects and runs them in parallel, returning their results as a list.
        task("Task 1", 5), 
        task("Task 2", 3),
        task("Task 3", 1)
    )

asyncio.run(main()) # Learning: asyncio.run() is used to run the main async function and manage the event loop. It starts the event loop, runs the main function, and closes the loop when done.
