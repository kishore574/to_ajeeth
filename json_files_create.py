import os
import pickle
import json

# Define the FunctionNode class to ensure proper unpickling
class FunctionNode:
    def __init__(self, name, params, file, line, code):
        self.name = name
        self.params = params
        self.file = file
        self.line = line
        self.code = code
        self.called_functions = []
        self.local_variables = []

    def to_dict(self):
        return {
            "name": self.name,
            "params": self.params,
            "file": self.file,
            "line": self.line,
            "code": self.code,
            "called_functions": self.called_functions,
            "local_variables": self.local_variables,
        }

    def __repr__(self):
        return (f"FunctionNode(name={self.name}, params={self.params}, file={self.file}, "
                f"line={self.line}, code={self.code}, called_functions={self.called_functions}, "
                f"local_variables={self.local_variables})")

# Function to load pickle file
def load_pickle_file(file_path):
    try:
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
            return data
    except Exception as e:
        print(f"An error occurred while loading the pickle file: {e}")
        return None

# Function to convert objects to dictionary format
def convert_to_dict(data):
    if isinstance(data, dict):
        return {k: convert_to_dict(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_to_dict(item) for item in data]
    elif hasattr(data, 'to_dict'):
        return data.to_dict()
    elif hasattr(data, '__dict__'):
        return {k: convert_to_dict(v) for k, v in data.__dict__.items()}
    else:
        return data

# Function to save data to JSON file
def save_to_json(data, output_file):
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        print(f"Data successfully saved to {output_file}")
    except Exception as e:
        print(f"An error occurred while saving to JSON: {e}")

# Function to create JSON structure from node to root
def create_json_to_root(node_name, data):
    visited = set()
    sequence = 1  # Initialize sequence counter
    json_output = []

    def traverse_to_root(current_name):
        nonlocal sequence
        if current_name in visited or current_name not in data:
            return
        visited.add(current_name)
        current_node = data[current_name]
        
        node_info = {
            "sequence": sequence,
            "name": current_node.name,
            "params": current_node.params,
            "file": current_node.file,
            "line": current_node.line,
            "called_functions": current_node.called_functions
        }
        json_output.append(node_info)
        sequence += 1  # Increment sequence number

        for parent_name, parent_node in data.items():
            if current_name in parent_node.called_functions:
                traverse_to_root(parent_name)

    traverse_to_root(node_name)
    return json_output

# Function to create JSON structure from node to leaves
def create_json_to_leaves(node_name, data):
    visited = set()
    sequence = 1  # Initialize sequence counter
    json_output = []

    def traverse_to_leaves(current_name):
        nonlocal sequence
        if current_name in visited or current_name not in data:
            return
        visited.add(current_name)
        current_node = data[current_name]

        node_info = {
            "sequence": sequence,
            "name": current_node.name,
            "params": current_node.params,
            "file": current_node.file,
            "line": current_node.line,
            "local_variables": current_node.local_variables,
            "called_functions": current_node.called_functions
        }
        json_output.append(node_info)
        sequence += 1  # Increment sequence number

        for called_function in current_node.called_functions:
            traverse_to_leaves(called_function)

    traverse_to_leaves(node_name)
    return json_output

def main(pickle_file, output_dir_to_root, output_dir_to_leaves):
    # Load the pickle file
    data = load_pickle_file(pickle_file)
    
    if data is not None:
        # Convert the data to a dictionary format for general JSON output
        data_dict = convert_to_dict(data)
        
        # Save the converted data to a general JSON file
        json_file = os.path.join(output_dir_to_root, 'function_tree.json')
        save_to_json(data_dict, json_file)
        
        # Create output directories if they don't exist
        os.makedirs(output_dir_to_root, exist_ok=True)
        os.makedirs(output_dir_to_leaves, exist_ok=True)

        # Save individual JSON files for each function showing paths to root and leaves
        for func_name in data.keys():
            # JSON from node to root
            json_to_root = create_json_to_root(func_name, data)
            json_to_root_path = os.path.join(output_dir_to_root, f'{func_name}.json')
            with open(json_to_root_path, 'w', encoding='utf-8') as f:
                json.dump(json_to_root, f, indent=4)
            print(f"JSON to root for {func_name} saved to {json_to_root_path}")

            # JSON from node to leaves
            json_to_leaves = create_json_to_leaves(func_name, data)
            json_to_leaves_path = os.path.join(output_dir_to_leaves, f'{func_name}.json')
            with open(json_to_leaves_path, 'w', encoding='utf-8') as f:
                json.dump(json_to_leaves, f, indent=4)
            print(f"JSON to leaves for {func_name} saved to {json_to_leaves_path}")

        print("All JSON files have been generated and saved.")
    else:
        print("No data to convert.")

if __name__ == "__main__":
    # Specify the paths for the pickle and output JSON files
    pickle_file = "D:/code/c_ai_browser/parser/pkl_file/function_tree.pkl"  # Replace with your pickle file path
    output_dir_to_root = 'D:/code/output_json/to_root'
    output_dir_to_leaves = 'D:/code/output_json/to_leaves'
    
    # Convert the pickle file to JSON files
    main(pickle_file, output_dir_to_root, output_dir_to_leaves)
