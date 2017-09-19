import sys
import os


"""
CS121 HW2 2017
"""

counter = 0
prefix = "var_"

'''
These make properly formated strings given triples of variables.
'''
def NAND_line(f, output, input1, input2):
    f.write("%s := %s NAND %s\n" % (output, input1, input2))

'''
Returns a tuple of [quantity number of] new formatted variable names
'''
def new_vars(quantity):
    global counter
    var_list = []
    for i in xrange(quantity):
        var_list.append("%s%d" % (prefix, counter))
        counter += 1
    return tuple(var_list)
    

'''
Returns vars from line with binary operator
'''
def parse_BIN(line):
    # ASSUMES SPACING!
    vars = line.split()
    output = vars[0]
    input1 = vars[2]
    input2 = vars[4]
    return output, input1, input2

"""
Returns vars from MAJ line
"""
def parse_MAJ(line):
    # ASSUMES SPACING!
    words = line.split()
    output = words[0]
    variables = words[2].split(',')
    index = variables[0].index('(')
    input1 = variables[0][index+1:]
    input2 = variables[1]
    input3 = variables[2][:len(variables[2]) - 1]
    return output, input1, input2, input3


"""
Takes an AND triple and writes a series of NAND lines to file
"""
def AND_to_NAND(f, output, input1, input2):
    (a,) = new_vars(1)
    NAND_line(f, a, input1, input2)
    NAND_line(f, output, a, a)

"""
Takes an OR triple and writes a series of NAND lines to file
"""
def OR_to_NAND(f, output, input1, input2):
    (a, b) = new_vars(2)
    NAND_line(f, a, input1, input1)
    NAND_line(f, b, input2, input2)
    NAND_line(f, output, a, b)

"""
Takes an XOR triple and writes a series of NAND lines to file
"""
def XOR_to_NAND(f, output, input1, input2):
    (a, b, c) = new_vars(3)
    NAND_line(f, a, input1, input2)
    NAND_line(f, b, input1, a)
    NAND_line(f, c, input2, a)
    NAND_line(f, output, b, c)

"""
Takes a MAJ line and writes a series of NAND lines to file
"""
def MAJ_to_NAND(f, line):
    (output, input1, input2, input3) = parse_MAJ(line)
    (a, b, c, d, e) = new_vars(5)
    NAND_line(f, a, input1, input2)
    NAND_line(f, b, input1, input3)
    NAND_line(f, c, input2, input3)
    NAND_line(f, d, a, b)
    NAND_line(f, e, d, d)
    NAND_line(f, output, c, e)

"""
Converts to NAND
"""
def NANDify(f, prog):  
    for line in prog:
        if "MAJ" in line:
            MAJ_to_NAND(f, line)
        else:
            (output, input1, input2) = parse_BIN(line)
            if "XOR" in line:
                XOR_to_NAND(f, output, input1, input2)
            elif "OR" in line:
                OR_to_NAND(f, output, input1, input2)
            elif "NAND" in line:
                f.write(line)
            elif "AND" in line:
                AND_to_NAND(f, output, input1, input2)
                

"""
usage: python NANDp2NAND.py "filename.nandp"
writes "filename_converted.nand"
"""
def main():
	inname = sys.argv[1]
	name,ext = os.path.splitext(inname)
	with open(inname,'r') as infile:
		prog = infile.readlines()
	outfile = open(name+'_converted.nand','w')
	NANDify(outfile,prog)
	outfile.close()

if __name__ == "__main__":
    main()

