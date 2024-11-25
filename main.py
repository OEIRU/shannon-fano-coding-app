import tkinter as tk
from tkinter import ttk, messagebox, filedialog


class ShannonFanoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Shannon-Fano Coding Application")

        # Variables for alphabet and probabilities
        self.alphabet = []
        self.probabilities = []
        self.sequence = ""
        self.codes = {}

        # Interface setup
        self.setup_ui()

    def setup_ui(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky="NSEW")

        # Input fields with file loading option
        self.create_input_field(frame, "Alphabet:", 0, self.load_alphabet_from_file)
        self.create_input_field(frame, "Probabilities (comma-separated):", 1, self.load_probabilities_from_file)
        self.create_input_field(frame, "Sequence to encode:", 2, self.load_sequence_from_file)
        self.create_input_field(frame, "Text to encode:", 3, self.load_text_to_encode_from_file)

        # Buttons in one row
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Generate Codes", command=self.generate_codes).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Encode Text", command=self.encode_text).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Decode Sequence", command=self.decode_sequence).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Calculate Properties", command=self.calculate_properties).grid(row=0, column=3,
                                                                                                      padx=5)

        # Output text area
        self.result_text = tk.Text(frame, width=80, height=25)
        self.result_text.grid(row=5, column=0, columnspan=2, pady=10)

    def create_input_field(self, frame, label_text, row, file_load_command):
        ttk.Label(frame, text=label_text).grid(row=row, column=0, sticky="W")
        entry = ttk.Entry(frame, width=50)
        entry.grid(row=row, column=1, sticky="W")
        file_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Load from file", variable=file_var, command=lambda: file_load_command(entry)).grid(
            row=row, column=2)

        # Set the entry as an attribute of the class
        if "Alphabet" in label_text:
            self.alphabet_entry = entry
        elif "Probabilities" in label_text:
            self.probabilities_entry = entry
        elif "Sequence to encode" in label_text:
            self.sequence_entry = entry
        elif "Text to encode" in label_text:
            self.text_to_encode_entry = entry

    def load_from_file(self, entry):
        filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))
        if filename:
            try:
                with open(filename, 'r') as file:
                    entry.delete(0, tk.END)
                    entry.insert(0, file.read().strip())
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open file: {str(e)}")

    def load_alphabet_from_file(self, entry):
        self.load_from_file(entry)

    def load_probabilities_from_file(self, entry):
        self.load_from_file(entry)

    def load_sequence_from_file(self, entry):
        self.load_from_file(entry)

    def load_text_to_encode_from_file(self, entry):
        self.load_from_file(entry)

    def shannon_fano(self, symbols, probabilities):
        if len(symbols) == 1:
            return {symbols[0]: ""}

        # Sort symbols and probabilities
        sorted_pairs = sorted(zip(symbols, probabilities), key=lambda x: x[1], reverse=True)
        symbols, probabilities = zip(*sorted_pairs)

        total = sum(probabilities)
        cumulative_prob = 0

        # Use a loop to find the split point
        split_point = 0
        min_diff = float('inf')
        for i in range(len(probabilities) - 1):
            cumulative_prob += probabilities[i]
            diff = abs(cumulative_prob - (total - cumulative_prob))
            if diff < min_diff:
                min_diff = diff
                split_point = i
        #split_point = 0
        #for i in range(len(probabilities) - 1):
        #    cumulative_prob += probabilities[i]
        #    if abs(cumulative_prob - (total - cumulative_prob)) < abs(cumulative_prob - (total - cumulative_prob)):
        #        split_point = i
        left_symbols, left_probs = symbols[:split_point + 1], probabilities[:split_point + 1]
        right_symbols, right_probs = symbols[split_point + 1:], probabilities[split_point + 1:]

        left_codes = self.shannon_fano(left_symbols, left_probs)
        right_codes = self.shannon_fano(right_symbols, right_probs)

        # Add prefixes
        return {k: '0' + v for k, v in left_codes.items()} | {k: '1' + v for k, v in right_codes.items()}

    def generate_codes(self):
        try:
            self.alphabet = self.alphabet_entry.get().strip().split(',')
            self.probabilities = list(map(float, self.probabilities_entry.get().strip().split(',')))
            self.sequence = self.sequence_entry.get().strip()

            if not self.alphabet or not self.probabilities:
                raise ValueError("Alphabet and probabilities cannot be empty.")
            if len(self.alphabet) != len(self.probabilities):
                raise ValueError("The number of symbols must match the number of probabilities.")
            if abs(sum(self.probabilities) - 1) > 1e-6:
                raise ValueError("Invalid probabilities: must sum to 1.")

            self.codes = self.shannon_fano(self.alphabet, self.probabilities)
            self.display_codes()

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def display_codes(self):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Generated Codes:\n")
        for char, code in self.codes.items():
            self.result_text.insert(tk.END, f"{char}: {code}\n")

    def encode_text(self):
        try:
            if not self.codes:
                raise ValueError("Generate codes first!")

            text_to_encode = self.text_to_encode_entry.get().strip()
            if not text_to_encode:
                raise ValueError("Text to encode cannot be empty.")

            encoded_sequence = "".join(self.codes.get(char, '') for char in text_to_encode)
            if not encoded_sequence:
                raise ValueError("None of the characters in the text to encode are in the alphabet.")

            self.result_text.insert(tk.END, f"\nEncoded Text: {encoded_sequence}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_sequence(self):
        try:
            if not self.codes:
                raise ValueError("Generate codes first!")

            encoded_sequence = self.sequence_entry.get().strip()
            if not encoded_sequence:
                raise ValueError("Encoded sequence cannot be empty.")

            decoded_sequence, buffer = "", ""
            code_to_char = {v: k for k, v in self.codes.items()}

            for bit in encoded_sequence:
                buffer += bit
                if buffer in code_to_char:
                    decoded_sequence += code_to_char[buffer]
                    buffer = ""

            if buffer:
                raise ValueError("The encoded sequence contains invalid bits.")

            self.result_text.insert(tk.END, f"\nDecoded Sequence: {decoded_sequence}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_properties(self):
        try:
            if not self.codes:
                raise ValueError("Generate codes first!")

            avg_length = self.calculate_average_code_length()
            entropy_value = self.entropy()
            redundancy_value = self.redundancy(avg_length, entropy_value)
            kraft_check = "Yes" if self.kraft_mcmillan_inequality_check() else "No"

            self.result_text.insert(tk.END, f"\nProperties:\n"
                                            f"Average Code Length: {avg_length:.2f}\n"
                                            f"Entropy: {entropy_value:.2f}\n"
                                            f"Redundancy: {redundancy_value:.2f}\n"
                                            f"Kraft-McMillan Inequality: {kraft_check}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def calculate_average_code_length(self):
        return sum(len(code) * prob for code, prob in zip(self.codes.values(), self.probabilities))

    def entropy(self):
        return -sum(p * (p if p > 0 else 0) for p in self.probabilities)

    def redundancy(self, avg_length, entropy_value):
        return avg_length - entropy_value

    def kraft_mcmillan_inequality_check(self):
        return sum(2 ** -len(code) for code in self.codes.values()) <= 1


if __name__ == "__main__":
    root = tk.Tk()
    app = ShannonFanoApp(root)
    root.mainloop()
