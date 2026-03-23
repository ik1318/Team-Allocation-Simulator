import statistics
from .utils import extract, control_maker
from .engine import sorter

def wrangle(group_size, sorted_list):
    """
    Performs data wrangling, runs the grouping algorithm, and returns 
    improvement statistics compared to random assignment.
    """
    control_list = control_maker(sorted_list, group_size)
    final_sorted_list = sorter(sorted_list, group_size)

    num_tut_groups = len(sorted_list)
    if num_tut_groups == 0:
        return [0, 0, 0, []]

    # Calculate statistics for comparison
    # CGPA Standard Deviation
    control_mean_list = [[statistics.mean(extract(c_sub, 5)) for c_sub in control_list[x]] for x in range(num_tut_groups)]
    mean_list = [[statistics.mean(extract(p_grp, 5)) for p_grp in final_sorted_list[x]] for x in range(num_tut_groups)]
    
    mean_std_randomised = statistics.mean([statistics.stdev(c_means) if len(c_means) > 1 else 0 for c_means in control_mean_list])
    mean_std_algorithm = statistics.mean([statistics.stdev(m_means) if len(m_means) > 1 else 0 for m_means in mean_list])
    
    # Gender Balance (Majority Excess)
    def calc_gender_excess(group):
        males = extract(group, 4).count("Male")
        return abs(len(group) - 2 * males)

    control_gender_diff = [statistics.mean([calc_gender_excess(c_sub) for c_sub in control_list[x]]) for x in range(num_tut_groups)]
    gender_diff = [statistics.mean([calc_gender_excess(sub) for sub in final_sorted_list[x]]) for x in range(num_tut_groups)]
    
    mean_maj_randomised = statistics.mean(control_gender_diff)
    mean_maj_algorithm = statistics.mean(gender_diff)
    
    # School Diversity (Duplicate Schools)
    def calc_school_dupes(group):
        schools = extract(group, 2)
        return len(schools) - len(set(schools))

    control_school_dupe = [statistics.mean([calc_school_dupes(c_sub) for c_sub in control_list[x]]) for x in range(num_tut_groups)]
    school_dupe = [statistics.mean([calc_school_dupes(sub) for sub in final_sorted_list[x]]) for x in range(num_tut_groups)]
    
    mean_dupe_randomised = statistics.mean(control_school_dupe)
    mean_dupe_algorithm = statistics.mean(school_dupe)
    
    # Improvements
    # Gender improvement uses a correction for odd group sizes (subtracting 1 if odd)
    # mirroring the notebook's 'mean_majority_gender_randomised_corrected' logic
    odd_correction = (group_size % 2) > 0
    adj_maj_randomised = mean_maj_randomised - odd_correction
    adj_maj_algorithm = mean_maj_algorithm - odd_correction

    mean_std_imp = (mean_std_randomised / mean_std_algorithm - 1) * 100 if mean_std_algorithm > 0 else 0
    mean_gender_imp = (adj_maj_randomised / adj_maj_algorithm - 1) * 100 if adj_maj_algorithm > 0 else 0
    mean_dupe_imp = (mean_dupe_randomised / mean_dupe_algorithm - 1) * 100 if mean_dupe_algorithm > 0 else 0

    print(f"Comparison Summary (Grp Size {group_size}):")
    print(f"- CGPA Balance Improvement: {mean_std_imp:.2f}%")
    print(f"- Gender Balance Improvement (Corrected): {mean_gender_imp:.2f}%")
    print(f"- School Diversity Improvement: {mean_dupe_imp:.2f}%")
    print("-" * 30)

    return [mean_std_imp, mean_gender_imp, mean_dupe_imp, final_sorted_list]
