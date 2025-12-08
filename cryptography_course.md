# Modern Cryptography: From Classics to the Quantum Frontier
% Post-Quantum Cryptography for the Real World: Kyber, Dilithium, Falcon (IoT Focus)

> This course is written as a self-contained, AI-augmented textbook-style guide. Each section is short, multi-representational (intuition, math, system view), and includes quick self-checks and suggestions for going deeper.

---

## 0. Course Overview

### 0.1 Learning goals

By the end of this course you should be able to:

- Explain why post-quantum cryptography (PQC) is needed and what threat model it addresses.
- Describe the core ideas behind lattice-based cryptography: lattices, LWE, SIS, NTRU-like problems.
- Understand the design and usage of three flagship PQC schemes:
  - **ML-KEM / CRYSTALS-Kyber** (KEM / key establishment)
  - **ML-DSA / CRYSTALS-Dilithium** (digital signatures)
  - **Falcon** (compact, fast signatures)
- Reason about how these algorithms fit into protocols (TLS, VPN, firmware updates, IoT onboarding).
- Identify and apply key optimization levers to make PQC usable on constrained IoT devices.

### 0.2 Prerequisites

- Comfortable with basic discrete math (modular arithmetic, vectors, matrices).
- Introductory knowledge of symmetric-key crypto (block ciphers, AEAD) and classical public-key crypto (RSA, DH, basic signatures) is helpful but not mandatory.

If something feels too abstract, use the **Intuition Box** subsections and skim formulas on first pass.

### 0.3 Recommended reading style

- Read **Sections 1–3** in order the first time.
- Afterwards, you can jump:
  - To **Section 4** if you are more interested in signatures.
  - To **Section 6–8** if your focus is IoT and implementation.
- Each major section ends with **Check Yourself** questions. Try to answer them in your own words.

---

## 1. Why Post-Quantum Cryptography?

### 1.1 The problem: classical public-key crypto vs quantum computers

Most of today’s secure communication relies on two hard mathematical problems:

- **Integer factorization** (RSA)
- **Discrete logarithms** (Diffie–Hellman over finite fields or elliptic curves)

Both are threatened by large-scale quantum computers:

- **Shor’s algorithm** solves factorization and discrete log in polynomial time on a sufficiently powerful quantum computer.
- This would break RSA, Diffie–Hellman, and elliptic-curve schemes like ECDSA or X25519.

**Harvest now, decrypt later.** Even before large quantum computers exist, an adversary can:

1. Record sensitive encrypted traffic today.
2. Store it long-term.
3. Decrypt it in the future once quantum capabilities are available.

For data that must remain secret for 10–30+ years (government, healthcare, industrial IP), this is unacceptable.

### 1.2 What is post-quantum cryptography (PQC)?

- PQC consists of **public-key algorithms** that:
  - Run on **classical hardware**.
  - Are designed to remain secure even against adversaries with **quantum computers**.

NIST has run a multi-year standardization process to select and standardize PQC schemes. As of late 2025, the key outcomes include:

- **ML-KEM (CRYSTALS-Kyber)**: key-encapsulation mechanism (KEM) for **key establishment**.
- **ML-DSA (CRYSTALS-Dilithium)**: lattice-based **digital signature** scheme.
- **Falcon** and **SPHINCS+** as additional signature options.

### 1.3 Where will PQC be used?

- **Web security (TLS 1.3 / QUIC)**: replacing or augmenting ECDHE and ECDSA/EdDSA.
- **VPNs and secure tunnels**: IKEv2/IPsec, WireGuard-like protocols.
- **Code and firmware signing**: ensuring only authentic updates run on devices.
- **IoT deployments**: onboarding, device-to-cloud communication, firmware updates.

In all these cases, PQC must be fast and compact enough to run on:

- Powerful servers.
- Desktop and mobile clients.
- **Constrained IoT devices** with limited CPU, RAM, flash, and power.

### 1.4 Check yourself

1. Why can an attacker benefit from recording your encrypted traffic now, even if they cannot break it yet?
2. What are the two main categories of PQC algorithms we care about for internet protocols?

---

## 2. Lattice Cryptography Foundations

This section introduces the minimum lattice theory and hard problems you need to understand Kyber, Dilithium, and Falcon.

### 2.1 Intuition: lattices as high-dimensional grids

**Definition (informal).** A **lattice** $\mathcal{L}$ in $\mathbb{R}^n$ is the set of all integer combinations of some basis vectors $b_1, \dots, b_k$:

$$
\mathcal{L} = \left\{ \sum_{i=1}^k z_i b_i : z_i \in \mathbb{Z} \right\}.
$$

- In 2D, you can picture a lattice as a regular grid, but the basis vectors need not be orthogonal.
- In higher dimensions, it’s still a “grid”, just impossible to visualize directly.

**Intuition Box.** Imagine you live on a city grid: you can only move in integer multiples of a few directions (streets). A lattice is like all the intersections reachable by integer steps along those directions.

### 2.2 Hard geometric problems: SVP and CVP

Two central computational problems on lattices are believed to be very hard:

- **Shortest Vector Problem (SVP):**
  - Input: a lattice basis.
  - Task: find the shortest nonzero lattice vector.
- **Closest Vector Problem (CVP):**
  - Input: a lattice basis and a target point in $\mathbb{R}^n$.
  - Task: find the lattice vector closest to the target.

Both have versions that are **NP-hard**. Cryptographic constructions use structured versions of these problems.

### 2.3 SIS and LWE: average-case problems for crypto

Practical lattice-based cryptography relies on **average-case** problems that can be efficiently sampled.

1. **Short Integer Solution (SIS)**

    - Fix integers $q$ and dimensions $m, n$.
    - Sample a random matrix $A \in \mathbb{Z}_q^{m \times n}$.
    - **Problem:** find a *short*, nonzero vector $x \in \mathbb{Z}^n$ such that

      $$
      A x \equiv 0 \pmod{q}.
      $$

    - “Short” means coefficients of $x$ are small in absolute value.

2. **Learning With Errors (LWE)**

    - Fix secret vector $s \in \mathbb{Z}_q^n$.
    - For each sample, draw random $a_i \in \mathbb{Z}_q^n$ and small error $e_i$.
    - Compute

      $$
      b_i = \langle a_i, s \rangle + e_i \pmod{q}.
      $$

    - **Problem:** given many pairs $(a_i, b_i)$, recover $s$ (or distinguish these from random pairs).

**Why “errors”?** The noise term $e_i$ makes the system of equations inconsistent, hiding $s$ from efficient solvers.

There are structured variants used for efficiency:

- **Ring-LWE**: replace vectors by polynomials over a ring.
- **Module-LWE and Module-SIS**: work with small modules over rings, balancing efficiency and security.

Many PQC schemes, including Kyber and Dilithium, are built on module-LWE and module-SIS assumptions.

### 2.4 Check yourself

1. In your own words, what does the noise in LWE achieve?
2. Why are SIS and LWE useful for building cryptographic schemes, compared to SVP directly?

---

## 3. ML-KEM / CRYSTALS-Kyber

Kyber (standardized as **ML-KEM**) is a lattice-based key-encapsulation mechanism used for **key establishment**.

### 3.1 Problem: secure key establishment

Goal: two parties (client and server, or IoT device and gateway) want to agree on a shared secret key over an insecure network.

- Classical solutions: Diffie–Hellman (DH) over finite fields or elliptic curves.
- Quantum threat: Shor’s algorithm breaks DH.

Kyber provides a **post-quantum** alternative.

### 3.2 Philosophy of Kyber

Design goals:

- **Security**: reduce security to module-LWE, a well-studied lattice problem.
- **Performance**: be fast on typical CPUs and reasonably efficient on embedded devices.
- **Compactness**: keep keys and ciphertexts small enough for practical use.
- **Simplicity**: avoid overly complicated mathematical structures.

### 3.3 Algebraic setting (informal)

Kyber works over a polynomial ring:

$$
R_q = \mathbb{Z}_q[x]/(x^n + 1),
$$

where:

- $q$ is a prime modulus.
- $n$ is a power of 2 (e.g., 256).

We can think of elements of $R_q$ as polynomials of degree $< n$ with coefficients in $\mathbb{Z}_q$.

Kyber uses **module-LWE** over $R_q$:

- Secrets and errors: small polynomials in $R_q$.
- Public data: a matrix $A$ with entries in $R_q$.

### 3.4 Key generation (high-level)

1. Sample small secret vector $s$ and error vector $e$ in $R_q^k$.
2. Derive public random matrix $A \in R_q^{k \times k}$ from a seed.
3. Compute

    $$
    t = A s + e.
    $$

4. Public key: $(\text{seed}, t)$.  
    Secret key: $s$ (plus some additional bookkeeping values in the full spec).

This forms a module-LWE instance: $t$ looks like a noisy linear function of $s$.

### 3.5 Encapsulation and decapsulation (intuition)

To encapsulate a key to a public key $(\text{seed}, t)$:

1. Reconstruct $A$ from the seed.
2. Sample fresh small vectors $r, e_1, e_2$.
3. Compute:
    - $u = A r + e_1$.
    - $v = t r + e_2 + \Delta(m)$, where $m$ encodes a message / shared secret seed.
4. Ciphertext: $(u, v)$.
5. Derive a shared key by hashing $m$ and/or $(u, v)$.

Decapsulation using secret $s$:

1. Compute

    $$
    v - u s \approx \Delta(m) + \text{small noise}.
    $$

2. Remove the small noise and decode $m$.
3. Use $m$ and/or $(u, v)$ in a KDF to derive the shared key.

Security: breaking this process should be as hard as solving underlying module-LWE instances.

### 3.6 Where Kyber is used

- In **TLS 1.3 / QUIC** handshakes to replace or augment ECDHE.
- In **VPNs** (IKEv2) for key establishment.
- For **device onboarding** in IoT: device and backend derive a shared secret key.

### 3.7 Check yourself

1. Why does Kyber use noise in its computations, instead of exact linear algebra?
2. In very broad terms, what does the receiver do during decapsulation to recover the shared secret?

---

## 4. ML-DSA / CRYSTALS-Dilithium

Dilithium (standardized as **ML-DSA**) is a lattice-based digital signature scheme.

### 4.1 Problem: authentication and integrity

We need to verify that:

- A software or firmware update is published by the legitimate vendor.
- A server really controls a particular private key (TLS certificates).
- Messages in a protocol have not been tampered with.

Classically, we use RSA signatures, ECDSA, or EdDSA (e.g., Ed25519). Post-quantum we need alternatives.

### 4.2 Philosophy of Dilithium

Design goals:

- Security based on **module-SIS/module-LWE**.
- Conceptual simplicity compared to more mathematically intricate designs.
- Efficiency: acceptable key and signature sizes, fast verification.

### 4.3 Core idea (informal)

Dilithium follows a “Fiat–Shamir with aborts” design over module lattices:

1. There is a public matrix $A$ and public vector $t = A s_1 + s_2$, where $s_1, s_2$ are small secret vectors.
2. To sign message $M$:
    - Sample random small vector $y$.
    - Compute $w = A y$.
    - Hash $(M, \text{high bits of } w)$ to get a challenge $c$.
    - Compute response $z = y + c s_1$.
    - If $z$ is too large (violating bounds), **abort** and resample $y$.
3. Signature is $(z, c, \text{hints})$.

Verification recomputes a version of $w$ from $z$ and public data, checks consistency with $c$, and verifies size bounds.

The rejection step (aborts) ensures the distribution of $z$ does not leak the secret $s_1$.

### 4.4 Security sketch

- A successful forgery roughly gives a short vector satisfying linear relations defined by $A$.
- This can be transformed into a solution to a **module-SIS** problem.
- Since module-SIS is believed hard (quantum-resistant), unforgeability should hold.

Formal proofs are more intricate, but this is the high-level picture.

### 4.5 Usage patterns

- **Software/firmware signing**: vendor signs image; IoT device verifies before applying.
- **TLS certificates**: CAs sign certificates using Dilithium.
- **Secure boot**: bootloader verifies signatures of subsequent firmware stages.

In many IoT setups, the device **verifies** signatures much more often than it **produces** them.

### 4.6 Check yourself

1. In very broad terms, what is the purpose of the rejection (abort) step in Dilithium signing?
2. In what scenario might an IoT device only need to verify Dilithium signatures and never sign itself?

---

## 5. Falcon

Falcon is a lattice-based digital signature scheme designed for **small signatures** and **fast verification**, based on **NTRU lattices** and sophisticated sampling techniques.

### 5.1 Motivation and philosophy

Why another signature scheme if we already have Dilithium?

- **Signature size**: Falcon signatures are significantly smaller than Dilithium’s.
- **Verification speed**: Falcon verification is very fast.

Trade-off:

- More complex mathematics (NTRU-based lattices, discrete Gaussian sampling).
- Implementations are trickier to get right, especially with side-channel resistance.

Falcon is attractive in bandwidth-constrained settings or where massive numbers of signatures need to be verified.

### 5.2 Very high-level math idea

- Falcon builds on the NTRU lattice framework.
- It uses a **trapdoor**: extra secret information that lets the signer efficiently find **short lattice vectors** in certain cosets.
- The signer uses a **discrete Gaussian sampler** over the lattice:
  - For a given message-dependent target point, the sampler outputs a short vector following a carefully designed distribution.
  - This vector acts as the signature.

Security relies on the hardness of underlying NTRU-related lattice problems and the indistinguishability of the signature distribution.

### 5.3 Practical considerations

- Pros:
  - Very compact signatures and public keys.
  - Very fast verification.
- Cons:
  - Implementation is more delicate (especially correct and side-channel-safe discrete Gaussian sampling).
  - Less “simple” than Dilithium; easier to make subtle mistakes.

### 5.4 Where Falcon fits

- Bandwidth-constrained systems where signature size is critical.
- Systems that verify many signatures (e.g., content distribution, some IoT broadcast scenarios).

### 5.5 Check yourself

1. Why might a designer choose Falcon over Dilithium for a specific system?
2. What is a potential downside of Falcon in terms of implementation complexity?

---

## 6. System Integration: How These Algorithms Work Together

### 6.1 Typical pattern in protocols

Modern secure protocols often separate:

- **Key establishment** (KEM): derive shared symmetric keys.
- **Authentication** (signatures): prove identity and integrity.

Mapping to our algorithms:

- **ML-KEM / Kyber**: used to establish shared keys.
- **ML-DSA / Dilithium** and **Falcon**: used to sign certificates, messages, firmware.

Examples:

- **TLS 1.3 / QUIC**:
  - Server certificate signed with Dilithium or Falcon.
  - Handshake uses Kyber (possibly hybrid with classical ECDHE) to agree on symmetric keys.
- **VPN (IKEv2)**:
  - Identity authentication with signatures.
  - Key establishment with Kyber.
- **Firmware updates**:
  - Firmware images signed using Dilithium or Falcon.
  - Optionally, Kyber-secured channel for delivering updates.

### 6.2 Hybrid cryptography

During a transition period, we want security even if:

- A classical scheme is broken.
- A PQC scheme is broken.

Hybrid approach:

- For KEM: combine classical ECDH with Kyber.
  - Final key = `KDF(shared_classical || shared_pqc)`.
- For signatures: include both a classical and a PQC signature (or dual certificates).

This hedges against unforeseen weaknesses, though it increases message size.

### 6.3 Check yourself

1. In a TLS-like protocol, which algorithm is responsible for agreeing on a shared symmetric key?
2. Why might deployments use “hybrid” modes combining classical and PQC algorithms for some time?

---

## 7. PQC on Constrained IoT Devices

We now focus on your main practical concern: making PQC work on small IoT devices.

### 7.1 Constraints and resource model

A typical low-end IoT device might have:

- CPU: small MCU (e.g., ARM Cortex-M3/M4, RISC-V embedded core).
- Flash: 64–512 KB of program storage.
- RAM: 8–64 KB.
- No FPU; limited hardware acceleration.
- Low bandwidth network (LPWAN, BLE, constrained Wi-Fi).

Resource impacts of PQC:

1. **Code size** (flash): crypto library + tables.
2. **Working memory** (RAM): buffers for keys, ciphertexts, polynomials.
3. **Cycles / energy**: CPU cycles per KEM/signature operation.
4. **Network**: bytes sent/received (key, ciphertext, signature sizes).

### 7.2 Roles and algorithm selection

First decide each device’s **role**:

- Does the device **sign** messages or firmware?
- Does it mainly **verify** signatures from others?
- How often does it need to perform **key establishment**?

Examples:

- Simple sensor node:
  - Rarely or never signs.
  - Verifies signatures on firmware updates.
  - Performs key establishment only at onboarding or infrequently.
- Gateway or base station:
  - Verifies many signatures from devices.
  - Handles many key exchanges.

**Mapping to algorithms:**

- Use **Kyber** for KEM.
- Use **Dilithium** or **Falcon** for signatures:
  - Dilithium: simpler and main NIST recommendation.
  - Falcon: smaller signatures and faster verification, but more complex.

### 7.3 Protocol design to minimize PQC cost

You can lighten PQC load at **protocol level**, not just implementation level.

1. **One-time heavy cost** (onboarding):
    - Perform PQC key exchange on first boot or provisioning.
    - Derive long-lived keys or credentials.

2. **Session resumption and tickets**:
    - After one expensive key exchange, use tickets or resumption mechanisms to avoid repeating it often.

3. **Use gateways / edge nodes**:
    - Let a more capable local gateway terminate PQC-heavy protocols and speak lightweight protocols to tiny devices.

4. **Firmware updates and signing**:
    - Device only verifies signatures on updates; signing happens in the backend.

### 7.4 Implementation-level optimization

Concrete strategies to make Kyber, Dilithium, Falcon lighter on MCUs:

1. **Parameter choice within standards**:
    - Choose the **lowest NIST security level** (e.g., level 1) that still meets your security lifetime requirements.
    - Lower levels generally mean smaller keys and faster operations.

2. **Polynomial arithmetic tuning**:
    - Implement polynomial multiplication using:
      - **Number-Theoretic Transform (NTT)** when you have enough flash and need high speed.
      - Simpler “schoolbook” multiplication if flash is scarce and performance requirements are lower.

3. **Memory layout and buffer reuse**:
    - Use **in-place transforms** to avoid extra buffers.
    - Reuse a single scratch buffer across operations to limit peak RAM.
    - Stream data into hash functions instead of buffering whole messages.

4. **Constant-time and side-channel safety**:
    - Remove branches on secret data.
    - Use fixed-time loops and masked table accesses.
    - Side-channel-safe implementations may be slightly slower but are essential for security.

5. **Code size reduction techniques**:
    - Share code between Kyber and Dilithium (NTT, sampling, hashing).
    - Compile out unused functionality (e.g., omit signing code on verification-only devices).
    - Use link-time optimization (LTO) and `-Os` (optimize for size).

6. **Leverage hardware acceleration** (if available):
    - Use hardware AES/SHA accelerators for PRFs and hashing.
    - Use MAC/DSP instructions for fast polynomial arithmetic.

### 7.5 Example: PQC-secure firmware update flow

**Scenario:** tiny device that needs secure firmware updates.

1. **Manufacturing time**:
    - Burn the vendor’s **PQC public key** (Dilithium or Falcon) into device ROM.

2. **Firmware signing (server-side)**:
    - Vendor signs firmware image hash with its private Dilithium/Falcon key.
    - Publishes firmware + signature.

3. **Update process (device-side)**:
    - Device downloads firmware + signature (possibly over a channel secured by Kyber-based key).
    - Verifies signature using vendor public key.
    - If valid, installs firmware; otherwise rejects.

4. **Benefits**:
    - Device only needs **verification** code (no signing, no keygen for signatures).
    - PQC protects against attackers who might later acquire a quantum computer.

### 7.6 Check yourself

1. Why is it often acceptable for a tiny IoT device to do only signature verification rather than signature generation?
2. Name two implementation techniques you can use to reduce RAM usage of PQC on a microcontroller.

---

## 8. Optimization Playbook (Summary)

This section summarizes optimization strategies as a checklist.

1. **Clarify roles**:
    - Does the device sign, verify, perform KEM, or some combination?

2. **Select algorithms and security levels**:
    - Kyber parameter set (e.g., ML-KEM-512) for KEM.
    - Dilithium or Falcon parameter set for signatures.

3. **Benchmark on target hardware**:
    - Measure flash, RAM, and cycle counts for key operations.

4. **Optimize polynomial arithmetic**:
    - Choose NTT vs schoolbook; use hardware support if available.

5. **Minimize memory footprint**:
    - In-place operations, buffer reuse, streaming.

6. **Harden against side channels**:
    - Constant-time code, careful random number generation.

7. **Simplify device responsibilities**:
    - Offload heavy tasks to gateways or servers.
    - Use one-time onboarding and long-lived keys where acceptable.

8. **Review and iterate**:
    - Profile again after optimizations.
    - Revisit parameter choices if constraints change.

---

## 9. Recap and Learning Path

You have seen:

- Why PQC is needed and what threat it addresses.
- Basic lattice crypto foundations: lattices, SIS, LWE.
- The structure and purpose of three key PQC schemes:
  - Kyber (ML-KEM) for key establishment.
  - Dilithium (ML-DSA) for signatures.
  - Falcon for compact, fast signatures.
- How these algorithms fit into real protocols.
- How to think about performance and optimization on constrained devices.

**Suggested next steps:**

1. Work through resources and videos listed in `cryptography_resources.md` section-by-section.
2. Try to implement small building blocks (e.g., polynomial operations, simple LWE toy examples) in a language of your choice.
3. Explore benchmark results of PQC schemes on microcontrollers to understand real-world trade-offs.

Use this document as a conceptual “map”, and rely on the resources file for deeper dives into each topic.

**Instructor:** Professor Antigravity (MIT Persona)
**Course Level:** Intermediate to Advanced
**Prerequisites:** Basic understanding of algebra and binary arithmetic.

---

## Course Introduction

Welcome. Cryptography is the invisible backbone of the modern internet. Every time you send a message, buy something online, or log into your bank, you are relying on mathematical fortresses built over decades. Today, we will explore how these fortresses work, why they are under siege by quantum mechanics, and how we are rebuilding them.

We will cover:
1.  **The Workhorses**: AES and RSA (Symmetric vs. Asymmetric).
2.  **The Mechanics**: A deep dive into the math with a "Hello World" example.
3.  **The Cracks**: Limitations and side-channel attacks.
4.  **The Threat**: How Quantum Computers (Shor's & Grover's Algorithms) break our current encryption.
5.  **The Future**: NIST's Post-Quantum Cryptography (PQC) standards.

---

## Module 1: The Workhorses of the Internet (AES & RSA)

To understand cryptography, we must distinguish between two fundamental types: **Symmetric** and **Asymmetric**.

### 1.1 AES (Advanced Encryption Standard) - The Symmetric Workhorse
**Analogy:** A safe where the *same key* locks and unlocks it.
**Use Case:** Encrypting large amounts of data (files, hard drives, Wi-Fi traffic) because it is extremely fast.

AES is a **block cipher**. It doesn't encrypt a message byte-by-byte like a stream; it chops the message into fixed blocks of 128 bits (16 bytes) and scrambles them using a key.

#### How AES Works (High Level)
AES operates in "rounds". For a 128-bit key, there are 10 rounds. Each round consists of four mathematical transformations:
1.  **SubBytes**: Non-linear substitution (like a secret decoder ring). This provides "confusion".
2.  **ShiftRows**: Shifting rows of the data matrix. This provides "diffusion".
3.  **MixColumns**: Mixing data within columns linearly. More diffusion.
4.  **AddRoundKey**: XORing the data with a part of the key.

### 1.2 RSA (Rivest–Shamir–Adleman) - The Asymmetric Guardian
**Analogy:** A mailbox. Anyone can put a letter in (using the **Public Key**), but only the owner with the key can open it (using the **Private Key**).
**Use Case:** Key exchange and digital signatures. It's slow, so we don't use it to encrypt the whole file. We use RSA to securely share the AES key, then use AES for the rest.

#### How RSA Works (High Level)
RSA relies on a simple fact: It is easy to multiply two large prime numbers together, but extremely difficult to take the result and find the original primes (Integer Factorization Problem).

---

## Lab: The "Hello World" Walkthrough

Let's trace the encryption of the message "Hello world" using both methods.

### Part A: AES Encryption of "Hello world"
**Scenario:** Alice wants to send "Hello world" to Bob using AES-128.
**Key:** `THATSMYKUNGFOO!!` (16 bytes)
**Message:** `Hello world` (11 bytes)

**Step 1: Padding**
AES requires 128-bit (16-byte) blocks. Our message is only 11 bytes. We must add padding (PKCS#7 is standard).
- Hex of "Hello world": `48 65 6c 6c 6f 20 77 6f 72 6c 64`
- We need 5 more bytes to reach 16. The value of each padding byte is `05`.
- **Input Block (State):**
  ```
  48 65 6c 6c
  6f 20 77 6f
  72 6c 64 05
  05 05 05 05
  ```
  *(Note: AES processes data in a 4x4 column-major matrix)*

**Step 2: Initial Round Key Addition**
We XOR the Input Block with the Key.
- Key: `54 48 41 54 53 4d 59 4b 55 4e 47 46 4f 4f 21 21` ("THATSMYKUNGFOO!!")
- Result = Input XOR Key.
  - `0x48` XOR `0x54` = `0x1C`
  - ...and so on for all 16 bytes.

**Step 3: The Rounds (Focus on Round 1)**
Inside the rounds, the magic happens.
1.  **SubBytes**: We look up each byte in a fixed table called the **S-Box**.
    - If our byte is `1C`, we find row `1`, column `C` in the S-Box. Let's say it maps to `9C`.
    - This destroys any linear relationship between the key and the ciphertext.
2.  **ShiftRows**:
    - Row 0: No shift.
    - Row 1: Shift left by 1.
    - Row 2: Shift left by 2.
    - Row 3: Shift left by 3.
3.  **MixColumns**:
    - Each column is multiplied by a fixed matrix in the Galois Field $GF(2^8)$.
    - Math: $[s'_0, s'_1, s'_2, s'_3]^T = M \times [s_0, s_1, s_2, s_3]^T$
    - This spreads a change in one byte to the entire column.
4.  **AddRoundKey**:
    - XOR the result with the Round Key (derived from the main key).

**Step 4: Output**
After 10 rounds, we get a block of random-looking bytes: `C3 89 ...`
This is the ciphertext.

---

### Part B: RSA Encryption of "Hello world"
**Scenario:** Alice encrypts "Hello world" with Bob's Public Key.
**Math Basis:** Modular Arithmetic.

**Step 1: Key Generation (Bob does this)**
1.  Select two small primes (for this example): $p = 61$, $q = 53$.
2.  Compute modulus $n = p \times q = 61 \times 53 = 3233$.
    - $n$ (3233) is the **Public Modulus**.
3.  Compute Euler's Totient $\phi(n) = (p-1)(q-1) = 60 \times 52 = 3120$.
4.  Choose a Public Exponent $e$.
    - Must be $1 < e < \phi(n)$ and coprime to 3120.
    - Let's choose $e = 17$.
    - **Public Key:** $(n=3233, e=17)$.
5.  Compute Private Exponent $d$.
    - $d \times e \equiv 1 \pmod{\phi(n)}$.
    - $d \times 17 \equiv 1 \pmod{3120}$.
    - Using Extended Euclidean Algorithm, we find $d = 2753$.
    - **Private Key:** $(n=3233, d=2753)$.

**Step 2: Encryption (Alice)**
1.  Convert message to a number $m$.
    - "H" (ASCII 72). Let's just encrypt "H" for simplicity. $m = 72$.
2.  Formula: $c = m^e \pmod n$.
3.  Calculation: $c = 72^{17} \pmod{3233}$.
    - $72^{17}$ is a huge number, but we use "Modular Exponentiation" to compute it efficiently.
    - Result: $c = 995$.
4.  Alice sends `995` to Bob.

**Step 3: Decryption (Bob)**
1.  Bob receives $c = 995$.
2.  Formula: $m = c^d \pmod n$.
3.  Calculation: $m = 995^{2753} \pmod{3233}$.
    - Again, using modular exponentiation.
    - Result: $m = 72$.
4.  Bob converts 72 back to ASCII -> "H".

---

## Module 2: Cracks in the Armor (Limitations)

While mathematically sound, these algorithms have practical issues:

1.  **Key Management (The Human Problem)**:
    - AES is fast, but how do you get the key to the other person securely? You need RSA.
    - RSA is slow and computationally expensive.
2.  **Implementation Flaws (Side-Channels)**:
    - **Timing Attacks**: If the computer takes slightly longer to process a '1' than a '0' in the private key, a hacker can measure the time and guess the key.
    - **Power Analysis**: Monitoring the power consumption of the CPU can reveal the operations being performed.
3.  **Forward Secrecy**:
    - If an attacker records all your encrypted traffic today and steals your private key 10 years from now, they can decrypt *everything* from the past. (Modern protocols use Ephemeral Keys to fix this).

---

## Module 3: The Quantum Storm

The biggest threat to RSA and ECC (Elliptic Curve Cryptography) is **Quantum Computing**.

### 3.1 Why Quantum is Different
Classical computers use bits (0 or 1). Quantum computers use **Qubits**, which can be in a state of superposition (both 0 and 1 at the same time). This allows them to perform massive parallel computations for specific types of problems.

### 3.2 Shor's Algorithm (The RSA Killer)
- **Target**: Asymmetric Algorithms (RSA, ECC, Diffie-Hellman).
- **Mechanism**: Shor's algorithm can find the prime factors of a large integer $n$ exponentially faster than any classical algorithm.
- **Impact**:
    - Classical complexity for factoring: Sub-exponential (hard).
    - Quantum complexity (Shor's): Polynomial (easy).
    - **Result**: A sufficiently powerful quantum computer could derive your Private Key ($d$) from your Public Key ($n, e$) in hours or minutes. **RSA is dead.**

### 3.3 Grover's Algorithm (The AES Weakener)
- **Target**: Symmetric Algorithms (AES, SHA-2 hashes).
- **Mechanism**: It speeds up searching an unsorted database. Brute-forcing a key is essentially searching for the right key in a space of $2^{128}$ possibilities.
- **Impact**:
    - It provides a quadratic speedup. It reduces the effective security by half.
    - AES-128 becomes as weak as AES-64 (which is breakable).
- **The Fix**: Simply double the key size. **AES-256** provides 128 bits of quantum security, which is considered safe against Grover's.

---

## Module 4: The Future - Post-Quantum Cryptography (PQC)

We cannot wait for a quantum computer to be built to fix this. We need **Post-Quantum Cryptography (PQC)**: algorithms that run on classical computers but are immune to quantum attacks.

### 4.1 The NIST Standardization (2024-2025)
After a 6-year competition, NIST has released the first finalized standards (FIPS).

#### **FIPS 203: ML-KEM (Module-Lattice-Based Key-Encapsulation Mechanism)**
- **Replaces**: RSA/Diffie-Hellman for key exchange.
- **Origin**: CRYSTALS-Kyber.
- **Math**: Based on **Lattices**. Finding the closest vector in a high-dimensional lattice with added noise is incredibly hard, even for quantum computers (Learning With Errors problem).
- **Status**: The primary standard for general encryption.

#### **FIPS 204: ML-DSA (Module-Lattice-Based Digital Signature Algorithm)**
- **Replaces**: RSA/ECDSA for digital signatures.
- **Origin**: CRYSTALS-Dilithium.
- **Math**: Also Lattice-based.
- **Status**: The primary standard for digital signatures.

#### **FIPS 205: SLH-DSA (Stateless Hash-Based Digital Signature Algorithm)**
- **Origin**: SPHINCS+.
- **Math**: Based on **Hash Functions**. We know hash functions are very secure. This is a conservative backup in case a mathematical breakthrough breaks Lattices.
- **Trade-off**: Larger signature sizes but very high confidence in security.

### 4.2 The Road Ahead
- **Migration**: Companies must start inventorying their crypto assets now. "Harvest Now, Decrypt Later" is a real threat—attackers are storing encrypted data today to decrypt it when they get a quantum computer.
- **Crypto-Agility**: Systems should be designed to swap algorithms easily if one is found to be vulnerable.

---

**End of Course**
*Professor Antigravity*
