#!/usr/bin/env python3
"""
Refined Thesis Visualization Generator
Abdessamad JAOUAD - M2 Big Data & IoT - January 2026

Complete, consistent, and accurate visualizations for all thesis chapters.
Focus: LZ4 compression + Kyber768 PQC for IoT endpoints

Usage: python3 generate_thesis_figures.py
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch, Rectangle
import numpy as np
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams.update({
    'font.family': 'DejaVu Sans',
    'font.size': 11,
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'savefig.facecolor': 'white',
})

COLORS = {
    'lz4': '#9b59b6', 'zlib': '#3498db', 'zstd': '#2ecc71',
    'original': '#e74c3c', 'pqc': '#f39c12', 'secure': '#27ae60',
}

OUTPUT_DIR = '.'
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Consistent benchmark data
DATA = {
    'compression': {
        'lz4': {'ratio': 3.66, 'speed': 500, 'mem': 16, 'compressed_kb': 2.73},
        'zlib': {'ratio': 5.12, 'speed': 50, 'mem': 32, 'compressed_kb': 1.95},
        'zstd': {'ratio': 5.69, 'speed': 200, 'mem': 64, 'compressed_kb': 1.76},
    },
    'pqc': {
        'kyber512': {'pk': 800, 'ct': 768}, 
        'kyber768': {'pk': 1184, 'ct': 1088},
        'kyber1024': {'pk': 1568, 'ct': 1568},
    },
    'classical': {'ecc256': 32, 'rsa2048': 256},
    'message_kb': 10.0,
}

# ============================================================================
# CHAPTER 1: CONTEXT
# ============================================================================

def create_iot_architecture():
    """3-layer IoT architecture showing solution placement"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12); ax.set_ylim(0, 8); ax.axis('off')
    
    # Layer 1: IoT Devices
    devices = [(1.5, 1.5, 'Temp\nSensors'), (4, 1.5, 'Actuators'), 
               (6.5, 1.5, 'Wearables'), (9, 1.5, 'Industrial\nSensors')]
    for x, y, label in devices:
        rect = FancyBboxPatch((x-0.6, y-0.5), 1.2, 1, boxstyle="round,pad=0.05",
                              fc=COLORS['zlib'], ec='black', lw=2)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', fontsize=9, 
                fontweight='bold', color='white')
    
    # Highlight our solution targets Layer 1
    highlight = FancyBboxPatch((0.5, 0.7), 9.5, 1.7, boxstyle="round,pad=0.1",
                               fill=False, ec='#27ae60', lw=3, ls='--')
    ax.add_patch(highlight)
    ax.text(5.25, 0.35, '🎯 PQC + LZ4 Solution Targets This Layer', 
            ha='center', fontsize=11, fontweight='bold', color='#27ae60')
    
    # Layer 2: Gateway
    gateway = FancyBboxPatch((3.5, 3.2), 5, 1.2, boxstyle="round,pad=0.05",
                             fc=COLORS['zstd'], ec='black', lw=2)
    ax.add_patch(gateway)
    ax.text(6, 3.8, 'Edge Gateway / Fog Computing', ha='center', va='center',
            fontsize=10, fontweight='bold', color='white')
    
    # Layer 3: Cloud
    cloud = FancyBboxPatch((3, 5.5), 6, 1.5, boxstyle="round,pad=0.1",
                           fc=COLORS['lz4'], ec='black', lw=2)
    ax.add_patch(cloud)
    ax.text(6, 6.25, 'Cloud Platform\n(Storage, Analytics, Applications)', 
            ha='center', va='center', fontsize=10, fontweight='bold', color='white')
    
    # Arrows
    for x, _, _ in devices:
        ax.annotate('', xy=(6, 3.2), xytext=(x, 2.4),
                   arrowprops=dict(arrowstyle='->', color='#34495e', lw=2))
    ax.annotate('', xy=(6, 5.5), xytext=(6, 4.4),
               arrowprops=dict(arrowstyle='<->', color='#34495e', lw=2.5))
    
    # Labels
    ax.text(11, 1.5, 'Layer 1:\nPerception', ha='center', fontsize=10, 
            fontweight='bold', style='italic')
    ax.text(11, 3.8, 'Layer 2:\nNetwork', ha='center', fontsize=10, 
            fontweight='bold', style='italic')
    ax.text(11, 6.25, 'Layer 3:\nApplication', ha='center', fontsize=10, 
            fontweight='bold', style='italic')
    ax.text(6, 7.5, 'Three-Layer IoT Architecture', ha='center', 
            fontsize=14, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/iot_architecture.png', dpi=300, bbox_inches='tight')
    print("✓ iot_architecture.png")
    plt.close()


def create_iot_constraints():
    """Radar chart: IoT device resource limitations"""
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    categories = ['Processing', 'Memory', 'Bandwidth', 'Energy', 'Storage', 'Security']
    N = len(categories)
    angles = [n / N * 2 * np.pi for n in range(N)] + [0]
    
    # Scale 0-10
    class0 = [2, 1, 1, 1, 2, 2] + [2]  # 8-bit
    class1 = [5, 4, 4, 4, 5, 5] + [5]  # 32-bit (our target)
    class2 = [9, 8, 8, 7, 8, 9] + [9]  # Linux
    
    ax.plot(angles, class0, 'o-', lw=2.5, label='Class 0: <10 KB RAM', 
            color='#e74c3c', ms=8)
    ax.fill(angles, class0, alpha=0.2, color='#e74c3c')
    
    ax.plot(angles, class1, 's-', lw=2.5, label='Class 1: ~32-64 KB RAM ⭐', 
            color='#f39c12', ms=8)
    ax.fill(angles, class1, alpha=0.2, color='#f39c12')
    
    ax.plot(angles, class2, '^-', lw=2.5, label='Class 2: >256 KB RAM', 
            color='#2ecc71', ms=8)
    ax.fill(angles, class2, alpha=0.2, color='#2ecc71')
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=11, fontweight='bold')
    ax.set_ylim(0, 10)
    ax.legend(loc='upper right', bbox_to_anchor=(1.4, 1.1), fontsize=10)
    ax.set_title('IoT Device Classes: Resource Capabilities\n⭐ Target: Class 1 (32-bit MCUs)', 
                 fontsize=13, fontweight='bold', pad=20)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/iot_constraints.png', dpi=300, bbox_inches='tight')
    print("✓ iot_constraints.png")
    plt.close()


def create_quantum_timeline():
    """Timeline showing quantum threat urgency"""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    events = [
        (1994, "Shor's\nAlgorithm", '#e74c3c'), (2016, "NIST PQC\nStarts", '#3498db'),
        (2019, "Quantum\nSupremacy", '#f39c12'), (2022, "Kyber\nSelected", '#2ecc71'),
        (2024, "FIPS 203/204", '#9b59b6'), (2030, "CRQC\nExpected", '#c0392b'),
    ]
    
    ax.plot([1992, 2036], [0, 0], 'k-', lw=3)
    
    for i, (year, label, color) in enumerate(events):
        ax.plot(year, 0, 'o', ms=18, color=color, zorder=5, mec='black', mew=2)
        y_off = 0.6 if i % 2 == 0 else -0.6
        y_txt = 1.3 if i % 2 == 0 else -1.3
        ax.plot([year, year], [0, y_off], color=color, lw=2.5)
        ax.text(year, y_txt, f"{year}\n{label}", ha='center', va='center',
                fontsize=9, fontweight='bold', bbox=dict(boxstyle='round,pad=0.5',
                fc=color, alpha=0.3, ec=color, lw=2))
    
    # Threat window
    ax.axvspan(2020, 2035, alpha=0.15, color='red', zorder=1)
    ax.text(2027.5, 2.2, '"Harvest Now, Decrypt Later" Threat', ha='center',
            fontsize=12, color='#c0392b', fontweight='bold',
            bbox=dict(boxstyle='round', fc='#fadbd8', ec='#c0392b', lw=2))
    
    ax.set_xlim(1992, 2036); ax.set_ylim(-2.8, 2.8)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_title('Timeline: Quantum Computing Threat to Classical Cryptography', 
                 fontsize=14, fontweight='bold')
    ax.set_yticks([])
    for spine in ['left', 'right', 'top']: ax.spines[spine].set_visible(False)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/quantum_timeline.png', dpi=300, bbox_inches='tight')
    print("✓ quantum_timeline.png")
    plt.close()


# ============================================================================
# CHAPTER 2: PQC
# ============================================================================

def create_pqc_families_comparison():
    """Bar chart justifying lattice-based choice"""
    fig, ax = plt.subplots(figsize=(13, 7))
    
    families = ['Lattice\n(Kyber)', 'Hash\n(SPHINCS+)', 'Code\n(McEliece)', 'Multivar.\n(Rainbow†)']
    metrics = {
        'Key Size': [8, 3, 1, 7], 'Speed': [9, 4, 6, 8],
        'Security': [8, 10, 9, 3], 'IoT Fit': [9, 5, 2, 4],
    }
    
    x = np.arange(len(families))
    width = 0.2
    colors_list = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
    
    for i, ((attr, vals), col) in enumerate(zip(metrics.items(), colors_list)):
        bars = ax.bar(x + width*i, vals, width, label=attr, color=col, ec='black', lw=1.2)
        for bar in bars:
            h = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2, h + 0.2, f'{int(h)}',
                   ha='center', fontsize=9, fontweight='bold')
    
    # Highlight lattice-based
    highlight = Rectangle((-0.5, 0), 1, 12, fill=False, ec='#27ae60', lw=3, ls='--')
    ax.add_patch(highlight)
    ax.text(0, 11.5, '⭐ NIST Selected\n(Best for IoT)', fontsize=10,
            color='#27ae60', fontweight='bold', ha='center')
    ax.text(3, 1, '†Broken 2022', fontsize=8, color='#c0392b', ha='center', style='italic')
    
    ax.set_ylabel('Score (0-10)', fontsize=12, fontweight='bold')
    ax.set_xlabel('PQC Algorithm Family', fontsize=12, fontweight='bold')
    ax.set_title('PQC Families Comparison → Justifying Kyber Choice', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x + width*1.5); ax.set_xticklabels(families)
    ax.legend(loc='upper right', fontsize=10, ncol=2)
    ax.set_ylim(0, 12); ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/pqc_families_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ pqc_families_comparison.png")
    plt.close()


def create_pqc_sizes():
    """PQC vs classical key sizes - showing large overhead"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Kyber variants
    kyber_names = ['Kyber512', 'Kyber768', 'Kyber1024']
    pk = [DATA['pqc'][k]['pk'] for k in ['kyber512', 'kyber768', 'kyber1024']]
    ct = [DATA['pqc'][k]['ct'] for k in ['kyber512', 'kyber768', 'kyber1024']]
    
    x = np.arange(3); width = 0.35
    bars1 = ax1.bar(x - width/2, pk, width, label='Public Key', color='#3498db', ec='black', lw=1.5)
    bars2 = ax1.bar(x + width/2, ct, width, label='Ciphertext', color='#e74c3c', ec='black', lw=1.5)
    
    # Highlight Kyber768
    highlight = Rectangle((0.6, 0), 0.8, 1700, fill=False, ec='#27ae60', lw=3, ls='--')
    ax1.add_patch(highlight)
    ax1.text(1, 1650, '⭐ Recommended\n(NIST-3)', ha='center', 
            fontsize=10, color='#27ae60', fontweight='bold')
    
    for bars in [bars1, bars2]:
        for bar in bars:
            h = bar.get_height()
            ax1.text(bar.get_x() + bar.get_width()/2, h + 50, f'{int(h)} B',
                    ha='center', fontsize=9, fontweight='bold')
    
    ax1.set_xlabel('Kyber Variant', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Size (bytes)', fontsize=12, fontweight='bold')
    ax1.set_title('Kyber Key & Ciphertext Sizes', fontsize=13, fontweight='bold')
    ax1.set_xticks(x); ax1.set_xticklabels(kyber_names)
    ax1.legend(fontsize=10); ax1.grid(axis='y', alpha=0.3); ax1.set_ylim(0, 1800)
    
    # Right: Classical vs PQC
    algos = ['ECC-256\n(Classical)', 'RSA-2048\n(Classical)', 'Kyber768\n(PQC)']
    sizes = [DATA['classical']['ecc256'], DATA['classical']['rsa2048'], DATA['pqc']['kyber768']['pk']]
    colors = ['#95a5a6', '#95a5a6', COLORS['pqc']]
    bars = ax2.bar(algos, sizes, color=colors, ec='black', lw=2)
    
    for i, bar in enumerate(bars):
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 40, f'{int(h)} B',
                ha='center', fontsize=11, fontweight='bold')
        if i == 2:
            mult = f'~{h/sizes[0]:.0f}x ECC\n~{h/sizes[1]:.1f}x RSA'
            ax2.text(bar.get_x() + bar.get_width()/2, h + 150, mult, ha='center',
                    fontsize=9, color='#c0392b', fontweight='bold',
                    bbox=dict(boxstyle='round', fc='#fadbd8', alpha=0.7))
    
    ax2.set_ylabel('Public Key Size (bytes)', fontsize=12, fontweight='bold')
    ax2.set_title('PQC Size Overhead', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3); ax2.set_ylim(0, 1400)
    
    fig.text(0.5, 0.02, '⚠ PQC keys 4-37x larger → Compression essential!',
             ha='center', fontsize=11, fontweight='bold', color='#c0392b',
             bbox=dict(boxstyle='round', fc='#fadbd8', ec='#c0392b', lw=2))
    
    plt.tight_layout(rect=[0, 0.05, 1, 1])
    plt.savefig(f'{OUTPUT_DIR}/pqc_sizes.png', dpi=300, bbox_inches='tight')
    print("✓ pqc_sizes.png")
    plt.close()


# ============================================================================
# CHAPTER 3: COMPRESSION (LZ4)
# ============================================================================

def create_compression_tradeoff():
    """Scatter: Speed vs Ratio with LZ4 highlighted"""
    fig, ax = plt.subplots(figsize=(11, 8))
    
    algos = {
        'RLE': (1.2, 800, 2, 100, '#e74c3c'),
        'Huffman': (1.5, 150, 4, 120, '#e67e22'),
        'LZ77': (2.3, 80, 8, 140, '#f1c40f'),
        'LZ4': (3.7, 500, 16, 400, COLORS['lz4']),
        'ZLIB': (5.1, 50, 32, 200, COLORS['zlib']),
        'Zstd': (5.7, 200, 64, 250, COLORS['zstd']),
        'Brotli': (6.2, 30, 128, 180, '#34495e'),
    }
    
    for name, (ratio, speed, mem, size, color) in algos.items():
        if name == 'LZ4':
            ax.scatter(ratio, speed, s=size, c=color, ec='black', lw=3, zorder=10, label='LZ4 ⭐')
            circle = Circle((ratio, speed), 0.4, fill=False, ec='#27ae60', lw=3, ls='--', zorder=9)
            ax.add_patch(circle)
        else:
            ax.scatter(ratio, speed, s=size, c=color, ec='black', lw=1.5, zorder=5, alpha=0.7)
        
        offset_y = 40 if name == 'LZ4' else 20
        fontweight = 'bold' if name == 'LZ4' else 'normal'
        fontsize = 11 if name == 'LZ4' else 9
        ax.annotate(f'{name}\n({mem} KB)', (ratio, speed), xytext=(0.15, offset_y),
                   textcoords='offset points', fontsize=fontsize, fontweight=fontweight,
                   bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.8, ec=color))
    
    ax.annotate('⭐ Optimal for IoT:\n• Fast (real-time)\n• Low memory\n• Good compression',
               xy=(3.7, 500), xytext=(5.5, 650),
               arrowprops=dict(arrowstyle='->', color='#27ae60', lw=3),
               fontsize=11, color='#27ae60', fontweight='bold',
               bbox=dict(boxstyle='round', fc='#d5f5e3', ec='#27ae60', lw=2))
    
    ax.set_xlabel('Compression Ratio (higher = better)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speed (MB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Compression Trade-offs (Bubble = Memory)', fontsize=14, fontweight='bold')
    ax.set_xlim(0.8, 7); ax.set_ylim(0, 900)
    ax.grid(True, alpha=0.3, ls='--'); ax.legend(loc='upper right', fontsize=11)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/compression_tradeoff.png', dpi=300, bbox_inches='tight')
    print("✓ compression_tradeoff.png")
    plt.close()


def create_memory_footprint():
    """Memory footprint: LZ4+Kyber fits in 32KB"""
    fig, ax = plt.subplots(figsize=(11, 7))
    
    components = ['LZ4', 'ZLIB', 'Zstd', 'Kyber768\nStack', 'LZ4 +\nKyber768']
    memory = [16, 32, 64, 10, 26]
    colors = [COLORS['lz4'], COLORS['zlib'], COLORS['zstd'], COLORS['pqc'], '#27ae60']
    
    bars = ax.bar(components, memory, color=colors, ec='black', lw=2)
    
    ax.axhline(32, color='#f39c12', ls='--', lw=2.5, label='32 KB MCU', zorder=3)
    ax.axhline(64, color='#e74c3c', ls=':', lw=2.5, label='64 KB MCU', zorder=3)
    
    for bar, val in zip(bars, memory):
        ax.text(bar.get_x() + bar.get_width()/2, val + 1.5, f'{val} KB',
                ha='center', fontsize=12, fontweight='bold')
        if val <= 32:
            ax.text(bar.get_x() + bar.get_width()/2, val + 5, '✓ Fits 32KB',
                   ha='center', fontsize=9, color='#27ae60', fontweight='bold')
        elif val <= 64:
            ax.text(bar.get_x() + bar.get_width()/2, val + 5, '⚠ 64KB only',
                   ha='center', fontsize=9, color='#f39c12', fontweight='bold')
        else:
            ax.text(bar.get_x() + bar.get_width()/2, val + 5, '✗ Too large',
                   ha='center', fontsize=9, color='#c0392b', fontweight='bold')
    
    ax.annotate('✓ LZ4+Kyber fits\nin typical MCU!', xy=(4, 26), xytext=(3, 50),
               arrowprops=dict(arrowstyle='->', color='green', lw=2),
               fontsize=11, color='green', fontweight='bold')
    
    ax.set_ylabel('Memory (KB)', fontsize=12, fontweight='bold')
    ax.set_title('Memory Footprint: Compression + PQC\n(Critical for IoT)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10); ax.set_ylim(0, 80); ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/memory_footprint.png', dpi=300, bbox_inches='tight')
    print("✓ memory_footprint.png")
    plt.close()


def create_speed_vs_ratio():
    """Alternative view: Speed vs Ratio with memory bubbles"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    data_comp = DATA['compression']
    for name, vals in data_comp.items():
        size = vals['mem'] * 10
        color = COLORS[name]
        ax.scatter(vals['ratio'], vals['speed'], s=size, c=color, ec='black',
                  lw=2, alpha=0.8, zorder=5, label=f"{name.upper()} ({vals['mem']} KB)")
        ax.annotate(name.upper(), (vals['ratio'], vals['speed']), xytext=(10, 10),
                   textcoords='offset points', fontsize=10, fontweight='bold')
    
    ax.set_xlabel('Compression Ratio', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speed (MB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Speed vs Ratio vs Memory\n(Bubble size = Memory footprint)', 
                fontsize=14, fontweight='bold')
    ax.legend(fontsize=10); ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/speed_vs_ratio.png', dpi=300, bbox_inches='tight')
    print("✓ speed_vs_ratio.png")
    plt.close()


def create_compression_comparison():
    """Bar chart: LZ4 is 10x faster than ZLIB"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    data_comp = DATA['compression']
    algos = ['LZ4', 'ZLIB', 'Zstd']
    ratios = [data_comp[a.lower()]['ratio'] for a in algos]
    speeds = [data_comp[a.lower()]['speed'] for a in algos]
    colors = [COLORS[a.lower()] for a in algos]
    
    # Compression ratio
    bars1 = ax1.bar(algos, ratios, color=colors, ec='black', lw=1.5)
    for bar in bars1:
        h = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2, h + 0.1, f'{h:.2f}x',
                ha='center', fontsize=11, fontweight='bold')
    ax1.text(0, ratios[0] + 0.4, '⭐ IoT Choice', ha='center', 
            fontsize=9, color='#27ae60', fontweight='bold')
    ax1.set_ylabel('Compression Ratio', fontsize=12, fontweight='bold')
    ax1.set_title('Compression Ratio (Higher = Better)', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Speed
    bars2 = ax2.bar(algos, speeds, color=colors, ec='black', lw=1.5)
    for bar in bars2:
        h = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, h + 10, f'{int(h)}',
                ha='center', fontsize=11, fontweight='bold')
    ax2.annotate('10x faster\nthan ZLIB!', xy=(0, 500), xytext=(1, 400),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, color='red', fontweight='bold')
    ax2.set_ylabel('Speed (MB/s)', fontsize=12, fontweight='bold')
    ax2.set_title('Speed (Higher = Better)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/compression_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ compression_comparison.png")
    plt.close()


# ============================================================================
# CHAPTER 4: COMBINED SOLUTION
# ============================================================================

def create_system_architecture():
    """Pipeline: Input → LZ4 → Kyber → AES → Output"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14); ax.set_ylim(0, 8); ax.axis('off')
    
    boxes = [
        (0.5, 3, 2, 2, COLORS['original'], 'Raw IoT\nData', f"{DATA['message_kb']} KB"),
        (3.5, 3, 2.5, 2, COLORS['lz4'], '⭐ LZ4\nCompression', f"~{DATA['compression']['lz4']['compressed_kb']:.1f} KB"),
        (7, 5.5, 2.5, 2, COLORS['pqc'], 'Kyber768\nKEM', 'Shared Secret'),
        (7, 2.5, 2.5, 2, COLORS['original'], 'AES-256\nGCM', '+16 B tag'),
        (10.5, 3, 2.5, 2, COLORS['secure'], 'Secure\nPacket', '~3.8 KB total'),
    ]
    
    for x, y, w, h, color, label, detail in boxes:
        rect = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                              fc=color, ec='black', lw=2)
        ax.add_patch(rect)
        ax.text(x + w/2, y + h/2 + 0.2, label, ha='center', va='center',
                fontsize=11, fontweight='bold', color='white')
        ax.text(x + w/2, y + h/2 - 0.3, detail, ha='center', va='center',
                fontsize=9, color='white', fontweight='bold')
    
    # Arrows
    ax.annotate('', xy=(3.5, 4), xytext=(2.5, 4),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(7, 4), xytext=(6, 4),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(8.25, 5.5), xytext=(8.25, 4.5),
               arrowprops=dict(arrowstyle='->', color='#9b59b6', lw=2))
    ax.annotate('', xy=(10.5, 4), xytext=(9.5, 4),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Title
    ax.text(7, 7.5, 'Combined Approach: Kyber768 + LZ4', ha='center',
            fontsize=14, fontweight='bold', color='#27ae60',
            bbox=dict(boxstyle='round', fc='#d5f5e3', ec='#27ae60', lw=2))
    
    ax.text(7, 0.8, 'Pipeline: Compress (LZ4) → Key Exchange (Kyber) → Encrypt (AES-GCM) → Transmit',
            ha='center', fontsize=11, fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/system_architecture.png', dpi=300, bbox_inches='tight')
    print("✓ system_architecture.png")
    plt.close()


def create_bandwidth_breakdown():
    """Waterfall chart showing bandwidth savings"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    msg_kb = DATA['message_kb']
    comp_kb = DATA['compression']['lz4']['compressed_kb']
    pqc_kb = DATA['pqc']['kyber768']['ct'] / 1024
    total_kb = comp_kb + pqc_kb
    
    categories = ['Original\nData', 'After LZ4\nCompression', 'PQC\nOverhead', 'Final\nPacket']
    sizes = [msg_kb, comp_kb, pqc_kb, total_kb]
    colors = [COLORS['original'], COLORS['lz4'], COLORS['pqc'], COLORS['secure']]
    
    bars = ax.bar(categories, sizes, color=colors, ec='black', lw=2)
    
    for bar, val in zip(bars, sizes):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.3,
                f'{val:.2f} KB', ha='center', fontsize=12, fontweight='bold')
    
    # Savings arrows
    savings_pct = (1 - comp_kb/msg_kb) * 100
    ax.annotate('', xy=(1, comp_kb), xytext=(0, msg_kb),
               arrowprops=dict(arrowstyle='->', color='green', lw=3))
    ax.text(0.5, (msg_kb + comp_kb)/2, f'{savings_pct:.0f}%\nsavings', 
            fontsize=11, fontweight='bold', color='#27ae60', ha='center',
            bbox=dict(boxstyle='round', fc='#d5f5e3'))
    
    net_savings_pct = (1 - total_kb/msg_kb) * 100
    ax.annotate('', xy=(3, total_kb), xytext=(0, msg_kb),
               arrowprops=dict(arrowstyle='->', color='blue', lw=3, ls='--'))
    ax.text(1.5, msg_kb - 1.5, f'Net: {net_savings_pct:.0f}% savings', 
            fontsize=12, fontweight='bold', color='#3498db',
            bbox=dict(boxstyle='round', fc='#ebf5fb', ec='#3498db', lw=2))
    
    ax.set_ylabel('Size (KB)', fontsize=12, fontweight='bold')
    ax.set_title('Bandwidth Savings: LZ4 + Kyber768\n(Positive Net Savings!)', 
                fontsize=14, fontweight='bold')
    ax.set_ylim(0, msg_kb + 2)
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/bandwidth_breakdown.png', dpi=300, bbox_inches='tight')
    print("✓ bandwidth_breakdown.png")
    plt.close()


def create_workflow_diagram():
    """Simplified workflow for slides"""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('off')
    
    msg_kb = DATA['message_kb']
    comp_kb = DATA['compression']['lz4']['compressed_kb']
    pqc_kb = DATA['pqc']['kyber768']['ct'] / 1024
    total_kb = comp_kb + pqc_kb
    
    boxes = [
        {'x': 0.05, 'y': 0.5, 'w': 0.15, 'h': 0.25, 'color': COLORS['original'], 
         'label': 'Original\nMessage', 'size': f"{msg_kb:.0f} KB"},
        {'x': 0.28, 'y': 0.5, 'w': 0.15, 'h': 0.25, 'color': COLORS['lz4'],
         'label': 'LZ4\nCompressed', 'size': f"{comp_kb:.1f} KB"},
        {'x': 0.51, 'y': 0.5, 'w': 0.15, 'h': 0.25, 'color': COLORS['pqc'],
         'label': 'Kyber768\nEncrypted', 'size': f"+{pqc_kb:.2f} KB"},
        {'x': 0.74, 'y': 0.5, 'w': 0.18, 'h': 0.25, 'color': COLORS['secure'],
         'label': 'Final\nPacket', 'size': f"{total_kb:.1f} KB"}
    ]
    
    for box in boxes:
        rect = FancyBboxPatch((box['x'], box['y']), box['w'], box['h'],
                              boxstyle="round,pad=0.02", fc=box['color'], 
                              ec='black', lw=2, alpha=0.9)
        ax.add_patch(rect)
        ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2 + 0.03,
               box['label'], ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')
        ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2 - 0.06,
               box['size'], ha='center', va='center',
               fontsize=9, fontweight='bold', color='white')
    
    # Arrows
    for x in [0.21, 0.44, 0.67]:
        ax.annotate('', xy=(x + 0.05, 0.625), xytext=(x, 0.625),
                   arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    ax.text(0.5, 0.9, 'PQC + LZ4 Compression Workflow', ha='center',
           fontsize=16, fontweight='bold')
    
    savings = (1 - total_kb/msg_kb) * 100
    ax.text(0.5, 0.15, f"Bandwidth Savings: {savings:.0f}%", ha='center',
           fontsize=18, fontweight='bold', color='#27ae60',
           bbox=dict(boxstyle='round', fc='#d5f4e6', ec='#27ae60', lw=2))
    
    ax.set_xlim(0, 1); ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/workflow_diagram.png', dpi=300, bbox_inches='tight')
    print("✓ workflow_diagram.png")
    plt.close()


# ============================================================================
# CHAPTER 5: RESULTS
# ============================================================================

def create_combined_comparison():
    """Final proof: PQC+LZ4 < original insecure data"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    msg_kb = DATA['message_kb']
    
    # Left: Size comparison for all compression methods
    configs = []
    transmitted = []
    colors_list = []
    
    for comp in ['lz4', 'zlib', 'zstd']:
        comp_kb = DATA['compression'][comp]['compressed_kb']
        pqc_kb = DATA['pqc']['kyber768']['ct'] / 1024
        total = comp_kb + pqc_kb
        configs.append(f"Kyber768\n+{comp.upper()}")
        transmitted.append(total)
        colors_list.append(COLORS[comp])
    
    x = np.arange(len(configs))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, [msg_kb]*3, width, label='Original (Insecure)',
                   color='#e74c3c', ec='black', lw=1.5, alpha=0.7)
    bars2 = ax1.bar(x + width/2, transmitted, width, label='After PQC+Compress',
                   color=colors_list, ec='black', lw=1.5)
    
    ax1.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Size (KB)', fontsize=12, fontweight='bold')
    ax1.set_title('Transmission Size: Secure < Insecure!', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, fontsize=10)
    ax1.legend(fontsize=10)
    ax1.grid(axis='y', alpha=0.3)
    
    # Right: Bandwidth savings
    savings = [(1 - t/msg_kb) * 100 for t in transmitted]
    bars = ax2.bar(configs, savings, color=colors_list, ec='black', lw=1.5)
    
    ax2.axhline(60, color='gray', ls='--', alpha=0.5, label='60% threshold')
    
    for i, bar in enumerate(bars):
        h = bar.get_height()
        label = f'{h:.1f}%'
        if 'LZ4' in configs[i]:
            label += '\n(Lowest memory!)'
        ax2.text(bar.get_x() + bar.get_width()/2, h + 1, label,
                ha='center', fontweight='bold', fontsize=10)
    
    ax2.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bandwidth Savings (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Bandwidth Savings', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/combined_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ combined_comparison.png")
    plt.close()


def create_summary_table():
    """Clean data table of exact savings and memory usage"""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('tight'); ax.axis('off')
    
    msg_kb = DATA['message_kb']
    header = ['Configuration', 'Original\n(KB)', 'Compressed\n(KB)', 'Total Tx\n(KB)', 
              'Savings\n(%)', 'Memory\n(KB)']
    
    table_data = [header]
    for comp in ['lz4', 'zlib', 'zstd']:
        comp_kb = DATA['compression'][comp]['compressed_kb']
        pqc_kb = DATA['pqc']['kyber768']['ct'] / 1024
        total = comp_kb + pqc_kb
        savings = (1 - total/msg_kb) * 100
        mem = DATA['compression'][comp]['mem']
        
        row = [
            f"Kyber768 + {comp.upper()}",
            f"{msg_kb:.1f}",
            f"{comp_kb:.2f}",
            f"{total:.2f}",
            f"{savings:.1f}",
            f"{mem}"
        ]
        table_data.append(row)
    
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.25, 0.12, 0.12, 0.12, 0.12, 0.12])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.2)
    
    # Style header
    for i in range(6):
        cell = table[(0, i)]
        cell.set_facecolor('#3498db')
        cell.set_text_props(weight='bold', color='white')
    
    # Style data rows
    for i in range(1, 4):
        for j in range(6):
            cell = table[(i, j)]
            if 'LZ4' in table_data[i][0]:
                cell.set_facecolor('#e8daef')  # Light purple
            else:
                cell.set_facecolor('#ecf0f1')
            if j == 4:  # Savings
                cell.set_text_props(weight='bold', color='#27ae60')
    
    ax.text(0.5, 0.95, 'Benchmark Results: Kyber768 + Compression', ha='center',
           fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    ax.text(0.5, 0.05, '⭐ LZ4 recommended: Lowest memory + positive bandwidth savings',
           ha='center', fontsize=11, color='#9b59b6', fontweight='bold', 
           transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig(f'{OUTPUT_DIR}/summary_table.png', dpi=300, bbox_inches='tight')
    print("✓ summary_table.png")
    plt.close()


# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "="*70)
    print("THESIS VISUALIZATION GENERATOR - LZ4 + Kyber768 for IoT")
    print("="*70 + "\n")
    
    print("Chapter 1: Context")
    create_iot_architecture()
    create_iot_constraints()
    create_quantum_timeline()
    
    print("\nChapter 2: Post-Quantum Cryptography")
    create_pqc_families_comparison()
    create_pqc_sizes()
    
    print("\nChapter 3: Compression Selection (LZ4)")
    create_compression_tradeoff()
    create_memory_footprint()
    create_speed_vs_ratio()
    create_compression_comparison()
    
    print("\nChapter 4: Combined Solution")
    create_system_architecture()
    create_bandwidth_breakdown()
    create_workflow_diagram()
    
    print("\nChapter 5: Results")
    create_combined_comparison()
    create_summary_table()
    
    print("\n" + "="*70)
    print(f"✅ ALL FIGURES GENERATED IN: {OUTPUT_DIR}/")
    print("="*70)
    print("\nGenerated files:")
    files = [
        "iot_architecture.png", "iot_constraints.png", "quantum_timeline.png",
        "pqc_families_comparison.png", "pqc_sizes.png",
        "compression_tradeoff.png", "memory_footprint.png", 
        "speed_vs_ratio.png", "compression_comparison.png",
        "system_architecture.png", "bandwidth_breakdown.png", "workflow_diagram.png",
        "combined_comparison.png", "summary_table.png"
    ]
    for f in files:
        print(f"  • {f}")
    print()


if __name__ == "__main__":
    main()