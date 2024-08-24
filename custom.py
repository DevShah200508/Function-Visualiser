# Custom rounding function used 
def custom_round(value: float, decimals: int) -> int:
    rounded_value = round(value, decimals)
    return int(rounded_value) if rounded_value.is_integer() else rounded_value

# Custom is constant check
def custom_is_constant(user_input: str) -> bool:
    try:
        float(user_input)
        return True 
    except ValueError:
        return False  

# Custom function to filter domain and range of a function between min and max bounds
def custom_function_filter(x: list, y: list, min_x: float, max_x: float, min_y: float, max_y: float) -> tuple:
    predicate = lambda pair: (min_x <= pair[0] <= max_x) and (min_y <= pair[1] <= max_y)
    joined_list = zip(x, y)
    filtered_list = list(filter(predicate, joined_list))
    x_filtered, y_filtered = zip(*filtered_list)
    return x_filtered, y_filtered
    
def main():
    value1 = custom_round(-0.0001, 3)
    print(value1)

if __name__ == "__main__":
    main()