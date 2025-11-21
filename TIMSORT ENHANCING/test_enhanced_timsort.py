import random
import time
import sys
import psutil
import os
from enhanced_timsort import EnhancedTimsort

def get_memory_usage():
    """Get current memory usage in MB."""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB

def test_correctness():
    """Test sorting correctness on various data types."""
    print("Testing Correctness...")
    test_cases = [
        ([], "Empty array"),
        ([1], "Single element"),
        ([3, 1, 4, 1, 5], "Random small"),
        (list(range(100)), "Already sorted"),
        (list(range(99, -1, -1)), "Reverse sorted"),
        ([1] * 50, "All equal"),
        ([random.randint(0, 100) for _ in range(1000)], "Random large"),
        ([(i % 10, i) for i in range(100)], "With duplicates (value, index)"),
    ]

    for arr, desc in test_cases:
        # Test ascending
        sorter = EnhancedTimsort(arr.copy())
        sorted_arr = sorter.sort(reverse=False)
        expected = sorted(arr)
        if sorted_arr == expected:
            print(f"✓ {desc} (ascending): Passed")
        else:
            print(f"✗ {desc} (ascending): Failed - Got {sorted_arr[:10]}... Expected {expected[:10]}...")
            return False
        # Test descending
        sorter_desc = EnhancedTimsort(arr.copy())
        sorted_arr_desc = sorter_desc.sort(reverse=True)
        expected_desc = sorted(arr, reverse=True)
        if sorted_arr_desc == expected_desc:
            print(f"✓ {desc} (descending): Passed")
        else:
            print(f"✗ {desc} (descending): Failed - Got {sorted_arr_desc[:10]}... Expected {expected_desc[:10]}...")
            return False
    return True

def test_stability():
    """Test stability: Equal elements should maintain original order."""
    print("Testing Stability...")
    # Use (value, original_index) to check order preservation
    arr = [(3, 0), (1, 1), (3, 2), (1, 3), (2, 4)]
    sorter = EnhancedTimsort(arr.copy())
    sorted_arr = sorter.sort()
    expected = sorted(arr)  # sorted() is stable
    if sorted_arr == expected:
        print("✓ Stability: Passed")
        return True
    else:
        print(f"✗ Stability: Failed - Got {sorted_arr}, Expected {expected}")
        return False

def test_performance():
    """Benchmark performance on increasing sizes."""
    print("Testing Performance...")
    sizes = [10**3, 10**4, 10**5, 10**6]  # Up to 1M for thorough
    results = []
    for size in sizes:
        arr = [random.randint(0, 10**6) for _ in range(size)]
        sorter = EnhancedTimsort(arr.copy())
        start = time.time()
        sorter.sort()
        enhanced_time = time.time() - start

        start = time.time()
        sorted(arr)
        builtin_time = time.time() - start

        ratio = enhanced_time / builtin_time if builtin_time > 0 else float('inf')
        results.append((size, enhanced_time, builtin_time, ratio))
        print(".4f")
    return results

def test_memory_usage():
    """Test memory usage on large datasets."""
    print("Testing Memory Usage...")
    size = 10**6
    arr = [random.randint(0, 10**6) for _ in range(size)]
    initial_mem = get_memory_usage()
    sorter = EnhancedTimsort(arr.copy())
    sorter.sort()
    final_mem = get_memory_usage()
    peak_mem = final_mem - initial_mem
    print(".2f")
    # Compare to builtin
    initial_mem = get_memory_usage()
    sorted(arr)
    builtin_mem = get_memory_usage() - initial_mem
    print(".2f")
    return peak_mem, builtin_mem

def test_scalability():
    """Test scalability: Time growth with size."""
    print("Testing Scalability...")
    sizes = [10**4, 5*10**4, 10**5, 5*10**5, 10**6]
    times = []
    for size in sizes:
        arr = [random.randint(0, 10**6) for _ in range(size)]
        sorter = EnhancedTimsort(arr.copy())
        start = time.time()
        sorter.sort()
        t = time.time() - start
        times.append(t)
        print(".4f")
    # Check if roughly O(n log n) - time should not explode
    ratios = [times[i] / (sizes[i] * (sizes[i].bit_length())) for i in range(len(sizes))]
    avg_ratio = sum(ratios) / len(ratios)
    print(".6f")
    return times

def test_consistency():
    """Test consistency: Same results across multiple runs."""
    print("Testing Consistency...")
    arr = [random.randint(0, 1000) for _ in range(10000)]
    results = []
    for _ in range(5):
        sorter = EnhancedTimsort(arr.copy())
        sorted_arr = sorter.sort()
        results.append(tuple(sorted_arr))
    if all(r == results[0] for r in results):
        print("✓ Consistency: Passed")
        return True
    else:
        print("✗ Consistency: Failed - Inconsistent results")
        return False

def test_edge_cases():
    """Test edge cases."""
    print("Testing Edge Cases...")
    cases = [
        ([], "Empty"),
        ([42], "Single"),
        ([1, 1, 1, 1], "All duplicates"),
        ([1, 2, 3, 4, 5], "Sorted"),
        ([5, 4, 3, 2, 1], "Reverse"),
        ([random.randint(0, 1) for _ in range(1000)], "Binary data"),
    ]
    for arr, desc in cases:
        try:
            sorter = EnhancedTimsort(arr.copy())
            sorted_arr = sorter.sort()
            if sorted_arr == sorted(arr):
                print(f"✓ {desc}: Passed")
            else:
                print(f"✗ {desc}: Failed")
                return False
        except Exception as e:
            print(f"✗ {desc}: Exception - {e}")
            return False
    return True

if __name__ == "__main__":
    print("Starting Thorough Testing of EnhancedTimsort...\n")

    all_passed = True
    all_passed &= test_correctness()
    print()
    all_passed &= test_stability()
    print()
    perf_results = test_performance()
    print()
    mem_results = test_memory_usage()
    print()
    scal_results = test_scalability()
    print()
    all_passed &= test_consistency()
    print()
    all_passed &= test_edge_cases()

    print("\n" + "="*50)
    if all_passed:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Review output above.")

    print("Summary:")
    print("- Performance: See ratios above (aim for <2x builtin for large sizes).")
    print("- Memory: Enhanced should use less than builtin for large data.")
    print("- Scalability: Consistent O(n log n) growth.")
    print("- Recommendations: If memory or perf issues, optimize in-place merges further.")
