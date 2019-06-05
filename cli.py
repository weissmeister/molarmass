#!/usr/bin/python3
import sys
from common import calcmolmass


def helpfunction():
    print("Molar mass calculator by Weissmeister, CLI version.\n\n"
          "Usage:\n"
          "Use molecular formula as the first (and only) argument. This is case-sensitive.\n"
          "Brackets () can be used to multiply the part within the brackets. "
          "Nested brackets are not supported for now.\n"
          "Output is in g/mol.\n\n"
          "Examples:\n"
          "molarmass C2H5OH\n"
          "molarmass MgSO4(H2O)7\n\n"
          "Use --help or -h to display this help.")


if len(sys.argv) != 2:
    print("Error: Wrong amount of arguments.\n"
          "Use --help or -h for help.")
    quit()

if sys.argv[1] == "--help" or sys.argv[1] == "-h":
    helpfunction()
    quit()

success, molmass, errormsg = calcmolmass(sys.argv[1])
if success:
    print(molmass)
else:
    print("Error: {0}\nUse --help or -h for help.".format(errormsg))
