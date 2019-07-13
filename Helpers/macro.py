import sys,os,traceback
import re,argparse,configparser
from os import listdir
from os.path import isfile, join

import blessings
term=blessings.Terminal()

parser = argparse.ArgumentParser(description='Macro generator')
parser.add_argument('command',choices=["macro","varnames","diff",'show'],help="The selected command")
parser.add_argument('characters',default=["all"],help="Name of the characters to list, all by default",nargs="*")
parser.add_argument("-o",metavar="output",default="tty",help="File for the output command, tty by default",nargs="?")
parser.add_argument("-v",default=False,action='store_true',help="Default")
parser.add_argument("--version",default="last",help="The version to pick from or from wich to make the diff from",nargs="?")
verbose=False
def dprint(text):
    if verbose:
        print(text)

reserved_chars=["exemple.ini","God.ini"]
errors={
    "notfound":term.red("Couldn't find {char} in the Character directory"),
    "sectionnotfound":term.red("Coulnd't find section {section} in {where}")
}


def macro(e):
    pass

def show(characters,output,version):
    list_files=get_char(characters)
    if not list_files:
        return
    ret=""
    for file in list_files:
        ret+=show_one(file,output,version)
    if output=="tty":
        print(ret)
    else:
        with open(output,"r") as f:
            f.write(ret)

def show_one(character,output,version):
    config=configparser.ConfigParser()
    config.read(character)
    ret=""
    for sect in config.sections():
        text=""
        text+=term.bold_green("[{level}] {title}\n").format(title=config[sect]["display_name"],level=config[sect]["level"])
        for dname,sname in (('Description',"description"),("Description personelle",'self'),("Description publique","others"),("Spécial","special")):
            try:
                adden=" {t}\n   {c}\n".format(t=term.green_underline(dname),c=config[sect][sname].replace("\n","\n   "))
                text+=adden
            except:
                dprint(errors["sectionnotfound"].format(section=sname,where=sect))
        ret+=text
    return ret

def varnames(e):
    pass

def diff(characters,output,version):
    import subprocess
    chars=get_char(characters)
    if len(chars)==0:
        dprint(errors["notfound"].format(char="any character"))
        return
    list=["git", "diff","HEAD","--word-diff=color","--function-context"]+chars
    if output=="tty":
        dprint("Printing diff")
        pi=subprocess.check_output(list).decode("utf-8")
        print(pi)
    else:
        proc=subprocess.Popen(list,stdout=subprocess.PIPE)
        pi=subprocess.check_output(("./ansi2html.sh"),stdin=proc.stdout)
        with open(output,"wb") as file:
            file.write(pi)

def get_char(names):
    if names[0]=="all":
        return get_all_chars()
    char=[]
    for n in names:
        c=join("Characters", n+".ini")
        if isfile(c):
            char.append(c)
        else:
            dprint(errors["notfound"].format(char=c))
    return char

def get_all_chars():
    return [join("Characters", f) for f in listdir("Characters") if (f not in reserved_chars and isfile(join("Characters", f)))]

if __name__ == '__main__':
    try:
        args=parser.parse_args(sys.argv[1:])
        verbose=args.v
    except:
        parser.print_help()
        sys.exit()
    #print(args)
    commands={"macro":macro,"varnames":varnames,"diff":diff,"show":show}
    commands[args.command](args.characters,args.o,args.version)
