Here's the updated `README.md` reflecting progress through:

- Scanning: Identifiers, Reserved Words  
- Parsing: Booleans, Nil, Number Literals, and String Literals  

---

```markdown
# Interpreter - Python Implementation

The aim is to build an interpreter from scratch by implementing each phase: scanning, parsing, resolving, interpreting, and more. This README documents the progress of the **Scanner (Lexer)** and **Parser** stages.

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

## 🧮 Parser Features Implemented

The parser translates tokens into expressions in an Abstract Syntax Tree (AST).

### ✅ Supported Expression Parsing:

- **Booleans & Nil**: Parses `true`, `false`, and `nil` as literal expressions.
- **Number Literals**: Parses numeric tokens into literal expression nodes.
- **String Literals**: Parses quoted text into string literal expressions.

---

## 🔬 Testing

The project uses Python’s built-in `unittest` framework. Tests are written to cover all scanning and parsing functionalities.

To run the tests:

```bash
python -m unittest discover tests
```

You should see an output similar to:

```
....................
----------------------------------------------------------------------
Ran 20 tests in 0.004s

OK
```

---

## 🚀 Upcoming Features

- Full expression grammar support (grouping, unary, binary operations)
- Parsing logical operators, comparison, equality
- AST pretty-printing / visualization
- Expression evaluation (Interpreter)
- Variable declarations and environments
- Control flow: `if`, `while`, `for`
- Functions, classes, and closures
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

Let me know if you want this split into multiple sections (e.g., `SCANNER.md`, `PARSER.md`), or if you'd like badges, TOC, or diagrams added.