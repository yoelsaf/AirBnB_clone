#!/usr/bin/python3
"""Defines the HBnB console."""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review

#!/usr/bin/python3
"""
    Main Console program
"""
import cmd
import models
import re


class HBNBCommand(cmd.Cmd):
    """Console"""
    prompt = "(hbnb) "

    @classmethod
    def fetch_command(cls, command):
        commands = {"all": cls.do_all, "show": cls.do_show,
                    "destroy": cls.do_destroy, "update": cls.do_update,
                    "count": cls.do_count}
        if command in commands:
            return commands[command]
        else:
            return None

    def do_EOF(self, arg):
        """Quit the program"""
        return True

    def do_quit(self, arg):
        """Quit the program"""
        return True

    def emptyline(self):
        """Ignore empty inputs"""
        pass

    def do_create(self, arg):
        """Creates a new instance of a Model"""
        if arg:
            try:
                args = arg.split()
                template = models.dummy_classes[args[0]]
                new_instance = template()
                try:
                    for pair in args[1:]:
                        pair_split = pair.split("=")
                        if (hasattr(new_instance, pair_split[0])):
                            value = pair_split[1]
                            flag = 0
                            if (value.startswith('"')):
                                value = value.strip('"')
                                value = value.replace("\\", "")
                                value = value.replace("_", " ")
                            elif ("." in value):
                                try:
                                    value = float(value)
                                except:
                                    flag = 1
                            else:
                                try:
                                    value = int(value)
                                except:
                                    flag = 1
                            if (not flag):
                                setattr(new_instance, pair_split[0], value)
                        else:
                            continue
                    new_instance.save()
                    print(new_instance.id)
                except:
                    new_instance.rollback()
            except:
                print("** class doesn't exist **")
                models.storage.rollback()
        else:
            print("** class name missing **")

    def do_show(self, arg):
        """string representation of an instance"""
        if arg:
            arg = arg.split()
            if arg[0] in models.dummy_classes:
                if len(arg) > 1:
                    key = "{}.{}".format(arg[0], arg[1])
                    try:
                        print(models.storage.all()[key])
                    except:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_destroy(self, arg):
        """ Deletes an instance based on the class name and id"""
        if arg:
            arg = arg.split()
            if arg[0] in models.dummy_classes:
                if len(arg) > 1:
                    key = "{}.{}".format(arg[0], arg[1])
                    try:
                        garbage = models.storage.all().pop(key)
                        del(garbage)
                        models.storage.save()
                    except:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_all(self, arg):
        """string representation of all instances"""
        result = []
        if arg:
            arg = arg.split()
            if arg[0] in models.dummy_classes:
                current_inst = models.dummy_classes[arg[0]]
                for i, o in models.storage.all(current_inst).items():
                    if i.split('.')[0] == arg[0]:
                        result.append(str(o))
            else:
                print("** class doesn't exist **")
        else:
            for instance, obj in models.storage.all().items():
                result.append(str(obj))
        if result:
            print(result)

    def do_update(self, arg):
        """Updates an instance adding or updating attribute"""
        if arg:
            arg = arg.split()
            if arg[0] in models.dummy_classes:
                if len(arg) > 1:
                    key = "{}.{}".format(arg[0], arg[1])
                    try:
                        instance = models.storage.all()[key]
                        if len(arg) > 2:
                            if len(arg) > 3:
                                setattr(instance, arg[2], arg[3].strip('"'))
                                instance.save()
                            else:
                                print("** value missing **")
                        else:
                            print("** attribute name missing **")
                    except:
                        print("** no instance found **")
                else:
                    print("** instance id missing **")
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")

    def do_count(self, arg):
        """
        count number of instances
        """
        count = 0
        if arg:
            arg = arg.split()
            if arg[0] in models.dummy_classes:
                for instance, obj in models.storage.all().items():
                    if instance.split('.')[0] == arg[0]:
                        count += 1
            else:
                print("** class doesn't exist **")
        else:
            for instance, obj in models.storage.all().items():
                count += 1
        print(count)

    def default(self, line):
        """
        handle invalid commands and
        special commands like <class name>.<command>()
        """
        match = re.fullmatch(r"[A-Za-z]+\.[A-Za-z]+\(.*?\)", line)
        if match:
            splited = line.split('.')
            if splited[0] in models.dummy_classes:
                parsed = splited[1].split("(")
                parsed[1] = parsed[1].strip(")")
                args = parsed[1].split(",")
                args = [arg.strip() for arg in args]
                if len(args) >= 3:
                    temp = args[2]
                    args = [arg.strip('"') for arg in args[:2]]
                    args.append(temp)
                else:
                    args = [arg.strip('"') for arg in args]
                command = self.fetch_command(parsed[0])
                if command:
                    reconstructed_args = [arg for arg in args]
                    reconstructed_args.insert(0, splited[0])
                    reconstructed_command = " ".join(reconstructed_args)
                    command(self, reconstructed_command)
                else:
                    print("*** Unknown syntax: {}".format(line))
            else:
                print("** class doesn't exist **")
        else:
            print("*** Unknown syntax: {}".format(line))


if __name__ == "__main__":
    HBNBCommand().cmdloop()
def parse(arg):
    curly_braces = re.search(r"\{(.*?)\}", arg)
    brackets = re.search(r"\[(.*?)\]", arg)
    if curly_braces is None:
        if brackets is None:
            return [i.strip(",") for i in split(arg)]
        else:
            lexer = split(arg[:brackets.span()[0]])
            retl = [i.strip(",") for i in lexer]
            retl.append(brackets.group())
            return retl
    else:
        lexer = split(arg[:curly_braces.span()[0]])
        retl = [i.strip(",") for i in lexer]
        retl.append(curly_braces.group())
        return retl


class HBNBCommand(cmd.Cmd):
    """Defines the HolbertonBnB command interpreter.
    Attributes:
        prompt (str): The command prompt.
    """

    prompt = "(hbnb) "
    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """Do nothing upon receiving an empty line."""
        pass

    def default(self, arg):
        """Default behavior for cmd module when input is invalid"""
        argdict = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        match = re.search(r"\.", arg)
        if match is not None:
            argl = [arg[:match.span()[0]], arg[match.span()[1]:]]
            match = re.search(r"\((.*?)\)", argl[1])
            if match is not None:
                command = [argl[1][:match.span()[0]], match.group()[1:-1]]
                if command[0] in argdict.keys():
                    call = "{} {}".format(argl[0], command[1])
                    return argdict[command[0]](call)
        print("*** Unknown syntax: {}".format(arg))
        return False

    def do_quit(self, arg):
        """Quit command to exit the program."""
        return True

    def do_EOF(self, arg):
        """EOF signal to exit the program."""
        print("")
        return True

    def do_create(self, arg):
        """Usage: create <class>
        Create a new class instance and print its id.
        """
        argl = parse(arg)
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            print(eval(argl[0])().id)
            storage.save()

    def do_show(self, arg):
        """Usage: show <class> <id> or <class>.show(<id>)
        Display the string representation of a class instance of a given id.
        """
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict:
            print("** no instance found **")
        else:
            print(objdict["{}.{}".format(argl[0], argl[1])])

    def do_destroy(self, arg):
        """Usage: destroy <class> <id> or <class>.destroy(<id>)
        Delete a class instance of a given id."""
        argl = parse(arg)
        objdict = storage.all()
        if len(argl) == 0:
            print("** class name missing **")
        elif argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
        else:
            del objdict["{}.{}".format(argl[0], argl[1])]
            storage.save()

    def do_all(self, arg):
        """Usage: all or all <class> or <class>.all()
        Display string representations of all instances of a given class.
        If no class is specified, displays all instantiated objects."""
        argl = parse(arg)
        if len(argl) > 0 and argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objl = []
            for obj in storage.all().values():
                if len(argl) > 0 and argl[0] == obj.__class__.__name__:
                    objl.append(obj.__str__())
                elif len(argl) == 0:
                    objl.append(obj.__str__())
            print(objl)

    def do_count(self, arg):
        """Usage: count <class> or <class>.count()
        Retrieve the number of instances of a given class."""
        argl = parse(arg)
        count = 0
        for obj in storage.all().values():
            if argl[0] == obj.__class__.__name__:
                count += 1
        print(count)

    def do_update(self, arg):
        """Usage: update <class> <id> <attribute_name> <attribute_value> or
       <class>.update(<id>, <attribute_name>, <attribute_value>) or
       <class>.update(<id>, <dictionary>)
        Update a class instance of a given id by adding or updating
        a given attribute key/value pair or dictionary."""
        argl = parse(arg)
        objdict = storage.all()

        if len(argl) == 0:
            print("** class name missing **")
            return False
        if argl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(argl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(argl[0], argl[1]) not in objdict.keys():
            print("** no instance found **")
            return False
        if len(argl) == 2:
            print("** attribute name missing **")
            return False
        if len(argl) == 3:
            try:
                type(eval(argl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(argl) == 4:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            if argl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[argl[2]])
                obj.__dict__[argl[2]] = valtype(argl[3])
            else:
                obj.__dict__[argl[2]] = argl[3]
        elif type(eval(argl[2])) == dict:
            obj = objdict["{}.{}".format(argl[0], argl[1])]
            for k, v in eval(argl[2]).items():
                if (k in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[k]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[k])
                    obj.__dict__[k] = valtype(v)
                else:
                    obj.__dict__[k] = v
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
