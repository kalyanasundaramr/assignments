
import asyncio

async def add(a, b): # Learning: This is an asynchronous function that simulates adding two numbers with a delay. It takes two arguments, a and b, and returns their sum after a delay of 1 second.
    await asyncio.sleep(2)
    return a + b

async def multiply(a, b): # Learning: This is an asynchronous function that simulates multiplying two numbers with a delay. It takes two arguments, a and b, and returns their product after a delay of 3 seconds.
    await asyncio.sleep(3)
    return a * b
 
async def main(): # Learning: This is the main asynchronous function that calls the add and multiply functions concurrently using asyncio.gather(). It waits for both functions to complete and prints their results.
    results = await asyncio.gather( # Learning: asyncio.gather() is used to run multiple asynchronous tasks concurrently. It takes multiple awaitable objects and runs them in parallel, returning their results as a list.
        add(10, 20), # Learning: The add function is called with arguments 10 and 20, and its result will be included in the results list.
        multiply(5, 4) # Learning: The multiply function is called with arguments 5 and 4, and its result will be included in the results list.
    )

    print("Addition:", results[0])
    print("Multiplication:", results[1])

asyncio.run(main()) # Learning: asyncio.run() is used to run the main async function and manage the event loop. It starts the event loop, runs the main function, and closes the loop when done.
