

def flatten_tuple(input_tuple):
    output_tuple = []
    for item in input_tuple:
        if isinstance(item, tuple):
            output_tuple.extend(item)
        else:
            output_tuple.append(item)
    return tuple(output_tuple)