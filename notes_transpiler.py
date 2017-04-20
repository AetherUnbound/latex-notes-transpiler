#!/usr/bin/python
import os
import sys
import subprocess


def create_tex(template_file, input_file, output_file):
    with open(template_file, 'r') as template:
        template_lines = template.readlines()
    template_lines = [line.strip('\n') for line in template_lines]
    start_index = template_lines.index("%%%TEXT GOES HERE%%%")
    tex_lines = transpile(input_file)
    out_lines = template_lines[:start_index] + tex_lines + template_lines[start_index + 1:]
    # print("\n".join(out_lines))
    with open(output_file, 'w') as out:
        out.write('\n'.join(out_lines))
    subprocess.call(["pdflatex", output_file])


def transpile(filename):
    with open(filename, 'r') as f:
        # Trim newlines, trailing tabs, and convert 4 spaces into tabs
        lines = list(map(lambda x: x.replace("    ", "\t").strip('\n').rstrip('\t'), f.readlines()))
        # Remove any empty strings
        lines = list(filter(None, lines))
        return tex_body(lines)


def tex_body(input):
    level = 0
    i = 0
    output = []
    while True:
        if i == len(input):
            break
        if level == 0:
            output.append("\\subsection*{" + input[i][0].upper() + input[i][1:] + "}")
            i += 1
            if i == len(input):
                break
        curr_level = len(input[i]) - len(input[i].lstrip('\t'))
        if curr_level > 0:
            out, i, level = to_itemize(input, i, curr_level)
            output.extend(out)
        elif i == len(input): break
    return output


def to_itemize(input, loc, level):
    output = []
    i = loc
    while True:
        output.append("\t" * level + "\\begin{itemize}")
        while True:
            s_out = input[i].lstrip('\t')
            s_out = "\\item " + s_out[0].upper() + s_out[1:]
            output.append("\t" * (level + 1) + s_out)
            i += 1
            if i == len(input):
                level = 0
                break
            next_level = len(input[i]) - len(input[i].lstrip('\t'))

            # Go deeper
            if next_level > level:
                out, i, level = to_itemize(input, i, next_level)
                output.extend(out)

            # Otherwise end itemize and return to that level
            elif next_level < level:
                output.append("\t" * level + "\\end{itemize}")
                level = next_level
                return output, i, level
            if level == 0: break
        if level == 0:
            output.append("\t" * (level + 1) + "\\end{itemize}")
            break
    return output, i, level


if __name__ == "__main__":
    # TODO: use argparser for better handling
    template = sys.argv[1]
    notes = sys.argv[2]
    output = sys.argv[3]
    create_tex(template, notes, output)
    # create_tex("template.tex", "example_notes_small.txt", "output.tex")
