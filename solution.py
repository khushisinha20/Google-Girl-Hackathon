import itertools

class CircuitEvaluator:
    _instance = None

    @staticmethod
    def get_instance():
        if CircuitEvaluator._instance is None:
            CircuitEvaluator()
        return CircuitEvaluator._instance

    def __init__(self):
        if CircuitEvaluator._instance is not None:
            raise Exception("This class is a Singleton!")
        else:
            CircuitEvaluator._instance = self

    def evaluate_circuit(self, circuit_logic, input_values):
        Z = None
        for variable, value in input_values.items():
            exec(f"{variable} = {value}", globals())
        exec(circuit_logic.replace("~", "not "), globals())

        if "Z" in globals():
            Z = globals()["Z"]

        return Z


class FaultTestFinder:
    def __init__(self, circuit_evaluator):
        self.circuit_evaluator = circuit_evaluator

    def generate_input_combinations(self, input_variables):
        return list(itertools.product([0, 1], repeat=len(input_variables)))

    def find_fault_test_input(self, circuit_logic, fault_info, input_variables):
        fault_node_location, fault_type = fault_info
        input_combinations = self.generate_input_combinations(input_variables)
        fault_identifying_combination = None
        output = None

        for combination in input_combinations:
            input_values = {var: val for var, val in zip(input_variables, combination)}
            Z = self.circuit_evaluator.evaluate_circuit(circuit_logic, input_values)
            fault_condition = eval(fault_node_location)

            if (fault_type == "SA0" and fault_condition == 1) or (fault_type == "SA1" and fault_condition == 0):
                fault_identifying_combination = combination

            if (fault_type == "SA0" and fault_condition == 0) or (fault_type == "SA1" and fault_condition == 1):
                output = Z

            if output is not None and fault_identifying_combination is not None:
                return fault_identifying_combination, output

        raise ValueError("No fault test input found that satisfies the fault condition")



class FileManager:
    @staticmethod
    def read_file(file_path):
        try:
            with open(file_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {file_path}")

    @staticmethod
    def write_file(file_path, content):
        try:
            with open(file_path, "w") as file:
                file.write(content)
        except IOError:
            raise IOError(f"Error writing to file: {file_path}")


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


def main():
    circuit_file = "circuit.txt"
    fault_file = "fault.txt"
    output_file = "output.txt"
    input_variables = ["A", "B", "C", "D"]

    try:
        circuit_logic = FileManager.read_file(circuit_file)
        fault_info = get_fault_info(fault_file)
        
        circuit_evaluator = CircuitEvaluator.get_instance()
        fault_test_finder = FaultTestFinder(circuit_evaluator)
        
        fault_test_input, expected_output = fault_test_finder.find_fault_test_input(circuit_logic, fault_info, input_variables)

        input_vector = ", ".join(f"{variable}={value}" for variable, value in zip(input_variables, fault_test_input))
        content = f"Input Vector\t\tExpected Output\n{input_vector}\t{expected_output}\n"
        FileManager.write_file(output_file, content)
    except (FileNotFoundError, IOError, ValueError) as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()