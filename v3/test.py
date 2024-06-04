import multiprocessing

def test1():
    return "hello test1" 

def test2():
    return "hello test2" 

def test3():
    return "hello test3" 

def worker_function(item):
    key, func = item
    result = func()
    return (key, result)

if __name__=="__main__":
    
    _data = {
        "test1": test1,
        "test2": test2,
        "test3": test3
    }

    manager = multiprocessing.Manager()
    results = manager.dict()  # Shared dictionary to store results

    # Create a pool of worker processes
    pool = multiprocessing.Pool(processes=4)

    # Apply the worker_function to each item in _data asynchronously
    async_results = [pool.apply_async(worker_function, args=((key, func),)) for key, func in _data.items()]

    # Collect results
    for async_result in async_results:
        key, result = async_result.get()
        results[key] = result

    # Close the pool and wait for the work to finish
    pool.close()
    pool.join()

    # Print the results
    print("Results:", dict(results))
