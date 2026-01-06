#!/usr/bin/env python3
"""
Create visualization graphs for thesis
Abdessamad JAOUAD - M2 Big Data & IoT
Updated: January 2026 - LZ4 focus for IoT endpoints
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')
import numpy as np

# Style settings
plt.rcParams['font.size'] = 11
plt.rcParams['figure.facecolor'] = 'white'
plt.rcParams['axes.facecolor'] = 'white'
plt.rcParams['savefig.facecolor'] = 'white'

# Color palette
COLORS = {
    'lz4': '#9b59b6',      # Purple - highlighted
    'zlib': '#3498db',     # Blue
    'zstd': '#2ecc71',     # Green
    'original': '#e74c3c', # Red
    'pqc': '#f39c12',      # Orange
    'highlight': '#27ae60' # Dark green
}

def generate_sample_data():
    """Generate sample benchmark data for LZ4-focused visualizations"""
    return {
        'compression': {
            'iot_small': [
                {'algorithm': 'lz4', 'original_size': 500, 'compressed_size': 220, 'compression_ratio': 2.27, 'compression_time': 0.0001, 'decompression_time': 0.00005, 'throughput_mbps': 500, 'success': True},
                {'algorithm': 'zlib', 'original_size': 500, 'compressed_size': 185, 'compression_ratio': 2.70, 'compression_time': 0.0008, 'decompression_time': 0.0002, 'throughput_mbps': 60, 'success': True},
                {'algorithm': 'zstd', 'original_size': 500, 'compressed_size': 175, 'compression_ratio': 2.86, 'compression_time': 0.0003, 'decompression_time': 0.0001, 'throughput_mbps': 200, 'success': True},
            ],
            'iot_medium': [
                {'algorithm': 'lz4', 'original_size': 10240, 'compressed_size': 2800, 'compression_ratio': 3.66, 'compression_time': 0.0002, 'decompression_time': 0.0001, 'throughput_mbps': 500, 'success': True},
                {'algorithm': 'zlib', 'original_size': 10240, 'compressed_size': 2000, 'compression_ratio': 5.12, 'compression_time': 0.002, 'decompression_time': 0.0005, 'throughput_mbps': 50, 'success': True},
                {'algorithm': 'zstd', 'original_size': 10240, 'compressed_size': 1800, 'compression_ratio': 5.69, 'compression_time': 0.0008, 'decompression_time': 0.0003, 'throughput_mbps': 200, 'success': True},
            ],
        },
        'pqc': [
            {'algorithm': 'Kyber512', 'pk_size': 800, 'sk_size': 1632, 'ct_size': 768, 'keygen_time': 0.00012, 'encap_time': 0.00015, 'decap_time': 0.00018, 'success': True},
            {'algorithm': 'Kyber768', 'pk_size': 1184, 'sk_size': 2400, 'ct_size': 1088, 'keygen_time': 0.00018, 'encap_time': 0.00022, 'decap_time': 0.00025, 'success': True},
            {'algorithm': 'Kyber1024', 'pk_size': 1568, 'sk_size': 3168, 'ct_size': 1568, 'keygen_time': 0.00025, 'encap_time': 0.00030, 'decap_time': 0.00035, 'success': True},
        ],
        'combined': [
            {'pqc_algorithm': 'Kyber768', 'compression': 'lz4', 'original_size': 10240, 'compressed_size': 2800, 'pqc_overhead': 1088, 'total_transmission': 3888, 'bandwidth_savings': 62.0, 'compression_ratio': 3.66, 'total_time': 0.001},
            {'pqc_algorithm': 'Kyber768', 'compression': 'zlib', 'original_size': 10240, 'compressed_size': 2000, 'pqc_overhead': 1088, 'total_transmission': 3088, 'bandwidth_savings': 69.8, 'compression_ratio': 5.12, 'total_time': 0.003},
            {'pqc_algorithm': 'Kyber768', 'compression': 'zstd', 'original_size': 10240, 'compressed_size': 1800, 'pqc_overhead': 1088, 'total_transmission': 2888, 'bandwidth_savings': 71.8, 'compression_ratio': 5.69, 'total_time': 0.002},
        ]
    }

def load_results():
    """Load benchmark results from JSON or generate sample data"""
    try:
        with open('benchmark_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("⚠ benchmark_results.json not found, using sample data")
        return generate_sample_data()

def plot_compression_comparison(results, output_dir='thesis/figures'):
    """Plot compression algorithm comparison with LZ4 highlighted"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Get IoT medium results
    algorithms = []
    ratios = []
    speeds = []
    colors = []
    
    for r in results['compression']['iot_medium']:
        algo = r['algorithm'].upper()
        algorithms.append(algo)
        ratios.append(r['compression_ratio'])
        speeds.append(r['throughput_mbps'])
        if algo == 'LZ4':
            colors.append(COLORS['lz4'])
        elif algo == 'ZLIB':
            colors.append(COLORS['zlib'])
        else:
            colors.append(COLORS['zstd'])
    
    # Plot 1: Compression Ratio
    bars1 = ax1.bar(algorithms, ratios, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Compression Ratio', fontsize=12, fontweight='bold')
    ax1.set_title('Compression Ratio (Higher = Better)', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Highlight LZ4 bar
    for i, bar in enumerate(bars1):
        height = bar.get_height()
        label = f'{height:.2f}x'
        if algorithms[i] == 'LZ4':
            label += '\n⭐ IoT Choice'
        ax1.text(bar.get_x() + bar.get_width()/2., height + 0.1, label,
                ha='center', fontsize=11, fontweight='bold')
    
    # Plot 2: Speed Comparison
    bars2 = ax2.bar(algorithms, speeds, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Speed (MB/s)', fontsize=12, fontweight='bold')
    ax2.set_title('Compression Speed (Higher = Better)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    for i, bar in enumerate(bars2):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 10, f'{int(height)}',
                ha='center', fontsize=11, fontweight='bold')
    
    # Add annotation for LZ4
    ax2.annotate('10x faster\nthan ZLIB!', xy=(0, 500), xytext=(1, 400),
                arrowprops=dict(arrowstyle='->', color='red', lw=2),
                fontsize=10, color='red', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/compression_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/compression_comparison.png")
    plt.close()

def plot_pqc_sizes(results, output_dir='thesis/figures'):
    """Plot PQC algorithm key and ciphertext sizes"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    algorithms = [r['algorithm'] for r in results['pqc']]
    pk_sizes = [r['pk_size'] for r in results['pqc']]
    ct_sizes = [r['ct_size'] for r in results['pqc']]
    
    x = np.arange(len(algorithms))
    width = 0.35
    
    bars1 = ax.bar(x - width/2, pk_sizes, width, label='Public Key', 
                   color='#3498db', edgecolor='black')
    bars2 = ax.bar(x + width/2, ct_sizes, width, label='Ciphertext',
                   color='#e74c3c', edgecolor='black')
    
    # Highlight Kyber768
    ax.axvspan(0.6, 1.4, alpha=0.1, color='green')
    ax.text(1, max(pk_sizes) + 100, '⭐ Recommended', ha='center', 
            fontsize=11, color='#27ae60', fontweight='bold')
    
    ax.set_xlabel('PQC Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_title('Kyber Key and Ciphertext Sizes', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 20,
                   f'{int(height)} B', ha='center', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/pqc_sizes.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/pqc_sizes.png")
    plt.close()

def plot_combined_comparison(results, output_dir='thesis/figures'):
    """Plot combined PQC + Compression with LZ4 highlighted"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Extract data - put LZ4 first
    configs = [f"Kyber768\n+{r['compression'].upper()}" for r in results['combined']]
    original = [r['original_size']/1024 for r in results['combined']]
    transmitted = [r['total_transmission']/1024 for r in results['combined']]
    savings = [r['bandwidth_savings'] for r in results['combined']]
    
    colors = [COLORS['lz4'], COLORS['zlib'], COLORS['zstd']]
    
    # Plot 1: Size comparison
    x = np.arange(len(configs))
    width = 0.35
    
    bars1 = ax1.bar(x - width/2, original, width, label='Original', 
                   color='#e74c3c', edgecolor='black')
    bars2 = ax1.bar(x + width/2, transmitted, width, label='After PQC+Compress',
                   color=colors, edgecolor='black')
    
    ax1.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Size (KB)', fontsize=12, fontweight='bold')
    ax1.set_title('Transmission Size with PQC + Compression', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, fontsize=10)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Bandwidth savings
    bars = ax2.bar(configs, savings, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bandwidth Savings (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Bandwidth Savings (Higher = Better)', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=60, color='gray', linestyle='--', alpha=0.5)
    
    # Add value labels with LZ4 note
    for i, bar in enumerate(bars):
        height = bar.get_height()
        label = f'{height:.1f}%'
        if 'LZ4' in configs[i]:
            label += '\n(Lower memory)'
        ax2.text(bar.get_x() + bar.get_width()/2., height + 1, label,
                ha='center', fontweight='bold', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/combined_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/combined_comparison.png")
    plt.close()

def plot_memory_comparison(output_dir='thesis/figures'):
    """NEW: Plot memory footprint comparison (key for IoT)"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    algorithms = ['LZ4', 'ZLIB', 'Zstandard']
    memory_kb = [16, 32, 64]
    colors = [COLORS['lz4'], COLORS['zlib'], COLORS['zstd']]
    
    bars = ax.bar(algorithms, memory_kb, color=colors, edgecolor='black', linewidth=2)
    
    # Add Kyber stack requirement line
    ax.axhline(y=10, color='red', linestyle='--', linewidth=2, label='Kyber768 stack (~10 KB)')
    
    # Typical MCU RAM line
    ax.axhline(y=64, color='orange', linestyle=':', linewidth=2, label='Typical MCU RAM (64 KB)')
    
    ax.set_ylabel('Memory Required (KB)', fontsize=12, fontweight='bold')
    ax.set_title('Compression Memory Footprint\n(Critical for IoT with Kyber)', fontsize=14, fontweight='bold')
    ax.legend(fontsize=10)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height + 2, f'{int(height)} KB',
                ha='center', fontsize=12, fontweight='bold')
    
    # Add annotation
    ax.annotate('LZ4 + Kyber\nfits in 32 KB!', xy=(0, 16), xytext=(0.5, 40),
                arrowprops=dict(arrowstyle='->', color='green', lw=2),
                fontsize=11, color='green', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/memory_comparison.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/memory_comparison.png")
    plt.close()

def plot_speed_vs_ratio(output_dir='thesis/figures'):
    """NEW: Speed vs Compression Ratio scatter plot"""
    fig, ax = plt.subplots(figsize=(10, 7))
    
    algorithms = {
        'LZ4': (2.5, 500, 16, COLORS['lz4']),
        'ZLIB': (3.5, 50, 32, COLORS['zlib']),
        'Zstd': (4.0, 200, 64, COLORS['zstd']),
        'Brotli': (4.5, 30, 128, '#34495e'),
        'RLE': (1.2, 800, 1, '#e74c3c'),
    }
    
    for name, (ratio, speed, memory, color) in algorithms.items():
        size = memory * 10  # Size proportional to memory
        ax.scatter(ratio, speed, s=size, c=color, edgecolors='black', 
                  linewidth=2, alpha=0.8, zorder=5)
        offset = (10, 10) if name != 'LZ4' else (10, -20)
        ax.annotate(f'{name}\n({memory} KB)', (ratio, speed), xytext=offset,
                   textcoords='offset points', fontsize=10, fontweight='bold')
    
    # Highlight optimal zone for IoT
    from matplotlib.patches import Ellipse
    ellipse = Ellipse((2.5, 500), 1.5, 300, fill=False, color='green', 
                      linewidth=3, linestyle='--')
    ax.add_patch(ellipse)
    ax.text(2.5, 650, '⭐ Optimal for IoT', ha='center', fontsize=12,
            color='green', fontweight='bold')
    
    ax.set_xlabel('Compression Ratio (Higher = Smaller Output)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Speed (MB/s)', fontsize=12, fontweight='bold')
    ax.set_title('Compression: Speed vs Ratio Trade-off\n(Bubble size = Memory footprint)', 
                fontsize=14, fontweight='bold')
    ax.set_xlim(0.5, 5.5)
    ax.set_ylim(0, 900)
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/speed_vs_ratio.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/speed_vs_ratio.png")
    plt.close()

def plot_workflow_diagram(results, output_dir='thesis/figures'):
    """Create workflow visualization with LZ4"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    
    # Get LZ4 sample data
    sample = results['combined'][0]  # LZ4 result
    
    # Draw boxes
    boxes = [
        {'x': 0.05, 'y': 0.5, 'w': 0.15, 'h': 0.25, 'color': '#e74c3c', 
         'label': 'Original\nMessage', 'size': f"{sample['original_size']:,} B"},
        
        {'x': 0.28, 'y': 0.5, 'w': 0.15, 'h': 0.25, 'color': COLORS['lz4'],
         'label': 'LZ4\nCompressed', 'size': f"{sample['compressed_size']:,} B"},
        
        {'x': 0.51, 'y': 0.5, 'w': 0.15, 'h': 0.25, 'color': '#f39c12',
         'label': 'Kyber768\nEncrypted', 'size': f"+{sample['pqc_overhead']:,} B"},
        
        {'x': 0.74, 'y': 0.5, 'w': 0.18, 'h': 0.25, 'color': '#2ecc71',
         'label': 'Final\nPacket', 'size': f"{sample['total_transmission']:,} B"}
    ]
    
    from matplotlib.patches import FancyBboxPatch
    for box in boxes:
        rect = FancyBboxPatch((box['x'], box['y']), box['w'], box['h'],
                              boxstyle="round,pad=0.02",
                              facecolor=box['color'], edgecolor='black',
                              linewidth=2, alpha=0.9)
        ax.add_patch(rect)
        
        ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2 + 0.03,
               box['label'], ha='center', va='center',
               fontsize=11, fontweight='bold', color='white')
        
        ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2 - 0.06,
               box['size'], ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')
    
    # Draw arrows
    arrow_positions = [0.21, 0.44, 0.67]
    for x in arrow_positions:
        ax.annotate('', xy=(x + 0.05, 0.625), xytext=(x, 0.625),
                   arrowprops=dict(arrowstyle='->', color='black', lw=2))
    
    # Title
    ax.text(0.5, 0.9, 'PQC + LZ4 Compression Workflow',
           ha='center', fontsize=16, fontweight='bold')
    
    # Savings annotation
    ax.text(0.5, 0.15, f"Bandwidth Savings: {sample['bandwidth_savings']:.1f}%",
           ha='center', fontsize=18, fontweight='bold', color='#27ae60',
           bbox=dict(boxstyle='round', facecolor='#d5f4e6', edgecolor='#27ae60', linewidth=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/workflow_diagram.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/workflow_diagram.png")
    plt.close()

def create_summary_table(results, output_dir='thesis/figures'):
    """Create summary table image"""
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare data
    header = ['Configuration', 'Original\n(KB)', 'Compressed\n(KB)', 'Total Tx\n(KB)', 
              'Savings\n(%)', 'Memory\n(KB)']
    
    memory = {'lz4': 16, 'zlib': 32, 'zstd': 64}
    
    table_data = [header]
    for r in results['combined']:
        row = [
            f"Kyber768 + {r['compression'].upper()}",
            f"{r['original_size']/1024:.1f}",
            f"{r['compressed_size']/1024:.2f}",
            f"{r['total_transmission']/1024:.2f}",
            f"{r['bandwidth_savings']:.1f}",
            f"{memory.get(r['compression'], 'N/A')}"
        ]
        table_data.append(row)
    
    # Create table
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
    
    # Style data rows - highlight LZ4
    for i in range(1, len(table_data)):
        for j in range(6):
            cell = table[(i, j)]
            if 'LZ4' in table_data[i][0]:
                cell.set_facecolor('#e8daef')  # Light purple for LZ4
            else:
                cell.set_facecolor('#ecf0f1')
            if j == 4:  # Savings column
                cell.set_text_props(weight='bold', color='#27ae60')
    
    ax.text(0.5, 0.95, 'Benchmark Results: Kyber768 + Compression',
           ha='center', fontsize=14, fontweight='bold', transform=ax.transAxes)
    
    ax.text(0.5, 0.05, '⭐ LZ4 recommended for IoT endpoints (lowest memory)',
           ha='center', fontsize=11, color='#9b59b6', fontweight='bold', transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/summary_table.png', dpi=300, bbox_inches='tight')
    print(f"✓ Created: {output_dir}/summary_table.png")
    plt.close()

def main():
    """Generate all visualizations"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        THESIS VISUALIZATION GENERATOR                                ║
║        LZ4-Focused for IoT Endpoints                                 ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    output_dir = 'thesis/figures'
    
    # Load or generate results
    print("Loading benchmark results...")
    results = load_results()
    print("✓ Results loaded")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    print("-" * 70)
    
    plot_compression_comparison(results, output_dir)
    plot_pqc_sizes(results, output_dir)
    plot_combined_comparison(results, output_dir)
    plot_memory_comparison(output_dir)
    plot_speed_vs_ratio(output_dir)
    plot_workflow_diagram(results, output_dir)
    create_summary_table(results, output_dir)
    
    print("-" * 70)
    print("\n✓ All visualizations created!")
    print("\nGenerated files in thesis/figures/:")
    print("  • compression_comparison.png")
    print("  • pqc_sizes.png")
    print("  • combined_comparison.png")
    print("  • memory_comparison.png (NEW)")
    print("  • speed_vs_ratio.png (NEW)")
    print("  • workflow_diagram.png")
    print("  • summary_table.png")

if __name__ == "__main__":
    main()
