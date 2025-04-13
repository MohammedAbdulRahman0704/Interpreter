from scanner import Scanner

def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()
    for token in tokens:
        print(token)

if __name__ == "__main__":
    code = ""  # Empty input
    run(code)