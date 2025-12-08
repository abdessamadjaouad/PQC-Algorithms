# Post-Quantum Cryptography Course – Resources

This file lists key references and suggested videos for each section of `cryptography_course.md`. When a resource is especially relevant to a specific subsection, that is noted as well. Where possible, a local PDF filename under `resources/` is given so you can read offline.

---

## Section 1 – Why Post-Quantum Cryptography?

### Primary references
- NIST PQC Project Overview – motivation, process, and high-level goals.
  - Online: https://csrc.nist.gov/projects/post-quantum-cryptography
  - Local HTML snapshot: `resources/post-quantum-cryptography`
- NIST Status Reports on PQC Standardization – rationale for algorithm selection and security considerations.
  - Third Round Report (NISTIR 8413, update 1):
    - Online: https://csrc.nist.gov/pubs/ir/8413/upd1/final
    - (You can fetch the PDF manually from the NIST page if needed.)
  - Fourth Round Report (NISTIR 8545):
    - Online: https://csrc.nist.gov/pubs/ir/8545/final
    - Local PDF (NCCoE project description variant): `resources/pqc-migration-project-description-final.pdf`
- John Preskill, "Quantum Computing in the NISQ era and beyond" (for context on quantum capabilities).
  - Online abstract: https://arxiv.org/abs/1801.00862
  - Local PDF: `resources/arxiv-1801.00862-preskill-nisq.pdf`

### Videos
- NIST: "Introduction to Post-Quantum Cryptography" – overview talk.
  - Search: `NIST Introduction to Post-Quantum Cryptography talk` on YouTube.
- Martin R. Albrecht: "An Introduction to Post-Quantum Cryptography" – conference talk.
  - Search: `Martin Albrecht introduction post-quantum cryptography`.

Used in: Section 1 (motivation, threat model, NIST process).

---

## Section 2 – Lattice Cryptography Foundations

### Primary references
- Chris Peikert, "A Decade of Lattice Cryptography" – survey.
  - Online: https://web.eecs.umich.edu/~cpeikert/pubs/lattice-survey.pdf
  - Local PDF: `resources/lattice-survey.pdf`
- Oded Regev, "On lattices, learning with errors, random linear codes, and cryptography" – foundational LWE paper.
  - Online: https://cims.nyu.edu/~regev/papers/lwesurvey.pdf (survey-style)
  - Online: https://cims.nyu.edu/~regev/papers/qcrypto.pdf (original STOC paper)
  - Local PDFs: `resources/lwesurvey.pdf`, `resources/qcrypto.pdf`
- Vadim Lyubashevsky et al., "Lattice Signatures and Applications" (for SIS and lattice signatures background).
  - Search: `Lyubashevsky lattice signatures and applications`.

### Videos
- Chris Peikert: "What is lattice-based cryptography?" – tutorial-style.
  - Search: `Chris Peikert lattice-based cryptography tutorial`.
- Simons Institute Bootcamp lectures on Lattices and Cryptography.
  - Search: `Simons Institute lattices and cryptography boot camp`.

Used in: Section 2 (lattices, SVP/CVP, SIS, LWE, module-LWE/SIS).

---

## Section 3 – ML-KEM / CRYSTALS-Kyber

### Primary references
- FIPS 203 – "Module-Lattice-Based Key-Encapsulation Mechanism Standard" (ML-KEM / Kyber).
  - Online index: https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-standards
  - Direct PDF: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.203.pdf
  - Local PDF: `resources/nist-fips-203-ml-kem.pdf`
- Original Kyber submission and specification (CRYSTALS-Kyber).
  - Online: https://pq-crystals.org/kyber
  - Local HTML snapshot: `resources/kyber`
  - NIST submission package: via the selected algorithms page.
    - Online: https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-standardization/selected-algorithms
    - Local HTML snapshot: `resources/selected-algorithms`
- NIST PQC FAQ – specific Kyber questions.
  - Online: https://csrc.nist.gov/Projects/post-quantum-cryptography/faqs
  - Local HTML snapshot: `resources/faqs`

### Videos
- Kyber introduction by one of the authors (e.g., Peter Schwabe, Vadim Lyubashevsky) from PQC or RWC workshops.
  - Search: `"CRYSTALS-Kyber" talk`, `PQC 2018 Kyber presentation`, `RWC Kyber`.
- Cloudflare or Google TLS team talks on PQC experiments in TLS.
  - Search: `Cloudflare post-quantum TLS Kyber`.

Used in: Section 3.1–3.6 (problem, philosophy, algebraic setting, keygen/encap/decap intuition, protocol usage).

---

## Section 4 – ML-DSA / CRYSTALS-Dilithium

### Primary references
- FIPS 204 – "Module-Lattice-Based Digital Signature Standard" (ML-DSA / Dilithium).
  - Online index: https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-standards
  - Direct PDF: https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.204.pdf
  - Local PDF: `resources/nist-fips-204-ml-dsa.pdf`
- Original Dilithium submission and specification (CRYSTALS-Dilithium).
  - Online: https://pq-crystals.org/dilithium
  - Local HTML snapshot: `resources/dilithium`
  - NIST PQC submission package via selected algorithms page.
    - Online: https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-standardization/selected-algorithms
    - Local HTML snapshot: `resources/selected-algorithms`
- Lyubashevsky, Ducas, Kiltz, Lepoint, Schwabe, Seiler, Stehlé, "CRYSTALS-Dilithium: Digital Signatures from Module Lattices".
  - Search: `CRYSTALS-Dilithium digital signatures from module lattices paper`.

### Videos
- Talks from RWC (Real World Crypto) or PQCrypto on Dilithium.
  - Search: `"CRYSTALS-Dilithium" Real World Crypto talk`.
- High-level explanation from conference tutorials.
  - Search: `Dilithium lattice signatures tutorial`.

Used in: Section 4.2–4.5 (design goals, signing/verification, security sketch, use cases).

---

## Section 5 – Falcon

### Primary references
- Falcon submission and specification.
  - Online: https://falcon-sign.info
  - Local HTML snapshot: `resources/falcon-sign.info`
- Fouque, Hoffstein, Kirchner, Lyubashevsky, Pornin, Prest, Ricosset, Seiler, Whyte, Zhang, "Falcon: Fast-Fourier Lattice-based Compact Signatures over NTRU".
  - Search: `Falcon fast-fourier lattice-based compact signatures over NTRU`.
- Background on GPV signatures and discrete Gaussian sampling.
  - Gentry, Peikert, Vaikuntanathan, "Trapdoors for Hard Lattices and New Cryptographic Constructions".

### Videos
- Falcon overview talks (e.g., at RWC or PQCrypto).
  - Search: `Falcon NTRU signatures talk`.
- Lectures on discrete Gaussian sampling in lattices.
  - Search: `discrete Gaussian sampling lattices tutorial`.

Used in: Section 5.1–5.4 (motivation, math idea, pros/cons, deployment niches).

---

## Section 6 – System Integration and Hybrid Protocols

### Primary references
- NIST PQC Migration Project (NCCoE) – migration and integration guidance.
  - Online: https://csrc.nist.gov/Projects/migration-to-post-quantum-cryptography-nccoe
  - Local PDF (project description): `resources/pqc-migration-project-description-final.pdf`
- IETF drafts and RFCs for PQC in TLS and IKEv2.
  - Example: `Hybrid key exchange in TLS 1.3` Internet-Drafts (look for `draft-ietf-tls-hybrid-design` or similar).
  - PQC-in-TLS experiments by Cloudflare, Google, etc.
- ENISA / ETSI reports on PQC deployment.
  - Search: `ENISA post-quantum cryptography deployment`.

### Videos
- IETF or NIST webinars on PQC migration and hybrid key exchange.
  - Search: `IETF PQC hybrid TLS webinar`.
- Cloudflare and Google Chrome team talks about real-world experiments with Kyber in TLS.
  - Search: `post-quantum TLS Cloudflare Google experiment`.

Used in: Section 6.1–6.3 (mapping KEM + signatures into protocols, hybrid modes).

---

## Section 7 – PQC on Constrained IoT Devices

### Primary references
- NIST NCCoE PQC migration for enterprise and IoT context.
  - Online: https://csrc.nist.gov/Projects/migration-to-post-quantum-cryptography-nccoe
  - Local PDF (project description): `resources/pqc-migration-project-description-final.pdf`
- Benchmarks and implementation papers on PQC for microcontrollers.
  - For Kyber: look for papers and code labeled as `Kyber on ARM Cortex-M`.
    - Example search terms: `CRYSTALS-Kyber ARM Cortex-M4 implementation`.
  - For Dilithium and Falcon: `CRYSTALS-Dilithium microcontroller`, `Falcon ARM Cortex-M implementation`.
- NIST reference and optimized implementations in their artifacts (source code bundles for each algorithm).
  - Online: https://csrc.nist.gov/projects/post-quantum-cryptography/pqc-standardization/selected-algorithms
  - Local HTML snapshot: `resources/selected-algorithms`

### Videos
- Embedded systems / IoT security conference talks on PQC.
  - Search: `post-quantum cryptography IoT microcontroller implementation`.
- Vendor or research group presentations (e.g., ARM, RISC-V vendors) on PQC benchmarks.
  - Search: `PQC on Cortex-M benchmark`.

Used in: Section 7.1–7.5 and Section 8 (resource constraints, optimization strategies, concrete IoT flows).

---

## Section 8 – Optimization Playbook and Case Studies

### Primary references
- Same as Section 7, plus implementation notes in each algorithm’s specification and reference code.
  - Kyber/Dilithium/Falcon source code comments often include optimization hints.
- Additional optimization-focused papers:
  - Search: `"constant-time" Kyber implementation`, `masking Kyber`, `side-channel resistant lattice-based cryptography`.

### Videos
- Talks focused on side-channel attacks and countermeasures for lattice-based PQC.
  - Search: `side-channel attacks on lattice-based cryptography`.

Used in: Section 8 (practical optimization checklist and performance engineering mindset).

---

## Pedagogical / Learning-Science Background

### Primary references
- Gal Elidan et al., "Towards an AI-Augmented Textbook" (LearnLM Team, Google).
  - Online abstract: https://arxiv.org/abs/2509.13348
  - Local PDF: `resources/arxiv-2509.13348-ai-augmented-textbook.pdf`
- General resources on active learning and worked examples in STEM education.
  - Search: `worked examples cognitive load`, `active learning STEM evidence`.

Used in: Overall design of `cryptography_course.md` – multiple representations, frequent check-yourself questions, modular structure.

---

## How to Use These Resources

- As you read each section of `cryptography_course.md`, pick one paper/tutorial and one video from the matching section here.
- Start with high-level talks for intuition, then dive into specifications and submissions for mathematical and implementation details.
- For implementation and IoT optimization:
  - Use the local PDFs where available for offline reading.
  - Compare optimized microcontroller implementations described in research papers with your target platform.
