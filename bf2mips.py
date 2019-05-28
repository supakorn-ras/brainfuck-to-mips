#!/usr/bin/env python3
import sys
import argparse
import io

def main():
    mem = 2500
    aparse = argparse.ArgumentParser() 
    aparse.add_argument('-f', '--file', type=str, dest='file')
    aparse.add_argument('-o', '--outfile', type=str, default=None, dest='out')

    args = aparse.parse_args()
    strfile = io.open(args.file)
    bracketstack = [0]

    with io.StringIO() as fout:
        fout.write(".data\n")
        fout.write("  bf_arr: .byte 0:{:d}\n".format(mem))
        fout.write(".text\n")
        fout.write("main:\n")
        fout.write("  la $t0 bf_arr\n")
        fout.write("  addi $t0 $t0 {:d}\n".format(mem//2))
            
            
        while True:
            bfchar = strfile.read(1)
            if not bfchar:
                break
            if bfchar == '+':
                fout.write("  lb $t1 0($t0)\n")
                fout.write("  addi $t1 $t1 1\n")
                fout.write("  sb $t1 0($t0)\n")
            if bfchar == '-':
                fout.write("  lb $t1 0($t0)\n")
                fout.write("  addi $t1 $t1 -1\n")
                fout.write("  sb $t1 0($t0)\n")
            if bfchar == '<':
                fout.write("  addi $t0 $t0 1\n")
            if bfchar == '>':
                fout.write("  addi $t0 $t0 -1\n")
            if bfchar == '.':
                fout.write("  addi $v0 $zero 11\n")
                fout.write("  lb $a0 0($t0)\n")
                fout.write("  syscall\n")
            if bfchar == ',':
                fout.write("  addi $v0 $zero 12\n")
                fout.write("  syscall\n")
                fout.write("  sb $v0 0($t0)\n")
            if bfchar == '[':
                bracketname = '_'.join([str(v) for v in bracketstack])
                fout.write("  lb $t1 0($t0)\n")
                fout.write("  beq $t1 $zero cl_b_{:s}\n".format(bracketname))
                fout.write("  op_b_{:s}:\n".format(bracketname))    
                bracketstack.append(0)
            if bfchar == ']':
                bracketstack.pop()
                bracketname = '_'.join([str(v) for v in bracketstack])
                fout.write("  lb $t1 0($t0)\n")
                fout.write("  bne $t1 $zero op_b_{:s}\n".format(bracketname))
                fout.write("  cl_b_{:s}:\n".format(bracketname))
                bracketstack[-1] += 1


        fout.write("  jr $ra\n")
        finalstr = fout.getvalue()
    strfile.close()

    if args.out is None:
        print(finalstr)
    else:
        outfile = io.open(args.out, 'w')
        outfile.write(finalstr)
        outfile.close()

if __name__ == '__main__':
    sys.exit(main() or 0)