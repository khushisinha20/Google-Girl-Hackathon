# Fault Test Input Finder

<p>This code provides a solution to identify the input vector required to identify a fault at a given node in a given circuit. The circuit is defined in a circuit.txt file, and the fault information is provided in a fault.txt file. The code finds the input vector and expected output that would reveal the fault and writes them to an output.txt file.</p>

### Installation

<p>To run the code, you need Python 3 installed on your system. You can clone the code repository from GitHub:</p>

```bash
git clone https://github.com/khushisinha20/Google-Girl-Hackathon.git
```

### Usage

1. Create two files: `circuit.txt` and `fault.txt`.
2. In `ciruit.txt`, define the circuit logic.
    - The circuit should have 4 inputs: A, B, C, D, with boolean values 0 and 1.
    - The circuit will always produce a boolean output represented by 'Z'.
    - The circuit uses the following logic gates: AND (&), OR (|), NOT (~), and XOR (^).
    - The circuit must be a purely combinational logic circuit.
    - Internal nodes in the circuit should be named as "net_&lt;alphanumeric_string&gt;".
    - Every input (A, B, C, D) should be used exactly once within the circuit.
3. In the `fault.txt` file, provide the fault information in the following format:
    - `FAULT_AT = <fault_node_location>`: Specify the location of the fault node in the circuit.
    - `FAULT_TYPE = <fault_type>`: Specify the type of fault (`SA0` for stuck-at-0 or `SA1` for stuck-at-1).
4. Run the code using the following command:
```bash
python solution.py
```
5. The output vector and expected output will be written to the `output.txt` file.

### Example

Let's consider an example to illustrate the input format and expected output:

#### Circuit File (`circuit.txt`):
```makefile
net_e = A & B
net_f = C | D
net_g = ~ net_f
Z = net_g ^ net_e
```

#### Fault File (`fault.txt`):
```makefile
FAULT_AT = net_f
FAULT_TYPE = SA0
```

#### Expected Output (`output.txt`):
```makefile
Input Vector       Expected Output
A=0, B=0, C=0, D=1   Z=1
```

<p>In this example, the code will identify the input vector [0, 0, 0, 0] that will reveal the fault at node net_f. The expected output for this input vector is Z=1.</p>

### Requirements
<p>The code does not have any external dependencies beyond the Python standard library.</p>

<p>Feel free to modify and adapt the code as needed for your specific requirements.</p>