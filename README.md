# Interpreter - Python Implementation

The aim is to build an interpreter from scratch by implementing each phase: scanning, parsing, resolving, interpreting, and more. This README documents the progress of the **Scanner (Lexer)**, **Parser**, and **Evaluator** stages.

---

## ⚙️ Setup Instructions

1. **Clone the repository**:
   ```bash
   git clone https://github.com/MohammedAbdulRahman0704/Interpreter.git
   cd Interpreter
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**:
   ```bash
   python -m unittest discover tests
   ```

---

## 📘 What is Scanning?

**Scanning (Lexical Analysis)** is the first phase in the interpretation process. It reads raw source code and converts it into a list of tokens which represent keywords, symbols, identifiers, etc.

---

## ✅ Implemented Scanner Features

We’ve implemented the following token scanning features so far:

### 1. 📄 Empty File Handling
- Gracefully processes and returns no tokens.

### 2. 🔄 Parentheses Scanning
- Recognizes `(` and `)` as valid tokens.

### 3. 🧱 Braces Scanning
- Recognizes `{` and `}`.

### 4. 🔣 Other Single-Character Tokens
- Handles characters like `,`, `.`, `;`, `-`, `+`, `*`, `/`.

### 5. ❌ Lexical Errors
- Detects and raises errors for unrecognized characters.

### 6. 🟰 Assignment & Equality Operators
- Handles `=` and `==` correctly.

### 7. ❗ Negation & Inequality Operators
- Recognizes `!` and `!=`.

### 8. 🔃 Relational Operators
- Supports `<`, `<=`, `>`, and `>=`.

### 9. ➗ Division Operator & Comments
- Differentiates between `/` (division) and `//` (comments).
- Ignores comments when tokenizing.

### 10. ␣ Whitespace Handling
- Skips over spaces, tabs, and newlines correctly.
- Keeps track of line numbers for error reporting.

### 11. 🧵 Multi-line Error Reporting
- Maintains correct line numbers when reporting errors across multiple lines.

### 12. 🧶 String Literals with Escape Sequences
- Supports string scanning like `"Hello, world!"` and `"He said \"Hi\"!"`.
- Detects unterminated strings and raises lexical errors.

### 13. 🔡 Identifiers and Keywords
- Recognizes variable names, function names, etc.
- Distinguishes between identifiers and reserved keywords like `if`, `else`, `true`, `false`, `nil`, `for`, `while`, etc.

### 14. 🔢 Number Literals
- Scans both integer and floating-point numbers, e.g. `123`, `3.14`.

---

## 🌲 Parser Features Implemented

The parser translates tokens into expressions in an Abstract Syntax Tree (AST).

### ✅ Supported Expression Parsing:

- **Booleans & Nil**: Parses `true`, `false`, and `nil` as literal expressions.
- **Number Literals**: Parses numeric tokens into literal expression nodes.
- **String Literals**: Parses quoted text into string literal expressions.
- **Grouping (Parentheses)**: Supports expressions like `(1 + 2)`.
- **Unary Operators**: Parses unary `!` and `-` expressions.
- **Binary Arithmetic (Part 1)**: Parses `*` and `/` for multiplication and division.
- **Binary Arithmetic (Part 2)**: Parses `+` and `-` for addition and subtraction.
- **String Concatenation**: Recognizes string concatenation via the `+` operator.
- **Comparison Operators**: Parses `<`, `<=`, `>`, `>=`.
- **Equality Operators**: Parses `==`, `!=`.

---

## 🧠 Evaluator Features Implemented

The interpreter evaluates expressions by traversing the AST.

### ✅ Supported Evaluation:

- **Literals**: Evaluates boolean, `nil`, string, and number literals.
- **Grouping**: Correctly evaluates parenthesized expressions.
- **Unary Operators**:
  - Logical NOT: `!`
  - Numeric Negation: `-`
- **Arithmetic Operators**:
  - Multiplication (`*`) and Division (`/`)
  - Addition (`+`) and Subtraction (`-`)
- **String Concatenation**:
  - Evaluates expressions like `"Hello, " + "World!"` resulting in string joining.
- **Equality Operators**:
  - Proper handling for `==` and `!=`, including comparison between different types and `nil`.

---

## 🔬 Testing

The project uses Python’s built-in `unittest` framework. Tests are written to cover scanning, parsing, and evaluation.

To run the tests:

```bash
python -m unittest discover tests
```

Example output:

```
........................................
----------------------------------------------------------------------
Ran 40 tests in 0.007s

OK
```

---

## 🚀 Upcoming Features

- Logical operators (`and`, `or`) in expressions
- AST pretty-printing / visualization
- Variable declarations and environments
- Expression statements and print statements
- Control flow: `if`, `while`, `for`
- Functions, closures, and classes
- REPL and file execution support

---

## 🙌 Contributions

Pull requests are welcome! If you’d like to contribute, feel free to fork the repository and submit a PR. Please ensure all tests pass before submitting.

---

## 🧠 Author

Developed with ❤️ by Mohammed Abdul Rahman

---

## 📖 License

This project is open-source and available under the [MIT License](LICENSE).
```

---