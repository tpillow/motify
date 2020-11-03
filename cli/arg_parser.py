# Imports
import getopt
import sys


def printUsage(exitStatus: int) -> None:
    """Prints the program usage statement and exits.

    Args:
        exitStatus (int): the exit status to return
    """
    print("Motify Usage:")
    print("-n, --notification-type \t required (simple|yes_no)")
    print("\t simple: a clickable notification with a title and content")
    print("-t, --title \t the title of the notification")
    print("-c, --content \t the text content of the notification")
    print("-h, --help \t print usage")
    sys.exit(exitStatus)


class Args:
    """Container class for all possible program argument values.
    """
    type: str = None
    title: str = ""
    content: str = ""

    def __repr__(self) -> str:
        """Nice string representation of all arguments (for debug).

        Returns:
            str: a string representation
        """
        return "\n".join("%s: %s" % item for item in vars(self).items())


# The global instance of program arguments
args = Args()

# Parse arguments
try:
    opts, _ = getopt.getopt(sys.argv[1:], "hn:t:c:")
except getopt.GetoptError:
    printUsage(-1)

# Process arguments
for opt, arg in opts:
    if opt in ("-h", "--help"):
        printUsage(0)
    elif opt in ("-n", "--notification-type"):
        args.type = arg
        if args.type not in ("simple", "yes_no"):
            print(f"Invalid notification type {args.type}")
            sys.exit(-1)
    elif opt in ("-t", "--title"):
        args.title = arg
    elif opt in ("-c", "--content"):
        args.content = arg
    else:
        print(f"Unknown option {opt}")
        sys.exit(-1)

# Check if everything was specified
if not args.type:
    print("Unspecified notification type")
    sys.exit(-1)

# Debug print data
print(args)
