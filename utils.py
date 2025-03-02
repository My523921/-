# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import math
import copy
import textwrap
import itertools
import re
# import blf

width_adjust = 10


def parse_chatgpt_content(context, answer):
    # ! 1. answer is for log and copying the whole answer
    # TODO put into log

    # ! 2. split lines at line boundaries (for example linesep: \n)
    answer_list = answer.splitlines()

    # ! 3. separate into text/code/list parts
    # for special treatment of individual parts
    answer_parts = []
    index = 0
    current_type = "none"
    switch = False
    first_list_item = True
    jumping_list_gap = False
    code_started = False

    for line in answer_list:
        # * switching between parts
        # code ends, afterwards could be anything
        if "```" in line and code_started:
            current_type = "none"
            code_started = False
            continue
        # code begins
        elif "```" in line:
            # TODO get type of code (for example python, javascript, ...)
            current_type = "code"
            index += 1
            switch = True
            code_started = True
        # list line
        elif re.search(r"^\d+\.\s", line):
            current_type = "list"
            if first_list_item or not jumping_list_gap:
                first_list_item = False
                index += 1
                new_part = {"type": current_type,
                            "content": []}
                answer_parts.append(new_part)
        # remove blank lines after a list entry
        elif current_type == "list" and len(line) == 0:
            jumping_list_gap = True
            continue
        # first line after last list line
        elif current_type == "list" and not re.search(r"^\d+\.\s", line):
            current_type = "text"
            index += 1
            switch = True
            first_list_item = True
        # after code, the type is none, and is followed by blank text lines
        elif current_type == "none" and len(line) == 0:
            current_type = "text"
            index += 1
            switch = True
        else:
            pass

        # * adding of lines to parts
        # create first part
        if len(answer_parts) == 0:
            # add text part
            current_type = "text"
            new_part = {"type": current_type,
                        "content": [line, ]}
            answer_parts.append(new_part)
        # create part of certain type
        elif switch:
            new_part = {"type": current_type,
                        "content": []}
            answer_parts.append(new_part)
            switch = False
        # append line to current part type
        else:
            answer_parts[index]["content"].append(line)

        # reset if we are currently just jumping over a blank line
        # between list items
        jumping_list_gap = False

    # add indices
    for index, part in enumerate(answer_parts):
        part["index"] = index

    return answer_parts


def wrap_parts_to_panel(context, answer_parts):
    # dpi = bpy.context.preferences.system.dpi
    # points = bpy.context.preferences.ui_styles[0].widget_label.points
    # Get the DPI scale factor
    # dpi_scale_factor = bpy.context.preferences.system.dpi / 72
    # Calculate the font size in pixels
    # pixel_size = points * dpi_scale_factor
    # print("Font size in pixels:", pixel_size)

    region_width = context.region.width
    max_width = math.floor(region_width / width_adjust)
    wrapped_answer_parts = copy.deepcopy(answer_parts)

    for part in wrapped_answer_parts:
        wrapped_part = []
        for line in part["content"]:
            # wrap each line if exceeding panel width
            wrap_list = textwrap.wrap(line, max_width)
            # add empty string to empty list
            # otherwise it gets lost in chaining later
            # (this will be an empty line)
            if len(wrap_list) == 0:
                wrap_list = [""]
            wrapped_part.append(wrap_list)
        part["content"] = list(itertools.chain.from_iterable(wrapped_part))

    return wrapped_answer_parts


def wrap_array(context, array):
    region_width = context.region.width
    max_width = math.floor(region_width / width_adjust)

    wrapped_array = []
    for line in array:
        # wrap each line if exceeding panel width
        wrap_list = textwrap.wrap(line, max_width)
        # add empty string to empty list
        # otherwise it gets lost in chaining later
        # (this will be an empty line)
        if len(wrap_list) == 0:
            wrap_list = [""]
        wrapped_array.append(wrap_list)
    wrapped_array = list(itertools.chain.from_iterable(wrapped_array))

    return wrapped_array


def wrap_non_code_parts(answer_parts, width_in_px=50):

    wrapped_answer_parts = copy.deepcopy(answer_parts)

    for part in wrapped_answer_parts:
        wrapped_part = []
        for line in part["content"]:
            if part["type"] != "code":
                # wrap each line if exceeding panel width
                wrap_list = textwrap.wrap(line, width_in_px)
            else:
                wrap_list = [line]
            # add empty string to empty list
            # otherwise it gets lost in chaining later
            # (this will be an empty line)
            if len(wrap_list) == 0:
                wrap_list = [""]
            wrapped_part.append(wrap_list)
        part["content"] = list(itertools.chain.from_iterable(wrapped_part))

    return wrapped_answer_parts


def wrap_string_to_panel(context, string, adjust=width_adjust):
    region_width = context.region.width
    max_width = math.floor(region_width / adjust)
    wrapped_string = copy.copy(string)

    # wrap each line if exceeding panel width
    wrap_list = textwrap.wrap(wrapped_string, max_width)

    return wrap_list


def parts_to_pretty_string(parts):
    pretty_string = ''
    previous_type = "text"
    begin_comment = False
    end_comment = False
    for part in parts:
        # put multiline comment at the beginning of text part
        if part["type"] == "text" and not begin_comment:
            begin_comment = True
        for line in part["content"]:
            # add multiline comment
            if begin_comment:
                pretty_string += '"""\n'
                begin_comment = False
                end_comment = True
            # put an extra line break after code
            if part["type"] == "text" and previous_type == "code":
                pretty_string += '\n'
            # concatenate the line with a line break
            pretty_string += line + '\n'

            previous_type = part["type"]

        # add multiline comment at end of text block
        if end_comment:
            pretty_string += '"""\n'
            end_comment = False

    return pretty_string
