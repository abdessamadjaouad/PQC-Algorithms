#!/usr/bin/env python3
"""
Compression Algorithms Demonstration
Demonstrates RLE, Huffman, and modern compression (LZ4, Zstandard)
For IoT PQC Project - Abdessamad JAOUAD
"""

import zlib
import gzip
import time
from collections import Counter
import heapq

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
# 3. MODERN COMPRESSION (using libraries)
# ============================================

def compress_with_library(data, algorithm='zlib'):
    """Compress using standard libraries"""
    if algorithm == 'zlib':
        return zlib.compress(data, level=9)
    elif algorithm == 'gzip':
        return gzip.compress(data, compresslevel=9)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

def decompress_with_library(data, algorithm='zlib'):
    """Decompress using standard libraries"""
    if algorithm == 'zlib':
        return zlib.decompress(data)
    elif algorithm == 'gzip':
        return gzip.decompress(data)
    else:
        raise ValueError(f"Unknown algorithm: {algorithm}")

# ============================================
# DEMONSTRATION
# ============================================

def demonstrate_compression():
    """Demonstrate different compression algorithms"""
    
    print("=" * 70)
    print("COMPRESSION ALGORITHMS DEMONSTRATION")
    print("=" * 70)
    
    # Test data
    test_cases = {
        "Repetitive data": b"AAAAAABBBBBBCCCCCCDDDDDD" * 10,
        "JSON-like data": b'{"sensor":"temp","value":25.5,"unit":"C"}' * 20,
        "Random data": bytes(range(256)) * 2,
    }
    
    for name, data in test_cases.items():
        print(f"\n{'=' * 70}")
        print(f"Test Case: {name}")
        print(f"Original size: {len(data)} bytes")
        print(f"{'=' * 70}")
        
        # 1. RLE
        try:
            start = time.time()
            rle_compressed = rle_encode(data)
            rle_time = time.time() - start
            rle_decoded = rle_decode(rle_compressed)
            
            print(f"\n1. Run-Length Encoding (RLE)")
            print(f"   Compressed size: {len(rle_compressed)} bytes")
            print(f"   Compression ratio: {len(data)/len(rle_compressed):.2f}x")
            print(f"   Time: {rle_time*1000:.2f} ms")
            print(f"   Correct: {rle_decoded == data}")
        except Exception as e:
            print(f"\n1. RLE failed: {e}")
        
        # 2. Huffman
        try:
            start = time.time()
            huffman_compressed, codes = huffman_encode(data)
            huffman_time = time.time() - start
            
            print(f"\n2. Huffman Coding")
            print(f"   Compressed size: {len(huffman_compressed)} bytes")
            print(f"   Compression ratio: {len(data)/len(huffman_compressed):.2f}x")
            print(f"   Time: {huffman_time*1000:.2f} ms")
            print(f"   Unique symbols: {len(codes)}")
        except Exception as e:
            print(f"\n2. Huffman failed: {e}")
        
        # 3. ZLIB (DEFLATE)
        try:
            start = time.time()
            zlib_compressed = compress_with_library(data, 'zlib')
            zlib_time = time.time() - start
            zlib_decompressed = decompress_with_library(zlib_compressed, 'zlib')
            
            print(f"\n3. ZLIB (DEFLATE)")
            print(f"   Compressed size: {len(zlib_compressed)} bytes")
            print(f"   Compression ratio: {len(data)/len(zlib_compressed):.2f}x")
            print(f"   Time: {zlib_time*1000:.2f} ms")
            print(f"   Correct: {zlib_decompressed == data}")
        except Exception as e:
            print(f"\n3. ZLIB failed: {e}")
        
        # 4. GZIP
        try:
            start = time.time()
            gzip_compressed = compress_with_library(data, 'gzip')
            gzip_time = time.time() - start
            
            print(f"\n4. GZIP")
            print(f"   Compressed size: {len(gzip_compressed)} bytes")
            print(f"   Compression ratio: {len(data)/len(gzip_compressed):.2f}x")
            print(f"   Time: {gzip_time*1000:.2f} ms")
        except Exception as e:
            print(f"\n4. GZIP failed: {e}")
        
        print()
    
    # Optional: Try LZ4 and Zstandard if available
    try:
        import lz4.frame
        import zstandard as zstd
        
        print(f"\n{'=' * 70}")
        print("MODERN COMPRESSION (LZ4 & Zstandard)")
        print(f"{'=' * 70}")
        
        test_data = b'{"sensor":"temperature","value":25.5}' * 100
        print(f"\nTest data size: {len(test_data)} bytes")
        
        # LZ4
        start = time.time()
        lz4_compressed = lz4.frame.compress(test_data)
        lz4_time = time.time() - start
        print(f"\nLZ4:")
        print(f"   Compressed: {len(lz4_compressed)} bytes")
        print(f"   Ratio: {len(test_data)/len(lz4_compressed):.2f}x")
        print(f"   Time: {lz4_time*1000:.2f} ms")
        
        # Zstandard
        cctx = zstd.ZstdCompressor(level=3)
        start = time.time()
        zstd_compressed = cctx.compress(test_data)
        zstd_time = time.time() - start
        print(f"\nZstandard:")
        print(f"   Compressed: {len(zstd_compressed)} bytes")
        print(f"   Ratio: {len(test_data)/len(zstd_compressed):.2f}x")
        print(f"   Time: {zstd_time*1000:.2f} ms")
        
    except ImportError:
        print("\n[INFO] LZ4 and Zstandard not installed")
        print("Install with: pip install lz4 zstandard")

if __name__ == "__main__":
    demonstrate_compression()
