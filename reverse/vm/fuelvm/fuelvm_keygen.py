# 
# A solution to daybreak's FuelVM Keygenme (http://crackmes.de/users/daybreak/fuelvm_keygenme/)
# Author: slackspace
# 

import os, sys
import struct
import random, string

BYTECODE = [
    0x0a, 0x05, 0x09, 0x98, 0x0c, 0x03, 0x0a, 0x04, 0x1c, 0x01, 0x11, 0x00, 0x0c, 0x08, 0xb0, 0x00, 0x1d, 0x03, 0x0b, 0x02,
    0x0c, 0x01, 0x0d, 0x02, 0x88, 0x00, 0x1c, 0x01, 0x09, 0x00, 0x1b, 0x01, 0xff, 0xff, 0x1d, 0x01, 0x0f, 0x04, 0x0f, 0x04,
    0x0a, 0x04, 0x0e, 0x01, 0x0b, 0x03, 0x0f, 0x01, 0x0f, 0x01, 0x0a, 0x05, 0xba, 0x00, 0x0b, 0x02, 0x0e, 0x02, 0x0e, 0x02,
    0x0e, 0x02, 0x0f, 0x02, 0x1d, 0x01, 0x0b, 0x03, 0x1d, 0x02, 0x1c, 0x01, 0x22, 0x00, 0x0a, 0x03, 0x0b, 0x02, 0x1d, 0x01,
    0xff, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01,
    0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01,
    0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02,
    0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02,
    0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00,
    0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03,
    0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03,
    0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01,
    0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01,
    0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02,
    0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02,
    0x03, 0x01, 0x02, 0x03, 0x01, 0x00, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01, 0x02, 0x03, 0x01,
]

EIP   = 0
ESP   = 0x32
STACK = [0] * 1024
REGS  = [0, 0, 0, 0]
ZF    = 0
SF    = 0
KEYI  = 0

PASSWORD = ""

SINGLESTEP = False
DEBUGMODE  = True

def print_state():
    global EIP, ESP, STACK, REGS, ZF, SF

    flags = ""
    if ZF != 0:
        flags += "Z"
    else:
        flags += "z"

    if SF != 0:
        flags += "S"
    else:
        flags += "s"

    print "-=- r1: %.4x r2: %.4x r3: %.4x r4: %.4x ip: %.4x sp: %.4x flags: %s -=-" % (REGS[0], REGS[1], REGS[2], REGS[3], EIP, ESP, flags)
    for i in range(ESP-4, ESP+4):
        if i == ESP:
            v = "<==== ESP"
        else:
            v = ""
        print "\tmem[%04x] = %02x\t%s" % (i, STACK[i], v)


def do_push_reg(regno):
    global ESP, STACK, REGS

    ESP -= 4
    STACK[ESP]   = REGS[regno-1] & 0xff
    STACK[ESP+1] = (REGS[regno-1] >> 8) & 0xff

    return "push r%d" % regno
    

def do_push_imm(value):
    global ESP, STACK

    ESP -= 4
    STACK[ESP]   = value & 0xff
    STACK[ESP+1] = (value >> 8) & 0xff

    return "push 0x%04x" % value


def do_pop(regno):
    global ESP, STACK, REGS

    v = (STACK[ESP+1] << 8) | STACK[ESP]
    REGS[regno-1] = v
    ESP += 4

    return "pop r%d" % regno


def do_move_reg(dst, src):
    global REGS
    
    assert dst != src
    REGS[dst-1] = REGS[src-1] & 0xffff

    return "move r%d, r%d" % (dst, src)


def do_move_imm(dst, val):
    global REGS
    REGS[dst-1] = val & 0xffff
    return "move r%d, 0x%04x" % (dst, val)


def do_or(r, val):
    global REGS
    REGS[r-1] = (REGS[r-1] | val) & 0xffff
    return "or r%d, 0x%04x" % (r, val)


def do_and(r, val):
    global REGS
    REGS[r-1] = (REGS[r-1] & val) & 0xffff
    return "and r%d, 0x%04x" % (r, val)


def do_xor(dst, src):
    global REGS, EIP

    x = REGS[src-1]

    if x == 0:
        EIP += 2
        x = struct.unpack("H", "".join([chr(x) for x in BYTECODE[EIP:EIP+2]]))[0]
        r = "xor r%d, 0x%04x" % (dst, x)
    else:
        r = "xor r%d, r%d" % (dst, src)

    REGS[dst-1] = REGS[dst-1] ^ x
    return r


def do_dec(op):
    global REGS
    REGS[op-1] = REGS[op-1] - 1
    return "dec r%d" % op


def do_inc(op):
    global REGS
    REGS[op-1] = REGS[op-1] + 1
    return "inc r%d" % op


def do_cmp(op1, op2):
    global REGS, EIP, ZF, SF

    if op2 == 0:
        EIP += 2
        x = struct.unpack("H", "".join([chr(x) for x in BYTECODE[EIP:EIP+2]]))[0]
        r = "cmp r%d, 0x%04x" % (op1, x)
    else:
        x = REGS[op2-1]
        r = "cmp r%d, r%d" % (op1, op2)

    if REGS[op1-1] < x:
        SF = 1
        ZF = 0
    elif REGS[op1-1] > x:
        SF = 0
        ZF = 0
    else:
        assert REGS[op1-1] == x
        SF = 0
        ZF = 1

    return r


def vm_init():
    global KEYI, ESP, EIP, REGS, ZF, SF
    
    EIP = 0
    ESP = 0x32
    ZF  = 0
    SF  = 0

    REGS[0] = 0
    REGS[1] = 0
    REGS[2] = 0

    REGS[3] = ord(USERNAME[KEYI])

    KEYI += 1


def main(originaluser):
    global BYTECODE, EIP, KEYI, REGS, USERNAME, PASSWORD

    if len(originaluser) < 7:
        print "[!] User name must be at least 7 characters long"
        exit(0)

    # Obscure username
    s = ""
    for i in range(len(originaluser)):
        s += chr(ord(originaluser[i]) ^ i)
    USERNAME = s


    # First two password characters can be choosen arbitrarily
    PASSWORD += random.choice(string.letters + string.digits)
    PASSWORD += random.choice(string.letters + string.digits)

    # Initialize the VM. As a side effect of invoking the init function for two
    # times, the first two password characters are ignored
    vm_init()
    vm_init()

    done = False
    while not done:
        if DEBUGMODE:
            print_state()

        opcode = BYTECODE[EIP]
        disasm = None

        if opcode == 0x0a:
            # PUSH
            operand = BYTECODE[EIP+1]
            assert 1 <= operand <= 5

            if operand == 5:
                EIP += 2
                val = struct.unpack("H", "".join([chr(x) for x in BYTECODE[EIP:EIP+2]]))[0]
                disasm = do_push_imm(val)
            else:
                disasm = do_push_reg(operand)
    
        elif opcode == 0x0b:
            # POP
            operand = BYTECODE[EIP+1]
            assert 1 <= operand <= 4
            disasm = do_pop(operand)

        elif opcode == 0x0c:
            # MOVE
            operand = BYTECODE[EIP+1]
            assert operand in [1, 2, 3, 6, 7, 8]

            if operand in [6, 7, 8]:
                EIP += 2
                val = struct.unpack("H", "".join([chr(x) for x in BYTECODE[EIP:EIP+2]]))[0]
                disasm = do_move_imm(operand - 5, val)
            else:
                disasm = do_move_reg(1, operand+1)
    
        elif opcode == 0x0d:
            # CMP
            operand = BYTECODE[EIP+1]
            assert 1 <= operand <= 5

            if operand == 1:
                op1 = 1
                op2 = 2
            else:
                op1 = operand - 1
                op2 = 0
            
            disasm = do_cmp(op1, op2)

        elif opcode == 0x0e:
            # INC
            operand = BYTECODE[EIP+1]
            assert 1 <= operand <= 4            
            disasm = do_inc(operand)
    
        elif opcode == 0x0f:
            # DEC
            operand = BYTECODE[EIP+1]
            assert 1 <= operand <= 4            
            disasm = do_dec(operand)

        elif opcode == 0x1b:    
            # AND
            operand = BYTECODE[EIP+1]
            assert operand == 1
            EIP += 2
            val = struct.unpack("H", "".join([chr(x) for x in BYTECODE[EIP:EIP+2]]))[0]
            disasm = do_and(operand, val)
    
        elif opcode == 0x1c:
            # OR
            operand = BYTECODE[EIP+1]
            assert operand == 1
            EIP += 2
            val = struct.unpack("H", "".join([chr(x) for x in BYTECODE[EIP:EIP+2]]))[0]
            disasm = do_or(operand, val)
    
        elif opcode == 0x1d:
            # XOR
            operand = BYTECODE[EIP+1]
            assert operand in [1, 2, 3, 4]
            
            disasm = do_xor(1, 2)

        elif opcode == 0xff:
            # PASSWORD CHECK
            operand = BYTECODE[EIP+1]

            x = REGS[0] & 0xff
            if x < 0x21:
                x += 0x21

            PASSWORD += chr(x)

            disasm = "passcheck #%d" % KEYI

            if KEYI == len(USERNAME):
                done = True
            else:
                vm_init()

        else:
            assert False, "[!] Unsupported opcode #%.2x" % opcode

        if opcode != 0xff:
            EIP += 2

        if DEBUGMODE:
            print "Executing \"%s\"" % disasm
            print

        if SINGLESTEP:
            print "[*] Single stepping. Press ENTER to continue..."
            sys.stdin.readline()
    
    print "[*] Password for user '%s' is: %s" % (originaluser, PASSWORD)


if __name__ == "__main__":
    main(sys.argv[1])

