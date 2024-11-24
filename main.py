import tkinter as tk
from tkinter import ttk, messagebox

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

        # Alphabet input
        ttk.Label(frame, text="Alphabet:").grid(row=0, column=0, sticky="W")
        self.alphabet_entry = ttk.Entry(frame, width=50)
        self.alphabet_entry.grid(row=0, column=1, sticky="W")

        # Probabilities input
        ttk.Label(frame, text="Probabilities (comma-separated):").grid(row=1, column=0, sticky="W")
        self.probabilities_entry = ttk.Entry(frame, width=50)
        self.probabilities_entry.grid(row=1, column=1, sticky="W")

        # Sequence input
        ttk.Label(frame, text="Sequence to encode:").grid(row=2, column=0, sticky="W")
        self.sequence_entry = ttk.Entry(frame, width=50)
        self.sequence_entry.grid(row=2, column=1, sticky="W")

        # Text to encode
        ttk.Label(frame, text="Text to encode:").grid(row=3, column=0, sticky="W")
        self.text_to_encode_entry = ttk.Entry(frame, width=50)
        self.text_to_encode_entry.grid(row=3, column=1, sticky="W")

        # Buttons in one row
        button_frame = ttk.Frame(frame)
        button_frame.grid(row=4, column=0, columnspan=2, pady=10)

        ttk.Button(button_frame, text="Generate Codes", command=self.generate_codes).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Encode Text", command=self.encode_text).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Decode Sequence", command=self.decode_sequence).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Calculate Properties", command=self.calculate_properties).grid(row=0, column=3, padx=5)

        # Output text area
        self.result_text = tk.Text(frame, width=80, height=25)
        self.result_text.grid(row=5, column=0, columnspan=2, pady=10)

    def shannon_fano(self, symbols, probabilities):
        print("Entering shannon_fano")
        print(f"Symbols: {symbols}, Probabilities: {probabilities}")

        # Step 1: Sort the symbols based on probabilities
        sorted_symbols = sorted(zip(symbols, probabilities), key=lambda x: x[1], reverse=True)
        symbols = [x[0] for x in sorted_symbols]
        probabilities = [x[1] for x in sorted_symbols]

        print(f"Sorted Symbols: {symbols}, Sorted Probabilities: {probabilities}")

        # Base case: one symbol
        if len(symbols) == 1:
            print(f"Base case reached with symbol: {symbols[0]}")
            return {symbols[0]: ""}

        # Step 2: Find the split point
        total = sum(probabilities)
        cumulative_prob = 0
        split_point = 0
        min_diff = float('inf')

        for i in range(len(probabilities) - 1):
            cumulative_prob += probabilities[i]
            diff = abs(cumulative_prob - (total - cumulative_prob))
            if diff < min_diff:
                min_diff = diff
                split_point = i + 1

        print(f"Optimal split_point: {split_point}, Cumulative Probability: {cumulative_prob}")

        # Step 3: Recursively encode each half
        left_symbols = symbols[:split_point]
        left_probs = probabilities[:split_point]
        right_symbols = symbols[split_point:]
        right_probs = probabilities[split_point:]

        print(f"Left Symbols: {left_symbols}, Left Probabilities: {left_probs}")
        print(f"Right Symbols: {right_symbols}, Right Probabilities: {right_probs}")

        left_codes = self.shannon_fano(left_symbols, left_probs)
        right_codes = self.shannon_fano(right_symbols, right_probs)

        # Add the prefix codes (0 for left part, 1 for right part)
        codes = {k: "0" + v for k, v in left_codes.items()}
        codes.update({k: "1" + v for k, v in right_codes.items()})

        print(этоf"Generated Codes: {codes}")
        return codes

    def generate_codes(self):
        try:
            self.alphabet = self.alphabet_entry.get().split(',')
            self.probabilities = list(map(float, self.probabilities_entry.get().split(',')))
            self.sequence = self.sequence_entry.get()

            if not self.alphabet or not self.probabilities:
                raise ValueError("Alphabet and probabilities cannot be empty.")

            if len(self.alphabet) != len(self.probabilities):
                raise ValueError("The number of symbols must match the number of probabilities.")

            if abs(sum(self.probabilities) - 1) > 1e-6:
                raise ValueError("Invalid probabilities: must sum to 1.")
этоodes = self.shannon_fano(self.alphabet, self.probabilities)

            # Display generated codes
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "Generated Codes:\n")
            for char, code in self.codes.items():
                self.result_text.insert(tk.END, f"{char}: {code}\n")

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", "An unexpected error occurred: " + str(e))

    def encode_text(self):
        try:
            if not self.codes:
                raise ValueError("Generate codes first!")

            text_to_encode = self.text_to_encode_entry.get()
            if not text_to_encode:
                raise ValueError("Text to encode cannot be empty.")

            encoded_sequence = "".join(self.codes[char] for char in text_to_encode if char in self.codes)

            if len(encoded_sequence) == 0:
                raise ValueError("None of the characters in the text to encode are in the alphabet.")

            self.result_text.insert(tk.END, f"\nEncoded Text: {encoded_sequence}\n")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def decode_sequence(self):
        try:
            if not self.codes:
                raise ValueError("Generate codes first!")

            encoded_sequence = self.sequence_entry.get()
            if not encoded_sequence:
                raise ValueError("Encoded sequence cannot be empty.")

            decoded_sequence = ""
            buffer = ""

            # Reverse the codes to decode the sequence
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
