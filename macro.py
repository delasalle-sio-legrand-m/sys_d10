import sys,os,traceback
import re,argparse

import blessings

parser = argparse.ArgumentParser(description='Macro generator')
parser.add_argument('command',choices=["macro","varnames","diff"],help="The selected command")
parser.add_argument('character',default="all",help="Name of the character, all by default",nargs="?")
parser.add_argument("-o",metavar="output",default="tty",help="File for the output command, tty by default",nargs="?")
parser.add_argument("-v",default=False,action='store_true',help="Default")
parser.add_argument("version",default="last",help="The version to pick from or from wich to make the diff from",nargs="?")

try:
    parser.parse_args(sys.argv[1:])
except:
    parser.print_help()

commands={"macro":macro,"varnames":varnames,"diff":diff}
def macro(e):
    pass

def varnames(e):
    pass

def diff(e):
    pass
