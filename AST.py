class AST:
    def __str__(self):
        return self._str_recursive(0)

    def _str_recursive(self, indent_level):
        raise NotImplementedError("'_str_recursive' method must be implemented in subclasses.")


class NumberNode(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def _str_recursive(self, indent_level):
        indent = "  " * indent_level
        return f"{indent}NumberNode({self.value})"


class BinOpNode(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

    def _str_recursive(self, indent_level):
        indent = "  " * indent_level
        op_str = self.op.value
        left_str = self.left._str_recursive(indent_level + 1)
        right_str = self.right._str_recursive(indent_level + 1)
        return f"{indent}BinOpNode(\n{left_str},\n{indent}  op=Token({self.op.type}, {op_str}),\n{right_str}\n{indent})"

    # To retrieve the operator symbol
    def get_op_symbol(self):
        return self.op.value
