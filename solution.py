import itertools

def read_file(file_path):
    try:
        with open(file_path, "r") as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")

def write_file(file_path, content):
    try:
        with open(file_path, "w") as file:
            file.write(content)
    except IOError:
        raise IOError(f"Error writing to file: {file_path}")

def evaluate_circuit(circuit_logic, input_values):
    Z = None  
    for variable, value in input_values.items():
        exec(f"{variable} = {value}", globals())
    exec(circuit_logic.replace("~", "not "), globals())

    if "Z" in globals():  
        Z = globals()["Z"]

    return Z

def get_fault_info(fault_file):
    fault_node_location = None
    fault_type = None

    with open(fault_file, "r") as file:
        for line in file:
            variable, value = line.strip().split("=")
            if variable.strip() == "FAULT_AT":
                fault_node_location = value.strip()
            elif variable.strip() == "FAULT_TYPE":
                fault_type = value.strip()

    if not fault_node_location or not fault_type:
        raise ValueError("Fault information not found in the fault file")

    return fault_node_location, fault_type

def generate_input_combinations(input_variables):
    return list(itertools.product([0, 1], repeat=len(input_variables)))

def find_fault_test_input(circuit_logic, fault_info, input_variables):
    fault_node_location, fault_type = fault_info
    input_combinations = generate_input_combinations(input_variables)

    for combination in input_combinations:
        input_values = {var: val for var, val in zip(input_variables, combination)}
        Z = evaluate_circuit(circuit_logic, input_values)
        fault_condition = eval(fault_node_location)

        if (fault_type == "SA0" and fault_condition == 0) or (fault_type == "SA1" and fault_condition == 1):
            return combination, Z

    raise ValueError("No fault test input found that satisfies the fault condition")

def main():
    circuit_file = "circuit.txt"
    fault_file = "fault.txt"
    output_file = "output.txt"
    input_variables = ["A", "B", "C", "D"]

    try:
        circuit_logic = read_file(circuit_file)
        fault_info = get_fault_info(fault_file)
        fault_test_input, expected_output = find_fault_test_input(circuit_logic, fault_info, input_variables)

        input_vector = ", ".join(f"{variable}={value}" for variable, value in zip(input_variables, fault_test_input))
        content = f"Input Vector\t\tExpected Output\n{input_vector}\t{expected_output}\n"
        write_file(output_file, content)
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()