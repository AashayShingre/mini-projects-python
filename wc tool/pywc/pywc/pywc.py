import argparse
import sys
import locale
import time
from typing import BinaryIO


def pywc_main() -> None:
    parser = argparse.ArgumentParser(description="wc tool made with python")
    parser.add_argument(
        "file",
        help="File name. If no files are specified, the standard input is used and no file name is displayed.",
        nargs="*",
    )
    parser.add_argument(
        "-l",
        action="store_true",
        required=False,
        help="The number of lines in each input file is written to the standard output.",
    )
    parser.add_argument(
        "-w",
        action="store_true",
        required=False,
        help="The number of words in each input file is written to the standard output.",
    )
    parser.add_argument(
        "-c",
        action="store_true",
        required=False,
        help="The number of bytes in each input file is written to the standard output.  This will cancel out any prior usage of the -m option.",
    )
    parser.add_argument(
        "-m",
        action="store_true",
        required=False,
        help="The number of characters in each input file is written to the standard output.  If the current locale does not support multibyte characters, this is equivalent to the -c option.  This will cancel out any prior usage of the -c option.",
    )
    args = parser.parse_args()

    file_list = args.file
    print_options = {
        "word": args.w,
        "char": args.m,
        "line": args.l,
        "byte": args.c,
        "all": not (args.w or args.m or args.l or args.c),
    }

    if file_list:
        for file_name in file_list:
            with open(
                file_name,
                "rb",  # read with binary mode instead of text, else it fails to read some characters
                # readline without binary mode -> '\ufeffThe Project Gutenberg eBook of The Art of War\n'
                # readline with binary mode then decoded to utf-8 -> '\ufeffThe Project Gutenberg eBook of The Art of War\n'
                # because readline has 'universal newline support' -> which reads '\r\n' as '\n'.
                # Alternative to this is `open(file_name, newline='')`, which has universal readline support (in the sense that it knows the end of line), but doesn't convert '\r\n' to '\n'
                # source: https://softwareengineering.stackexchange.com/questions/298677/why-is-universal-newlines-mode-deprecated-in-python, https://softwareengineering.stackexchange.com/questions/298677/why-is-universal-newlines-mode-deprecated-in-python
            ) as f:
                print_counts(print_options, get_counts(f), file_name)
    else:
        f = sys.stdin.buffer  # sys.stdin is TextIO and .buffer gets the BinaryIO
        print_counts(print_options, get_counts(f))


# NOTE: BinaryIO is a child of class IO. Other class is TextIO
def get_counts(file_obj: BinaryIO) -> dict[str, int]:
    """Given <class '_io.TextIOWrapper'> object, returns line count, word count, byte count, char count"""
    line_count, word_count, byte_count, char_count = 0, 0, 0, 0
    while line := file_obj.readline():
        line_count += 1
        word_count += len(line.split())  # split takes isSpace by default
        byte_count += len(line)  # in utf-8 encoded bytestring each character is 1 byte
        char_count += len(
            line.decode(locale.getpreferredencoding())
        )  # read with whatever encoding is set by the system

    return {
        "line": line_count,
        "word": word_count,
        "byte": byte_count,
        "char": char_count,
    }


def print_counts(
    print_options: dict[str, bool], counts: dict[str, int], file_name: str = ""
) -> None:
    """Prints the counts same as `wc` command line utility"""
    result = []
    if print_options["line"] or print_options["all"]:
        result.append(counts["line"])
    if print_options["word"] or print_options["all"]:
        result.append(counts["word"])
    if print_options["byte"] or print_options["all"]:
        result.append(counts["byte"])
    elif print_options["char"]:
        result.append(counts["char"])

    print(*(str(num).rjust(8) for num in result), file_name)
