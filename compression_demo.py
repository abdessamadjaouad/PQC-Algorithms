#!/usr/bin/env python3
"""
Compression Algorithms Demonstration
Demonstrates RLE, Huffman, and modern compression with LZ4 as primary choice
For IoT PQC Project - Abdessamad JAOUAD
Updated: January 2026 - LZ4 focus for resource-constrained IoT devices
"""

import zlib
import gzip
import time
from collections import Counter
import heapq

# Check for optional libraries
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
# 1. RUN-LENGTH ENCODING (RLE)
# ============================================

def rle_encode(data):
    """Simple Run-Length Encoding implementation"""
    if not data:
        return b''
    
    encoded = []
    count = 1
    prev = data[0]
    
    for byte in data[1:]:
        if byte == prev and count < 255:
            count += 1
        else:
            encoded.append(prev)
            encoded.append(count)
            prev = byte
            count = 1
    
    encoded.append(prev)
    encoded.append(count)
    
    return bytes(encoded)

def rle_decode(data):
    """Decode RLE encoded data"""
    decoded = []
    for i in range(0, len(data), 2):
        if i + 1 < len(data):
            decoded.extend([data[i]] * data[i + 1])
    return bytes(decoded)

# ============================================
# 2. HUFFMAN CODING
# ============================================

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None
    
    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(data):
    """Build Huffman tree from data"""
    frequency = Counter(data)
    heap = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0] if heap else None

def build_codes(node, prefix="", codebook=None):
    """Build Huffman code table"""
    if codebook is None:
        codebook = {}
    
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + "0", codebook)
        build_codes(node.right, prefix + "1", codebook)
    
    return codebook

def huffman_encode(data):
    """Encode data using Huffman coding"""
    if not data:
        return b'', {}
    
    tree = build_huffman_tree(data)
    codes = build_codes(tree)
    
    encoded_bits = ''.join(codes[byte] for byte in data)
    
    # Convert bit string to bytes
    padding = 8 - len(encoded_bits) % 8
    if padding != 8:
        encoded_bits += '0' * padding
    
    encoded_bytes = int(encoded_bits, 2).to_bytes(len(encoded_bits) // 8, 'big')
    
    return encoded_bytes, codes

# ============================================
# 3. MODERN COMPRESSION
# ============================================

def compress_lz4(data):
    """Compress using LZ4 (primary algorithm for IoT)"""
    if HAS_LZ4:
        return lz4.compress(data)
    return data

def decompress_lz4(data):
    """Decompress LZ4 data"""
    if HAS_LZ4:
        return lz4.decompress(data)
    return data

def compress_zlib(data, level=6):
    """Compress using ZLIB (comparison)"""
    return zlib.compress(data, level=level)

def decompress_zlib(data):
    """Decompress ZLIB data"""
    return zlib.decompress(data)

def compress_zstd(data, level=3):
    """Compress using Zstandard (comparison)"""
    if HAS_ZSTD:
        cctx = zstd.ZstdCompressor(level=level)
        return cctx.compress(data)
    return data

def decompress_zstd(data):
    """Decompress Zstandard data"""
    if HAS_ZSTD:
        dctx = zstd.ZstdDecompressor()
        return dctx.decompress(data)
    return data

# ============================================
# DEMONSTRATION
# ============================================

def demonstrate_compression():
    """Demonstrate compression algorithms with LZ4 as primary focus"""
    
    print("=" * 70)
    print("COMPRESSION ALGORITHMS DEMONSTRATION")
    print("Focus: LZ4 for Resource-Constrained IoT Devices")
    print("=" * 70)
    
    # Check library availability
    print(f"\n📦 Library Status:")
    print(f"   LZ4:       {'✓ Available' if HAS_LZ4 else '✗ Not installed (pip install lz4)'}")
    print(f"   Zstandard: {'✓ Available' if HAS_ZSTD else '✗ Not installed (pip install zstandard)'}")
    
    # Test data - IoT sensor JSON
    test_cases = {
        "IoT JSON (500 B)": b'{"sensor":"temp_001","timestamp":"2026-01-06T10:30:00","readings":{"temperature":25.5,"humidity":60.2,"pressure":1013.25}}' * 4,
        "IoT Batch (5 KB)": b'{"sensor":"temp_001","value":25.5,"unit":"C"}' * 100,
        "Repetitive data": b"AAAAAABBBBBBCCCCCCDDDDDD" * 20,
    }
    
    results = []
    
    for name, data in test_cases.items():
        print(f"\n{'=' * 70}")
        print(f"Test: {name}")
        print(f"Original size: {len(data):,} bytes")
        print(f"{'=' * 70}")
        
        # LZ4 (PRIMARY - highlighted)
        if HAS_LZ4:
            start = time.perf_counter()
            lz4_compressed = compress_lz4(data)
            lz4_time = time.perf_counter() - start
            lz4_decompressed = decompress_lz4(lz4_compressed)
            
            ratio = len(data) / len(lz4_compressed)
            savings = (1 - len(lz4_compressed) / len(data)) * 100
            
            print(f"\n⭐ LZ4 (PRIMARY - Recommended for IoT)")
            print(f"   Compressed:   {len(lz4_compressed):,} bytes")
            print(f"   Ratio:        {ratio:.2f}x")
            print(f"   Savings:      {savings:.1f}%")
            print(f"   Time:         {lz4_time*1000:.3f} ms")
            print(f"   Memory:       ~16 KB (compression)")
            print(f"   Integrity:    {'✓ OK' if lz4_decompressed == data else '✗ FAILED'}")
            
            results.append(('LZ4', len(data), len(lz4_compressed), lz4_time))
        
        # ZLIB (comparison)
        start = time.perf_counter()
        zlib_compressed = compress_zlib(data)
        zlib_time = time.perf_counter() - start
        
        ratio = len(data) / len(zlib_compressed)
        print(f"\n   ZLIB (comparison)")
        print(f"   Compressed:   {len(zlib_compressed):,} bytes")
        print(f"   Ratio:        {ratio:.2f}x")
        print(f"   Time:         {zlib_time*1000:.3f} ms")
        print(f"   Memory:       ~32 KB (sliding window)")
        
        results.append(('ZLIB', len(data), len(zlib_compressed), zlib_time))
        
        # Zstandard (comparison)
        if HAS_ZSTD:
            start = time.perf_counter()
            zstd_compressed = compress_zstd(data)
            zstd_time = time.perf_counter() - start
            
            ratio = len(data) / len(zstd_compressed)
            print(f"\n   Zstandard (comparison)")
            print(f"   Compressed:   {len(zstd_compressed):,} bytes")
            print(f"   Ratio:        {ratio:.2f}x")
            print(f"   Time:         {zstd_time*1000:.3f} ms")
            print(f"   Memory:       ~64 KB+ (FSE tables)")
            
            results.append(('Zstd', len(data), len(zstd_compressed), zstd_time))
    
    # Summary: Why LZ4 for IoT
    print(f"\n{'=' * 70}")
    print("SUMMARY: Why LZ4 for IoT Endpoints")
    print("=" * 70)
    print("""
✓ LOWEST MEMORY:     16 KB vs 32 KB (ZLIB) vs 64 KB+ (Zstd)
✓ FASTEST SPEED:     500+ MB/s vs 50-100 MB/s (ZLIB)
✓ ENERGY EFFICIENT:  Minimal CPU time = minimal battery drain
✓ GOOD COMPRESSION:  50-75% reduction on JSON sensor data
✓ PREDICTABLE:       Simple execution, no data-dependent branching

Note: ZLIB/Zstd achieve better ratios but at higher memory/CPU cost.
      Use them at gateways, not on constrained IoT endpoints.
""")

if __name__ == "__main__":
    demonstrate_compression()
