#encoding:UTF-8
import sys,os,traceback
import re,argparse,configparser
from os import listdir
from os.path import isfile, join
import subprocess
import blessings
term=blessings.Terminal()

parser = argparse.ArgumentParser(description='Macro generator')
parser.add_argument('command',choices=["macro","varnames","diff",'show'],help="The selected command")
parser.add_argument('characters',default=["all"],help="Name of the characters to list, all by default",nargs="*")
parser.add_argument("-o",metavar="output",default="tty",help="File for the output command, tty by default",nargs="?")
parser.add_argument("-v",default=False,action='store_true',help="Default")
parser.add_argument("--version",default="HEAD",help="The version to pick from or from wich to make the diff from",nargs="?")
verbose=False
def dprint(text):
    if verbose:
        print(text)

reserved_chars=["exemple.ini","God.ini"]
errors={
    "notfound":term.red("Couldn't find {char} in the Character directory"),
    "sectionnotfound":term.red("Coulnd't find section {section} in {where}"),
    "noreplacement":term.red("Couldn't find replacement for {var} in {where}")
}
god=configparser.ConfigParser()
god.read("Characters/God.ini")


def macro(e):
    pass

def show(characters,output,version):
    list_files=get_char(characters)
    if not list_files:
        return
    ret=""
    for file,name in zip(list_files,characters):
        ret=show_one(file,output,version)
        if output=="tty":
            print(ret)
        else:
            pi=subprocess.Popen(("./ansi2html.sh","--palette=xterm"),stdin=subprocess.PIPE,stdout=subprocess.PIPE)
            e=str.encode(ret,"utf8")
            pi.stdin.write(e)
            pi.stdin.close()
            output=join(output,name+".html")
            with open(output,"wb") as f:
                while True:
                    line=pi.stdout.readline()
                    if not line:
                        break
                    f.write(line)


def show_one(character,output,version):
    config=configparser.ConfigParser()
    config.read(character)
    ret=""
    for sect in config.sections():
        text=""
        text+=term.bold_blue("[{level}] {title} [{cost}]\n").format(title=config[sect]["display_name"],level=config[sect]["level"],cost=config[sect]["cost"])
        for dname,sname in (('Description',"description"),("Description personelle",'self'),("Description publique","others"),("Spécial","special"),("Type de technique","type")):
            try:
                content=replace_vars(config[sect][sname],config,god,sname,sect,character)
                adden=" {t}\n   {c}\n".format(t=term.blue_underline(dname),c=content.replace("\n","\n   "))
                text+=adden
            except KeyError:
                dprint(errors["sectionnotfound"].format(section=sname,where=sect))
        ret+=text+'\n'
    return ret

toreplace=re.compile("\{([\w_-]*)\}")
def replace_vars(text,char,god,section,name,character):
    vars=toreplace.findall(text)
    if vars:
        for group in vars:
            try:
                text=text.replace("{"+group+"}",char[name][group])
            except:
                try:
                    if character not in god:
                        w="DEFAULT"
                    else:
                        w=character
                    text=text.replace("{"+group+"}",god[w][group])
                except:
                    dprint(errors["noreplacement"].format(var=group,where=name))
    return text

def varnames(e):
    pass

def diff(characters,output,version):
    chars=get_char(characters)
    if len(chars)==0:
        dprint(errors["notfound"].format(char="any character"))
        return
    list=["git", "diff",version,"--word-diff=color","--function-context"]+chars
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
