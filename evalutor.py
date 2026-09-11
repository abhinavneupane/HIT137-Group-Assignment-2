# HIT137 Assignment 2 Q2
# Student: Bilal Maqbool

def tokenize(expression):
    tokens = []
    index = 0
    while index < len(expression):
        ch = expression[index]
        if ch == ' ':
            index = index+1
            continue
        if ch.isdigit():
            number = ''
            while index < len(expression) and (expression[index].isdigit() or expression[index] == '.'):

                number += expression[index]
                index += 1
            tokens.append(('NUM', number))
            continue

        elif ch in '+-*/%^':
            tokens.append(('OP', ch))
        elif ch == ')':
            tokens.append(('RPAREN', ch))
        elif ch == '(':
            tokens.append(('LPAREN', ch))
        else:
            return None
        index += 1

    tokens.append(('END', ''))
    return tokens


def format_tokens(tokens):
    token_str = ''
    for token_type, token_value in tokens:
        if token_type == 'END':
            token_str += '[END]'
        else:
            token_str += '['+token_type+':'+token_value+']'
    return token_str.strip()


def current(parser):
    return parser['tokens'][parser]['index']


def eat(parser, expected=None):
    tok = current(parser)
    if expected and tok[0] != expected:
        raise Exception('ERROR')
    parser['index'] += 1
    return tok


def primary(parser):
    tok_type, tok_val = current(parser)
    if tok_type == 'NUM':
        eat(parser, 'NUM')
        return {'type': 'num', 'value': float(tok_val)}
    if tok_type == 'LPAREN':
        eat(parser, 'LPAREN')
        node = expr(parser)
        eat(parser, 'RPAREN')
        return node
    raise Exception('ERROR')


def unary(parser):
    tok_type, tok_val = current(parser)
    if tok_type == "OP" and tok_val == '-':
        eat(parser, 'OP')
        node = unary(parser)
        return {'type': 'op', 'op': '-', 'left': {'type': 'num', 'value': 0.0}, 'right': node}
    return primary(parser)


def evaluate_file(input_path):
    results = []
    infile = open(input_path, 'r')
    lines = infile.readlines()
    infile.close()
    for line in lines:
        expression = line.strip()
        if expression == '':
            continue

        tokens = tokenize(expression)
        if tokens is None:
            print(expression)
            print('ERROR')
            print()
        else:
            formatted = format_tokens(tokens)
            print(expression)
            print(formatted)
            print()
    return results


evaluate_file('sample_input.txt')
