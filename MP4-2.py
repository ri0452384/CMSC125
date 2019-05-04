"""
This code will recognize the input string as either infix, prefix, or postfix, and generate its other counterparts from the given input

references:
http://interactivepython.org/lpomz/courselib/static/pythonds/BasicDS/InfixPrefixandPostfixExpressions.html
https://www.aoprogrammer.com/infix-prefix-and-postfix-notation/

"""

from pythonds.basic.stack import Stack


def classify(expression):
    tokenList = expression.split()
    if tokenList[0] in "^*/+-":
        return "prefix"
    elif tokenList[-1] in "^*/+-":
        return "postfix"
    else:
        return "infix"


def prefixToInfix(prefixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    infixStack = Stack()
    tokenList = prefixexpr[::-1].split()
    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or token in "0123456789":
            infixStack.push(token.__str__())
        else:
            operand1 = infixStack.pop()
            operand2 = infixStack.pop()
            infixStack.push(("( " + operand1 + " "+ token + " " + operand2 + " )"))
    output = ""
    output += infixStack.pop()
    if infixStack.isEmpty():
        return output
    else:
        print("Error! Invalid Input!")
        exit(1)


def infix_to_prefix(infixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec[")"] = 1
    prec["("] = 1
    opStack = Stack()
    prefixStack = Stack()
    tokenList = infixexpr[::-1].split()
    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or token in "0123456789":
            prefixStack.push(token)
        elif token == ')':
                opStack.push(token)
        elif token == '(':
            topToken = opStack.pop()
            while topToken != ')':
                prefixStack.push(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and (prec[opStack.peek()] >= prec[token]):
                prefixStack.push(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        prefixStack.push(opStack.pop())
    output = ""
    while not prefixStack.isEmpty():
        output += prefixStack.pop()+ " "
    return output


def postfix_to_infix(postfixexpr):
    infixStack = Stack()
    tokenList = postfixexpr.split()
    print(tokenList)
    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or token in "0123456789":
            infixStack.push(token)
        else:
            if infixStack.size() < 2:
                print("Error! Invalid Input")
                exit(-1)
            else:
                operand2 = infixStack.pop()
                operand1 = infixStack.pop()
                infixStack.push(("( " + operand1 + " " + token + " " + operand2 + " )"))
    output = ""
    output += infixStack.pop()
    if infixStack.isEmpty():
        return output
    else:
        print("Error! Invalid Input!")
        exit(1)


def infix_to_postfix(infixexpr):
    prec = {}
    prec["^"] = 4
    prec["*"] = 3
    prec["/"] = 3
    prec["+"] = 2
    prec["-"] = 2
    prec["("] = 1
    opStack = Stack()
    postfixList = []
    tokenList = infixexpr.split()

    for token in tokenList:
        if token in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz" or token in "0123456789":
            postfixList.append(token)
        elif token == '(':
            opStack.push(token)
        elif token == ')':
            topToken = opStack.pop()
            while topToken != '(':
                postfixList.append(topToken)
                topToken = opStack.pop()
        else:
            while (not opStack.isEmpty()) and \
               (prec[opStack.peek()] >= prec[token]):
                  postfixList.append(opStack.pop())
            opStack.push(token)

    while not opStack.isEmpty():
        postfixList.append(opStack.pop())
    return " ".join(postfixList)


def postfix_eval(postfixExpr):
    operandStack = Stack()
    tokenList = postfixExpr.split()

    for token in tokenList:
        if token in "0123456789":
            operandStack.push(int(token))
        else:
            operand2 = operandStack.pop()
            operand1 = operandStack.pop()
            result = do_math(token,operand1,operand2)
            operandStack.push(result)
    return operandStack.pop()

def do_math(op, op1, op2):
    if op == "^":
        return op1 ^ op2
    elif op == "*":
        return op1 * op2
    elif op == "/":
        return op1 / op2
    elif op == "+":
        return op1 + op2
    else:
        return op1 - op2


#main starts here
entered_input = input("Enter an expression: ")
classification = classify(entered_input)

if classification == "infix":
    print("Infix detected \n infix:"+entered_input)
    print("\n prefix: "+infix_to_prefix(entered_input))
    print("\n postfix: "+infix_to_postfix(entered_input))
elif classification == "postfix":
    print("Postfix detected \n postfix: " + entered_input)
    a = postfix_to_infix(entered_input)
    print("\n infix: "+a)
    print("\n prefix: "+infix_to_prefix(a))
else:
    print("Prefix detected \n prefix: " + entered_input)
    a = prefixToInfix(entered_input)
    print("\n infix: "+a)
    print("\n postfix: "+infix_to_postfix(a))

