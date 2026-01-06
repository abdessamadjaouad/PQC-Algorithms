#!/usr/bin/env python3
"""
PQC + Compression Demonstration
Combines Post-Quantum Cryptography with Compression for IoT
For IoT PQC Project - Abdessamad JAOUAD

Requires: pip install liboqs-python lz4 zstandard
"""

import time
import zlib
import sys

# Check if liboqs is available
HAS_OQS = False
try:
    import oqs
    HAS_OQS = True
except (ImportError, RuntimeError, Exception) as e:
    # liboqs-python not installed or C library not found
    print("WARNING: liboqs C library not found!")
    print("The Python package is installed but needs the system library.")
    print("Running in simulation mode...\n")

# Check for compression libraries
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
# COMPRESSION FUNCTIONS
# ============================================

def compress_data(data, algorithm='zlib'):
    """Compress data using specified algorithm"""
    if algorithm == 'zlib':
        return zlib.compress(data, level=9)
    elif algorithm == 'lz4' and HAS_LZ4:
        return lz4.compress(data)
    elif algorithm == 'zstd' and HAS_ZSTD:
        cctx = zstd.ZstdCompressor(level=3)
        return cctx.compress(data)
    else:
        return data

def decompress_data(data, algorithm='zlib'):
    """Decompress data using specified algorithm"""
    if algorithm == 'zlib':
        return zlib.decompress(data)
    elif algorithm == 'lz4' and HAS_LZ4:
        return lz4.decompress(data)
    elif algorithm == 'zstd' and HAS_ZSTD:
        dctx = zstd.ZstdDecompressor()
        return dctx.decompress(data)
    else:
        return data

# ============================================
# PQC OPERATIONS (using liboqs)
# ============================================

class PQCSimulator:
    """Simulates PQC operations when liboqs is not available"""
    def __init__(self, alg_name):
        self.alg_name = alg_name
        # Approximate sizes for common algorithms
        self.sizes = {
            'Kyber512': {'pk': 800, 'sk': 1632, 'ct': 768},
            'Kyber768': {'pk': 1184, 'sk': 2400, 'ct': 1088},
            'Kyber1024': {'pk': 1568, 'sk': 3168, 'ct': 1568},
            'Dilithium2': {'pk': 1312, 'sk': 2528, 'sig': 2420},
        }
    
    def keypair(self):
        sizes = self.sizes.get(self.alg_name, {'pk': 1000, 'sk': 2000})
        return bytes(sizes['pk']), bytes(sizes['sk'])
    
    def encap_secret(self, pk):
        sizes = self.sizes.get(self.alg_name, {'ct': 1000})
        return bytes(sizes['ct']), bytes(32)
    
    def decap_secret(self, sk, ct):
        return bytes(32)

def pqc_encrypt_decrypt(message, algorithm='Kyber768', compression='zlib'):
    """
    Complete workflow: Compress → Encrypt (PQC) → Decrypt → Decompress
    """
    print(f"\n{'='*70}")
    print(f"PQC + COMPRESSION WORKFLOW")
    print(f"Algorithm: {algorithm}, Compression: {compression}")
    print(f"{'='*70}")
    
    results = {}
    
    # Original message
    print(f"\n[1] Original Message")
    print(f"    Size: {len(message)} bytes")
    print(f"    Preview: {message[:50]}..." if len(message) > 50 else f"    Content: {message}")
    results['original_size'] = len(message)
    
    # Step 1: Compression
    print(f"\n[2] Compression ({compression})")
    start = time.time()
    compressed_message = compress_data(message, compression)
    compression_time = time.time() - start
    
    compression_ratio = len(message) / len(compressed_message) if len(compressed_message) > 0 else 1
    print(f"    Compressed size: {len(compressed_message)} bytes")
    print(f"    Compression ratio: {compression_ratio:.2f}x")
    print(f"    Savings: {((1 - len(compressed_message)/len(message)) * 100):.1f}%")
    print(f"    Time: {compression_time*1000:.2f} ms")
    results['compressed_size'] = len(compressed_message)
    results['compression_time'] = compression_time
    
    # Step 2: PQC Setup
    print(f"\n[3] PQC Key Generation ({algorithm})")
    
    if HAS_OQS:
        kem = oqs.KeyEncapsulation(algorithm)
        start = time.time()
        public_key = kem.generate_keypair()
        keygen_time = time.time() - start
    else:
        kem = PQCSimulator(algorithm)
        start = time.time()
        public_key, _ = kem.keypair()
        keygen_time = time.time() - start
    
    print(f"    Public key size: {len(public_key)} bytes")
    print(f"    Key generation time: {keygen_time*1000:.2f} ms")
    results['public_key_size'] = len(public_key)
    results['keygen_time'] = keygen_time
    
    # Step 3: PQC Encapsulation (simulate encryption)
    print(f"\n[4] PQC Encapsulation")
    start = time.time()
    
    if HAS_OQS:
        ciphertext, shared_secret = kem.encap_secret(public_key)
    else:
        ciphertext, shared_secret = kem.encap_secret(public_key)
    
    encap_time = time.time() - start
    
    print(f"    Ciphertext size: {len(ciphertext)} bytes")
    print(f"    Shared secret size: {len(shared_secret)} bytes")
    print(f"    Encapsulation time: {encap_time*1000:.2f} ms")
    results['ciphertext_size'] = len(ciphertext)
    results['encap_time'] = encap_time
    
    # Calculate total transmission size
    total_size = len(compressed_message) + len(ciphertext)
    print(f"\n[5] Total Transmission")
    print(f"    Compressed message: {len(compressed_message)} bytes")
    print(f"    PQC ciphertext: {len(ciphertext)} bytes")
    print(f"    Total: {total_size} bytes")
    print(f"    Overhead vs original: {((total_size/len(message) - 1) * 100):.1f}%")
    results['total_transmission'] = total_size
    
    # Step 4: PQC Decapsulation (simulate decryption)
    print(f"\n[6] PQC Decapsulation")
    start = time.time()
    
    if HAS_OQS:
        recovered_secret = kem.decap_secret(ciphertext)
    else:
        recovered_secret = kem.decap_secret(None, ciphertext)
    
    decap_time = time.time() - start
    
    print(f"    Decapsulation time: {decap_time*1000:.2f} ms")
    print(f"    Secret match: {recovered_secret == shared_secret}")
    results['decap_time'] = decap_time
    
    # Step 5: Decompression
    print(f"\n[7] Decompression")
    start = time.time()
    decompressed_message = decompress_data(compressed_message, compression)
    decompression_time = time.time() - start
    
    print(f"    Decompressed size: {len(decompressed_message)} bytes")
    print(f"    Time: {decompression_time*1000:.2f} ms")
    print(f"    Message integrity: {decompressed_message == message}")
    results['decompression_time'] = decompression_time
    
    # Summary
    total_time = compression_time + keygen_time + encap_time + decap_time + decompression_time
    print(f"\n{'='*70}")
    print(f"SUMMARY")
    print(f"{'='*70}")
    print(f"Total processing time: {total_time*1000:.2f} ms")
    print(f"Data reduction: {((1 - len(compressed_message)/len(message)) * 100):.1f}%")
    print(f"Final transmission: {total_size} bytes (vs {len(message)} original)")
    
    return results

# ============================================
# COMPARISON TESTS
# ============================================

def compare_approaches():
    """Compare different PQC algorithms and compression methods"""
    
    # Test message (simulating IoT sensor data)
    sensor_data = b'{"sensor_id":"temp_001","timestamp":"2026-01-04T10:30:00","temperature":25.5,"humidity":60.2,"pressure":1013.25}' * 20
    
    print("=" * 70)
    print("COMPARISON: PQC Algorithms with Different Compression")
    print("=" * 70)
    print(f"\nTest Data: IoT Sensor Readings (JSON format)")
    print(f"Original size: {len(sensor_data)} bytes")
    
    algorithms = ['Kyber512', 'Kyber768', 'Kyber1024']
    compressions = ['lz4'] if HAS_LZ4 else ['zlib']
    
    if HAS_LZ4 and 'zlib' not in compressions:
        compressions.append('zlib')
    if HAS_ZSTD:
        compressions.append('zstd')
    
    results_table = []
    
    for alg in algorithms:
        for comp in compressions:
            try:
                result = pqc_encrypt_decrypt(sensor_data, alg, comp)
                results_table.append({
                    'algorithm': alg,
                    'compression': comp,
                    'total_size': result['total_transmission'],
                    'total_time': result['compression_time'] + result['encap_time'] + result['decap_time'],
                })
            except Exception as e:
                print(f"\n[ERROR] {alg} + {comp}: {e}")
    
    # Print comparison table
    print(f"\n{'='*70}")
    print("COMPARISON TABLE")
    print(f"{'='*70}")
    print(f"{'Algorithm':<12} {'Compression':<12} {'Total Size':<12} {'Total Time':<12}")
    print("-" * 70)
    
    for r in results_table:
        print(f"{r['algorithm']:<12} {r['compression']:<12} {r['total_size']:<12} {r['total_time']*1000:>10.2f} ms")

# ============================================
# MAIN
# ============================================

if __name__ == "__main__":
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║   PQC + COMPRESSION DEMONSTRATION FOR IoT                            ║
║   Abdessamad JAOUAD - M2 Big Data & IoT                             ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Check dependencies
    print("Checking dependencies...")
    print(f"  liboqs-python: {'✓ Installed' if HAS_OQS else '✗ Not installed (using simulator)'}")
    print(f"  lz4:           {'✓ Installed' if HAS_LZ4 else '✗ Not installed'}")
    print(f"  zstandard:     {'✓ Installed' if HAS_ZSTD else '✗ Not installed'}")
    print()
    
    # Simple example
    simple_message = b"IoT Sensor Data: Temperature=25.5C, Humidity=60%, Pressure=1013hPa" * 10
    pqc_encrypt_decrypt(simple_message, 'Kyber768', 'lz4' if HAS_LZ4 else 'zlib')
    
    # Comprehensive comparison
    print("\n\n")
    compare_approaches()
    
    print("\n" + "="*70)
    print("Demonstration complete!")
    print("="*70)
