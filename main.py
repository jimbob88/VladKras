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
            tokens.append(('END_BLOCK', char_pos, '{'))
            char_pos += 1
        elif text[char_pos] == ';':
            tokens.append(('END_LINE', char_pos, ';'))
            char_pos += 1
        elif text[char_pos] == '=':
            tokens.append(('ASSIGN', char_pos, '='))
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
            char_pos += temp_char_index + 1
        elif text[char_pos] in string.ascii_letters:
            if char_pos == 233:
                print(text[char_pos])
            temp_char=''
            temp_char_index=1
            t_str = text[char_pos]
            while temp_char in string.ascii_letters:
                temp_char = text[char_pos + temp_char_index]
                if not (temp_char in string.ascii_letters):
                    break
                t_str += temp_char
                temp_char_index += 1
            if temp_char == '(':
                tokens.append(('FUNCTION', char_pos, t_str))
                char_pos += temp_char_index + 1
            elif temp_char == ' ' and t_str.lower() in ['sub', 'var']:
                tokens.append(('STATEMENT', char_pos, t_str))
                char_pos += temp_char_index + 1
            elif temp_char in [' ', ')', ';']:
                tokens.append(('VARIABLE', char_pos, t_str))
                char_pos += temp_char_index
        else:
            char_pos += 1
            
        # if text[char_pos] == 's' and len(text) - char_pos >= 3:
        #     if text[char_pos:char_pos+3] == 'sub':
        #         tokens.append(('SUB_INIT', char_pos))
        #         char_pos += 3
        #         continue

        print(tokens)
        print(char_pos)
        if char_pos >= len(text) - 1:
            finished = True
            break


    pprint.pprint(tokens)
        
