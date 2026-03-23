def extract(a_list, index):
    """
    Helper function to extract a specific index from a list of lists.
    Returns [0] as default if the list is empty.
    """
    extracted_list = [item[index] for item in a_list]
    if extracted_list == []:
        extracted_list = [0]
    return extracted_list

def control_maker(sorted_list, grp_size):
    """
    Splits the tutorial groups into smaller project groups of the specified size.
    """
    control_list = []
    for tut_group in sorted_list:
        control_list.append([tut_group[x:x+grp_size] for x in range(0, len(tut_group), grp_size)])
    return control_list
