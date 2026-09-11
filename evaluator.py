def tokenize(expression):
    tokens = []
    i = 0

    while i < len(expression):
        char = expression[i]

        # Ignore spaces
        if char.isspace():
            i += 1
            continue

        # Numbers
        if char.isdigit():
            number = char
            i += 1

            while i < len(expression) and expression[i].isdigit():
                number += expression[i]
                i += 1

            # Check for decimal part
            if i < len(expression) and expression[i] == ".":
                number += "."
                i += 1

                if i >= len(expression) or not expression[i].isdigit():
                    raise ValueError("Invalid number")

                while i < len(expression) and expression[i].isdigit():
                    number += expression[i]
                    i += 1

            tokens.append(("NUM", number))
            continue

        # Opening parenthesis
        if char == "(":
            tokens.append(("LPAREN", "("))
            i += 1
            continue

        # Closing parenthesis
        if char == ")":
            tokens.append(("RPAREN", ")"))
            i += 1
            continue

        # Operators
        if char in "+-*/%^":
            tokens.append(("OP", char))
            i += 1
            continue

        # Invalid character
        raise ValueError("Invalid character")

    tokens.append(("END", ""))
    return tokens


def parse_primary(tokens, position):
    token_type, token_value = tokens[position]

    # Number
    if token_type == "NUM":
        return token_value, position + 1

    # Parentheses
    if token_type == "LPAREN":
        position += 1

        tree, position = parse_expression(tokens, position)

        if tokens[position][0] != "RPAREN":
            raise ValueError("Expected closing parenthesis")

        position += 1
        return tree, position

    raise ValueError("Expected number or parenthesis")


def parse_power(tokens, position):
    left, position = parse_primary(tokens, position)

    # Exponentiation is right-associative
    if tokens[position][0] == "OP" and tokens[position][1] == "^":
        position += 1

        # Allow unary negative after ^
        right, position = parse_unary(tokens, position)

        left = ("^", left, right)

    return left, position


def parse_unary(tokens, position):
    # Unary negative
    if tokens[position][0] == "OP" and tokens[position][1] == "-":
        position += 1

        operand, position = parse_unary(tokens, position)

        return ("neg", operand), position

    # Unary plus is not supported
    if tokens[position][0] == "OP" and tokens[position][1] == "+":
        raise ValueError("Unary plus is not supported")

    return parse_power(tokens, position)


def parse_term(tokens, position):
    left, position = parse_unary(tokens, position)

    while True:

        # Normal multiplication, division, or modulo
        if tokens[position][0] == "OP" and tokens[position][1] in "*/%":
            operator = tokens[position][1]
            position += 1

            right, position = parse_unary(tokens, position)

            left = (operator, left, right)

        # Implicit multiplication with opening parenthesis
        elif tokens[position][0] == "LPAREN":
            right, position = parse_unary(tokens, position)

            left = ("*", left, right)

        # Implicit multiplication after closing parenthesis
        elif tokens[position][0] == "NUM":
            if position > 0 and tokens[position - 1][0] == "RPAREN":
                right, position = parse_unary(tokens, position)

                left = ("*", left, right)
            else:
                # Example: 2 3 is NOT implicit multiplication
                raise ValueError("Adjacent numbers are not allowed")

        else:
            break

    return left, position


def parse_expression(tokens, position):
    left, position = parse_term(tokens, position)

    # Addition and subtraction
    while tokens[position][0] == "OP" and tokens[position][1] in "+-":
        operator = tokens[position][1]
        position += 1

        right, position = parse_term(tokens, position)

        left = (operator, left, right)

    return left, position


def tree_to_string(tree):
    # Number
    if isinstance(tree, str):
        return tree

    # Unary negative
    if tree[0] == "neg":
        return "(neg " + tree_to_string(tree[1]) + ")"

    # Binary operator
    operator = tree[0]
    left = tree_to_string(tree[1])
    right = tree_to_string(tree[2])

    return "(" + operator + " " + left + " " + right + ")"


def evaluate_tree(tree):
    # Number
    if isinstance(tree, str):
        return float(tree)

    # Unary negative
    if tree[0] == "neg":
        return -evaluate_tree(tree[1])

    # Binary operation
    operator = tree[0]

    left = evaluate_tree(tree[1])
    right = evaluate_tree(tree[2])

    if operator == "+":
        return left + right

    if operator == "-":
        return left - right

    if operator == "*":
        return left * right

    if operator == "/":
        if right == 0:
            raise ZeroDivisionError

        return left / right

    if operator == "%":
        if right == 0:
            raise ZeroDivisionError

        return left % right

    if operator == "^":
        result = left ** right

        # Reject complex results
        if isinstance(result, complex):
            raise ValueError("Complex result")

        return result

    raise ValueError("Unknown operator")


def tokens_to_string(tokens):
    parts = []

    for token_type, token_value in tokens:

        if token_type == "END":
            parts.append("[END]")
        else:
            parts.append(
                "[" + token_type + ":" + token_value + "]"
            )

    return " ".join(parts)


def evaluate_file(input_path: str) -> list[dict]:
    results = []

    # Read input file
    with open(input_path, "r") as file:
        lines = file.readlines()

    # Process each expression
    for line in lines:

        # Remove only the line ending
        expression = line.rstrip("\r\n")

        # Skip empty lines
        if expression.strip() == "":
            continue

        try:
            # Tokenize
            tokens = tokenize(expression)

            # Parse
            tree, position = parse_expression(tokens, 0)

            # Make sure the entire expression was used
            if tokens[position][0] != "END":
                raise ValueError("Unexpected token")

            # Convert tree and tokens
            tree_text = tree_to_string(tree)
            tokens_text = tokens_to_string(tokens)

            # Calculate result
            try:
                result = evaluate_tree(tree)

            except (
                ZeroDivisionError,
                ValueError,
                OverflowError,
                TypeError
            ):
                result = "ERROR"

        except (
            ValueError,
            IndexError
        ):
            tree_text = "ERROR"
            tokens_text = "ERROR"
            result = "ERROR"

        # Store result
        results.append({
            "input": expression,
            "tree": tree_text,
            "tokens": tokens_text,
            "result": result
        })

    # Create output.txt in the same folder
    import os

    output_path = os.path.join(
        os.path.dirname(input_path),
        "output.txt"
    )

    # Write output file
    with open(output_path, "w") as file:

        for index, item in enumerate(results):

            file.write(
                "Input: " + item["input"] + "\n"
            )

            file.write(
                "Tree: " + item["tree"] + "\n"
            )

            file.write(
                "Tokens: " + item["tokens"] + "\n"
            )

            result = item["result"]

            if result == "ERROR":
                result_text = "ERROR"

            elif result == int(result):
                result_text = str(int(result))

            else:
                result_text = (
                    f"{result:.4f}"
                    .rstrip("0")
                    .rstrip(".")
                )

            file.write(
                "Result: " + result_text + "\n"
            )

            # Blank line between expressions
            if index < len(results) - 1:
                file.write("\n")

    return results


if __name__ == "__main__":
    evaluate_file("input.txt")