# Post-Quantum Cryptography and Hardware Acceleration References

## Research Sources and Bibliography

### Post-Quantum Cryptography

#### NIST Standards (2024)
1. **FIPS 203 (ML-KEM/CRYSTALS-Kyber)** - Module-Lattice-Based Key-Encapsulation Mechanism
   - Type: Lattice-based cryptography
   - Key sizes: 1,632-1,952 bytes (public key)
   - Source: NIST Post-Quantum Cryptography Standardization

2. **FIPS 204 (ML-DSA/CRYSTALS-Dilithium)** - Module-Lattice-Based Digital Signature Algorithm
   - Type: Lattice-based cryptography
   - Public key: 1,312-2,592 bytes
   - Private key: 2,560-4,896 bytes
   - Source: NIST Post-Quantum Cryptography Standardization

3. **FIPS 205 (SLH-DSA/SPHINCS+)** - Stateless Hash-Based Digital Signature Algorithm
   - Type: Hash-based cryptography
   - Public key: 32 bytes
   - Private key: 64 bytes
   - Signature: ~8,000-50,000 bytes
   - Source: NIST Post-Quantum Cryptography Standardization

4. **FIPS 206 (FN-DSA/Falcon)** - FFT over NTRU-Lattice-Based Digital Signature Algorithm
   - Type: Lattice-based cryptography (NTRU)
   - Compact signatures
   - Source: NIST Post-Quantum Cryptography Standardization (Draft)

#### PQC Algorithm Families
1. **Lattice-based cryptography**
   - Learning With Errors (LWE) problem
   - Ring-LWE, Module-LWE variants
   - Examples: Kyber, Dilithium, NTRU

2. **Hash-based signatures**
   - Based on hash function security
   - Stateless (SPHINCS+) and stateful (XMSS, LMS) variants
   - Conservative security assumptions

3. **Code-based cryptography**
   - Based on error-correcting codes
   - McEliece cryptosystem (1978)
   - Large key sizes

4. **Multivariate polynomial cryptography**
   - Based on solving multivariate quadratic equations
   - Rainbow (broken 2022), GeMSS

5. **Isogeny-based cryptography**
   - Based on elliptic curve isogenies
   - SIDH/SIKE (broken 2022)
   - CSIDH remains under study

#### Key Research Papers
- Bernstein, D. J., & Lange, T. (2017). "Post-quantum cryptography." Nature, 549(7671), 188-194.
- Chen, L., et al. (2016). "Report on Post-Quantum Cryptography." NIST Internal Report 8105.
- Alagic, G., et al. (2022). "Status Report on the Third Round of the NIST Post-Quantum Cryptography Standardization Process." NIST Internal Report 8413.

#### Open Source Implementations
- **Open Quantum Safe (OQS)** - liboqs library
  - URL: https://openquantumsafe.org/
  - C library with PQC algorithm implementations
  - Integration with OpenSSL (oqs-provider)

### GPU Computing and CUDA

#### NVIDIA CUDA
- First released: February 2007
- Current version: 13.x
- Programming model: SIMT (Single Instruction, Multiple Threads)
- Supported languages: C, C++, Fortran, Python

#### Key CUDA Libraries
1. **cuBLAS** - Linear algebra operations
2. **cuFFT** - Fast Fourier Transform
3. **cuRAND** - Random number generation
4. **cuSPARSE** - Sparse matrix operations
5. **cuDNN** - Deep neural network primitives
6. **NPP** - Performance primitives

#### CUDA Programming Concepts
- **Kernels**: Functions executed on GPU
- **Threads**: Smallest execution unit
- **Blocks**: Groups of threads
- **Grids**: Groups of blocks
- **Shared memory**: Fast on-chip memory
- **Global memory**: Large off-chip memory

#### Research Papers
- Nickolls, J., Buck, I., Garland, M., & Skadron, K. (2008). "Scalable Parallel Programming with CUDA." ACM Queue, 6(2), 40-53.
- Owens, J.D., et al. (2008). "GPU Computing." Proceedings of the IEEE, 96(5), 879-899.

### OpenCL

#### Overview
- Vendor-independent GPGPU standard
- Managed by Khronos Group
- Current version: 3.0.19 (July 2025)
- Supports: CPUs, GPUs, DSPs, FPGAs

#### Memory Hierarchy
1. **Global memory** - Shared by all processing elements
2. **Constant memory** - Read-only, low latency
3. **Local memory** - Shared within work-group
4. **Private memory** - Per work-item (registers)

#### Key Concepts
- **Compute kernel**: Function executed on device
- **Work-item**: Single execution instance
- **Work-group**: Collection of work-items
- **NDRange**: Multi-dimensional index space

#### Research Papers
- Stone, J.E., Gohara, D., & Shi, G. (2010). "OpenCL: A Parallel Programming Standard for Heterogeneous Computing Systems." Computing in Science & Engineering, 12(3), 66-73.
- Du, P., et al. (2012). "From CUDA to OpenCL: Towards a Performance-Portable Solution for Multi-Platform GPU Programming." Parallel Computing, 38(8), 391-407.

### FPGA-Based Computing

#### Major Vendors
- **AMD/Xilinx** - Artix, Kintex, Virtex, Versal families
- **Intel/Altera** - Cyclone, Arria, Stratix, Agilex families
- **Lattice Semiconductor** - iCE, ECP families
- **Microchip/Microsemi** - PolarFire, SmartFusion families

#### FPGA Architecture Components
1. **Configurable Logic Blocks (CLBs)** - Basic logic units
2. **Block RAM (BRAM)** - On-chip memory
3. **DSP slices** - Digital signal processing
4. **I/O blocks** - External interfaces
5. **Routing channels** - Interconnect fabric
6. **Hard IP blocks** - PCIe, DDR controllers

#### Programming Languages
- **HDL**: VHDL, Verilog, SystemVerilog
- **HLS**: C/C++ to hardware (Vivado HLS, Intel HLS)
- **OpenCL for FPGAs**: Xilinx SDAccel, Intel FPGA SDK

#### Research Papers
- Kuon, I., & Rose, J. (2007). "Measuring the Gap between FPGAs and ASICs." IEEE Transactions on Computer-Aided Design, 26(2), 203-215.
- Cong, J., et al. (2011). "High-Level Synthesis for FPGAs: From Prototyping to Deployment." IEEE Transactions on Computer-Aided Design, 30(4), 473-491.

### Hardware-Accelerated Compression

#### GPU Compression Libraries
1. **nvCOMP** (NVIDIA)
   - LZ4, Snappy, Cascaded, Bitcomp, GDeflate
   - Up to 500 GB/s throughput
   - CUDA-based

2. **GPU-LZ** implementations
   - Parallel LZ77/LZ78
   - DEFLATE on GPU

3. **GPU-based entropy coding**
   - Parallel Huffman encoding/decoding
   - ANS (Asymmetric Numeral Systems)

#### FPGA Compression Implementations
1. **Xilinx Data Compression Library**
   - GZIP, ZSTD, LZ4
   - Integrated with Vitis platform

2. **Intel FPGA Compression IP**
   - GZIP compression/decompression
   - PCIe integration

#### Research Papers
- Ozsoy, A., Swany, M., & Chauhan, A. (2012). "Pipelined Parallel LZSS for Streaming Data Compression on GPGPUs." IEEE International Conference on Parallel and Distributed Systems.
- Weißenberger, A., & Schmidt, B. (2018). "Massively Parallel Huffman Decoding on GPUs." International Conference on Parallel Processing.

### Compression with Post-Quantum Security

#### Challenges
1. **Increased key sizes** - PQC keys are 10-100x larger than classical
2. **Bandwidth constraints** - Need efficient compression
3. **Combined security** - Encryption + compression order matters
4. **Side-channel attacks** - Timing attacks via compression

#### CRIME/BREACH Attacks
- Compression-based side-channel attacks
- Affects TLS with compression enabled
- Mitigation: Disable compression or use random padding

#### Research Areas
1. **Key compression techniques**
   - Seed-based key generation
   - Structured lattice representations

2. **Ciphertext compression**
   - Rounding techniques
   - Modulus switching

3. **Hybrid schemes**
   - Classical + PQC combinations
   - Graceful security degradation

#### Research Papers
- Ducas, L., et al. (2018). "Crystals-Dilithium: A Lattice-Based Digital Signature Scheme." IACR Transactions on Cryptographic Hardware and Embedded Systems.
- Alkim, E., et al. (2016). "Post-quantum Key Exchange—A New Hope." USENIX Security Symposium.

### Online Resources

1. **NIST PQC Project**: https://csrc.nist.gov/projects/post-quantum-cryptography
2. **Open Quantum Safe**: https://openquantumsafe.org/
3. **NVIDIA Developer (CUDA)**: https://developer.nvidia.com/cuda-zone
4. **Khronos OpenCL**: https://www.khronos.org/opencl/
5. **NVIDIA nvCOMP**: https://developer.nvidia.com/nvcomp
6. **Xilinx Data Compression**: https://xilinx.github.io/Vitis_Libraries/data_compression/

### Books and Tutorials

1. Bernstein, D. J., & Lange, T. (Eds.). (2009). "Post-Quantum Cryptography." Springer.
2. Sanders, J., & Kandrot, E. (2010). "CUDA by Example." Addison-Wesley.
3. Kirk, D. B., & Hwu, W. W. (2016). "Programming Massively Parallel Processors." Morgan Kaufmann.
4. Munshi, A., et al. (2011). "OpenCL Programming Guide." Addison-Wesley.

---
*Last updated: December 2024*
*Prepared for: M2 Big Data & IoT, ENSAM Casablanca*
