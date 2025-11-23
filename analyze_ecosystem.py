import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np

# Set style for better-looking plots
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Load the data
print("Loading startup data...")
with open('startups_data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

startups = data['startups']
df = pd.DataFrame(startups)

print(f"Loaded {len(df)} startups")

# Create charts directory
import os
os.makedirs('charts', exist_ok=True)

# 1. Top 15 Industries Bar Chart
print("\n1. Generating industry distribution chart...")
industries = []
for startup in startups:
    if startup.get('industry'):
        industries.append(startup['industry']['name'])

industry_counts = Counter(industries)
top_industries = dict(sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)[:15])

plt.figure(figsize=(14, 7))
bars = plt.bar(range(len(top_industries)), list(top_industries.values()), color='#2E86AB')
plt.xlabel('Industry', fontsize=12, fontweight='bold')
plt.ylabel('Number of Startups', fontsize=12, fontweight='bold')
plt.title('Top 15 Industries in Uzbekistan Startup Ecosystem', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(top_industries)), list(top_industries.keys()), rotation=45, ha='right')
plt.tight_layout()

# Add value labels on bars
for i, (bar, value) in enumerate(zip(bars, top_industries.values())):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(value),
             ha='center', va='bottom', fontweight='bold')

plt.savefig('charts/01_top_industries.png', dpi=300, bbox_inches='tight')
plt.close()

# 2. Startup Stage Distribution
print("2. Generating stage distribution chart...")
stages_mapping = {
    'pre_seed': 'Pre-Seed',
    'seed_': 'Seed',
    'idea': 'Idea',
    'early_a': 'Early Stage A',
    'serias_a': 'Series A',
    'early_b': 'Early Stage B',
    'expension': 'Expansion',
    None: 'Not Specified'
}

stage_counts = Counter([stages_mapping.get(s.get('stage'), 'Not Specified') for s in startups])
stage_order = ['Idea', 'Pre-Seed', 'Seed', 'Early Stage A', 'Series A', 'Early Stage B', 'Expansion', 'Not Specified']
stage_counts_ordered = {k: stage_counts.get(k, 0) for k in stage_order if stage_counts.get(k, 0) > 0}

plt.figure(figsize=(12, 6))
colors = ['#A23B72', '#F18F01', '#2E86AB', '#06A77D', '#D62246', '#8B5A3C', '#6C4B5E', '#999999']
bars = plt.bar(range(len(stage_counts_ordered)), list(stage_counts_ordered.values()),
               color=colors[:len(stage_counts_ordered)])
plt.xlabel('Funding Stage', fontsize=12, fontweight='bold')
plt.ylabel('Number of Startups', fontsize=12, fontweight='bold')
plt.title('Startup Distribution by Funding Stage', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(stage_counts_ordered)), list(stage_counts_ordered.keys()), rotation=45, ha='right')
plt.tight_layout()

# Add value labels
for bar, value in zip(bars, stage_counts_ordered.values()):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5, str(value),
             ha='center', va='bottom', fontweight='bold', fontsize=11)

plt.savefig('charts/02_funding_stages.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Regional Distribution (Top 10 Regions)
print("3. Generating regional distribution chart...")
regions = []
for startup in startups:
    if startup.get('region'):
        regions.append(startup['region']['name'])
    else:
        regions.append('Not Specified')

region_counts = Counter(regions)
top_regions = dict(sorted(region_counts.items(), key=lambda x: x[1], reverse=True)[:10])

plt.figure(figsize=(12, 7))
bars = plt.barh(range(len(top_regions)), list(top_regions.values()), color='#06A77D')
plt.ylabel('Region', fontsize=12, fontweight='bold')
plt.xlabel('Number of Startups', fontsize=12, fontweight='bold')
plt.title('Top 10 Regions by Startup Count', fontsize=14, fontweight='bold', pad=20)
plt.yticks(range(len(top_regions)), list(top_regions.keys()))
plt.gca().invert_yaxis()
plt.tight_layout()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_regions.values())):
    plt.text(bar.get_width() + 5, bar.get_y() + bar.get_height()/2, str(value),
             ha='left', va='center', fontweight='bold')

plt.savefig('charts/03_regional_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 4. Industry vs Stage Heatmap (Top 10 Industries)
print("4. Generating industry-stage heatmap...")
industry_stage_data = []
for startup in startups:
    if startup.get('industry'):
        industry_stage_data.append({
            'industry': startup['industry']['name'],
            'stage': stages_mapping.get(startup.get('stage'), 'Not Specified')
        })

is_df = pd.DataFrame(industry_stage_data)
top_10_industries = is_df['industry'].value_counts().head(10).index
is_filtered = is_df[is_df['industry'].isin(top_10_industries)]

heatmap_data = pd.crosstab(is_filtered['industry'], is_filtered['stage'])
stage_order_filtered = [s for s in stage_order if s in heatmap_data.columns]
heatmap_data = heatmap_data[stage_order_filtered]

plt.figure(figsize=(14, 8))
sns.heatmap(heatmap_data, annot=True, fmt='d', cmap='YlOrRd', cbar_kws={'label': 'Number of Startups'})
plt.xlabel('Funding Stage', fontsize=12, fontweight='bold')
plt.ylabel('Industry', fontsize=12, fontweight='bold')
plt.title('Top 10 Industries by Funding Stage', fontsize=14, fontweight='bold', pad=20)
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('charts/04_industry_stage_heatmap.png', dpi=300, bbox_inches='tight')
plt.close()

# 5. Verification and Award Status
print("5. Generating verification and awards chart...")
status_data = {
    'Verified Startups': sum(1 for s in startups if s.get('is_verified')),
    'Digital Awards\nParticipants': sum(1 for s in startups if s.get('digital_startup_awards_participant')),
    'Platform Members': sum(1 for s in startups if s.get('is_member')),
    'Tech Awards\nWinners': sum(1 for s in startups if s.get('tech_awards_winner'))
}

plt.figure(figsize=(10, 6))
colors = ['#2E86AB', '#F18F01', '#06A77D', '#D62246']
bars = plt.bar(range(len(status_data)), list(status_data.values()), color=colors)
plt.xlabel('Status Category', fontsize=12, fontweight='bold')
plt.ylabel('Number of Startups', fontsize=12, fontweight='bold')
plt.title('Startup Verification and Recognition Status', fontsize=14, fontweight='bold', pad=20)
plt.xticks(range(len(status_data)), list(status_data.keys()))
plt.tight_layout()

# Add value labels and percentages
for bar, (key, value) in zip(bars, status_data.items()):
    percentage = (value / len(startups)) * 100
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 5,
             f'{value}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')

plt.savefig('charts/05_verification_awards.png', dpi=300, bbox_inches='tight')
plt.close()

# 6. Maturity Funnel Analysis
print("6. Generating maturity funnel chart...")
funnel_order = ['Idea', 'Pre-Seed', 'Seed', 'Early Stage A', 'Series A', 'Early Stage B', 'Expansion']
funnel_data = {stage: stage_counts.get(stage, 0) for stage in funnel_order}

plt.figure(figsize=(14, 10))
y_pos = np.arange(len(funnel_data))
values = list(funnel_data.values())
max_val = max(values)

colors_gradient = plt.cm.Blues(np.linspace(0.5, 0.95, len(funnel_data)))

for i, (stage, value) in enumerate(funnel_data.items()):
    bar_width = (value / max_val) * 0.85
    left = (1 - bar_width) / 2

    # Create trapezoid effect for funnel
    bar = plt.barh(i, bar_width, left=left, height=0.8, color=colors_gradient[i],
                   edgecolor='white', linewidth=2)

    # Add value and percentage inside the bar
    percentage = (value / len(startups)) * 100
    # Use black text for better visibility
    text_color = 'white' if i > 2 else 'navy'
    plt.text(0.5, i, f'{stage}', ha='center', va='center',
             fontweight='bold', fontsize=13, color=text_color)

    # Add count and percentage to the right of the bar
    plt.text(left + bar_width + 0.02, i, f'{value} ({percentage:.1f}%)',
             ha='left', va='center', fontweight='bold', fontsize=11, color='black')

plt.xlim(0, 1.15)
plt.ylim(-0.5, len(funnel_data) - 0.5)
plt.gca().invert_yaxis()  # Invert to show funnel from top to bottom
plt.axis('off')
plt.title('Startup Maturity Funnel: From Idea to Expansion',
          fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.savefig('charts/06_maturity_funnel.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Industry Maturity Analysis (Average stage by industry)
print("7. Generating industry maturity analysis...")
stage_numeric = {
    'Idea': 1,
    'Pre-Seed': 2,
    'Seed': 3,
    'Early Stage A': 4,
    'Series A': 5,
    'Early Stage B': 6,
    'Expansion': 7,
    'Not Specified': 0
}

industry_maturity = {}
for startup in startups:
    if startup.get('industry') and startup.get('stage'):
        industry = startup['industry']['name']
        stage = stages_mapping.get(startup.get('stage'), 'Not Specified')
        if industry not in industry_maturity:
            industry_maturity[industry] = []
        industry_maturity[industry].append(stage_numeric.get(stage, 0))

# Calculate average maturity score for top 12 industries
industry_avg_maturity = {}
for industry, stages in industry_maturity.items():
    if len(stages) >= 10:  # Only industries with at least 10 startups
        industry_avg_maturity[industry] = sum(stages) / len(stages)

top_mature_industries = dict(sorted(industry_avg_maturity.items(), key=lambda x: x[1], reverse=True)[:12])

plt.figure(figsize=(14, 7))
bars = plt.barh(range(len(top_mature_industries)), list(top_mature_industries.values()), color='#A23B72')
plt.ylabel('Industry', fontsize=12, fontweight='bold')
plt.xlabel('Average Maturity Score', fontsize=12, fontweight='bold')
plt.title('Industry Maturity Index (Higher = More Mature Startups)', fontsize=14, fontweight='bold', pad=20)
plt.yticks(range(len(top_mature_industries)), list(top_mature_industries.keys()))
plt.gca().invert_yaxis()
plt.tight_layout()

# Add value labels
for bar, value in zip(bars, top_mature_industries.values()):
    plt.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height()/2, f'{value:.2f}',
             ha='left', va='center', fontweight='bold')

plt.savefig('charts/07_industry_maturity.png', dpi=300, bbox_inches='tight')
plt.close()

# 8. Comparison: Tech vs Non-Tech Industries
print("8. Generating tech vs non-tech comparison...")
tech_industries = [
    'SaaS', 'AI & ML', 'EdTech', 'FinTech', 'HealthTech & MedTech',
    'E-commerce & Retail Tech', 'HRTech', 'Cybersecurity', 'Blockchain & Cryptocurrency',
    'Cloud Computing & Infrastructure', 'Data Analytics & Big Data', 'IoT (Internet of Things)',
    'DevOps & Development Tools', 'Automation & Robotics'
]

tech_count = 0
non_tech_count = 0
tech_stages = []
non_tech_stages = []

for startup in startups:
    if startup.get('industry'):
        industry_name = startup['industry']['name']
        stage = stages_mapping.get(startup.get('stage'), 'Not Specified')

        if industry_name in tech_industries:
            tech_count += 1
            tech_stages.append(stage_numeric.get(stage, 0))
        else:
            non_tech_count += 1
            non_tech_stages.append(stage_numeric.get(stage, 0))

comparison_data = {
    'Category': ['Tech Industries', 'Tech Industries', 'Non-Tech Industries', 'Non-Tech Industries'],
    'Metric': ['Count', 'Avg Maturity', 'Count', 'Avg Maturity'],
    'Value': [
        tech_count,
        sum(tech_stages) / len(tech_stages) if tech_stages else 0,
        non_tech_count,
        sum(non_tech_stages) / len(non_tech_stages) if non_tech_stages else 0
    ]
}

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Count comparison
ax1.bar(['Tech\nIndustries', 'Non-Tech\nIndustries'], [tech_count, non_tech_count],
        color=['#2E86AB', '#F18F01'], width=0.6)
ax1.set_ylabel('Number of Startups', fontsize=12, fontweight='bold')
ax1.set_title('Startup Count: Tech vs Non-Tech', fontsize=12, fontweight='bold')
for i, v in enumerate([tech_count, non_tech_count]):
    percentage = (v / (tech_count + non_tech_count)) * 100
    ax1.text(i, v + 10, f'{v}\n({percentage:.1f}%)', ha='center', va='bottom', fontweight='bold')

# Maturity comparison
avg_tech_maturity = sum(tech_stages) / len(tech_stages) if tech_stages else 0
avg_non_tech_maturity = sum(non_tech_stages) / len(non_tech_stages) if non_tech_stages else 0
ax2.bar(['Tech\nIndustries', 'Non-Tech\nIndustries'], [avg_tech_maturity, avg_non_tech_maturity],
        color=['#2E86AB', '#F18F01'], width=0.6)
ax2.set_ylabel('Average Maturity Score', fontsize=12, fontweight='bold')
ax2.set_title('Average Maturity: Tech vs Non-Tech', fontsize=12, fontweight='bold')
for i, v in enumerate([avg_tech_maturity, avg_non_tech_maturity]):
    ax2.text(i, v + 0.05, f'{v:.2f}', ha='center', va='bottom', fontweight='bold')

plt.tight_layout()
plt.savefig('charts/08_tech_vs_nontech.png', dpi=300, bbox_inches='tight')
plt.close()

# 9. Early Stage vs Growth Stage Distribution
print("9. Generating early vs growth stage analysis...")
early_stage = ['Idea', 'Pre-Seed', 'Seed']
growth_stage = ['Early Stage A', 'Series A', 'Early Stage B', 'Expansion']

industry_stage_split = {}
for startup in startups:
    if startup.get('industry'):
        industry = startup['industry']['name']
        stage = stages_mapping.get(startup.get('stage'), 'Not Specified')

        if industry not in industry_stage_split:
            industry_stage_split[industry] = {'early': 0, 'growth': 0}

        if stage in early_stage:
            industry_stage_split[industry]['early'] += 1
        elif stage in growth_stage:
            industry_stage_split[industry]['growth'] += 1

# Get top 10 industries with most growth stage startups
growth_sorted = sorted(industry_stage_split.items(), key=lambda x: x[1]['growth'], reverse=True)[:10]

industries_list = [item[0] for item in growth_sorted]
early_counts = [item[1]['early'] for item in growth_sorted]
growth_counts = [item[1]['growth'] for item in growth_sorted]

x = np.arange(len(industries_list))
width = 0.35

fig, ax = plt.subplots(figsize=(14, 7))
bars1 = ax.barh(x - width/2, early_counts, width, label='Early Stage (Idea, Pre-Seed, Seed)', color='#A8DADC')
bars2 = ax.barh(x + width/2, growth_counts, width, label='Growth Stage (Early A, Series A+)', color='#E63946')

ax.set_xlabel('Number of Startups', fontsize=12, fontweight='bold')
ax.set_ylabel('Industry', fontsize=12, fontweight='bold')
ax.set_title('Top 10 Industries: Early Stage vs Growth Stage Startups', fontsize=14, fontweight='bold', pad=20)
ax.set_yticks(x)
ax.set_yticklabels(industries_list)
ax.legend(loc='lower right', fontsize=10)
ax.invert_yaxis()

plt.tight_layout()
plt.savefig('charts/09_early_vs_growth.png', dpi=300, bbox_inches='tight')
plt.close()

# 10. Summary Statistics Visualization
print("10. Generating key metrics summary...")
key_metrics = {
    'Total Startups': len(startups),
    'Active Industries': len(set(s['industry']['name'] for s in startups if s.get('industry'))),
    'Covered Regions': len(set(s['region']['name'] for s in startups if s.get('region'))),
    'Growth Stage\nStartups': sum(1 for s in startups if stages_mapping.get(s.get('stage')) in growth_stage),
    'Tech Startups': tech_count,
    'Platform\nMembers': status_data['Platform Members']
}

fig, ax = plt.subplots(figsize=(14, 6))
colors_palette = ['#2E86AB', '#F18F01', '#06A77D', '#D62246', '#A23B72', '#8B5A3C']
bars = ax.bar(range(len(key_metrics)), list(key_metrics.values()), color=colors_palette)

ax.set_ylabel('Count', fontsize=12, fontweight='bold')
ax.set_title('Uzbekistan Startup Ecosystem: Key Metrics Overview', fontsize=14, fontweight='bold', pad=20)
ax.set_xticks(range(len(key_metrics)))
ax.set_xticklabels(list(key_metrics.keys()), fontsize=11)
ax.grid(axis='y', alpha=0.3)

for bar, value in zip(bars, key_metrics.values()):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 10, str(value),
            ha='center', va='bottom', fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig('charts/10_key_metrics.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("All charts generated successfully in the 'charts' directory!")
print("="*60)
print("\nGenerated charts:")
print("1. 01_top_industries.png - Top 15 industries distribution")
print("2. 02_funding_stages.png - Startup distribution by funding stage")
print("3. 03_regional_distribution.png - Top 10 regions by startup count")
print("4. 04_industry_stage_heatmap.png - Industry vs funding stage heatmap")
print("5. 05_verification_awards.png - Verification and recognition status")
print("6. 06_maturity_funnel.png - Startup maturity funnel analysis")
print("7. 07_industry_maturity.png - Industry maturity index")
print("8. 08_tech_vs_nontech.png - Tech vs non-tech industries comparison")
print("9. 09_early_vs_growth.png - Early stage vs growth stage by industry")
print("10. 10_key_metrics.png - Key ecosystem metrics overview")
print("="*60)
