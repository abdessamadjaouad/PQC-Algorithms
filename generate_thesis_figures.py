#!/usr/bin/env python3
"""
Generate additional figures for thesis chapters 1-4
Abdessamad JAOUAD - M2 Big Data & IoT
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle, Rectangle
import numpy as np
import matplotlib
matplotlib.use('Agg')

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['font.size'] = 11

def create_iot_architecture():
    """Chapter 1: IoT Architecture Diagram"""
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    # Colors
    colors = {
        'device': '#3498db',
        'gateway': '#2ecc71', 
        'cloud': '#9b59b6',
        'edge': '#e74c3c',
        'arrow': '#34495e'
    }
    
    # Layer 1: IoT Devices (bottom)
    devices = [
        (1.5, 1.5, 'Sensors'),
        (4, 1.5, 'Actuators'),
        (6.5, 1.5, 'Wearables'),
        (9, 1.5, 'Smart\nDevices')
    ]
    
    for x, y, label in devices:
        rect = FancyBboxPatch((x-0.6, y-0.5), 1.2, 1, 
                              boxstyle="round,pad=0.05",
                              facecolor=colors['device'], 
                              edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        ax.text(x, y, label, ha='center', va='center', 
                fontsize=9, fontweight='bold', color='white')
    
    # Layer 2: Edge/Gateway (middle)
    gateway = FancyBboxPatch((4, 3.2), 4, 1.2,
                             boxstyle="round,pad=0.05",
                             facecolor=colors['gateway'],
                             edgecolor='black', linewidth=2)
    ax.add_patch(gateway)
    ax.text(6, 3.8, 'Edge Gateway / Fog Computing', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    # Layer 3: Cloud (top)
    cloud = FancyBboxPatch((3, 5.5), 6, 1.5,
                           boxstyle="round,pad=0.1",
                           facecolor=colors['cloud'],
                           edgecolor='black', linewidth=2)
    ax.add_patch(cloud)
    ax.text(6, 6.25, 'Cloud Platform\n(Storage, Analytics, Services)', 
            ha='center', va='center', fontsize=11, fontweight='bold', color='white')
    
    # Arrows
    for x, _, _ in devices:
        ax.annotate('', xy=(6, 3.2), xytext=(x, 2),
                   arrowprops=dict(arrowstyle='->', color=colors['arrow'], lw=1.5))
    
    ax.annotate('', xy=(6, 5.5), xytext=(6, 4.4),
               arrowprops=dict(arrowstyle='<->', color=colors['arrow'], lw=2))
    
    # Labels
    ax.text(6, 0.3, 'Perception Layer', ha='center', fontsize=12, 
            fontweight='bold', style='italic')
    ax.text(10.5, 3.8, 'Network Layer', ha='center', fontsize=12,
            fontweight='bold', style='italic')
    ax.text(10.5, 6.25, 'Application Layer', ha='center', fontsize=12,
            fontweight='bold', style='italic')
    
    # Title
    ax.text(6, 7.5, 'Three-Layer IoT Architecture', ha='center', 
            fontsize=14, fontweight='bold')
    
    # Security concerns (side annotations)
    concerns = [
        (0.3, 6, '• Data Privacy\n• Access Control'),
        (0.3, 3.5, '• Secure Comm.\n• Authentication'),
        (0.3, 1.2, '• Physical Security\n• Resource Limits')
    ]
    for x, y, text in concerns:
        ax.text(x, y, text, fontsize=8, color='#c0392b', va='center')
    
    plt.tight_layout()
    plt.savefig('thesis/figures/iot_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Created: iot_architecture.png")
    plt.close()


def create_quantum_threat_timeline():
    """Chapter 1: Quantum Threat Timeline"""
    fig, ax = plt.subplots(figsize=(12, 5))
    
    # Timeline data
    events = [
        (1994, "Shor's Algorithm\nPublished", '#e74c3c'),
        (2016, "NIST PQC\nCompetition\nAnnounced", '#3498db'),
        (2019, "Google\nQuantum\nSupremacy", '#f39c12'),
        (2022, "NIST Selects\nKyber, Dilithium", '#2ecc71'),
        (2024, "FIPS 203/204\nStandards\nPublished", '#9b59b6'),
        (2030, "Crypto-relevant\nQuantum\n(Estimated)", '#c0392b')
    ]
    
    years = [e[0] for e in events]
    
    # Draw timeline
    ax.plot([1990, 2035], [0, 0], 'k-', linewidth=3)
    
    for i, (year, label, color) in enumerate(events):
        # Marker
        ax.plot(year, 0, 'o', markersize=15, color=color, zorder=5)
        
        # Alternating positions
        y_offset = 0.5 if i % 2 == 0 else -0.5
        y_text = 1.2 if i % 2 == 0 else -1.2
        
        # Connector line
        ax.plot([year, year], [0, y_offset], color=color, linewidth=2)
        
        # Label
        ax.text(year, y_text, f"{year}\n{label}", ha='center', va='center',
                fontsize=9, fontweight='bold',
                bbox=dict(boxstyle='round', facecolor=color, alpha=0.2))
    
    # Harvest now, decrypt later zone
    ax.axvspan(2020, 2035, alpha=0.1, color='red')
    ax.text(2027.5, 2, '"Harvest Now, Decrypt Later"\nThreat Window', 
            ha='center', fontsize=10, color='#c0392b', fontweight='bold')
    
    ax.set_xlim(1990, 2038)
    ax.set_ylim(-2.5, 2.5)
    ax.set_xlabel('Year', fontsize=12, fontweight='bold')
    ax.set_title('Timeline of Quantum Computing Threat to Cryptography', 
                 fontsize=14, fontweight='bold')
    ax.set_yticks([])
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('thesis/figures/quantum_timeline.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: quantum_timeline.png")
    plt.close()


def create_pqc_families_comparison():
    """Chapter 2: PQC Algorithm Families Comparison"""
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # Data for PQC families
    families = ['Lattice-based\n(Kyber, Dilithium)', 'Hash-based\n(SPHINCS+)', 
                'Code-based\n(Classic McEliece)', 'Multivariate\n(Rainbow†)']
    
    # Metrics (normalized 0-10 scale, higher is better)
    metrics = {
        'Key Size Efficiency': [8, 3, 2, 7],
        'Performance Speed': [9, 4, 6, 8],
        'Security Confidence': [8, 10, 9, 5],
        'Implementation Maturity': [9, 7, 6, 4],
    }
    
    x = np.arange(len(families))
    width = 0.2
    multiplier = 0
    
    colors = ['#3498db', '#2ecc71', '#e74c3c', '#9b59b6']
    
    for (attribute, measurement), color in zip(metrics.items(), colors):
        offset = width * multiplier
        bars = ax.bar(x + offset, measurement, width, label=attribute, color=color,
                     edgecolor='black', linewidth=1)
        multiplier += 1
    
    ax.set_ylabel('Score (0-10, higher is better)', fontsize=12, fontweight='bold')
    ax.set_xlabel('PQC Algorithm Family', fontsize=12, fontweight='bold')
    ax.set_title('Comparison of Post-Quantum Cryptography Families', 
                 fontsize=14, fontweight='bold')
    ax.set_xticks(x + width * 1.5)
    ax.set_xticklabels(families)
    ax.legend(loc='upper right', fontsize=10)
    ax.set_ylim(0, 12)
    ax.axhline(y=7, color='gray', linestyle='--', alpha=0.5, label='Threshold')
    
    # Add note about Rainbow
    ax.text(3, 1, '†Broken in 2022', fontsize=8, color='#c0392b', ha='center')
    
    # Highlight NIST selection
    ax.axvspan(-0.4, 0.8, alpha=0.1, color='green')
    ax.text(0.2, 11.3, 'NIST Selected', fontsize=10, color='#27ae60', 
            fontweight='bold', ha='center')
    
    plt.tight_layout()
    plt.savefig('thesis/figures/pqc_families_comparison.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: pqc_families_comparison.png")
    plt.close()


def create_pqc_vs_classical():
    """Chapter 2: PQC vs Classical Key Sizes"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    algorithms = ['RSA-2048', 'RSA-3072', 'ECC P-256', 'Kyber-512', 'Kyber-768', 'Kyber-1024']
    public_key = [256, 384, 64, 800, 1184, 1568]
    security_level = ['112-bit', '128-bit', '128-bit', 'Level 1', 'Level 3', 'Level 5']
    quantum_safe = [False, False, False, True, True, True]
    
    colors = ['#e74c3c' if not qs else '#2ecc71' for qs in quantum_safe]
    
    bars = ax.barh(algorithms, public_key, color=colors, edgecolor='black', linewidth=1.5)
    
    # Add security level labels
    for i, (bar, sec) in enumerate(zip(bars, security_level)):
        width = bar.get_width()
        ax.text(width + 30, bar.get_y() + bar.get_height()/2, 
                f'{sec}', va='center', fontsize=9)
    
    ax.set_xlabel('Public Key Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_title('Public Key Sizes: Classical vs Post-Quantum', fontsize=14, fontweight='bold')
    
    # Legend
    legend_elements = [mpatches.Patch(facecolor='#e74c3c', label='Quantum Vulnerable'),
                       mpatches.Patch(facecolor='#2ecc71', label='Quantum Resistant')]
    ax.legend(handles=legend_elements, loc='lower right', fontsize=10)
    
    ax.set_xlim(0, 2000)
    
    plt.tight_layout()
    plt.savefig('thesis/figures/pqc_vs_classical.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: pqc_vs_classical.png")
    plt.close()


def create_compression_algorithm_comparison():
    """Chapter 3: Compression Algorithm Performance"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    algorithms = ['RLE', 'Huffman', 'LZ77', 'LZ78', 'DEFLATE\n(ZLIB)', 'LZ4', 'Zstandard', 'Brotli']
    
    # Compression ratio (higher is better)
    compression_ratio = [1.2, 1.5, 2.5, 2.3, 3.5, 2.2, 4.0, 4.5]
    
    # Speed (MB/s, compression)
    speed = [500, 150, 80, 70, 50, 400, 200, 30]
    
    colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(algorithms)))
    
    # Plot 1: Compression Ratio
    bars1 = ax1.bar(algorithms, compression_ratio, color=colors, edgecolor='black', linewidth=1)
    ax1.set_ylabel('Compression Ratio', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax1.set_title('Compression Ratio Comparison\n(Higher is Better)', fontsize=12, fontweight='bold')
    ax1.tick_params(axis='x', rotation=45)
    ax1.axhline(y=3.5, color='#27ae60', linestyle='--', linewidth=2, label='ZLIB baseline')
    ax1.legend()
    
    # Add value labels
    for bar, val in zip(bars1, compression_ratio):
        ax1.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.1, 
                f'{val:.1f}x', ha='center', fontsize=9)
    
    # Plot 2: Speed
    bars2 = ax2.bar(algorithms, speed, color=colors, edgecolor='black', linewidth=1)
    ax2.set_ylabel('Speed (MB/s)', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Algorithm', fontsize=12, fontweight='bold')
    ax2.set_title('Compression Speed Comparison\n(Higher is Better)', fontsize=12, fontweight='bold')
    ax2.tick_params(axis='x', rotation=45)
    
    # Highlight IoT-suitable algorithms
    ax2.axhspan(50, 400, alpha=0.1, color='green')
    ax2.text(3.5, 420, 'IoT-Suitable Range', fontsize=10, color='#27ae60', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig('thesis/figures/compression_comparison_detailed.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: compression_comparison_detailed.png")
    plt.close()


def create_compression_tradeoff():
    """Chapter 3: Compression Ratio vs Speed Tradeoff"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    algorithms = {
        'RLE': (1.2, 500, '#e74c3c'),
        'Huffman': (1.5, 150, '#e67e22'),
        'LZ77': (2.5, 80, '#f1c40f'),
        'LZ78': (2.3, 70, '#2ecc71'),
        'ZLIB': (3.5, 50, '#3498db'),
        'LZ4': (2.2, 400, '#9b59b6'),
        'Zstandard': (4.0, 200, '#1abc9c'),
        'Brotli': (4.5, 30, '#34495e')
    }
    
    for name, (ratio, speed, color) in algorithms.items():
        ax.scatter(ratio, speed, s=300, c=color, edgecolors='black', linewidth=2, zorder=5)
        ax.annotate(name, (ratio, speed), xytext=(10, 5), textcoords='offset points',
                   fontsize=10, fontweight='bold')
    
    # Ideal zone (high ratio, high speed)
    ax.axvspan(2.5, 5, alpha=0.1, color='green')
    ax.axhspan(100, 600, alpha=0.1, color='blue')
    
    # Mark optimal for IoT
    ellipse = plt.Circle((3.5, 50), 0.3, fill=False, color='red', linewidth=3)
    ax.add_patch(ellipse)
    ax.annotate('Recommended\nfor IoT', (3.5, 50), xytext=(4.2, 120),
               arrowprops=dict(arrowstyle='->', color='red', lw=2),
               fontsize=11, color='red', fontweight='bold')
    
    ax.set_xlabel('Compression Ratio (higher = smaller output)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Compression Speed (MB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Compression Algorithm Trade-offs: Ratio vs Speed', fontsize=14, fontweight='bold')
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0, 600)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('thesis/figures/compression_tradeoff.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: compression_tradeoff.png")
    plt.close()


def create_system_architecture():
    """Chapter 4: Combined System Architecture"""
    fig, ax = plt.subplots(figsize=(14, 8))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 8)
    ax.axis('off')
    
    colors = {
        'input': '#3498db',
        'compress': '#2ecc71',
        'pqc': '#9b59b6',
        'encrypt': '#e74c3c',
        'output': '#f39c12'
    }
    
    # Input
    rect1 = FancyBboxPatch((0.5, 3), 2, 2, boxstyle="round,pad=0.1",
                           facecolor=colors['input'], edgecolor='black', linewidth=2)
    ax.add_patch(rect1)
    ax.text(1.5, 4, 'Raw IoT\nData', ha='center', va='center', 
            fontsize=11, fontweight='bold', color='white')
    ax.text(1.5, 2.5, '100 KB', ha='center', fontsize=10, color='#7f8c8d')
    
    # Compression
    rect2 = FancyBboxPatch((3.5, 3), 2.5, 2, boxstyle="round,pad=0.1",
                           facecolor=colors['compress'], edgecolor='black', linewidth=2)
    ax.add_patch(rect2)
    ax.text(4.75, 4, 'ZLIB\nCompression', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(4.75, 2.5, '~15 KB', ha='center', fontsize=10, color='#7f8c8d')
    
    # PQC Key Exchange
    rect3 = FancyBboxPatch((7, 5.5), 2.5, 2, boxstyle="round,pad=0.1",
                           facecolor=colors['pqc'], edgecolor='black', linewidth=2)
    ax.add_patch(rect3)
    ax.text(8.25, 6.5, 'Kyber768\nKEM', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(8.25, 5.2, 'Shared Secret', ha='center', fontsize=9, color='#7f8c8d')
    
    # Symmetric Encryption
    rect4 = FancyBboxPatch((7, 2.5), 2.5, 2, boxstyle="round,pad=0.1",
                           facecolor=colors['encrypt'], edgecolor='black', linewidth=2)
    ax.add_patch(rect4)
    ax.text(8.25, 3.5, 'AES-256\nGCM', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(8.25, 2.2, '~15 KB + 16 B', ha='center', fontsize=10, color='#7f8c8d')
    
    # Output
    rect5 = FancyBboxPatch((10.5, 3), 2.5, 2, boxstyle="round,pad=0.1",
                           facecolor=colors['output'], edgecolor='black', linewidth=2)
    ax.add_patch(rect5)
    ax.text(11.75, 4, 'Secure\nPacket', ha='center', va='center',
            fontsize=11, fontweight='bold', color='white')
    ax.text(11.75, 2.5, '~13 KB total', ha='center', fontsize=10, color='#27ae60', fontweight='bold')
    
    # Arrows
    ax.annotate('', xy=(3.5, 4), xytext=(2.5, 4),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(7, 4), xytext=(6, 4),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    ax.annotate('', xy=(8.25, 5.5), xytext=(8.25, 4.5),
               arrowprops=dict(arrowstyle='->', color='#9b59b6', lw=2))
    ax.annotate('', xy=(10.5, 4), xytext=(9.5, 4),
               arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Labels
    ax.text(7, 0.8, 'Processing Pipeline: Compress → Key Exchange → Encrypt → Transmit',
            ha='center', fontsize=12, fontweight='bold')
    
    # Bandwidth calculation
    ax.text(7, 7.5, 'Combined Approach: 86.9% Bandwidth Savings',
            ha='center', fontsize=14, fontweight='bold', color='#27ae60',
            bbox=dict(boxstyle='round', facecolor='#d5f5e3', edgecolor='#27ae60'))
    
    # Security properties box
    props_box = FancyBboxPatch((11, 5.5), 2.5, 2, boxstyle="round,pad=0.1",
                               facecolor='#ecf0f1', edgecolor='#34495e', linewidth=1)
    ax.add_patch(props_box)
    ax.text(12.25, 6.5, 'Security:\n✓ Quantum-Safe\n✓ Forward Secrecy\n✓ Authenticated',
            ha='center', va='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('thesis/figures/system_architecture.png', dpi=300, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print("✓ Created: system_architecture.png")
    plt.close()


def create_bandwidth_breakdown():
    """Chapter 4: Bandwidth Savings Breakdown"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    categories = ['Original\nData', 'After\nCompression', 'PQC\nOverhead', 'Final\nPacket']
    sizes = [100, 15, 2.4, 17.4]
    colors = ['#e74c3c', '#2ecc71', '#f39c12', '#3498db']
    
    bars = ax.bar(categories, sizes, color=colors, edgecolor='black', linewidth=2)
    
    # Add value labels
    for bar, val in zip(bars, sizes):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2,
                f'{val:.1f} KB', ha='center', fontsize=12, fontweight='bold')
    
    # Draw arrows showing savings
    ax.annotate('', xy=(1, 15), xytext=(0, 100),
               arrowprops=dict(arrowstyle='->', color='green', lw=3))
    ax.text(0.5, 60, '-85%', fontsize=14, fontweight='bold', color='#27ae60')
    
    ax.annotate('', xy=(3, 17.4), xytext=(0, 100),
               arrowprops=dict(arrowstyle='->', color='blue', lw=3, ls='--'))
    ax.text(1.8, 70, 'Net: -82.6%', fontsize=12, fontweight='bold', color='#3498db')
    
    ax.set_ylabel('Size (KB)', fontsize=12, fontweight='bold')
    ax.set_title('Bandwidth Usage Breakdown', fontsize=14, fontweight='bold')
    ax.set_ylim(0, 120)
    
    plt.tight_layout()
    plt.savefig('thesis/figures/bandwidth_breakdown.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: bandwidth_breakdown.png")
    plt.close()


def create_iot_constraints():
    """Chapter 1: IoT Device Constraints Visualization"""
    fig, ax = plt.subplots(figsize=(10, 8), subplot_kw=dict(projection='polar'))
    
    categories = ['Processing\nPower', 'Memory', 'Bandwidth', 'Energy', 'Storage', 'Security']
    N = len(categories)
    
    # Data for different device classes
    constrained = [2, 2, 1, 1, 2, 2]
    moderate = [5, 5, 4, 4, 5, 4]
    powerful = [9, 8, 8, 7, 8, 8]
    
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]
    
    constrained += constrained[:1]
    moderate += moderate[:1]
    powerful += powerful[:1]
    
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, fontsize=10, fontweight='bold')
    
    ax.plot(angles, constrained, 'o-', linewidth=2, label='Class 0 (8-bit MCU)', color='#e74c3c')
    ax.fill(angles, constrained, alpha=0.25, color='#e74c3c')
    
    ax.plot(angles, moderate, 'o-', linewidth=2, label='Class 1 (32-bit MCU)', color='#f39c12')
    ax.fill(angles, moderate, alpha=0.25, color='#f39c12')
    
    ax.plot(angles, powerful, 'o-', linewidth=2, label='Class 2 (Linux-capable)', color='#2ecc71')
    ax.fill(angles, powerful, alpha=0.25, color='#2ecc71')
    
    ax.set_ylim(0, 10)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    ax.set_title('IoT Device Classes: Resource Capabilities\n(Scale: 1-10)', 
                 fontsize=13, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('thesis/figures/iot_constraints.png', dpi=300, bbox_inches='tight',
                facecolor='white')
    print("✓ Created: iot_constraints.png")
    plt.close()


def main():
    print("=" * 70)
    print("Generating Additional Thesis Figures")
    print("=" * 70)
    
    print("\n📊 Chapter 1: IoT and Security Challenges")
    create_iot_architecture()
    create_iot_constraints()
    create_quantum_threat_timeline()
    
    print("\n📊 Chapter 2: Post-Quantum Cryptography")
    create_pqc_families_comparison()
    create_pqc_vs_classical()
    
    print("\n📊 Chapter 3: Compression Algorithms")
    create_compression_algorithm_comparison()
    create_compression_tradeoff()
    
    print("\n📊 Chapter 4: Combined Approach")
    create_system_architecture()
    create_bandwidth_breakdown()
    
    print("\n" + "=" * 70)
    print("✅ All figures generated successfully!")
    print("=" * 70)


if __name__ == "__main__":
    main()
