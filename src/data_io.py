import random
import statistics

def load_and_clean_data(file_path, shuffle_alternative=True):
    """
    Reads the student records from CSV, cleans data, and organizes into 
    shuffled sublists for each tutorial group.
    """
    datamain = []
    with open(file_path, mode='r') as file:
        for line in file:
            # Clean 'G-' prefix and split by comma
            datamain.append(line.replace('G-', '').strip().split(','))
            
    if not datamain:
        return []
        
    del datamain[0] # Remove header row
    
    # Data type conversion
    for row in datamain:
        try:
            row[0] = int(row[0]) # Tutorial Group Index
            row[5] = float(row[5]) # CGPA
        except (ValueError, IndexError):
            continue
        
    datamain.sort() # Ensure sorted by tutorial group
    
    # Split the sorted data into tutorial groups (assumed size 50)
    sorted_list = [datamain[x:x+50] for x in range(0, len(datamain), 50)]
    
    # Randomize or sort by CGPA distance from mean within each group
    for sub_list in sorted_list:
        if not sub_list:
            continue
        else:
            tut_group_mean = statistics.mean([i[5] for i in sub_list])
            sub_list.sort(reverse=True, key=lambda x: abs(x[5] - tut_group_mean))
            
    return sorted_list

def save_grouping_results(final_sorted_list, input_file, output_file):
    """
    Exports the final student grouping results to a new CSV file.
    Optimized version of the notebook's 'record_maker'.
    """
    # Read all original lines
    with open(input_file, mode='r') as f:
        lines = f.readlines()
    
    header = lines[0].strip() + ",Team Assigned\n"
    # Map Student ID to their group assignment for fast lookup
    assignment_map = {}
    for tut_idx, tut_group in enumerate(final_sorted_list):
        for grp_idx, group in enumerate(tut_group):
            for student in group:
                student_id = student[1]
                assignment_map[student_id] = grp_idx + 1
    
    with open(output_file, mode='w') as f:
        f.write(header)
        for line in lines[1:]:
            line_parts = line.strip().split(',')
            if len(line_parts) < 2: continue
            student_id = line_parts[1]
            group_num = assignment_map.get(student_id, "N/A")
            f.write(f"{line.strip()},{group_num}\n")
    
    print(f"Results successfully exported to {output_file}")
