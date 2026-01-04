# Installation Guide - PQC + Compression Implementation

## Installation de liboqs-python

### Option 1 : Installation via pip (recommandée)
```bash
pip install liboqs-python
```

### Option 2 : Installation depuis les sources
```bash
# Installer les dépendances
sudo pacman -S cmake ninja gcc python-pip

# Cloner et compiler liboqs
git clone https://github.com/open-quantum-safe/liboqs.git
cd liboqs
mkdir build && cd build
cmake -GNinja -DCMAKE_INSTALL_PREFIX=/usr/local ..
ninja
sudo ninja install

# Installer liboqs-python
cd ../..
git clone https://github.com/open-quantum-safe/liboqs-python.git
cd liboqs-python
pip install .
```

## Installation des bibliothèques de compression

```bash
pip install lz4 zstandard
```

## Vérification de l'installation

```bash
python3 -c "import oqs; print('liboqs:', oqs.__version__)"
python3 -c "import lz4; print('lz4: OK')"
python3 -c "import zstandard; print('zstandard: OK')"
```

## Scripts créés

1. **compression_demo.py** : Démonstration des algorithmes de compression (RLE, Huffman, LZ4)
2. **pqc_compression_demo.py** : Combinaison PQC + Compression
3. **benchmark_pqc_compression.py** : Benchmarks complets avec résultats
