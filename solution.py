import itertools

# Define the circuit file path
circuit_file = "circuit.txt"
# Define the fault file path
fault_file = "fault.txt"
# Define the output file path
output_file = "output.txt"

# Read the circuit file to obtain the circuit logic
with open(circuit_file, "r") as file:
    circuit_logic = file.read()

# Replace the ~ operator with not
circuit_logic = circuit_logic.replace("~", "not ")

# Read the fault file to obtain the fault node location and fault type
with open(fault_file, "r") as file:
    fault_node_location = None
    fault_type = None

    for line in file:
        variable, value = line.strip().split("=")
        if variable.strip() == "FAULT_AT":
            fault_node_location = value.strip()
        elif variable.strip() == "FAULT_TYPE":
            fault_type = value.strip()

# Initialize the input vector for testing the fault
fault_test_input = []

# Iterate through all possible combinations of input values for A, B, C, and D
input_variables = ["A", "B", "C", "D"]
input_combinations = list(itertools.product([0, 1], repeat=len(input_variables)))

for combination in input_combinations:
    # Assign the current input combination to the input variables
    for variable, value in zip(input_variables, combination):
        exec(f"{variable} = {value}")

    # Evaluate the circuit output
    exec(circuit_logic)

    # Check if the fault condition is satisfied at the fault node
    fault_condition = eval(fault_node_location)

    # Check if the fault condition matches the fault type
    if (fault_type == "SA0" and fault_condition == 0) or (fault_type == "SA1" and fault_condition == 1):
        fault_test_input = combination
        break

z_value = eval('Z')

# Print the fault test input vector and the expected output for confirmation of the fault
with open(output_file, "w") as file:
    file.write("Input Vector\tExpected Output\n")
    input_vector = ", ".join(f"{variable}={value}" for variable, value in zip(input_variables, fault_test_input))
    file.write(f"{input_vector}\t{z_value}\n")
