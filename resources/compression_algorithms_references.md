# Compression Algorithms Research References

## Document Information
- **Research Date**: January 2025
- **Author**: Abdessamad JAOUAD
- **Program**: M2 Big Data & IoT, ENSAM Casablanca
- **Purpose**: Reference material for compression algorithms educational document

---

## 1. Run-Length Encoding (RLE)

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Run-length_encoding

### Key Information
- **Type**: Lossless compression
- **Space Complexity**: O(n)
- **Best Use Case**: Data with many consecutive repeated values (icons, simple graphics, fax transmission)
- **How It Works**: Replaces consecutive identical symbols with count-symbol pairs
- **Example**: "WWWWWWWWWWWWBWWWWWWWWWWWWBBB" → "12W1B12W3B"

### Variants
- Sequential RLE
- Lossy RLE (PackBits)
- Adaptive RLE

---

## 2. Delta Encoding

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Delta_encoding

### Key Information
- **Type**: Lossless compression
- **Best Use Case**: Data with small/constant variation (time series, sensor data)
- **How It Works**: Stores differences between sequential values instead of absolute values
- **Example**: [2, 4, 6, 9, 7] → [2, 2, 2, 3, −2]

### Applications
- Video compression (motion vectors)
- Version control (Git, rsync)
- HTTP delta encoding (RFC 3229)
- Database storage

---

## 3. Huffman Coding

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Huffman_coding

### Key Information
- **Type**: Entropy encoding (lossless)
- **Inventor**: David Huffman (1952) at MIT
- **Time Complexity**: O(n log n) for tree construction
- **How It Works**: Creates optimal prefix-free codes based on symbol frequency
- **Property**: Optimal for symbol-by-symbol encoding

### Algorithm
1. Count frequency of each symbol
2. Build priority queue (min-heap)
3. Construct binary tree (merge lowest frequencies)
4. Assign codes (left=0, right=1)

### Applications
- DEFLATE (gzip, PNG, ZIP)
- JPEG image compression
- MP3 audio compression
- PKZIP

---

## 4. Arithmetic Coding

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Arithmetic_coding

### Key Information
- **Type**: Entropy encoding (lossless)
- **Inventors**: Jorma Rissanen (IBM) and Richard Pasco (1976)
- **Advantage**: Can approach theoretical entropy limit
- **How It Works**: Encodes entire message as single fractional number in [0,1)

### Comparison with Huffman
- More efficient for non-power-of-2 probabilities
- Can achieve fractional bits per symbol
- More computationally intensive

### Applications
- JPEG (optional mode)
- H.264/AVC video (CABAC)
- Data compression research

---

## 5. LZ77 and LZ78 (Lempel-Ziv)

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/LZ77_and_LZ78

### Key Information
- **Type**: Dictionary-based lossless compression
- **Inventors**: Abraham Lempel and Jacob Ziv (1977, 1978)
- **IEEE Milestone**: 2004

### LZ77
- Uses sliding window
- Outputs (offset, length, next-char) tuples
- Foundation for DEFLATE, gzip, LZMA

### LZ78
- Builds explicit dictionary
- Outputs (dictionary-index, next-char) pairs
- Foundation for LZW

---

## 6. LZW (Lempel-Ziv-Welch)

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Lempel%E2%80%93Ziv%E2%80%93Welch

### Key Information
- **Type**: Dictionary-based lossless compression
- **Year**: 1984
- **Inventor**: Terry Welch (improvement on LZ78)
- **Patent**: Expired 2003 (US), 2004 (international)

### How It Works
1. Initialize dictionary with single characters
2. Find longest match in dictionary
3. Output dictionary index
4. Add match + next character to dictionary

### Applications
- GIF image format
- TIFF (optional)
- PDF (optional)
- Unix compress utility

---

## 7. DEFLATE

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Deflate

### Key Information
- **Type**: Hybrid (LZ77 + Huffman)
- **Year**: 1990
- **Inventor**: Phil Katz (PKZIP)
- **Standard**: RFC 1951 (1996)

### Algorithm
1. LZ77: Find duplicate strings, replace with (length, distance) pairs
2. Huffman: Encode literals and length-distance pairs

### Parameters
- Window size: 32 KB
- Match length: 3-258 bytes
- Compression levels: 0-9

### Applications
- gzip (.gz)
- PNG images
- ZIP archives
- HTTP compression
- PDF

---

## 8. LZ4

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/LZ4_(compression_algorithm)

### Key Information
- **Type**: Dictionary-based lossless compression
- **Author**: Yann Collet
- **Focus**: Speed over compression ratio

### Characteristics
- No entropy coding stage
- Very fast compression/decompression
- Lower compression ratio than DEFLATE

### Applications
- Linux kernel (since 3.11)
- ZFS filesystem
- Facebook, Apple
- Hadoop/Spark
- MySQL InnoDB

---

## 9. Zstandard (zstd)

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Zstd

### Key Information
- **Type**: Hybrid (LZ77 + Huffman + FSE/tANS)
- **Author**: Yann Collet (Facebook, 2016)
- **Standard**: RFC 8478

### Characteristics
- Compression levels: -7 to 22
- Dictionary support
- Streaming support
- Adaptive compression

### Applications
- Linux kernel (btrfs, squashfs since 4.14)
- Facebook
- Arch Linux packages (.pkg.tar.zst)
- Chrome, Firefox
- rsync

---

## 10. Brotli

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Brotli

### Key Information
- **Type**: Hybrid (LZ77 + Huffman + context modeling)
- **Authors**: Jyrki Alakuijala, Zoltán Szabadka (Google, 2013)
- **Standard**: RFC 7932 (2016)

### Characteristics
- 120 KB static dictionary
- 16 MB sliding window
- Better than gzip for web content

### Applications
- HTTP compression
- WOFF2 web fonts
- All major browsers support "br" encoding

---

## 11. bzip2

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Bzip2

### Key Information
- **Type**: Block-sorting lossless compression
- **Author**: Julian Seward (1996)

### Algorithm Pipeline
1. Run-Length Encoding (RLE)
2. Burrows-Wheeler Transform (BWT)
3. Move-to-Front Transform (MTF)
4. Run-Length Encoding (second pass)
5. Huffman Coding

### Characteristics
- Block size: 100-900 KB
- Better ratio than gzip
- Slower than gzip

---

## 12. LZMA (Lempel-Ziv-Markov chain Algorithm)

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/LZMA

### Key Information
- **Type**: Dictionary + Range encoding
- **Author**: Igor Pavlov (1998)
- **Used in**: 7z format

### Characteristics
- Very high compression ratio
- Large dictionary support (up to 4 GB)
- Slow compression, fast decompression
- Context-specific modeling

### Applications
- 7-Zip (.7z)
- XZ Utils (.xz)
- Linux kernel compression

---

## 13. Snappy

### Sources
- Wikipedia: https://en.wikipedia.org/wiki/Snappy_(compression)

### Key Information
- **Type**: LZ77-based fast compression
- **Author**: Google (Jeff Dean, Sanjay Ghemawat, 2011)
- **Focus**: Speed

### Characteristics
- Compression: ~250 MB/s
- Decompression: ~500 MB/s
- No entropy encoding
- 20-100% lower ratio than gzip

### Applications
- Google BigTable
- MapReduce
- MongoDB
- LevelDB, RocksDB
- Apache Cassandra

---

## Comparison Summary

| Algorithm | Type | Speed | Ratio | Year | Best Use |
|-----------|------|-------|-------|------|----------|
| RLE | Simple | Very Fast | Low | Early | Simple patterns |
| Huffman | Entropy | Fast | Good | 1952 | General |
| LZW | Dictionary | Medium | Good | 1984 | GIF, TIFF |
| DEFLATE | Hybrid | Medium | Good | 1990 | General |
| bzip2 | Block-sort | Slow | Very Good | 1996 | Archives |
| LZMA | Dictionary | Slow | Excellent | 1998 | Archives |
| LZ4 | Dictionary | Very Fast | Medium | 2011 | Real-time |
| Snappy | LZ77 | Very Fast | Low-Medium | 2011 | Databases |
| Brotli | Hybrid | Medium | Very Good | 2013 | Web |
| Zstandard | Hybrid | Fast | Very Good | 2016 | General |

---

## Bibliography

1. Huffman, D. A. (1952). "A Method for the Construction of Minimum-Redundancy Codes"
2. Ziv, J., Lempel, A. (1977). "A Universal Algorithm for Sequential Data Compression"
3. Ziv, J., Lempel, A. (1978). "Compression of Individual Sequences via Variable-Rate Coding"
4. Welch, T. (1984). "A Technique for High-Performance Data Compression"
5. RFC 1951 - DEFLATE Compressed Data Format Specification (1996)
6. RFC 7932 - Brotli Compressed Data Format (2016)
7. RFC 8478 - Zstandard Compression and the application/zstd Media Type (2018)
8. Salomon, D. (2007). "Data Compression: The Complete Reference" (4th ed.)
9. Seward, J. - bzip2 and libbzip2 documentation
10. Collet, Y. - LZ4 and Zstandard documentation
