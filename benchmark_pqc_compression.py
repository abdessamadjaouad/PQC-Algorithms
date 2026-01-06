#!/usr/bin/env python3
"""
Comprehensive Benchmark: PQC + Compression for IoT
Measures performance metrics for thesis research
Abdessamad JAOUAD - M2 Big Data & IoT - ENSAM Casablanca
"""

import time
import zlib
import json
import sys
from datetime import datetime

# Check dependencies
HAS_OQS = False
try:
    import oqs
    HAS_OQS = True
except (ImportError, RuntimeError, Exception) as e:
    # liboqs-python not installed or C library not found
    pass

try:
    import lz4.frame as lz4
    HAS_LZ4 = True
except ImportError:
    HAS_LZ4 = False

try:
    import zstandard as zstd
    HAS_ZSTD = True
except ImportError:
    HAS_ZSTD = False

# ============================================
# TEST DATA GENERATION
# ============================================

def generate_iot_data(size_kb=1):
    """Generate realistic IoT sensor data"""
    base_reading = {
        "sensor_id": "temp_sensor_001",
        "device_type": "temperature_humidity",
        "timestamp": "2026-01-04T10:30:00Z",
        "location": {"lat": 33.5731, "lon": -7.5898},
        "readings": {
            "temperature": 25.5,
            "humidity": 60.2,
            "pressure": 1013.25,
            "battery": 87.5,
            "signal_strength": -65
        }
    }
    
    data = json.dumps(base_reading).encode()
    target_size = size_kb * 1024
    repetitions = target_size // len(data) + 1
    
    return (data * repetitions)[:target_size]

def generate_test_datasets():
    """Generate various test datasets"""
    return {
        'iot_small': generate_iot_data(1),      # 1 KB - single reading
        'iot_medium': generate_iot_data(10),    # 10 KB - batch of readings
        'iot_large': generate_iot_data(100),    # 100 KB - large batch
        'repetitive': b'0' * 5000 + b'1' * 5000,  # Highly compressible
        'random': bytes([i % 256 for i in range(10240)])  # Low compressibility
    }

# ============================================
# COMPRESSION BENCHMARK
# ============================================

def benchmark_compression(data, algorithm='zlib'):
    """Benchmark compression algorithm"""
    results = {
        'algorithm': algorithm,
        'original_size': len(data),
        'compressed_size': 0,
        'compression_time': 0,
        'decompression_time': 0,
        'compression_ratio': 0,
        'throughput_mbps': 0
    }
    
    try:
        # Compression
        start = time.perf_counter()
        if algorithm == 'zlib':
            compressed = zlib.compress(data, level=9)
        elif algorithm == 'lz4' and HAS_LZ4:
            compressed = lz4.compress(data)
        elif algorithm == 'zstd' and HAS_ZSTD:
            cctx = zstd.ZstdCompressor(level=3)
            compressed = cctx.compress(data)
        else:
            compressed = data
        
        results['compression_time'] = time.perf_counter() - start
        results['compressed_size'] = len(compressed)
        
        # Decompression
        start = time.perf_counter()
        if algorithm == 'zlib':
            decompressed = zlib.decompress(compressed)
        elif algorithm == 'lz4' and HAS_LZ4:
            decompressed = lz4.decompress(compressed)
        elif algorithm == 'zstd' and HAS_ZSTD:
            dctx = zstd.ZstdDecompressor()
            decompressed = dctx.decompress(compressed)
        else:
            decompressed = data
        
        results['decompression_time'] = time.perf_counter() - start
        
        # Calculate metrics
        if results['compressed_size'] > 0:
            results['compression_ratio'] = len(data) / results['compressed_size']
        
        total_time = results['compression_time'] + results['decompression_time']
        if total_time > 0:
            results['throughput_mbps'] = (len(data) / 1024 / 1024) / total_time
        
        results['success'] = (decompressed == data)
        
    except Exception as e:
        results['error'] = str(e)
        results['success'] = False
    
    return results

# ============================================
# PQC BENCHMARK
# ============================================

def benchmark_pqc(algorithm='Kyber768'):
    """Benchmark PQC algorithm"""
    results = {
        'algorithm': algorithm,
        'pk_size': 0,
        'sk_size': 0,
        'ct_size': 0,
        'keygen_time': 0,
        'encap_time': 0,
        'decap_time': 0
    }
    
    try:
        if HAS_OQS:
            kem = oqs.KeyEncapsulation(algorithm)
            
            # Key generation
            start = time.perf_counter()
            public_key = kem.generate_keypair()
            results['keygen_time'] = time.perf_counter() - start
            results['pk_size'] = len(public_key)
            results['sk_size'] = len(kem.export_secret_key())
            
            # Encapsulation
            start = time.perf_counter()
            ciphertext, shared_secret = kem.encap_secret(public_key)
            results['encap_time'] = time.perf_counter() - start
            results['ct_size'] = len(ciphertext)
            
            # Decapsulation
            start = time.perf_counter()
            recovered_secret = kem.decap_secret(ciphertext)
            results['decap_time'] = time.perf_counter() - start
            
            results['success'] = (recovered_secret == shared_secret)
        else:
            # Simulated results for demonstration
            sizes = {
                'Kyber512': {'pk': 800, 'sk': 1632, 'ct': 768},
                'Kyber768': {'pk': 1184, 'sk': 2400, 'ct': 1088},
                'Kyber1024': {'pk': 1568, 'sk': 3168, 'ct': 1568},
            }
            
            s = sizes.get(algorithm, {'pk': 1184, 'sk': 2400, 'ct': 1088})
            results['pk_size'] = s['pk']
            results['sk_size'] = s['sk']
            results['ct_size'] = s['ct']
            results['keygen_time'] = 0.001
            results['encap_time'] = 0.0015
            results['decap_time'] = 0.0015
            results['success'] = True
            results['simulated'] = True
    
    except Exception as e:
        results['error'] = str(e)
        results['success'] = False
    
    return results

# ============================================
# COMBINED BENCHMARK
# ============================================

def benchmark_combined(data, pqc_alg='Kyber768', comp_alg='zlib'):
    """Benchmark combined PQC + Compression approach"""
    results = {
        'pqc_algorithm': pqc_alg,
        'compression': comp_alg,
        'original_size': len(data),
        'success': False
    }
    
    try:
        # Compression phase
        comp_results = benchmark_compression(data, comp_alg)
        results['compressed_size'] = comp_results['compressed_size']
        results['compression_time'] = comp_results['compression_time']
        results['decompression_time'] = comp_results['decompression_time']
        results['compression_ratio'] = comp_results['compression_ratio']
        
        # PQC phase
        pqc_results = benchmark_pqc(pqc_alg)
        results['pqc_overhead'] = pqc_results['ct_size']
        results['keygen_time'] = pqc_results['keygen_time']
        results['encap_time'] = pqc_results['encap_time']
        results['decap_time'] = pqc_results['decap_time']
        
        # Total metrics
        results['total_transmission'] = comp_results['compressed_size'] + pqc_results['ct_size']
        results['total_time'] = (comp_results['compression_time'] + 
                                comp_results['decompression_time'] +
                                pqc_results['keygen_time'] +
                                pqc_results['encap_time'] +
                                pqc_results['decap_time'])
        
        results['bandwidth_savings'] = ((len(data) - results['total_transmission']) / len(data)) * 100
        results['success'] = comp_results['success'] and pqc_results['success']
        
    except Exception as e:
        results['error'] = str(e)
    
    return results

# ============================================
# REPORTING
# ============================================

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*80}")
    print(f"{title:^80}")
    print(f"{'='*80}\n")

def print_compression_results(results):
    """Print compression benchmark results"""
    print(f"Algorithm:         {results['algorithm']}")
    print(f"Original Size:     {results['original_size']:,} bytes")
    print(f"Compressed Size:   {results['compressed_size']:,} bytes")
    print(f"Compression Ratio: {results['compression_ratio']:.2f}x")
    print(f"Savings:           {((1 - results['compressed_size']/results['original_size']) * 100):.1f}%")
    print(f"Compression Time:  {results['compression_time']*1000:.3f} ms")
    print(f"Decompress Time:   {results['decompression_time']*1000:.3f} ms")
    print(f"Throughput:        {results['throughput_mbps']:.2f} MB/s")
    print(f"Status:            {'✓ SUCCESS' if results['success'] else '✗ FAILED'}")

def print_pqc_results(results):
    """Print PQC benchmark results"""
    print(f"Algorithm:       {results['algorithm']}")
    print(f"Public Key:      {results['pk_size']:,} bytes")
    print(f"Secret Key:      {results['sk_size']:,} bytes")
    print(f"Ciphertext:      {results['ct_size']:,} bytes")
    print(f"KeyGen Time:     {results['keygen_time']*1000:.3f} ms")
    print(f"Encap Time:      {results['encap_time']*1000:.3f} ms")
    print(f"Decap Time:      {results['decap_time']*1000:.3f} ms")
    print(f"Total Time:      {(results['keygen_time']+results['encap_time']+results['decap_time'])*1000:.3f} ms")
    if 'simulated' in results:
        print(f"Note:            [SIMULATED - Install liboqs-python for real results]")

def print_combined_results(results):
    """Print combined benchmark results"""
    print(f"Configuration:     {results['pqc_algorithm']} + {results['compression']}")
    print(f"Original Size:     {results['original_size']:,} bytes")
    print(f"Compressed:        {results['compressed_size']:,} bytes ({results['compression_ratio']:.2f}x)")
    print(f"PQC Overhead:      {results['pqc_overhead']:,} bytes")
    print(f"Total Transmission:{results['total_transmission']:,} bytes")
    print(f"Bandwidth Savings: {results['bandwidth_savings']:+.1f}%")
    print(f"Total Time:        {results['total_time']*1000:.3f} ms")
    print(f"Status:            {'✓ SUCCESS' if results['success'] else '✗ FAILED'}")

def export_results_json(all_results, filename='benchmark_results.json'):
    """Export results to JSON file"""
    with open(filename, 'w') as f:
        json.dump(all_results, f, indent=2, default=str)
    print(f"\n✓ Results exported to {filename}")

def export_results_latex(all_results, filename='benchmark_results.tex'):
    """Export results as LaTeX table"""
    with open(filename, 'w') as f:
        f.write("% Benchmark Results - Generated " + datetime.now().strftime("%Y-%m-%d %H:%M") + "\n\n")
        
        # Compression results table
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\caption{Compression Algorithm Performance}\n")
        f.write("\\begin{tabular}{lccccc}\n")
        f.write("\\hline\n")
        f.write("Algorithm & Size (KB) & Compressed & Ratio & Time (ms) & Throughput \\\\\n")
        f.write("\\hline\n")
        
        if 'compression' in all_results:
            for dataset, results in all_results['compression'].items():
                for r in results:
                    f.write(f"{r['algorithm']} & {r['original_size']/1024:.1f} & ")
                    f.write(f"{r['compressed_size']/1024:.1f} & {r['compression_ratio']:.2f}x & ")
                    f.write(f"{r['compression_time']*1000:.2f} & {r['throughput_mbps']:.1f} MB/s \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n\n")
        
        # PQC results table
        f.write("\\begin{table}[h]\n")
        f.write("\\centering\n")
        f.write("\\caption{Post-Quantum Cryptography Performance}\n")
        f.write("\\begin{tabular}{lcccccc}\n")
        f.write("\\hline\n")
        f.write("Algorithm & PK (B) & CT (B) & KeyGen (ms) & Encap (ms) & Decap (ms) \\\\\n")
        f.write("\\hline\n")
        
        if 'pqc' in all_results:
            for r in all_results['pqc']:
                f.write(f"{r['algorithm']} & {r['pk_size']} & {r['ct_size']} & ")
                f.write(f"{r['keygen_time']*1000:.2f} & {r['encap_time']*1000:.2f} & ")
                f.write(f"{r['decap_time']*1000:.2f} \\\\\n")
        
        f.write("\\hline\n")
        f.write("\\end{tabular}\n")
        f.write("\\end{table}\n")
    
    print(f"✓ LaTeX tables exported to {filename}")

# ============================================
# MAIN BENCHMARK SUITE
# ============================================

def run_full_benchmark():
    """Run comprehensive benchmark suite"""
    print("""
╔══════════════════════════════════════════════════════════════════════════════╗
║                  PQC + COMPRESSION BENCHMARK SUITE                           ║
║                  Abdessamad JAOUAD - M2 Big Data & IoT                       ║
║                  ENSAM Casablanca - January 2026                             ║
╚══════════════════════════════════════════════════════════════════════════════╝
""")
    
    # Check dependencies
    print("Checking dependencies...")
    print(f"  ├─ liboqs-python: {'✓' if HAS_OQS else '✗'} {'' if HAS_OQS else '(SIMULATED MODE)'}")
    print(f"  ├─ lz4:           {'✓' if HAS_LZ4 else '✗'}")
    print(f"  └─ zstandard:     {'✓' if HAS_ZSTD else '✗'}")
    
    all_results = {}
    
    # Generate test datasets
    print("\nGenerating test datasets...")
    datasets = generate_test_datasets()
    print(f"  ✓ Generated {len(datasets)} datasets")
    
    # Benchmark 1: Compression algorithms
    print_header("BENCHMARK 1: COMPRESSION ALGORITHMS")
    
    compression_algos = ['lz4'] if HAS_LZ4 else ['zlib']
    if HAS_LZ4 and 'zlib' not in compression_algos:
        compression_algos.append('zlib')
    if HAS_ZSTD:
        compression_algos.append('zstd')
    
    all_results['compression'] = {}
    
    for dataset_name, data in datasets.items():
        print(f"\nDataset: {dataset_name} ({len(data)} bytes)")
        print("-" * 80)
        
        all_results['compression'][dataset_name] = []
        
        for algo in compression_algos:
            result = benchmark_compression(data, algo)
            all_results['compression'][dataset_name].append(result)
            print_compression_results(result)
            print()
    
    # Benchmark 2: PQC algorithms
    print_header("BENCHMARK 2: POST-QUANTUM CRYPTOGRAPHY")
    
    pqc_algos = ['Kyber512', 'Kyber768', 'Kyber1024']
    all_results['pqc'] = []
    
    for algo in pqc_algos:
        print(f"\nTesting: {algo}")
        print("-" * 80)
        result = benchmark_pqc(algo)
        all_results['pqc'].append(result)
        print_pqc_results(result)
        print()
    
    # Benchmark 3: Combined approach
    print_header("BENCHMARK 3: COMBINED PQC + COMPRESSION")
    
    test_data = datasets['iot_medium']  # Use 10KB IoT data
    all_results['combined'] = []
    
    for pqc_alg in pqc_algos:
        for comp_alg in compression_algos:
            print(f"\nConfiguration: {pqc_alg} + {comp_alg}")
            print("-" * 80)
            result = benchmark_combined(test_data, pqc_alg, comp_alg)
            all_results['combined'].append(result)
            print_combined_results(result)
            print()
    
    # Export results
    print_header("EXPORTING RESULTS")
    export_results_json(all_results)
    export_results_latex(all_results)
    
    # Summary
    print_header("BENCHMARK COMPLETE")
    print("Results saved to:")
    print("  • benchmark_results.json (JSON format)")
    print("  • benchmark_results.tex (LaTeX tables)")
    print(f"\nBenchmark completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    return all_results

# ============================================
# QUICK BENCHMARK (for testing)
# ============================================

def run_quick_benchmark():
    """Run quick benchmark for testing"""
    print("\n[QUICK BENCHMARK MODE]\n")
    
    # Single test with medium IoT data
    data = generate_iot_data(10)
    
    print("Testing: Kyber768 + LZ4")
    print("-" * 60)
    result = benchmark_combined(data, 'Kyber768', 'lz4' if HAS_LZ4 else 'zlib')
    print_combined_results(result)

# ============================================
# ENTRY POINT
# ============================================

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == '--quick':
        run_quick_benchmark()
    else:
        run_full_benchmark()
