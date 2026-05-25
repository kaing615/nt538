#!/usr/bin/env python3
"""
Benchmark script for Challenge 2 - Continuous testing to find optimal parameters
Tests ProcessPoolExecutor, multiprocessing.Process, and sequential implementations
"""

import os
import sys
import time
import random
import struct
import multiprocessing
import gc
import shutil

# Import the challenge2 module
import challenge2 as c2

# Test parameters
TEST_ITERATIONS = 5


def generate_test_file(filepath, n, q, max_val=100000000):
    """Generate a test input file with random values"""
    with open(filepath, "wb") as f:
        f.write(f"{n} {q}\n".encode())
        values = [random.randint(0, max_val) for _ in range(n)]
        f.write(" ".join(str(v) for v in values).encode())


def generate_sparse_test_file(filepath, n, q, max_val=100000000):
    """Generate a test input file with sparse values (large gaps)"""
    with open(filepath, "wb") as f:
        f.write(f"{n} {q}\n".encode())
        values = sorted([random.randint(0, max_val) for _ in range(n)])
        f.write(" ".join(str(v) for v in values).encode())


def generate_dense_test_file(filepath, n, q, max_val=300000):
    """Generate a test input file with dense values (small gaps)"""
    with open(filepath, "wb") as f:
        f.write(f"{n} {q}\n".encode())
        values = sorted([random.randint(0, max_val) for _ in range(n)])
        f.write(" ".join(str(v) for v in values).encode())


def run_benchmark(filepath, label, iterations=TEST_ITERATIONS):
    """Run benchmark comparing all implementations"""
    print(f"\n{'='*70}")
    print(f"Benchmark: {label}")
    print(f"{'='*70}")
    
    # Warmup and verify all produce same results
    result_executor = c2.MAIN(filepath)
    result_process = c2.MAIN_process(filepath)
    result_sequential = c2.MAIN_sequential(filepath)
    
    if result_executor != result_process or result_process != result_sequential:
        print(f"ERROR: Results differ between implementations!")
        return None
    
    # Benchmark executor version
    executor_times = []
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        result_executor = c2.MAIN(filepath)
        end = time.perf_counter()
        executor_times.append(end - start)
    
    # Benchmark process version
    process_times = []
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        result_process = c2.MAIN_process(filepath)
        end = time.perf_counter()
        process_times.append(end - start)
    
    # Benchmark sequential version
    sequential_times = []
    for _ in range(iterations):
        gc.collect()
        start = time.perf_counter()
        result_sequential = c2.MAIN_sequential(filepath)
        end = time.perf_counter()
        sequential_times.append(end - start)
    
    # Calculate statistics
    executor_avg = sum(executor_times) / len(executor_times)
    executor_min = min(executor_times)
    
    process_avg = sum(process_times) / len(process_times)
    process_min = min(process_times)
    
    sequential_avg = sum(sequential_times) / len(sequential_times)
    sequential_min = min(sequential_times)
    
    print(f"\nProcessPoolExecutor:")
    print(f"  Average: {executor_avg*1000:.2f} ms | Best: {executor_min*1000:.2f} ms")
    
    print(f"\nmultiprocessing.Process:")
    print(f"  Average: {process_avg*1000:.2f} ms | Best: {process_min*1000:.2f} ms")
    
    print(f"\nSequential:")
    print(f"  Average: {sequential_avg*1000:.2f} ms | Best: {sequential_min*1000:.2f} ms")
    
    # Find best
    best_time = min(executor_min, process_min, sequential_min)
    if best_time == executor_min:
        best_name = "Executor"
    elif best_time == process_min:
        best_name = "Process"
    else:
        best_name = "Sequential"
    
    print(f"\n>>> Best: {best_name} with {best_time*1000:.2f} ms")
    
    return {
        'label': label,
        'executor_avg': executor_avg,
        'executor_min': executor_min,
        'process_avg': process_avg,
        'process_min': process_min,
        'sequential_avg': sequential_avg,
        'sequential_min': sequential_min,
        'best': best_name,
        'best_time': best_time
    }


def run_all_benchmarks():
    """Run all benchmark tests"""
    tmp_dir = "/tmp/challenge2_benchmark"
    os.makedirs(tmp_dir, exist_ok=True)
    
    results = []
    
    print("\n" + "="*70)
    print("GENERATING TEST FILES...")
    print("="*70)
    
    test_configs = [
        (f"{tmp_dir}/test_small.txt", "Small N (10k)", generate_test_file, 10000, 1000),
        (f"{tmp_dir}/test_medium.txt", "Medium N (50k)", generate_test_file, 50000, 1000),
        (f"{tmp_dir}/test_large.txt", "Large N (100k)", generate_test_file, 100000, 1000),
        (f"{tmp_dir}/test_xlarge.txt", "XLarge N (500k)", generate_test_file, 500000, 1000),
        (f"{tmp_dir}/test_xxlarge.txt", "XXLarge N (1M)", generate_test_file, 1000000, 1000),
        (f"{tmp_dir}/test_sparse.txt", "Sparse values", generate_sparse_test_file, 100000, 100000),
        (f"{tmp_dir}/test_dense.txt", "Dense values", generate_dense_test_file, 100000, 1000),
    ]
    
    for filepath, label, gen_func, n, q in test_configs:
        print(f"Generating {label}...")
        gen_func(filepath, n, q)
    
    print("\n" + "="*70)
    print("RUNNING BENCHMARKS...")
    print("="*70)
    
    for filepath, label, *_ in test_configs:
        result = run_benchmark(filepath, label)
        if result:
            results.append(result)
    
    # Cleanup
    shutil.rmtree(tmp_dir)
    
    # Summary
    print("\n" + "="*70)
    print("FINAL SUMMARY")
    print("="*70)
    print(f"\n{'Label':<20} {'Executor':<12} {'Process':<12} {'Sequential':<12} {'Best':<12}")
    print("-"*70)
    
    for r in results:
        print(f"{r['label']:<20} {r['executor_min']*1000:<12.2f} {r['process_min']*1000:<12.2f} {r['sequential_min']*1000:<12.2f} {r['best']:<12}")
    
    return results


def run_continuous_optimization():
    """Continuously run tests to find best parameters"""
    print("\n" + "="*70)
    print("CONTINUOUS OPTIMIZATION MODE")
    print("="*70)
    print("Running continuous benchmarks until interrupted...")
    print("Press Ctrl+C to stop.\n")
    
    iteration = 0
    best_overall_time = float('inf')
    best_result = None
    
    try:
        while True:
            iteration += 1
            print(f"\n{'='*70}")
            print(f"ITERATION {iteration}")
            print(f"{'='*70}")
            
            results = run_all_benchmarks()
            
            # Find best result
            for r in results:
                if r['best_time'] < best_overall_time:
                    best_overall_time = r['best_time']
                    best_result = r.copy()
                    print(f"\n*** NEW BEST: {best_overall_time*1000:.2f} ms ({r['label']} - {r['best']}) ***")
            
            print(f"\nBest overall time: {best_overall_time*1000:.2f} ms")
            
    except KeyboardInterrupt:
        print("\n\nStopping continuous optimization...")
        if best_result:
            print(f"\nFinal best result:")
            print(f"  Test: {best_result['label']}")
            print(f"  Best Method: {best_result['best']}")
            print(f"  Time: {best_result['best_time']*1000:.2f} ms")
    
    return best_result


def quick_verification():
    """Quick verification that all versions produce same results"""
    print("Running quick verification...")
    
    tmp_dir = "/tmp/challenge2_verify"
    os.makedirs(tmp_dir, exist_ok=True)
    
    test_cases = [
        (1000, 100, 10000),
        (5000, 1000, 50000),
        (10000, 500, 100000),
    ]
    
    all_passed = True
    for n, q, max_val in test_cases:
        filepath = f"{tmp_dir}/verify_{n}_{q}.txt"
        generate_test_file(filepath, n, q, max_val)
        
        result_executor = c2.MAIN(filepath)
        result_process = c2.MAIN_process(filepath)
        result_sequential = c2.MAIN_sequential(filepath)
        
        if result_executor != result_process or result_process != result_sequential:
            print(f"FAILED: n={n}, q={q}")
            all_passed = False
        else:
            print(f"PASSED: n={n}, q={q}")
    
    shutil.rmtree(tmp_dir)
    
    if all_passed:
        print("\nAll verification tests passed!")
    else:
        print("\nSome tests failed!")
    
    return all_passed


if __name__ == "__main__":
    print("Challenge 2 - Parallel Optimization Benchmark")
    print("="*70)
    
    # Verify correctness
    print("\n1. VERIFICATION")
    print("-"*40)
    if not quick_verification():
        sys.exit(1)
    
    # Run benchmarks
    print("\n2. SINGLE RUN BENCHMARKS")
    print("-"*40)
    run_all_benchmarks()
    
    # Continuous optimization
    print("\n3. CONTINUOUS OPTIMIZATION")
    print("-"*40)
    run_continuous_optimization()
