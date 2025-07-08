import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from tabulate import tabulate
import warnings
warnings.filterwarnings('ignore')

# Set up the plotting style
plt.style.use('default')
sns.set_palette("husl")

# Target valuations (working backwards)
TARGET_SERIES_A_VALUATION = 40_000_000  # $40M
TARGET_SEED_VALUATION = 23_000_000      # $23M

# ESOP estimate (created pre-Series A)
esop_pct = 0.10

# Series A assumptions
series_a_raise = 7_000_000  # Typical Series A raise
series_a_post_money = TARGET_SERIES_A_VALUATION + series_a_raise
series_a_dilution = series_a_raise / series_a_post_money

# Seed assumptions
seed_raise = 2_000_000  # Typical seed raise
seed_post_money = TARGET_SEED_VALUATION + seed_raise
seed_dilution = seed_raise / seed_post_money

# Calculate required pre-seed and angel SAFE terms to achieve target founder ownership
target_founder_ownership_after_series_a = 0.51  # Target 51% founder ownership after Series A

# Working backwards:
# Founder ownership after Series A = (1 - total_safe_dilution - seed_dilution - esop) * (1 - series_a_dilution)
# Solving for total_safe_dilution:
# total_safe_dilution = 1 - seed_dilution - esop - (target_founder_ownership_after_series_a / (1 - series_a_dilution))

required_total_safe_dilution = 1 - seed_dilution - esop_pct - (target_founder_ownership_after_series_a / (1 - series_a_dilution))

print(f"Required total SAFE dilution: {required_total_safe_dilution:.1%}")

# Generate angel and pre-seed scenarios
angel_valuations = [8_000_000, 10_000_000, 12_000_000, 15_000_000, 18_000_000, 20_000_000]  # Angel caps
angel_raises = [800_000, 1_000_000, 1_200_000, 1_500_000, 1_800_000, 2_000_000, 2_500_000]  # Angel raises

preseed_valuations = [8_000_000, 10_000_000, 12_000_000, 15_000_000, 18_000_000, 20_000_000]  # Pre-seed caps
preseed_raises = [800_000, 1_000_000, 1_200_000, 1_400_000, 1_600_000, 1_800_000, 2_000_000]  # Pre-seed raises

# Build backwards planning scenarios
rows = []
scenarios_analyzed = 0

for angel_val in angel_valuations:
    for angel_raise in angel_raises:
        if angel_raise <= angel_val * 0.25:  # Reasonable raise amount (max 25% of cap)
            for preseed_val in preseed_valuations:
                for preseed_raise in preseed_raises:
                    if preseed_raise <= preseed_val * 0.25:  # Reasonable raise amount
                        # Calculate SAFE dilutions
                        angel_dilution = angel_raise / angel_val
                        preseed_dilution = preseed_raise / preseed_val
                        total_safe_dilution = angel_dilution + preseed_dilution
                        
                        # Check if this combination achieves target founder ownership
                        ownership_after_seed = 1 - (total_safe_dilution + seed_dilution + esop_pct)
                        founder_ownership_post_series_a = ownership_after_seed * (1 - series_a_dilution)
                        
                        # Only include scenarios that achieve reasonable founder ownership (45-55%)
                        if 0.45 <= founder_ownership_post_series_a <= 0.55:
                            scenarios_analyzed += 1
                            if scenarios_analyzed <= 20:  # Limit to 20 best scenarios
                                rows.append({
                                    "Angel Cap": f"${angel_val/1e6:.1f}M",
                                    "Angel Raise": f"${angel_raise/1e6:.1f}M",
                                    "Angel Dilution": f"{angel_dilution:.1%}",
                                    "Pre-seed Cap": f"${preseed_val/1e6:.1f}M",
                                    "Pre-seed Raise": f"${preseed_raise/1e6:.1f}M",
                                    "Pre-seed Dilution": f"{preseed_dilution:.1%}",
                                    "Total SAFE Dilution": f"{total_safe_dilution:.1%}",
                                    "Founder % After Seed": f"{ownership_after_seed:.1%}",
                                    "Founder % After Series A": f"{founder_ownership_post_series_a:.1%}"
                                })

# Convert to DataFrame
df = pd.DataFrame(rows)

# Create a visually pleasing display
def display_backwards_planning_scenarios(df):
    """
    Display backwards planning scenarios in a visually pleasing format
    """
    print("\n" + "="*100)
    print("🔄 BACKWARDS PLANNING: Angel & Pre-seed SAFE Scenarios")
    print("="*100)
    
    print(f"\n🎯 Target Valuations:")
    print(f"   • Series A Valuation: ${TARGET_SERIES_A_VALUATION/1e6:.1f}M")
    print(f"   • Seed Valuation: ${TARGET_SEED_VALUATION/1e6:.1f}M")
    print(f"   • Target Founder Ownership: 51%")
    print(f"   • Required Total SAFE Dilution: {required_total_safe_dilution:.1%}")
    
    # Display summary statistics
    print(f"\n📊 Analysis Summary:")
    print(f"   • Scenarios analyzed: {scenarios_analyzed}")
    print(f"   • Viable scenarios found: {len(df)}")
    print(f"   • Angel cap range: ${min([float(x.replace('$', '').replace('M', '')) for x in df['Angel Cap']]):.1f}M - ${max([float(x.replace('$', '').replace('M', '')) for x in df['Angel Cap']]):.1f}M")
    print(f"   • Pre-seed cap range: ${min([float(x.replace('$', '').replace('M', '')) for x in df['Pre-seed Cap']]):.1f}M - ${max([float(x.replace('$', '').replace('M', '')) for x in df['Pre-seed Cap']]):.1f}M")
    
    # Find optimal scenarios
    df_numeric = df.copy()
    df_numeric['Founder % After Series A'] = df_numeric['Founder % After Series A'].str.rstrip('%').astype('float') / 100
    
    best_scenario = df_numeric.loc[df_numeric['Founder % After Series A'].idxmax()]
    worst_scenario = df_numeric.loc[df_numeric['Founder % After Series A'].idxmin()]
    
    print(f"\n🎯 Key Insights:")
    print(f"   • Best founder ownership: {best_scenario['Founder % After Series A']:.1%}")
    print(f"   • Worst founder ownership: {worst_scenario['Founder % After Series A']:.1%}")
    print(f"   • Ownership range: {worst_scenario['Founder % After Series A']:.1%} - {best_scenario['Founder % After Series A']:.1%}")
    
    # Display the scenarios table
    print(f"\n📋 Viable Angel & Pre-seed Scenarios:")
    print("-" * 100)
    
    # Use tabulate for better table formatting
    table_data = []
    for idx, row in df.iterrows():
        table_data.append([
            row['Angel Cap'],
            row['Angel Raise'],
            row['Pre-seed Cap'],
            row['Pre-seed Raise'],
            row['Total SAFE Dilution'],
            row['Founder % After Series A']
        ])
    
    headers = ['Angel Cap', 'Angel Raise', 'Pre-seed Cap', 'Pre-seed Raise', 'Total SAFE Dilution', 'Founder %']
    print(tabulate(table_data, headers=headers, tablefmt='grid', numalign='center'))
    
    # Create visualizations
    print(f"\n📈 Visual Analysis:")
    print("-" * 100)
    
    # Create subplots
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Founder ownership vs Total SAFE dilution
    df_numeric['Total SAFE Dilution'] = df_numeric['Total SAFE Dilution'].str.rstrip('%').astype('float') / 100
    ax1.scatter(df_numeric['Total SAFE Dilution'], df_numeric['Founder % After Series A'], 
                alpha=0.7, s=100, c='steelblue')
    ax1.set_xlabel('Total SAFE Dilution')
    ax1.set_ylabel('Founder Ownership After Series A')
    ax1.set_title('Founder Ownership vs SAFE Dilution')
    ax1.grid(True, alpha=0.3)
    
    # 2. Angel vs Pre-seed caps heatmap
    pivot_data = df_numeric.pivot_table(
        values='Founder % After Series A',
        index='Angel Cap',
        columns='Pre-seed Cap',
        aggfunc='mean'
    )
    sns.heatmap(pivot_data, annot=True, fmt='.1%', cmap='RdYlGn', ax=ax2)
    ax2.set_title('Founder Ownership by Angel & Pre-seed Caps')
    
    # 3. Capital raised distribution
    df_numeric['Angel Raise'] = df_numeric['Angel Raise'].str.replace('$', '').str.replace('M', '').astype(float)
    df_numeric['Pre-seed Raise'] = df_numeric['Pre-seed Raise'].str.replace('$', '').str.replace('M', '').astype(float)
    
    ax3.hist(df_numeric['Angel Raise'], alpha=0.7, label='Angel Raises', bins=10)
    ax3.hist(df_numeric['Pre-seed Raise'], alpha=0.7, label='Pre-seed Raises', bins=10)
    ax3.set_xlabel('Capital Raised ($M)')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Distribution of Capital Raises')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    
    # 4. Valuation progression
    stages = ['Angel', 'Pre-seed', 'Seed', 'Series A']
    valuations = [
        float(best_scenario['Angel Cap'].replace('$', '').replace('M', '')),
        float(best_scenario['Pre-seed Cap'].replace('$', '').replace('M', '')),
        TARGET_SEED_VALUATION/1e6,
        TARGET_SERIES_A_VALUATION/1e6
    ]
    
    ax4.plot(stages, valuations, 'o-', linewidth=2, markersize=8, color='green')
    ax4.set_ylabel('Valuation ($M)')
    ax4.set_title('Valuation Progression (Best Scenario)')
    ax4.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n💡 Recommendations:")
    print(f"   • Optimal Angel Cap: {best_scenario['Angel Cap']}")
    print(f"   • Optimal Angel Raise: {best_scenario['Angel Raise']}")
    print(f"   • Optimal Pre-seed Cap: {best_scenario['Pre-seed Cap']}")
    print(f"   • Optimal Pre-seed Raise: {best_scenario['Pre-seed Raise']}")
    print(f"   • Expected founder ownership: {best_scenario['Founder % After Series A']}")
    print("="*100)

# Display the results
display_backwards_planning_scenarios(df)
