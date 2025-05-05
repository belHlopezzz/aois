from language import Lexer, VARIABLE, NOT, AND, OR, LPAREN, RPAREN, IMP, EQU, EOF
from nodes import VariableNode, UnaryOperationNode, BinaryOperationNode

class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise Exception("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def element(self):
        token = self.current_token
        if token.type == VARIABLE:
            self.eat(VARIABLE)
            return VariableNode(token)
        elif token.type == NOT:
            self.eat(NOT)
            return UnaryOperationNode(token, self.element())
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.equivalence()
            self.eat(RPAREN)
            return node
        self.error()

    def conjunction(self): 
        node = self.element()
        while self.current_token.type == AND:
            operator = self.current_token
            self.eat(AND)
            node = BinaryOperationNode(
                left_operand=node,
                operator=operator,
                right_operand=self.element(),
            )
        return node

    def disjunction(self):
        node = self.conjunction()
        while self.current_token.type == OR:
            operator = self.current_token
            self.eat(OR)
            node = BinaryOperationNode(
                left_operand=node,
                operator=operator,
                right_operand=self.conjunction(),
            )
        return node

    def implication(self):
        node = self.disjunction()
        while self.current_token.type == IMP:
            operator = self.current_token
            self.eat(IMP)
            node = BinaryOperationNode(
                left_operand=node,
                operator=operator,
                right_operand=self.disjunction(), # Сейчас левая ассоциация, чтобы сделать правую: right_operand=self.implication()
            )
        return node

    def equivalence(self):
        node = self.implication()
        while self.current_token.type == EQU:
            operator = self.current_token
            self.eat(EQU)
            node = BinaryOperationNode(
                left_operand=node,
                operator=operator,
                right_operand=self.implication(),
            )
        return node

    def parse(self):
        node = self.equivalence()
        if self.current_token.type != EOF:
            self.error()
        return node
