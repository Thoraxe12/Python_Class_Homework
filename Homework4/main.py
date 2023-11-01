import random
import time
import matplotlib.pyplot as plt

from joblib import Parallel, delayed


def factorial(number: int) -> int:
    ans = 1
    for i in range(2, number + 1):
        ans *= i

    return ans


def main() -> None:
    nums = []
    times = []
    for _ in range(0, 100_000):
        nums.append(random.randint(1, 1_000))

    for i in range(1, 9):
        start_time = time.time()
        Parallel(n_jobs=i)(delayed(factorial)(num) for num in nums)
        times.append(time.time() - start_time)

    for i, _ in enumerate(times):
        print(f"Time to run {i} threads: {times[i]}")

    plt.xlabel("Threads")
    plt.ylabel("Time")
    plt.bar([i for i in range(1, 9)], times)

    plt.show()


main()
