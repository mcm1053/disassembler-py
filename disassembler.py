# To run: python dissassembler.py "Add.hack"
# TODO: Still outputting newlines between instrucitons
# TODO: Also isnt there supposed to be @R0 not @0???
import sys
from os.path import exists as file_exists

# Check if appropriate file extension
if ".hack" in sys.argv[1]:

    # Check if file exists
    if file_exists(sys.argv[1]):

        file = open(sys.argv[1], 'r')
        Lines = file.readlines()

        # List to be used for storing HACK instructions
        hackList = []

        # Computation Dictionary
        compTable = {
            '101010': '0',
            '111111': '1',
            '111010': '-1',
            '001100': 'D',
            '110000': 'A,M',
            '001101': '!D',
            '110001': '!A,!M',
            '001111': '-D',
            '110011': '-A,-M',
            '011111': 'D+1',
            '110111': 'A+1,M+1',
            '001110': 'D-1',
            '110010': 'A-1,M-1',
            '000010': 'D+A,D+M',
            '010011': 'D-A,D-M',
            '000111': 'A-D,M-D',
            '000000': 'D&A,D&M',
            '010101': 'D|A,D|M'
        }

        # Destination Dictionary
        destTable = {
            '000': '',
            '001': 'M=',
            '010': 'D=',
            '011': 'DM=',
            '100': 'A=',
            '101': 'AM=',
            '110': 'AD=',
            '111': 'ADM='
        }

        # Jump Dictionary
        jumpTable = {
            '000': '',
            '001': ';JGT',
            '010': ';JEQ',
            '011': ';JGE',
            '100': ';JLT',
            '101': ';JNE',
            '110': ';JLE',
            '111': ';JMP'
        }

        # Loop through all assembly lines in the HACK file
        for line in Lines:

            # A Instruction
            if line[0] == '0':
                # Convert the rest of the string to int
                value = int(line[1:16], 2)
                # Create hack instruction
                value = '@' + str(value)
                # Append to hackList
                hackList.append(value + '\n')

            # C Instruction
            elif line[0] == '1':

                # Dest = Comp;Jump
                # Destination + Comp bits
                dBit = line[10:13]
                dvalue = destTable[dBit]

                # Comp bits
                aBit = line[3]
                cBit = line[4:10]
                value = dvalue + compTable[cBit].split(',')[int(aBit)]
                # Append to hacklist
                hackList.append(value)

                # Jump bits
                jBit = line[13:16]
                value = jumpTable[jBit]
                # Append to hacklist
                hackList.append(value + '\n')

        # Write to file
        file = open(sys.argv[1].replace('.hack', '.asm'), 'w')
        file.writelines(hackList)
        file.close()
