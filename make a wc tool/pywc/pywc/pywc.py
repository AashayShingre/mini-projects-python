import argparse
import sys
import locale

def pywc_main(): 
    parser = argparse.ArgumentParser(description="wc tool made with python")
    parser.add_argument("file", help="File name. If no files are specified, the standard input is used and no file name is displayed.", nargs="*") 
    parser.add_argument("-l", action="store_true", required=False, help="The number of lines in each input file is written to the standard output.")
    parser.add_argument("-w", action="store_true", required=False, help="The number of words in each input file is written to the standard output.")
    parser.add_argument("-c", action="store_true", required=False, help="The number of bytes in each input file is written to the standard output.  This will cancel out any prior usage of the -m option.")
    parser.add_argument("-m", action="store_true", required=False, help="The number of characters in each input file is written to the standard output.  If the current locale does not support multibyte characters, this is equivalent to the -c option.  This will cancel out any prior usage of the -c option.")
    args = parser.parse_args()

    file_list = args.file
    print_options = {"word": args.w, "char": args.m, "line": args.l, "byte": args.c, "all": not (args.w or args.m or args.l or args.c)}

    if file_list: 
        for file_name in file_list:
            with open(file_name, 'rb') as f: # read with binary mode instead of text, else it removes \r characters from a file.
                print_counts(print_options, get_counts(f), file_name)
    else: 
        f =  sys.stdin.buffer
        print_counts(print_options, get_counts(f))

def get_counts(file_obj): 
    line_count, word_count, byte_count, char_count = 0, 0, 0, 0
    while line := file_obj.readline(): 
        line_count += 1 
        word_count += len(line.split()) # split takes isSpace by default
        byte_count += len(line)
        char_count += len(line.decode(locale.getpreferredencoding()))
    
    return {"line": line_count, "word": word_count, "byte": byte_count, "char": char_count}

def print_counts(print_options, counts, file_name=""): 
    result = []
    if print_options["line"] or print_options["all"]:
        result.append(counts["line"]) 
    if print_options["word"] or print_options["all"]:
        result.append(counts["word"])
    if print_options["byte"] or print_options["all"]:
        result.append(counts["byte"])
    elif print_options["char"]:
        result.append(counts["char"])
    
    print("".join(str(num).rjust(8) for num in result), file_name)
    

    