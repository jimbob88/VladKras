import string
import pprint

if __name__ == '__main__':
    with open('example2.st', 'r') as f:
        text = f.read()


    finished = False
    char_pos = 0
    whitespace = ['\n', '\r', ' ', '\t']
    tokens = [] # list of tuples
    temp_char=''
    while not finished:
        if text[char_pos] in whitespace:
            # Skips all whitespace
            char_pos += 1  
        elif text[char_pos] == '{':
            # Matches start of blocks
            tokens.append(('START_BLOCK', char_pos, '{'))
            char_pos += 1    
        elif text[char_pos] == '}':
            # Matches end of blocks
            tokens.append(('END_BLOCK', char_pos, '}'))
            char_pos += 1
        elif text[char_pos] == ';':
            tokens.append(('END_LINE', char_pos, ';'))
            char_pos += 1
        elif text[char_pos] == '+':
            if text[char_pos + 1] == '=':
                tokens.append(('PLUS_EQUALS', char_pos, '+='))
                char_pos += 2
            elif text[char_pos + 1] == '+':
                tokens.append(('PLUS_ONE', char_pos, '++'))
                char_pos += 2
            else:
                tokens.append(('PLUS', char_pos, '+'))
                char_pos += 1
        elif text[char_pos] == '-':
            if text[char_pos + 1] == '=':
                tokens.append(('MINUS_EQUALS', char_pos, '-='))
                char_pos += 2 
            elif text[char_pos + 1] == '-':
                tokens.append(('MINUS_ONE', char_pos, '--'))
                char_pos += 2 
            else:
                tokens.append(('MINUS', char_pos, '-'))
                char_pos += 1     
        elif text[char_pos] == '*':
            if text[char_pos + 1] != '=':
                tokens.append(('MULTIPLY', char_pos, '*'))
                char_pos += 1
            else:
                tokens.append(('MULTIPLY_EQUALS', char_pos, '*='))
                char_pos += 2 
        elif text[char_pos] == '/':
            if text[char_pos + 1] != '=':
                tokens.append(('DIVIDE', char_pos, '/'))
                char_pos += 1
            else:
                tokens.append(('DIVIDE_EQUALS', char_pos, '/='))
                char_pos += 2 
        elif text[char_pos] == '=':
            if text[char_pos + 1] != '=':
                tokens.append(('ASSIGN', char_pos, '='))
                char_pos += 1
            else:
                tokens.append(('COMPARISON', char_pos, '=='))
                char_pos += 2
        elif text[char_pos] == '!':
            if text[char_pos + 1] != '=':
                tokens.append(('NOT', char_pos, '='))
                char_pos += 1
            else:
                tokens.append(('NOT_EQUAL', char_pos, '!='))
                char_pos += 2
        elif text[char_pos] == '<':
            if text[char_pos + 1] != '=':
                tokens.append(('LESS_THAN', char_pos, '<'))
                char_pos += 1
            else:
                tokens.append(('LESS_OR_EQUAL', char_pos, '<='))
                char_pos += 2    
        elif text[char_pos] == '>':
            if text[char_pos + 1] != '=':
                tokens.append(('GREATER_THAN', char_pos, '>'))
                char_pos += 1
            else:
                tokens.append(('GREATER_OR_EQUAL', char_pos, '>='))
                char_pos += 2           
        elif text[char_pos] == ')':
            tokens.append(('ARGUMENTS_END', char_pos, ')'))
            char_pos += 1
        elif text[char_pos] == ',':
            tokens.append(('ARGUMENTS_SEP', char_pos, ','))
            char_pos += 1
        elif text[char_pos] == '|':
            tokens.append(('CONDITION_WRAPPER', char_pos, '|'))
            char_pos += 1
        elif text[char_pos] in ['"', "'"]:
            # Matches string literals
            temp_char=''
            temp_char_index=1
            t_str = ''
            while temp_char not in ['"', "'"]:
                temp_char = text[char_pos + temp_char_index]
                t_str += temp_char
                temp_char_index += 1
            tokens.append(('STRING', char_pos, t_str[:-1]))
            char_pos += temp_char_index
        elif text[char_pos] in string.ascii_letters:
            # Match functions statements and variables
            temp_char=''
            temp_char_index=1
            t_str = text[char_pos]
            while temp_char in string.ascii_letters:
                temp_char = text[char_pos + temp_char_index]
                if not (temp_char in string.ascii_letters):
                    break
                t_str += temp_char
                temp_char_index += 1
            # temp_char can be treated as the escape character in this case
            
            if (temp_char in [' ', '|', '(']) and t_str.lower() in ['sub', 'var', 'while', 'if', 'for', 'break', 'call', 'else']:
                tokens.append(('STATEMENT', char_pos, t_str))
                if temp_char == '(':
                    tokens.append(('ARGUMENTS_START', char_pos + temp_char_index, '('))
                char_pos += temp_char_index + 1
            elif temp_char == '(':
                tokens.append(('FUNCTION', char_pos, t_str))
                tokens.append(('ARGUMENTS_START', char_pos + temp_char_index, '('))
                char_pos += temp_char_index + 1
            elif temp_char in [' ', ')', ';', '|', '=', '+', '-', '*', '/']:
                if t_str in ['true', 'false']:
                    tokens.append(('BOOLEAN', char_pos, t_str))
                else:
                    tokens.append(('VARIABLE', char_pos, t_str))
                char_pos += temp_char_index
            elif temp_char == '$':
                tokens.append(('VARIABLE', char_pos, t_str+'$'))
                char_pos += temp_char_index
        elif text[char_pos].isnumeric():
            # Match numbers
            temp_char: str =''
            temp_char_index: int=1
            t_str: str = text[char_pos]
            while True:
                temp_char = text[char_pos + temp_char_index]
                if not (temp_char.isnumeric() or temp_char == '.'):
                    break
                t_str += temp_char
                temp_char_index += 1
            if '.' in t_str or temp_char == '.':
                tokens.append(('FLOAT', char_pos, float(t_str)))
                char_pos += temp_char_index
            else:
                tokens.append(('INT', char_pos, int(t_str)))
                char_pos += temp_char_index
            
        else:
            char_pos += 1

        print(tokens)
        print(char_pos)
        if char_pos >= len(text):
            finished = True
            break


    pprint.pprint(tokens)
        
