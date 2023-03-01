def scale_list(coordinate_list):
    min_value = min(coordinate_list)
    for index, current_coordinate in enumerate(coordinate_list):
        coordinate_list[index] = current_coordinate - min_value
    return coordinate_list
