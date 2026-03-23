from .utils import extract
from .scoring import grade

def sorter(student_list, grp_size):
    """
    Main algorithm to sort students into groups based on the custom grading function.
    Ensures diversity in gender, school, and academic performance.
    """
    # Initialize final_list for 120 tutorial groups
    # Each tutorial group is pre-filled with empty project groups
    num_tut_groups = len(student_list)
    final_list = [[[] for x in range(50 // grp_size + (50 % grp_size > 0))] for x in range(num_tut_groups)]
    
    for tut_idx, tut_group in enumerate(student_list):
        # Calculate the target CGPA for this tutorial group
        group_cgpas = extract(tut_group, 5)
        global_cgpa = sum(group_cgpas) / len(group_cgpas) if group_cgpas else 0
        
        for student in tut_group:
            is_male = student[4] == 'Male'
            school = student[2]
            cgpa = student[5]
            grade_list = []
            
            # Evaluate fitness of this student for each project group
            for project_group in final_list[tut_idx]:
                if len(project_group) == grp_size:
                    grade_list.append(-1) # Group is full
                    continue

                # Prepare info for scoring
                female_count = extract(project_group, 4).count('Female')
                male_count = extract(project_group, 4).count('Male')
                
                curr_cgpas = extract(project_group, 5)
                old_mean = (sum(curr_cgpas) / len(curr_cgpas)) if curr_cgpas else global_cgpa
                new_mean = (sum([*curr_cgpas, cgpa]) / (len(curr_cgpas) + 1))

                info = [
                    [int(female_count), int(male_count), is_male],
                    [extract(project_group, 2), school],
                    [old_mean, new_mean, global_cgpa]
                ]
                grade_list.append(grade(info))
            
            # Assign student to the best fitting group
            best_group_idx = grade_list.index(max(grade_list))
            final_list[tut_idx][best_group_idx].append(student)
            
    return final_list
