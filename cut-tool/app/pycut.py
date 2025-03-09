import argparse
import sys
import re


def cut():
    parser = argparse.ArgumentParser(description="cut tool made with python")
    parser.add_argument(
        "file",
        help="File name. If not files are specified, the standard input is used",
        nargs="*",
    )
    parser.add_argument(
        "-c", metavar="list", help="The list specifies character positions"
    )
    parser.add_argument("-b", metavar="list", help="The list specifies byte positions")
    parser.add_argument(
        "-d",
        metavar="delim",
        help="Use delim as the field delimiter character instead of the tab character.",
    )
    parser.add_argument(
        "-f",
        metavar="list",
        help="The list specifies fields, separated in the input by the field delimiter character (see the -d option).  Output fields are separated by a single occurrence of the field delimiter character.",
    )
    parser.add_argument(
        "-s",
        action="store_true",
        help="Suppress lines with no field delimiter characters.  Unless specified, lines with no delimiters are passed through unmodified.",
    )
    parser.add_argument(
        "-w",
        action="store_true",
        help="Use whitespace (spaces and tabs) as the delimiter.  Consecutive spaces and tabs count as one single field separator.",
    )

    args = parser.parse_args()

    if ((not args.c) and (not args.f)) or (args.c and args.f):
        raise ValueError("Illegal list value")

    cut_options = {
        "characters": decodeLine(args.c) if args.c else None,
        "columns": decodeLine(args.f) if args.f else None,
        "printDelimiter": args.d if args.d else "\t",
        "splitFunction": lambda s: (
            s.split(args.d)
            if args.d
            else (
                re.split(r"\s+", s) if args.w else s.split("\t")
            )  # NOTE: not str.split() because it has behaviour of removing consecutive whitespaces before split
        ),
        "suppress": args.s,
    }

    file_list = args.file
    if file_list:
        for file_name in file_list:
            with open(file_name) as file:
                cut_and_print(file, cut_options)
    else:
        file = sys.stdin
        cut_and_print(file, cut_options)


def decodeLine(line):
    line = line.strip()

    if "-" in line:
        start, end = line.split("-")
        if (
            (not start.isdigit())
            or (not end.isdigit())
            or (int(start) <= 0)
            or (int(end) < int(start))
        ):
            raise ValueError(f"Invalid numbers {line}")
        start, end = map(int, (start, end))
        return list(range(start - 1, end))

    # for selection -> split by ',' or " "
    values = line.split(",") if "," in line else line.split()
    valuesAdjusted = []
    for val in values:
        if not val.isdigit() or int(val) <= 0:
            raise ValueError(f"Invalid numbers mentioned {line}")
        valuesAdjusted.append(int(val) - 1)
    return valuesAdjusted


def cut_and_print(fileObj, cut_options):
    while line := fileObj.readline().rstrip("\r\n"):
        if chars := cut_options["characters"]:
            print(*(line[char] for char in chars), sep="")
        elif cols := cut_options["columns"]:
            splitLine = cut_options["splitFunction"](line)
            if len(splitLine) == 1:
                if cut_options["suppress"]:
                    continue
                else:
                    print(line)  # NOTE: this is strange behaviour in cut (refer README)
            else:
                print(
                    *(splitLine[col] for col in cols if col < len(splitLine)),
                    sep=cut_options["printDelimiter"],
                )
        else:
            raise ValueError("Invalid cut_options")  # unexpected
