import ast
import math
import tkinter as tk


class CalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculator")
        self.root.geometry("420x560")
        self.root.resizable(False, False)

        self.expression = ""
        self.result_shown = False

        self.display_var = tk.StringVar()
        self.display_var.set("0")

        display = tk.Entry(
            root,
            textvariable=self.display_var,
            font=("Arial", 34),
            bd=0,
            justify="right",
            readonlybackground="#f8f8f8",
            fg="#1f1f1f",
            relief="flat",
        )
        display.grid(row=0, column=0, columnspan=4, sticky="nsew", padx=12, pady=(12, 8))

        root.grid_rowconfigure(0, weight=1)
        for i in range(4):
            root.grid_columnconfigure(i, weight=1)
        root.grid_rowconfigure(1, weight=1)

        buttons = [
            ["C", "⌫", "/", "*"],
            ["7", "8", "9", "-"],
            ["4", "5", "6", "+"],
            ["1", "2", "3", "="],
            ["0", "."],
        ]

        self.button_map = {}
        for row_index, row in enumerate(buttons):
            for col_index, label in enumerate(row):
                btn = tk.Button(
                    root,
                    text=label,
                    font=("Arial", 20, "bold"),
                    command=lambda value=label: self.handle_button(value),
                    width=4,
                    height=2,
                    bg="#f2f2f2" if label not in {"+", "-", "*", "/", "="} else "#f7d9a4",
                    fg="#1f1f1f",
                    bd=0,
                    relief="flat",
                )
                btn.grid(row=row_index + 1, column=col_index, sticky="nsew", padx=5, pady=5)
                self.button_map[label] = btn

        root.grid_columnconfigure(0, weight=1)
        root.grid_columnconfigure(1, weight=1)
        root.grid_columnconfigure(2, weight=1)
        root.grid_columnconfigure(3, weight=1)

        for i in range(1, 6):
            root.grid_rowconfigure(i, weight=1)

        root.bind("<KeyPress>", self.key_press)

    def update_display(self):
        if self.expression == "":
            self.display_var.set("0")
        else:
            self.display_var.set(self.expression)

    def handle_button(self, value):
        if value == "C":
            self.expression = ""
            self.result_shown = False
            self.update_display()
            return

        if value == "⌫":
            if self.expression and not self.result_shown:
                self.expression = self.expression[:-1]
            elif self.result_shown:
                self.expression = ""
                self.result_shown = False
            self.update_display()
            return

        if value == "=":
            self.evaluate_expression()
            return

        if value in {"+", "-", "*", "/"}:
            if self.expression and self.expression[-1] in {"+", "-", "*", "/"}:
                self.expression = self.expression[:-1] + value
            else:
                self.expression += value
            self.result_shown = False
            self.update_display()
            return

        if value == ".":
            if self.result_shown:
                self.expression = ""
                self.result_shown = False
            if self.expression == "" or self.expression[-1] in {"+", "-", "*", "/", "("}:
                self.expression += "0."
            elif "." not in self.expression.split("+")[-1].split("-")[-1].split("*")[-1].split("/")[-1]:
                self.expression += "."
            self.update_display()
            return

        if self.result_shown:
            self.expression = ""
            self.result_shown = False

        self.expression += value
        self.update_display()

    def evaluate_expression(self):
        expr = self.expression.strip()
        if not expr:
            self.display_var.set("0")
            return

        try:
            result = self._safe_eval(expr)
        except ZeroDivisionError:
            self.display_var.set("Error")
            self.expression = ""
            self.result_shown = True
            return
        except Exception:
            self.display_var.set("Error")
            self.expression = ""
            self.result_shown = True
            return

        if isinstance(result, float) and math.isfinite(result):
            if result.is_integer():
                result = int(result)
            else:
                result = round(result, 10)
        self.expression = str(result)
        self.result_shown = True
        self.display_var.set(self.expression)

    def _safe_eval(self, expr):
        node = ast.parse(expr, mode="eval")
        return self._eval_node(node.body)

    def _eval_node(self, node):
        if isinstance(node, ast.Constant):
            number = node.value
            if isinstance(number, (int, float)):
                return number
            raise ValueError("Unsupported constant")

        if isinstance(node, ast.BinOp):
            left = self._eval_node(node.left)
            right = self._eval_node(node.right)

            if isinstance(node.op, ast.Add):
                return left + right
            if isinstance(node.op, ast.Sub):
                return left - right
            if isinstance(node.op, ast.Mult):
                return left * right
            if isinstance(node.op, ast.Div):
                return left / right
            raise ValueError("Unsupported operator")

        if isinstance(node, ast.UnaryOp):
            value = self._eval_node(node.operand)
            if isinstance(node.op, ast.UAdd):
                return +value
            if isinstance(node.op, ast.USub):
                return -value
            raise ValueError("Unsupported unary operator")

        raise ValueError("Unsupported expression")

    def key_press(self, event):
        key = event.char
        if key.isdigit() or key in {".", "+", "-", "*", "/"}:
            self.handle_button(key)
        elif key == "\r":
            self.evaluate_expression()
        elif key == "\x08":
            self.handle_button("⌫")
        elif key == "c" or key == "C":
            self.handle_button("C")


def main():
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
