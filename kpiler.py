from kparser import KParser
from klexer import KLexer

def hid(t):
    if isinstance(t, tuple):
        return " ".join([hid(x) for x in t])
    if isinstance(t, list):
        return '['+", ".join([hid(x) for x in t])+']'
    else:
        return str(t)

class KPiler:
    def __init__(self) -> None:
        self.func_to_argc = {}

    def compile_function(self, func):
        func_vars = {}
        func_vars_to_types = {}
        output = []
        name = func[1]
        block = func[4][1]
        args = func[3][1]
        arg_count = len(args)
        self.func_to_argc[name] = arg_count
        output.append(f"DEFINE {name} {arg_count}")
        for hi in args: # arguments
            func_vars[hi[1]] = len(func_vars)
            func_vars_to_types[hi[1]] = type(hi[1])
        for inst in block: # block
            result = self.compile_instruction(func_vars, inst)
            if isinstance(result, list):
                for res in result:
                    output.append(res)
            else:
                output.append(result)
        
        output.append('RETURN')
        output.append('END')
        return output
    def compile_instruction(self, func_vars, inst):
        if isinstance(inst, tuple):
            opcode = inst[0]
            if opcode == 'var':
                return f"GET_LOCAL {func_vars[inst[1]]}"
            elif opcode == 'PRINT':
                hi = []
                hi.append(self.compile_instruction(func_vars, inst[1]))
                hi.append('PRINT')
                return hi
            elif opcode == 'CALL':
                hi = []
                for arg in inst[2]:
                    hi.append(self.compile_instruction(func_vars, arg))
                hi.append(f'CALL {inst[1]} {self.func_to_argc[inst[1]]}')
                return hi
        elif isinstance(inst, str):
            return f"PUSH_STRING \"{inst}\""
        else:
            return f"PUSH_VALUE {inst}"
    def compile(self, src):
        lexer = KLexer()
        parser = KParser()
        parsed = parser.parse(lexer.tokenize(src))
        # with open('test.kmasm' ,'w') as f:
        #     f.write('\n'.join(hid(hello) for hello in parsed))
        output = ["# Automattically generated bytecode"]
        
        
        for hi in parsed:
            opcode = hi[0]
            if opcode == 'DECLARE_FUNC':
                output.extend(self.compile_function(hi))
        return '\n'.join(output)

def main(source: str):
    compiled = KPiler().compile(source)
    print('Compiled successfully')
    return compiled

