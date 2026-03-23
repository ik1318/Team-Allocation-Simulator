import math

def grade(info):
    """
    Evaluates fitness of a student in a group based on gender, school, and CGPA.
    Returns the sum of three component scores.
    """
    # 1. Gender Diversity Score (Sigmoid based)
    gender_difference = abs(info[0][0] - info[0][1])
    female_count, male_count = info[0][0], info[0][1]
    is_male = info[0][2]

    # Constants representing 'e'
    E = math.e

    if (female_count > male_count and is_male) or (female_count < male_count and not is_male):
        # Adding minority gender increases score
        gend_score = 1 / (1 + E ** -(gender_difference))
    elif (female_count < male_count and is_male) or (female_count > male_count and not is_male):
        # Adding majority gender decreases score
        gend_score = 1 / (1 + E ** (gender_difference))
    else:
        gend_score = 0.5

    # 2. School Diversity Score (Exponential decay)
    repeated_schools = info[1][0].count(info[1][1])
    sch_div_score = E ** -(repeated_schools)

    # 3. CGPA Score (Sigmoid based on improvement)
    old_mean_group_cgpa, new_mean_group_cgpa, mean_global_cgpa = info[2]
    old_difference = abs(old_mean_group_cgpa - mean_global_cgpa)
    new_difference = abs(new_mean_group_cgpa - mean_global_cgpa)
    change_in_difference = abs(old_difference - new_difference)

    if old_difference > new_difference:
        # Improvement (closer to global mean)
        cgpa_score = 1 / (1 + E ** -(change_in_difference))
    elif old_difference < new_difference:
        # Decline
        cgpa_score = 1 / (1 + E ** (change_in_difference))
    else:
        cgpa_score = 0.5

    return gend_score + sch_div_score + cgpa_score
