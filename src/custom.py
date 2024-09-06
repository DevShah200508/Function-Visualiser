from random import randint, uniform

"""Script to store all neccessary custom functions"""

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
    
# Custom method which tests a 100 different random values between -1000 and 1000 to see if the function inputted is actually valid 
def custom_test_valid_function(f) -> None:
    for _ in range(100):
        float(f(randint(-1000, 1000)))

# Custom function which returns a tuple containing random rgb values for a random color
def custom_get_random_color() -> tuple:
    r = uniform(0, 1)
    g = uniform(0, 1)
    b = uniform(0, 1)
    return (r, g, b)

def main():
    value1 = custom_round(-0.0001, 3)
    print(value1)

if __name__ == "__main__":
    main()
