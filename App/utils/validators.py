def get_input(type_value:object, prompt: str = "Please enter value: ") -> int | float | str:
    ''' This function takes input and checks its type. '''
    while True:
        try:
            user_input = input(prompt)
            check = user_input.replace(" ","")

            if not user_input:
                print("Input cannot be empty!")
                input("Enter to return...")
                continue

            if type_value == int or type_value == float:
                return type_value(check)
            
            if type_value == str:
                if check:
                    return user_input
                else:
                    print("Invalid input! Please use only letters.")

                    continue
        except:
            print("Invalid value. Please enter the correct value!")

def get_valid_choice(valid_list:list, prompt_text:str) -> str:
    """ Limit user access to list items """
    while True:
        user_input = input(prompt_text).strip().lower()
        if user_input in valid_list:
            return user_input
        else:
            print(f"Invalid input! Please choose from: {valid_list}")