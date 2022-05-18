from collections import OrderedDict
import ete3
import pprint
import itertools
import re
import logging

logger = logging.getLogger(__name__)


class tokenType:
    def __init__(self, tupe):
        self.tupe = tupe
        self.tokenType = tupe[0]
        self.tokenPos = tupe[1]
        self.tokenVal = tupe[2]

class Node:
    def __init__(self, uNode=None, t: tokenType=None) -> None:
        self.connectedLowerNodes = []
        self.connectedUpperNode = uNode
        self.tokenDetails = t

    def connectNode(self, n) -> None:
        self.connectedLowerNodes.append(n)

class Tree:
    def __init__(self) -> None:
        self.nullNode = Node()
        self.currentNode = self.nullNode

    def addNode(self, n) -> None:
        self.currentNode.connectNode(n)
        self.currentNode = n

    def connectToken(self, t) -> None:
        tempNode = Node(uNode=self.currentNode, t=t)
        self.currentNode.connectNode(tempNode)
        self.currentNode = tempNode

    def decreaseDepth(self):
        if self.currentNode.connectedUpperNode is not None:
            self.currentNode = self.currentNode.connectedUpperNode
        else:
            raise SyntaxError("It looks like there is an indentation issue")

def tokenify(tokens: list) -> list:
    classed_tokens = []
    for token in tokens:
        classed_tokens.append(tokenType(token))
    return classed_tokens

def treeify(tokens: list) -> Tree:
    # Tree based off subroutines
    classed_tokens = tokenify(tokens)

    # tree = OrderedDict()
    tree = Tree()
    token_idx = 0
    current_sub = 'NA'
    while True:
        if classed_tokens[token_idx].tokenVal == 'sub':
            if classed_tokens[token_idx+1].tokenType != 'VARIABLE':
                raise ValueError("Subroutine has no name")
            else:
                subName = classed_tokens[token_idx+1].tokenVal
                tree.connectToken(t=tokenType(("DEF_SUB", token_idx, subName)))
                token_idx += 2
        elif classed_tokens[token_idx].tokenType == 'START_BLOCK':
            token_idx += 1
        elif classed_tokens[token_idx].tokenType == 'END_BLOCK':
            tree.decreaseDepth()
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'while':
            if classed_tokens[token_idx+1].tokenType == 'CONDITION_WRAPPER':
                tree.connectToken(t=classed_tokens[token_idx])
            else:
                raise SyntaxError("While loop is not followed by condition wrapper '|'")
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'if':
            if classed_tokens[token_idx+1].tokenType == 'CONDITION_WRAPPER':
                tree.connectToken(t=classed_tokens[token_idx])
            else:
                raise SyntaxError("If statement is not followed by condition wrapper '|'")
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'else':
            tree.connectToken(t=classed_tokens[token_idx])
            token_idx += 1
        elif classed_tokens[token_idx].tokenVal == 'for':
            if classed_tokens[token_idx+1].tokenType == 'ARGUMENTS_START':
                tree.connectToken(t=classed_tokens[token_idx])
            else:
                raise SyntaxError("For loop has no parameters")
            token_idx += 1
        elif classed_tokens[token_idx].tokenType == 'CONDITION_WRAPPER':
            if tree.currentNode.tokenDetails.tokenType == 'CONDITION_WRAPPER':
                # If it is the terminating position
                tree.decreaseDepth()
            else:
                tree.connectToken(t=classed_tokens[token_idx])
            token_idx += 1
        else:
            tree.connectToken(t=classed_tokens[token_idx])
            tree.decreaseDepth()
            token_idx += 1

        if token_idx >= len(tokens):
            break

    return tree

def toNewick(l: list[Node]):
  t_tuple = []
  for idx, node in enumerate(l):
    if len(node.connectedLowerNodes) > 0:
      t_tuple.append([node.tokenDetails.tokenType, toNewick(node.connectedLowerNodes)])
    else:
      t_tuple.append(node.tokenDetails.tokenType)
  return str(t_tuple).replace('[', '(').replace(']', ')').replace("'", "").replace(' ', '') #tuple(tuple(sub) for sub in t_tuple)

def toNewickStr(l: list[Node]) -> str:
    return toNewick(l) + ";"

def toNewickTree(l: list[Node]) -> ete3.Tree:
    return ete3.Tree(toNewickStr(l))

def toList(l):
  tList = []
  for idx, node in enumerate(l):
    if len(node.connectedLowerNodes) > 0:
      tList.append([node.tokenDetails, toList(node.connectedLowerNodes)])
    else:
      tList.append(node.tokenDetails)
  return tList



def transpileFlat(flatTokenList: list) -> list:
    code = ['']
    # context = 'NA'
    currentVar = ''
    for token in flatTokenList:
        if token.tokenType in ['INT', 'FLOAT', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'LESS_THAN', 'GREATER_THAN', 'LESS_OR_EQUAL', 'GREATER_OR_EQUAL', 'ASSIGN', 'NOT_EQUAL']:
            code[-1] += str(token.tokenVal)
        elif token.tokenType == 'VARIABLE':
            code[-1] += token.tokenVal
            currentVar = token.tokenVal
        elif token.tokenType == 'END_LINE':
            code.append('')
        elif token.tokenType == 'COMPARISON':
            code[-1] += '='
        elif token.tokenType == 'PLUS_ONE':
            code[-1] += f'= {currentVar} + 1'
        elif token.tokenType == 'MINUS_ONE':
            code[-1] += f'= {currentVar} - 1'
        elif token.tokenType == 'MINUS_EQUALS':
            code[-1] += f'= {currentVar} - '
        elif token.tokenType == 'PLUS_EQUALS':
            code[-1] += f'= {currentVar} + '
        elif token.tokenVal == 'Print':
            code[-1] += 'PRINT '
        elif token.tokenVal == 'while':
            code[-1] += 'WHILE '
        elif token.tokenType == 'STRING':
            code[-1] += f'"{token.tokenVal}"'
        elif token.tokenVal == 'true':
            code[-1] += "1"
        elif token.tokenVal == 'false':
            code[-1] += "0"
        # elif token.tokenVal == 'askInput':


    return code

def cleanInputs(tokenList: list[tokenType]) -> list:
    noInputs = 0
    # for noInputs, idx in enumerate(inputs):
    while True:
        inputs = [idx for idx, token in enumerate(tokenList) if token.tokenVal == 'askInput']
        if len(inputs) == 0:
            break
        idx = inputs[0]
        noInputs += 1
        depth = 1
        tokenIdx = idx + 1
        while True:
            tokenIdx += 1
            if tokenList[tokenIdx].tokenType == 'ARGUMENTS_END':
                depth -= 1
            elif tokenList[tokenIdx].tokenType == 'ARGUMENTS_START':
                depth += 1
            if depth == 0:
                break
        
        inputString = tokenList[idx+2:tokenIdx]
        tokenList[idx:tokenIdx] = [
           tokenType(('VARIABLE', -1, f"reservedInputValue{noInputs}$"))
        ]
        lastLineSearch = [
            idx for idx, token in enumerate(tokenList[:idx]) 
            if token.tokenType in ['START_BLOCK', 'END_LINE']
        ][-1]
        tokenList[lastLineSearch:lastLineSearch] = [
            tokenType(('END_LINE', -1, ';')),
            tokenType(("STATEMENT", -1, "INPUT")),
            tokenType(('ARGUMENTS_START', -1, '(')),
        ] + inputString + [
            tokenType(('ARGUMENTS_SEP', -1, ',')),
            tokenType(('VARIABLE', -1, f"reservedInputValue{noInputs}$")),
            tokenType(('ARGUMENTS_END', -1, ')')),
            tokenType(('END_LINE', -1, ';'))
        ]
        
    return tokenList
        
def cleanForLoops(tokenList: list[tokenType]) -> list:
    """For loops can be rewritten as while statements

    for (i = 0, i < 39, i++) {
        
    }

    Can be rewritten as:

    i = 0
    WHILE i < 39 {

        i++
    }

    """

    noForLoops = 0
    while True:
        forLoops = [idx for idx, token in enumerate(tokenList) if token.tokenVal == 'for']
        if len(forLoops) == 0:
            break
        
        idx = forLoops[0]
        noForLoops += 1

        findArgumentEnd = [i+idx+2 for i, token in enumerate(tokenList[idx+2:]) if token.tokenType == 'ARGUMENTS_END']
        separatedConditions = list(list(g) for k,g in itertools.groupby(tokenList[idx+2:findArgumentEnd[0]], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)

        tokenIdx = findArgumentEnd[0] 
        depth = 0
        while True:
            tokenIdx += 1
            if tokenList[tokenIdx].tokenType == 'START_BLOCK':
                depth -= 1
            elif tokenList[tokenIdx].tokenType == 'END_BLOCK':
                depth += 1
            if depth == 0:
                break


        forLoopContents = tokenList[findArgumentEnd[0]+2:tokenIdx]
        forLoopStart = separatedConditions[0]
        forLoopCondition = separatedConditions[1]
        forLoopIterator = separatedConditions[2]


        tokenList[idx:tokenIdx+1] = forLoopStart + [
            tokenType(('END_LINE', -1, ';')),
            tokenType(('STATEMENT', -1, 'WHILE'))
        ] + forLoopCondition + [ 
            tokenType(('START_BLOCK', -1, '{'))
        ] + forLoopContents + forLoopIterator + [
            tokenType(('END_LINE', -1, ';')),
            tokenType(('END_BLOCK', -1, 'WEND'))
        ]
    
    return tokenList


def cleanWhile(tokenList: list[tokenType]) -> list:
    """While loops can more easily be defined as an indefinite loop

    while (condition) {

    }

    is the same as:

    while (1) {
        if (condition) {
            break
        }
    }
    """
    noWhiles = 0
    while True:
        whiles = [idx for idx, token in enumerate(tokenList) if token.tokenVal == 'while']
        if len(whiles) == 0:
            break
        
        idx = whiles[0]
        noWhiles += 1
        # tokenIdx = idx + 1

        findConditionWrapper = [i+idx+2 for i, token in enumerate(tokenList[idx+2:]) if token.tokenType == 'CONDITION_WRAPPER']
        # conditions = tokenList[idx+2:findConditionWrapper[0]]
        tokenIdx = idx + (findConditionWrapper[0]-idx)



        depth = 0
        while True:
            tokenIdx += 1
            if tokenList[tokenIdx].tokenType == 'START_BLOCK':
                depth -= 1
            elif tokenList[tokenIdx].tokenType == 'END_BLOCK':
                depth += 1
            if depth == 0:
                break

        tokenList[idx] = tokenType(('STATEMENT', -1, 'WHILE'))
        

        tokenList[tokenIdx] = tokenType(('END_BLOCK', -1, 'WEND'))
        


    return tokenList        

def cleanIfStatement(tokenList: list) -> list:
    """If statements can only be one line, so have to be separated

    if | x == 0 | {
        Print("Hello world");
    } else {
        Print("Access Denied");
    }

    Can be rewritten as

    if | x == 0 | {
        call reservedIf1;
    } else {
        call reservedElse1;
    }

    """

    noIfs = 0
    # noElse = 0
    while True:
        ifStatements = [idx for idx, token in enumerate(tokenList) if token.tokenVal == 'if']
        
        if len(ifStatements) == 0:
            break
        
        idx = ifStatements[0]
        noIfs += 1

        findConditionWrapper = [i+idx+2 for i, token in enumerate(tokenList[idx+2:]) if token.tokenType == 'CONDITION_WRAPPER']

        tokenIdx = findConditionWrapper[0]


        depth = 0
        while True:
            tokenIdx += 1
            if tokenList[tokenIdx].tokenType == 'START_BLOCK':
                depth -= 1
            elif tokenList[tokenIdx].tokenType == 'END_BLOCK':
                depth += 1
            if depth == 0:
                break

        endOfIfStatementBlock = tokenIdx
        elseStatement = False
        if tokenList[tokenIdx+1].tokenVal == 'else':
            tokenIdx += 1
            while True:
                tokenIdx += 1
                if tokenList[tokenIdx].tokenType == 'START_BLOCK':
                    depth -= 1
                elif tokenList[tokenIdx].tokenType == 'END_BLOCK':
                    depth += 1
                if depth == 0:
                    break
            endOfElseStatementBlock = tokenIdx
            elseStatement = True
            elseBlock = tokenList[endOfIfStatementBlock+3:endOfElseStatementBlock]
        
        subName =  f'reservedIfStatement{noIfs}'
        elseSubName =  f'reservedElseStatement{noIfs}'

        ifBlock = tokenList[findConditionWrapper[0]+2:endOfIfStatementBlock]

        if not elseStatement:
            tokenList[idx:endOfIfStatementBlock+1] = [
                tokenType(("STATEMENT", -1, 'IF')),
            ] + tokenList[idx+1:findConditionWrapper[0]+1] + [
                tokenType(("STATEMENT", -1, 'THEN')),
                tokenType(("STATEMENT", -1, 'call')),
                tokenType(('VARIABLE', -1, subName)),
                tokenType(('END_LINE', -1, ';'))
            ]
        else:
            tokenList[idx:endOfElseStatementBlock+1] = [
                tokenType(("STATEMENT", -1, 'IF')),
            ] + tokenList[idx+1:findConditionWrapper[0]+1] + [
                tokenType(("STATEMENT", -1, 'THEN')),
                tokenType(("STATEMENT", -1, 'call')),
                tokenType(('VARIABLE', -1, subName)),
                tokenType(("STATEMENT", -1, 'ELSE')),
                tokenType(("STATEMENT", -1, 'call')),
                tokenType(('VARIABLE', -1, elseSubName)),
                tokenType(('END_LINE', -1, ';'))
            ]



        tokenList.extend(
            [
                tokenType(('STATEMENT', -1, 'sub')),
                tokenType(('VARIABLE', -1, subName)),
                tokenType(('START_BLOCK', -1, '{'))
            ] + ifBlock + [
                tokenType(('END_BLOCK', -1, '}'))
            ]
        )
        if elseStatement:
             tokenList.extend(
                [
                    tokenType(('STATEMENT', -1, 'sub')),
                    tokenType(('VARIABLE', -1, elseSubName)),
                    tokenType(('START_BLOCK', -1, '{'))
                ] + elseBlock + [
                    tokenType(('END_BLOCK', -1, '}'))
                ]
            )


    return tokenList



def transpile(tokenList: list) -> str:
    tokenIdx = 0
    context = 'null'
    subName = 'NA'
    
    subroutines = OrderedDict()
    # noIfStatements = 0
    endLineStatementPos = [n for n, t in enumerate(tokenList) if t.tokenType == 'END_LINE']
    finishedLines = 0
    while True:
        if tokenList[tokenIdx].tokenVal == 'sub':
            # context = 'subroutine'
            subName = tokenList[tokenIdx+1].tokenVal
            subroutines[subName] = []
            tokenIdx += 2
        elif tokenList[tokenIdx].tokenVal == 'printAt':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+2:endLineStatementPos[finishedLines]-1], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            lineNo = ' '.join(temp[0])
            columnNo = ' '.join(temp[1])
            string = ' '.join(temp[2])
            subroutines[subName].append(
                f"PRINT move$;CHR$({lineNo}+32);CHR$({columnNo}+32);"
            )
            subroutines[subName].append(
                f"PRINT {string};"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'Print':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+2:endLineStatementPos[finishedLines]-1], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            string = ' '.join(temp[0])
            subroutines[subName].append(
                f"PRINT {string}"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'clearScreen':
            subroutines[subName].append(
                f"PRINT clear$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'enableCursor':
            subroutines[subName].append(
                f"PRINT con$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'disableCursor':
            subroutines[subName].append(
                f"PRINT coff$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        elif tokenList[tokenIdx].tokenVal == 'resetCursor':
            subroutines[subName].append(
                f"PRINT home$;"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx

        elif tokenList[tokenIdx].tokenVal == 'var':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+1:endLineStatementPos[finishedLines]], lambda x: x.tokenType not in ['ASSIGN']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]

            varName = ' '.join(temp[0])
            varValue = ' '.join(temp[1])
            subroutines[subName].append(
                f"{varName} = {varValue}"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx
        
        elif tokenList[tokenIdx].tokenVal == 'INPUT':
            temp = list(list(g) for k,g in itertools.groupby(tokenList[tokenIdx+2:endLineStatementPos[finishedLines]-1], lambda x: x.tokenType not in ['ARGUMENTS_SEP']) if k)
            temp = [transpileFlat(t_list) for t_list in temp]
            inputString = ' '.join(temp[0])
            variableName = ' '.join(temp[1])
            subroutines[subName].append(
                f"INPUT {inputString}, {variableName}"
            )
            tokenIdx += endLineStatementPos[finishedLines] - tokenIdx

        elif tokenList[tokenIdx].tokenVal == 'WHILE':
            findConditionWrapper = [i+tokenIdx+2 for i, token in enumerate(tokenList[tokenIdx+2:]) if token.tokenType == 'CONDITION_WRAPPER']

            conditions = tokenList[tokenIdx+2:findConditionWrapper[0]]
            subroutines[subName].append(
                f"WHILE {' '.join(transpileFlat(conditions))}"
            )

            tokenIdx += len(conditions) + 2

        elif tokenList[tokenIdx].tokenVal == 'WEND':
            subroutines[subName].append(
                f"WEND"
            )
            tokenIdx += 1

        elif tokenList[tokenIdx].tokenVal == 'IF':
            findConditionWrapper = [i+tokenIdx+2 for i, token in enumerate(tokenList[tokenIdx+2:]) if token.tokenType == 'CONDITION_WRAPPER']
            conditions = tokenList[tokenIdx+2:findConditionWrapper[0]]
            subroutines[subName].append(
                f"IF {' '.join(transpileFlat(conditions))} THEN "
            )

            tokenIdx += len(conditions) + 2

        elif tokenList[tokenIdx].tokenVal == 'ELSE':
            subroutines[subName][-1] += f" ELSE "
            tokenIdx += 1

        elif tokenList[tokenIdx].tokenVal == 'call':
            if tokenList[tokenIdx+1].tokenType != 'VARIABLE':
                raise SyntaxError("NO VARIABLE FOLLOWING CALL COMMAND")

            subroutines[subName][-1] += f" replaceCall {tokenList[tokenIdx+1].tokenVal}"
            tokenIdx += 2

        elif tokenList[tokenIdx].tokenType == 'VARIABLE':
            idx = tokenIdx
            while True:
                idx += 1
                if tokenList[idx].tokenType == 'END_LINE':
                    break
            subroutines[subName].append(
                ' '.join(transpileFlat(tokenList[tokenIdx:idx]))
            )
            tokenIdx += idx - tokenIdx
    
        # elif tokenList[tokenIdx].tokenType in ['INT', 'FLOAT', 'PLUS', 'MINUS', 'DIVIDE', 'MULTIPLY', 'LESS_THAN', 'GREATER_THAN', 'LESS_OR_EQUAL', 'GREATER_OR_EQUAL', 'ASSIGN', 'NOT_EQUAL']:

            
        elif tokenList[tokenIdx].tokenType == 'END_LINE':
            finishedLines += 1
            tokenIdx += 1
        else:
            tokenIdx += 1
        if tokenIdx >= len(tokenList):
            break

    return [f'REM SUB:{key}\n' + "\n".join(text) + "\nRETURN" for key, text in subroutines.items()]

def numberLines(transpiledCode: list[str]) -> str:
    constants = ['',
    'escape$=CHR$(27)',
    'clear$=escape$+"E"',
    'home$=escape$+"H"',
    'move$=escape$+"Y"',
    'con$=e$+"e"',
    'coff$=e$+"f"',
    "'",
    'replaceCall main']

    transpiledCode = constants + transpiledCode
    transpiledCode = '\n'.join(transpiledCode).split('\n')
    regex = r"REM SUB:([\w\d]+)"
    subroutinesDictionary = {re.match(regex, line).group(1): lineNo for lineNo, line in enumerate(transpiledCode) if re.match(regex, line)}
    for subName, subPos in subroutinesDictionary.items():
        transpiledCode = [
            line.replace(f"replaceCall {subName}", f"GOSUB {subPos*10}") for line in transpiledCode
        ]
    

    return '\n'.join(
        [f"{lineNo*10} {line}" for lineNo, line in enumerate(transpiledCode)]
    )


# if __name__ == '__main__':
#     # Create tree from tokens
#     t = treeify(tokens=input_tokens)

#     # Print tree
#     newickString = toNewick(t.currentNode.connectedLowerNodes) + ";"
#     newickTree = ete3.Tree(newickString)
#     print(newickTree)

#     # Create png of tree
#     ts = ete3.TreeStyle()
#     ts.show_leaf_name = True
#     ts.scale = 20
#     ts.rotation = 90
#     newickTree.render("Tree.png", w=1830, units="mm", tree_style=ts)
    
#     classTokens = tokenify(input_tokens)
#     classTokens = cleanInputs(classTokens)
#     classTokens = cleanForLoops(classTokens)
#     classTokens = cleanWhile(classTokens)
#     classTokens = cleanIfStatement(classTokens)
#     transpiledLines = transpile(classTokens)
#     print(numberLines(transpiledLines))