import numpy as np
import multiprocessing as mp
from multiprocessing import shared_memory

def invert_segment(start, end, shm_name):
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    np_array = np.ndarray((1000000,), dtype=np.uint8, buffer=existing_shm.buf)
    for i in range(start, end):
        np_array[i] = 255 - np_array[i]
    existing_shm.close()

if __name__ == "__main__":
    # Create shared memory array
    data = np.arange(1000000, dtype=np.uint8) % 256
    shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    shm_array = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
    np.copyto(shm_array, data)

    # Define ranges and processes
    num_procs = 4
    size = len(data)
    chunk = size // num_procs
    processes = []
    for i in range(num_procs):
        start = i * chunk
        end = size if i == num_procs - 1 else (i + 1) * chunk
        p = mp.Process(target=invert_segment, args=(start, end, shm.name))
        processes.append(p)
        p.start()

    for p in processes:
        p.join()

    # Check result
    print("First 10 values after inversion:", shm_array[:10])

    # Cleanup
    shm.close()
    shm.unlink()
