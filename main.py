import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from src.data_io import load_and_clean_data
from src.analysis import wrangle

def run_single_analysis(group_size, sorted_list):
    """
    Runs the grouping analysis for a single group size and displays a summary bar chart.
    """
    print(f"\nRunning Analysis for Group Size: {group_size}")
    results = wrangle(group_size, sorted_list)
    
    metrics = ['CGPA Balance', 'Gender Balance', 'School Diversity']
    improvements = [results[0], results[1], results[2]]
    
    df = pd.DataFrame({
        'Metric': metrics,
        'Improvement (%)': improvements
    })
    
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    ax = sns.barplot(x='Metric', y='Improvement (%)', data=df, hue='Metric', palette='viridis', legend=False)
    
    # Add percentage labels on top of bars
    for p in ax.patches:
        ax.annotate(f'{p.get_height():.1f}%', 
                    (p.get_x() + p.get_width() / 2., p.get_height()), 
                    ha = 'center', va = 'center', 
                    xytext = (0, 9), 
                    textcoords = 'offset points')
                    
    plt.title(f'Algorithm Performance Improvement (Group Size: {group_size})', fontsize=15)
    plt.ylabel('Improvement vs Random Sorting (%)')
    plt.tight_layout()
    
    output_file = f'outputs/performance_size_{group_size}.png'
    plt.savefig(output_file)
    print(f"Summary plot saved as {output_file}")
    plt.show()

def run_range_analysis(start_size, end_size, sorted_list):
    """
    Iterates through a range of group sizes and plots the improvement trends.
    Reproduces the complex graphing logic from the original notebook.
    """
    print(f"\nRunning Range Analysis (Sizes {start_size} to {end_size})...")
    data_points = []
    
    for size in range(start_size, end_size + 1):
        # We only need the first 3 return values (improvement percentages)
        results = wrangle(size, sorted_list)
        data_points.append([size, results[0], results[1], results[2]])
    
    df = pd.DataFrame(data_points, columns=[
        'Group Size', 
        'CGPA Balance (%)', 
        'Gender Balance (%)', 
        'School Diversity (%)'
    ])
    
    fig, axs = plt.subplots(3, 1, figsize=(12, 16))
    sns.set_theme(style="whitegrid")
    
    sns.lineplot(data=df, x='Group Size', y='CGPA Balance (%)', marker='o', ax=axs[0], color='blue')
    axs[0].set_title('CGPA Balance Improvement Trend')
    
    sns.lineplot(data=df, x='Group Size', y='Gender Balance (%)', marker='o', ax=axs[1], color='green')
    axs[1].set_title('Gender Balance Improvement Trend')
    
    sns.lineplot(data=df, x='Group Size', y='School Diversity (%)', marker='o', ax=axs[2], color='red')
    axs[2].set_title('School Diversity Improvement Trend')
    
    plt.tight_layout()
    plt.savefig('outputs/optimization_trends.png')
    print("Multi-size optimization trends saved as outputs/optimization_trends.png")
    plt.show()

from src.data_io import load_and_clean_data, save_grouping_results
from src.analysis import wrangle

def main():
    print("Team Allocation Simulator")
    print("==================================================")
    
    file_path = 'data/records.csv'
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found. Ensure it is in the root directory.")
        return
        
    # Load and clean data
    print("Loading datasets...")
    sorted_list = load_and_clean_data(file_path, shuffle_alternative=True)
    
    # 1. Run Analysis for Group Size 6
    print("\n[PART 1] Running standard analysis (Group Size 6)...")
    results = wrangle(6, sorted_list)
    final_sorted_list = results[3]
    
    # Generate single summary bar chart
    run_single_analysis(6, sorted_list)
    
    # 2. Export results to CSV (reproducing 'record_maker')
    print("\n[PART 2] Exporting results to CSV...")
    save_grouping_results(final_sorted_list, file_path, 'data/grouped_records.csv')
    
    # 3. Comprehensive Range Analysis (reproducing notebook trend chart)
    print("\n[PART 3] Running optimization trend analysis (Sizes 4 to 49)...")
    print("This may take a minute as it iterates through multiple permutations.")
    run_range_analysis(4, 49, sorted_list)
    
    print("\n" + "="*50)
    print("SUCCESS: All reports and visualizations have been generated.")
    print("Files created:")
    print("1. data/grouped_records.csv    - CSV with student IDs and group assignments")
    print("2. outputs/performance_size_6.png - Performance bar chart for size 6")
    print("3. outputs/optimization_trends.png - Trends for group sizes 4-49")
    print("="*50)

if __name__ == "__main__":
    # Use non-interactive backend to avoid blocking the terminal
    import matplotlib
    matplotlib.use('Agg')
    main()
