#!/usr/bin/env python3
"""
Create visualization graphs from benchmark results
For thesis presentation and report
Abdessamad JAOUAD - M2 Big Data & IoT
"""

import json
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend

def load_results():
    """Load benchmark results from JSON"""
    try:
        with open('benchmark_results.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: benchmark_results.json not found!")
        print("Run: python3 benchmark_pqc_compression.py first")
        return None

def plot_compression_comparison(results):
    """Plot compression algorithm comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Get IoT medium results
    iot_data = results['compression']['iot_medium'][0]
    
    # Plot 1: Compression Ratio
    algorithms = ['Original', 'ZLIB']
    sizes = [iot_data['original_size']/1024, iot_data['compressed_size']/1024]
    colors = ['#e74c3c', '#2ecc71']
    
    bars = ax1.bar(algorithms, sizes, color=colors, edgecolor='black', linewidth=1.5)
    ax1.set_ylabel('Size (KB)', fontsize=12, fontweight='bold')
    ax1.set_title('Data Size: Original vs Compressed', fontsize=14, fontweight='bold')
    ax1.grid(axis='y', alpha=0.3)
    
    # Add value labels on bars
    for bar in bars:
        height = bar.get_height()
        ax1.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f} KB',
                ha='center', va='bottom', fontweight='bold')
    
    # Plot 2: Compression Ratio
    ratio = iot_data['compression_ratio']
    savings = (1 - iot_data['compressed_size']/iot_data['original_size']) * 100
    
    metrics = ['Compression\nRatio', 'Bandwidth\nSavings']
    values = [ratio, savings]
    colors2 = ['#3498db', '#9b59b6']
    
    bars2 = ax2.bar(metrics, values, color=colors2, edgecolor='black', linewidth=1.5)
    ax2.set_ylabel('Value', fontsize=12, fontweight='bold')
    ax2.set_title('Compression Efficiency Metrics', fontsize=14, fontweight='bold')
    ax2.grid(axis='y', alpha=0.3)
    
    # Add value labels
    ax2.text(0, ratio, f'{ratio:.1f}x', ha='center', va='bottom', fontweight='bold', fontsize=12)
    ax2.text(1, savings, f'{savings:.1f}%', ha='center', va='bottom', fontweight='bold', fontsize=12)
    
    plt.tight_layout()
    plt.savefig('compression_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: compression_comparison.png")
    plt.close()

def plot_pqc_sizes(results):
    """Plot PQC algorithm key and ciphertext sizes"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    algorithms = [r['algorithm'] for r in results['pqc']]
    pk_sizes = [r['pk_size'] for r in results['pqc']]
    ct_sizes = [r['ct_size'] for r in results['pqc']]
    
    x = range(len(algorithms))
    width = 0.35
    
    bars1 = ax.bar([i - width/2 for i in x], pk_sizes, width, 
                   label='Public Key', color='#3498db', edgecolor='black')
    bars2 = ax.bar([i + width/2 for i in x], ct_sizes, width,
                   label='Ciphertext', color='#e74c3c', edgecolor='black')
    
    ax.set_xlabel('PQC Algorithm', fontsize=12, fontweight='bold')
    ax.set_ylabel('Size (bytes)', fontsize=12, fontweight='bold')
    ax.set_title('PQC Key and Ciphertext Sizes', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(algorithms)
    ax.legend(fontsize=11)
    ax.grid(axis='y', alpha=0.3)
    
    # Add value labels
    for bars in [bars1, bars2]:
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f'{int(height)}',
                   ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('pqc_sizes.png', dpi=300, bbox_inches='tight')
    print("✓ Created: pqc_sizes.png")
    plt.close()

def plot_combined_comparison(results):
    """Plot combined PQC + Compression comparison"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Extract data
    configs = [f"{r['pqc_algorithm']}\n+ZLIB" for r in results['combined']]
    original = [r['original_size']/1024 for r in results['combined']]
    transmitted = [r['total_transmission']/1024 for r in results['combined']]
    savings = [r['bandwidth_savings'] for r in results['combined']]
    
    # Plot 1: Size comparison
    x = range(len(configs))
    width = 0.35
    
    bars1 = ax1.bar([i - width/2 for i in x], original, width,
                   label='Original', color='#e74c3c', edgecolor='black')
    bars2 = ax1.bar([i + width/2 for i in x], transmitted, width,
                   label='After PQC+Compress', color='#2ecc71', edgecolor='black')
    
    ax1.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax1.set_ylabel('Size (KB)', fontsize=12, fontweight='bold')
    ax1.set_title('Total Transmission Size', fontsize=14, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(configs, fontsize=9)
    ax1.legend(fontsize=11)
    ax1.grid(axis='y', alpha=0.3)
    
    # Plot 2: Bandwidth savings
    colors = ['#2ecc71', '#27ae60', '#229954']
    bars = ax2.bar(configs, savings, color=colors, edgecolor='black', linewidth=1.5)
    ax2.set_xlabel('Configuration', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Bandwidth Savings (%)', fontsize=12, fontweight='bold')
    ax2.set_title('Bandwidth Savings with PQC + Compression', fontsize=14, fontweight='bold')
    ax2.set_xticklabels(configs, fontsize=9)
    ax2.grid(axis='y', alpha=0.3)
    ax2.axhline(y=80, color='r', linestyle='--', alpha=0.5, label='80% threshold')
    ax2.legend(fontsize=10)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}%',
                ha='center', va='bottom', fontweight='bold', fontsize=11)
    
    plt.tight_layout()
    plt.savefig('combined_comparison.png', dpi=300, bbox_inches='tight')
    print("✓ Created: combined_comparison.png")
    plt.close()

def plot_workflow_diagram(results):
    """Create simple workflow visualization"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('off')
    
    # Get sample data
    sample = results['combined'][1]  # Kyber768 + ZLIB
    
    # Draw boxes
    boxes = [
        {'x': 0.1, 'y': 0.7, 'w': 0.15, 'h': 0.2, 'color': '#e74c3c', 
         'label': 'Original\nMessage', 'size': f"{sample['original_size']} B"},
        
        {'x': 0.3, 'y': 0.7, 'w': 0.15, 'h': 0.2, 'color': '#3498db',
         'label': 'Compressed', 'size': f"{sample['compressed_size']} B"},
        
        {'x': 0.5, 'y': 0.7, 'w': 0.15, 'h': 0.2, 'color': '#9b59b6',
         'label': 'PQC\nEncrypted', 'size': f"+{sample['pqc_overhead']} B"},
        
        {'x': 0.7, 'y': 0.7, 'w': 0.15, 'h': 0.2, 'color': '#2ecc71',
         'label': 'Transmitted', 'size': f"{sample['total_transmission']} B"}
    ]
    
    for box in boxes:
        rect = plt.Rectangle((box['x'], box['y']), box['w'], box['h'],
                            facecolor=box['color'], edgecolor='black',
                            linewidth=2, alpha=0.8)
        ax.add_patch(rect)
        
        # Add label
        ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2 + 0.05,
               box['label'], ha='center', va='center',
               fontsize=12, fontweight='bold', color='white')
        
        # Add size
        ax.text(box['x'] + box['w']/2, box['y'] + box['h']/2 - 0.05,
               box['size'], ha='center', va='center',
               fontsize=10, fontweight='bold', color='white')
    
    # Draw arrows
    arrows = [
        {'x': 0.26, 'y': 0.8, 'dx': 0.03, 'label': 'ZLIB'},
        {'x': 0.46, 'y': 0.8, 'dx': 0.03, 'label': 'Kyber768'},
        {'x': 0.66, 'y': 0.8, 'dx': 0.03, 'label': 'Transmit'}
    ]
    
    for arrow in arrows:
        ax.arrow(arrow['x'], arrow['y'], arrow['dx'], 0,
                head_width=0.03, head_length=0.01, fc='black', ec='black')
        ax.text(arrow['x'] + arrow['dx']/2, arrow['y'] - 0.05,
               arrow['label'], ha='center', fontsize=10, style='italic')
    
    # Add title
    ax.text(0.5, 0.95, 'PQC + Compression Workflow',
           ha='center', fontsize=16, fontweight='bold')
    
    # Add savings annotation
    ax.text(0.5, 0.3, f"Bandwidth Savings: {sample['bandwidth_savings']:.1f}%",
           ha='center', fontsize=20, fontweight='bold', color='#27ae60',
           bbox=dict(boxstyle='round', facecolor='#d5f4e6', edgecolor='#27ae60', linewidth=2))
    
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    
    plt.tight_layout()
    plt.savefig('workflow_diagram.png', dpi=300, bbox_inches='tight')
    print("✓ Created: workflow_diagram.png")
    plt.close()

def create_summary_table_image(results):
    """Create a summary table as image"""
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.axis('tight')
    ax.axis('off')
    
    # Prepare data
    table_data = [
        ['Configuration', 'Original\n(KB)', 'Compressed\n(KB)', 'Total Tx\n(KB)', 
         'Savings\n(%)', 'Time\n(ms)']
    ]
    
    for r in results['combined']:
        row = [
            f"{r['pqc_algorithm']}\n+ ZLIB",
            f"{r['original_size']/1024:.1f}",
            f"{r['compressed_size']/1024:.2f}",
            f"{r['total_transmission']/1024:.2f}",
            f"{r['bandwidth_savings']:.1f}",
            f"{r['total_time']*1000:.2f}"
        ]
        table_data.append(row)
    
    # Create table
    table = ax.table(cellText=table_data, cellLoc='center', loc='center',
                    colWidths=[0.2, 0.13, 0.13, 0.13, 0.13, 0.13])
    
    table.auto_set_font_size(False)
    table.set_fontsize(11)
    table.scale(1, 2.5)
    
    # Style header
    for i in range(6):
        cell = table[(0, i)]
        cell.set_facecolor('#3498db')
        cell.set_text_props(weight='bold', color='white')
    
    # Style data rows
    colors = ['#ecf0f1', '#d5dbdb']
    for i in range(1, len(table_data)):
        for j in range(6):
            cell = table[(i, j)]
            cell.set_facecolor(colors[i % 2])
            if j == 4:  # Savings column
                cell.set_text_props(weight='bold', color='#27ae60')
    
    # Add title
    ax.text(0.5, 0.95, 'Benchmark Results Summary',
           ha='center', fontsize=16, fontweight='bold',
           transform=ax.transAxes)
    
    plt.tight_layout()
    plt.savefig('summary_table.png', dpi=300, bbox_inches='tight')
    print("✓ Created: summary_table.png")
    plt.close()

def main():
    """Generate all visualizations"""
    print("""
╔══════════════════════════════════════════════════════════════════════╗
║        BENCHMARK VISUALIZATION GENERATOR                             ║
║        Creating graphs for thesis presentation                       ║
╚══════════════════════════════════════════════════════════════════════╝
""")
    
    # Check matplotlib
    try:
        import matplotlib
        print(f"✓ Matplotlib version: {matplotlib.__version__}")
    except ImportError:
        print("✗ Error: matplotlib not installed!")
        print("  Install with: pip install matplotlib")
        return
    
    # Load results
    print("\nLoading benchmark results...")
    results = load_results()
    if not results:
        return
    print("✓ Results loaded")
    
    # Generate visualizations
    print("\nGenerating visualizations...")
    print("-" * 70)
    
    try:
        plot_compression_comparison(results)
        plot_pqc_sizes(results)
        plot_combined_comparison(results)
        plot_workflow_diagram(results)
        create_summary_table_image(results)
    except Exception as e:
        print(f"\n✗ Error creating visualizations: {e}")
        print("  Make sure matplotlib is installed: pip install matplotlib")
        return
    
    print("-" * 70)
    print("\n✓ All visualizations created successfully!\n")
    print("Generated files:")
    print("  • compression_comparison.png - Compression performance")
    print("  • pqc_sizes.png - PQC key and ciphertext sizes")
    print("  • combined_comparison.png - PQC + Compression results")
    print("  • workflow_diagram.png - Visual workflow representation")
    print("  • summary_table.png - Results summary table")
    print("\nThese images are ready to include in your thesis and presentation!")

if __name__ == "__main__":
    main()
