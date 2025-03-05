
# Project Structure: Sorting Visualization

# Sorting visualization Python code (sorting_visualization.py)
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import random

# Sorting algorithms
def bubble_sort(data):
    n = len(data)
    for i in range(n):
        for j in range(n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                yield data

def insertion_sort(data):
    for i in range(1, len(data)):
        key = data[i]
        j = i - 1
        while j >= 0 and key < data[j]:
            data[j + 1] = data[j]
            j -= 1
            yield data
        data[j + 1] = key
        yield data

def selection_sort(data):
    n = len(data)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if data[j] < data[min_idx]:
                min_idx = j
        data[i], data[min_idx] = data[min_idx], data[i]
        yield data

def quick_sort(data, low, high):
    if low < high:
        pivot_idx = partition(data, low, high)
        yield data
        yield from quick_sort(data, low, pivot_idx - 1)
        yield from quick_sort(data, pivot_idx + 1, high)

def partition(data, low, high):
    pivot = data[high]
    i = low - 1
    for j in range(low, high):
        if data[j] <= pivot:
            i += 1
            data[i], data[j] = data[j], data[i]
    data[i + 1], data[high] = data[high], data[i + 1]
    return i + 1

def merge_sort(data, start, end):
    if end - start > 1:
        mid = (start + end) // 2
        yield from merge_sort(data, start, mid)
        yield from merge_sort(data, mid, end)
        yield from merge(data, start, mid, end)

def merge(data, start, mid, end):
    left = data[start:mid]
    right = data[mid:end]
    k = start
    i = 0
    j = 0
    while start + i < mid and mid + j < end:
        if left[i] <= right[j]:
            data[k] = left[i]
            i += 1
        else:
            data[k] = right[j]
            j += 1
        k += 1
        yield data
    while start + i < mid:
        data[k] = left[i]
        i += 1
        k += 1
        yield data
    while mid + j < end:
        data[k] = right[j]
        j += 1
        k += 1
        yield data

def heap_sort(data):
    n = len(data)

    def heapify(data, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and data[left] > data[largest]:
            largest = left

        if right < n and data[right] > data[largest]:
            largest = right

        if largest != i:
            data[i], data[largest] = data[largest], data[i]
            yield from heapify(data, n, largest)

    for i in range(n // 2 - 1, -1, -1):
        yield from heapify(data, n, i)

    for i in range(n - 1, 0, -1):
        data[i], data[0] = data[0], data[i]
        yield from heapify(data, i, 0)

# Visualization function
def visualize_sorting(data, sorting_algorithm, title):
    fig, ax = plt.subplots()
    ax.set_title(title)
    bar_rects = ax.bar(range(len(data)), data, align="edge")
    ax.set_xlim(0, len(data))
    ax.set_ylim(0, int(1.1 * max(data)))

    text = ax.text(0.02, 0.95, "", transform=ax.transAxes)
    iteration = [0]

    def update_fig(data, rects, iteration):
        for rect, val in zip(rects, data):
            rect.set_height(val)
        iteration[0] += 1
        text.set_text(f"Iterations: {iteration[0]}")

    def generator():
        for step in sorting_algorithm(data):
            yield step

    anim = animation.FuncAnimation(
        fig, update_fig, frames=generator, fargs=(bar_rects, iteration), interval=100, repeat=False
    )

    plt.show()

if __name__ == "__main__":
    sorting_algorithms = {
        "bubble_sort": bubble_sort,
        "insertion_sort": insertion_sort,
        "selection_sort": selection_sort,
        "quick_sort": lambda data: quick_sort(data, 0, len(data) - 1),
        "merge_sort": lambda data: merge_sort(data, 0, len(data)),
        "heap_sort": heap_sort
    }

    print("Available sorting algorithms:")
    for name in sorting_algorithms.keys():
        print(f"- {name}")

    algo_name = input("Enter the sorting algorithm to visualize: ")
    if algo_name not in sorting_algorithms:
        print("Invalid algorithm name!")
    else:
        N = 20
        data = [random.randint(1, 100) for _ in range(N)]
        visualize_sorting(data, sorting_algorithms[algo_name], title=f"{algo_name.capitalize()} Visualization")
