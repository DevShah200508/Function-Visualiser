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

def main():
    value1 = custom_round(-0.0001, 3)
    print(value1)

if __name__ == "__main__":
    main()
