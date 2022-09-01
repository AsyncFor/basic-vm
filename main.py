# MIT License

# Copyright (c) 2022 AsyncFor

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import time
import re
import sys
from enum import Enum


class Register:
    def __init__(self, name: str, value: int = 0):
        self.name = name
        self.value = value

class Opcode(Enum):
    IN = "in"
    OUT = "out"
    MOV = "mov"
    ALLOC = "alloc"
    EXIT = "exit"
    TOSTRING = "tostring"
    ADD = "add"
    SUB = "sub"
    MUL = "mul"
    DIV = "div"
    HALT = "halt"
    PUSH = "push"
    POP = "pop"
    LEA = "lea"
    CALL = "call"
    JMP = "jmp"
    RET = "ret"
    VM_DEBUG = "vm_debug"
class InstructionBase:
    def __init__(self, op: Opcode, a = None, b = None, c = None):
        self.op = op
        self.a = a
        self.b = b
        self.c = c

class Mov(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.MOV, a, b, c)
    
    def __call__(self, vm):
        vm.get(self.a).value = vm.get(self.b).value
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Out(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.OUT, a, b, c)
    
    def __call__(self, vm):
        value = vm.get(self.a).value

        if type(value) == int:
            print(chr(value), end="")
        else:
            print(value, end="")
    
    def __str__(self):
        return f"{self.op.value} {self.a}"

class ToString(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.TOSTRING, a, b, c)
    
    def __call__(self, vm):
        vm.get(self.a).value = str(vm.get(self.b).value)
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Add(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.ADD, a, b, c)
    
    def __call__(self, vm):
        vm.get("r0").value = vm.get(self.a).value + vm.get(self.b).value
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Sub(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.SUB, a, b, c)
    
    def __call__(self, vm):
        vm.get("r0").value = vm.get(self.a).value - vm.get(self.b).value
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Mul(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.MUL, a, b, c)
    
    def __call__(self, vm):
        vm.get("r0").value = vm.get(self.a).value * vm.get(self.b).value
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Div(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.DIV, a, b, c)
    
    def __call__(self, vm):
        vm.get("r0").value = vm.get(self.a).value // vm.get(self.b).value
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Halt(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.HALT, a, b, c)
    
    def __call__(self, vm):
        time.sleep(vm.get(self.a).value/vm.speed)
    
    def __str__(self):
        return f"{self.op.value}"


class Exit(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.EXIT, a, b, c)
    
    def __call__(self, vm):
        vm.running = False
    
    def __str__(self):
        return f"{self.op.value}"

class In(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.IN, a, b, c)
    
    def __call__(self, vm):
        vm.get(self.a).value = input()
    
    def __str__(self):
        return f"{self.op.value} {self.a}"

class Push(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.PUSH, a, b, c)
    
    def __call__(self, vm):
        vm.stack.push(vm.get(self.a).value)
    
    def __str__(self):
        return f"{self.op.value} {self.a}"

class Lea(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.LEA, a, b, c)
    
    def __call__(self, vm):
        vm.get(self.a).value = vm.get(self.b).address
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b} {self.c}"

class Pop(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.POP, a, b, c)
    
    def __call__(self, vm):
        vm.get(self.a).value = vm.stack.pop()
    
    def __str__(self):
        return f"{self.op.value} {self.a}"

class Jmp(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.JMP, a, b, c)
    
    def __call__(self, vm):
        vm.ip = vm.get(self.a).value
    
    def __str__(self):
        return f"{self.op.value} {self.a}"

class Call(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.CALL, a, b, c)
    
    def __call__(self, vm):
        vm.stack.push(vm.ip)
        vm.ip = vm.get(self.a).value
    def __str__(self):
        return f"{self.op.value} {self.a}"

class Ret(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.RET, a, b, c)
    
    def __call__(self, vm):
        vm.ip = vm.stack.pop()
    
    def __str__(self):
        return f"{self.op.value}"

class VMDebug(InstructionBase):
    def __init__(self, a = None, b = None, c = None):
        super().__init__(Opcode.VM_DEBUG, a, b, c)
    
    def __call__(self, vm):
        if vm.get(self.a).value == 1:
            print(vm.stack)
        elif vm.get(self.a).value == 2:
            print(vm.registers)
    
    def __str__(self):
        return f"{self.op.value}"
class Instruction(InstructionBase):
    def __init__(self, op: Opcode, a = None, b = None, c = None):
        super().__init__(op, a, b, c)
    
    def __call__(self, vm):
        if self.op == Opcode.MOV:
            Mov(self.a, self.b)(vm)
        elif self.op == Opcode.OUT:
            Out(self.a)(vm)
        elif self.op == Opcode.TOSTRING:
            ToString(self.a, self.b)(vm)
        elif self.op == Opcode.ADD:
            Add(self.a, self.b)(vm)
        elif self.op == Opcode.SUB:
            Sub(self.a, self.b)(vm)
        elif self.op == Opcode.MUL:
            Mul(self.a, self.b)(vm)
        elif self.op == Opcode.DIV:
            Div(self.a, self.b)(vm)
        elif self.op == Opcode.EXIT:
            Exit(self.a)(vm)
        elif self.op == Opcode.HALT:
            Halt(self.a)(vm)
        elif self.op == Opcode.PUSH:
            Push(self.a)(vm)
        elif self.op == Opcode.POP:
            Pop(self.a)(vm)
        elif self.op == Opcode.LEA:
            Lea(self.a, self.b)(vm)
        elif self.op == Opcode.CALL:
            Call(self.a)(vm)
        elif self.op == Opcode.JMP:
            Jmp(self.a)(vm)
        elif self.op == Opcode.IN:
            In(self.a)(vm)
        elif self.op == Opcode.RET:
            Ret(self.a)(vm)
        elif self.op == Opcode.VM_DEBUG:
            VMDebug(self.a)(vm)
        else:
            raise Exception(f"Unknown opcode {self.op}")
    
    def __str__(self):
        return f"{self.op.value} {self.a} {self.b}"

class Constant:
    def __init__(self, value):
        self.value = value
        #self.string = string
    
    def __str__(self):
        return str(self.value)

class StackAddress:
    def __init__(self, address, value):
        self.address = address
        self.value = value
    
    def __str__(self):
        return str(self.value)

DELAY = 0.01

def parse(line: str):
    line = line.strip()
    line = re.sub(r"\/\/.*", "", line)
    if line == "":
        return None
    instruction = line.split(":")
    opcode, args = instruction[0], instruction[1:]
    # handle escape characters
    args = [arg.replace("\\n", "\n") for arg in args]
    opcode = Opcode(opcode)
    instruction = Instruction(opcode, *args)
    return instruction

class Stack:
    def __init__(self, vm, size, base: int = 0):
        self.size = size
        self.stack: list = [0] * size
        self.vm = vm
        self.vm.get("rbp").value = len(self.stack) - 1
        self.vm.get("rsp").value = self.base
    @property
    def base(self):
        return self.vm.get("rbp").value

    @property
    def top(self):
        return self.vm.get("rsp").value


    def push(self, value):
        self.stack.append(value)
        self.vm.get("rsp").value += 1
        self.size += 1

    def pop(self):
        value = self.stack.pop()
        self.vm.get("rsp").value -= 1
        self.size -= 1
        return value

    def __getattr__(self, name):
        return getattr(self.stack, name)
    
    def __getitem__(self, key):
        # dynamically grow stack
        if key >= len(self.stack):
            self.stack += [0] * (key - len(self.stack) + 1)

        return self.stack[self.base + key]
    
    def __setitem__(self, key, value):
        self.stack[key + self.base] = value
    
    def __str__(self):
        # return str(
        #     [
        #         ("*" if i == self.base-i else '')+str(item) for i, item in enumerate(self.stack)
        #     ]
        # )
        return self.__repr__()
    
    def __repr__(self):
        return str(
            [
                (
                    f'\033[38;5;180m' if i == self.base # highlight rbp 
                    else f'\033[38;5;190m' if i == (self.top) # highlight rsp 
                    else f'\033[38;5;194m' if item != 0
                    else f'\033[38;5;242m'
                )
                +
                str(item)
                +
                '\033[0m' 
                for i, item in enumerate(self.stack)
            ] 
        ).replace("\\x1b", "\033") + f" {self.base} {self.top}"

class VM:
    def __init__(self, start_point:int=0, labels:dict=None):
        self.registers = [
            Register("ip"), # instruction pointer
            Register("sp"), # stack pointer
            Register("bp"), # base pointer
            
            
            Register("ax"),
            Register("bx"),
            Register("cx"),
            Register("dx"),
            Register("ex"),
            Register("fx"),
        ]
        self.running = False
        self.program = []
        self.stack = Stack(self, 5)
        self.speed = 100
        self.start_point = start_point
        self.labels = labels if labels else {"_start": start_point}

    def get_register(self, name_or_number: int | str):
        if isinstance(name_or_number, int):
            general_purpose = ["ax", "bx", "cx", "dx", "ex", "fx"]
            for register in self.registers:
                if register.name == general_purpose[name_or_number]:
                    return register

            raise ValueError(f"Register {name_or_number} not found")
        else:
            for register in self.registers:
                if register.name == name_or_number:
                    return register
            raise ValueError(f"Register {name_or_number} not found")

    def calculate_address_math(self, address: str):
        regex = re.compile(r"([a-z A-Z]*)([+-])?([\d])?")
        matched = regex.match(address)
        if matched:
            a = matched.group(1)
            op = matched.group(2)
            b = matched.group(3)
            if op and b:
                if op == "+":
                    return self.get(a).value + self.get(b).value
                elif op == "-":
                    return self.get(a).value - self.get(b).value
            return self.get(a).value
    def get(self, name: str):
        if name[0] == "r":
            if name[1:].isnumeric():
                return self.get_register(int(name[1:]))
            return self.get_register(name[1:])
        elif name.isnumeric():
            return Constant(int(name))
        elif name.startswith("[") and name.endswith("]"):
            # calculate address, such as [rsp-4] or [rsp+4]
            address = name[1:-1]
            address = self.calculate_address_math(address)
            return StackAddress(address, self.stack[address - self.stack.base])
        elif name[0] in ("\"" , "'") and name[-1] in ("\"" , "'"):
            return Constant(name[1:-1])
        else:
            return Constant(self.labels[name])

    @property
    def ip(self):
        return self.get_register("ip").value

    @ip.setter
    def ip(self, value):
        self.get_register("ip").value = value


    def step(self):
        if self.ip >= len(self.program):
            self.ip = 0
        instruction = self.program[self.ip]
        self.ip += 1
        instruction(self)
        time.sleep(1/self.speed)


    def start(self):
        self.running = True
        self.ip = self.start_point
        while self.running:
            self.step()
    
    def sleep(self, seconds):
        time.sleep(seconds)

if __name__ == "__main__":
    input_fn = sys.argv[1]
    with open(input_fn, "r") as f:
        lines = f.readlines()
    program = []
    starting_point = None
    labels = {}
    for line in lines:
        if line.strip().startswith("!"):
            line = re.sub(r"\/\/.*", "", line)
            if line.strip() == "!start":
                starting_point = len(program)
            labels[line.strip()[1:]] = len(program)
            continue
        parsed = parse(line)
        if parsed:
            program.append(parsed)

    if starting_point is None:
        raise Exception("No starting point found")
    
    print("labels: ", labels)
    vm = VM(starting_point, labels)

    vm.program = program
    vm.start()

