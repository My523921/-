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

import json
from bpy.types import Panel
from .operator_copy import CHAT_COMPANION_OT_copy
from .operator_full_version import CHAT_COMPANION_OT_full_version
from .utils import wrap_parts_to_panel
from .utils import wrap_string_to_panel
from .utils import wrap_array
from .utils import parse_chatgpt_content
from .chat_setup import test_answer_1, test_answer_2, test_answer_3, test_answer_4  # noqa
from .panel import POLYGONINGENIEUR_panel


# TODO merge prompt and answer panel


class CHAT_COMPANION_PT_output(POLYGONINGENIEUR_panel, Panel):
    bl_idname = "CHAT_COMPANION_PT_output"
    bl_label = "Answer"
    bl_parent_id = "CHAT_COMPANION_PT_main"
    bl_order = 2

    def draw_header(self, context):
        self.layout.label(
            text="", icon="WORDWRAP_ON")

    def draw(self, context):
        chat_properties = context.scene.chat_companion_properties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # waiting for answer
        if chat_properties.waiting_for_answer:
            layout.label(
                text=chat_properties.waiting_string,
                icon=chat_properties.waiting_icon)
        else:
            if len(chat_properties.answer_parts) > 0:
                self.draw_answer(context, layout)
            else:
                layout.label(text="Give instructions in the prompt field above.")  # noqa

    def draw_answer(self, context, layout):
        chat_properties = context.scene.chat_companion_properties

        if chat_properties.full_variant:
            from .full.operator_copy_code_cursor import CHAT_COMPANION_OT_copy_code_cursor  # noqa
            from .full.operator_copy_code_clipboard import CHAT_COMPANION_OT_copy_code_clipboard   # noqa
            from .full.operator_copy_code_text import CHAT_COMPANION_OT_copy_code_text  # noqa
            from .full.operator_run_code import CHAT_COMPANION_OT_run_code

        # ! get separated answer parts
        answer_parts = json.loads(chat_properties.answer_parts)
        # TODO remove -> only for tests
        # answer_parts = parse_chatgpt_content(context, test_answer_4)
        # ! wrap to fit panel width
        wrapped_parts = wrap_parts_to_panel(context, answer_parts)

        for index, part in enumerate(answer_parts):
            # ! regular text to show
            if part["type"] == "text":
                wrapped_text = wrap_array(context, part["content"])
                for line in wrapped_text:
                    line_col = layout.column()
                    line_col.label(text=line)
                    if len(line) == 0:
                        line_col.scale_y = 0.3
                    else:
                        # TODO make dependent on point size
                        line_col.scale_y = 0.6

            # ! list items
            # TODO add checkbox, panel or execute button in front?
            if part["type"] == "list":
                list_box = layout.row(align=True)
                list_box.separator(factor=0.5)
                for list_item in part["content"]:
                    # list number
                    list_number = list_box.box()
                    list_number.label(text=list_item.split(".")[0] + ".")
                    list_number.alignment = "EXPAND"
                    list_number.scale_x = 0.075
                    # list text
                    list_text = list_box.column(align=True)
                    wrapped_list = wrap_string_to_panel(
                        context, list_item.split(".", 1)[-1])
                    for list_line in wrapped_list:
                        list_text.label(text=list_line)
                list_box.separator(factor=0.5)

            # ! code
            if part["type"] == "code":
                code_container = layout.column(align=True)

                header = code_container.column_flow(columns=3, align=True)
                header.scale_y = 1.1
                header.label(text="Code")

                # ! run code
                run_code_button = header.row(align=True)
                run_code_button.alignment = "CENTER"
                run_code_button.scale_x = 1.3
                run_code_button.enabled = chat_properties.full_variant
                if chat_properties.full_variant:
                    run_code = run_code_button.operator(
                        operator=CHAT_COMPANION_OT_run_code.bl_idname,
                        text="",
                        icon="PLAY")
                    run_code.content = json.dumps(
                        answer_parts[index]["content"])
                else:
                    run_code = run_code_button.operator(
                        operator=CHAT_COMPANION_OT_full_version.bl_idname,
                        text="",
                        icon="PLAY")

                copy_buttons = header.row(align=True)
                copy_buttons.alignment = "RIGHT"

                # ! copy to cursor in current script file
                copy_to_cursor_button = copy_buttons.column(align=True)
                copy_to_cursor_button.enabled = chat_properties.full_variant
                if chat_properties.full_variant:
                    copy_cursor = copy_to_cursor_button.operator(
                        operator=CHAT_COMPANION_OT_copy_code_cursor.bl_idname,
                        text="",
                        icon="ITALIC")
                    copy_cursor.content = json.dumps(
                        answer_parts[index]["content"])
                else:
                    copy_cursor = copy_to_cursor_button.operator(
                        operator=CHAT_COMPANION_OT_full_version.bl_idname,
                        text="",
                        icon="ITALIC")

                # ! copy to new a new script file
                copy_to_script_button = copy_buttons.column(align=True)
                copy_to_script_button.enabled = chat_properties.full_variant
                if chat_properties.full_variant:
                    copy_script = copy_to_script_button.operator(
                        operator=CHAT_COMPANION_OT_copy_code_text.bl_idname,
                        text="",
                        icon="TEXT")
                    copy_script.content = json.dumps(
                        answer_parts[index]["content"])
                else:
                    copy_script = copy_to_script_button.operator(
                        operator=CHAT_COMPANION_OT_full_version.bl_idname,
                        text="",
                        icon="TEXT")

                # ! copy code part
                copy_code_button = copy_buttons.column(align=True)
                copy_code_button.scale_y = 1
                copy_code_button.scale_x = 1
                copy_code_button.alignment = "RIGHT"
                copy_code_button.enabled = chat_properties.full_variant
                if chat_properties.full_variant:
                    copy_code = copy_code_button.operator(
                        operator=CHAT_COMPANION_OT_copy_code_clipboard.bl_idname,  # noqa
                        text="",
                        icon="DUPLICATE")
                    copy_code.content = json.dumps(
                        answer_parts[index]["content"])
                else:
                    copy_code = copy_code_button.operator(
                        operator=CHAT_COMPANION_OT_full_version.bl_idname,
                        text="",
                        icon="DUPLICATE")

                # ! show code
                # TODO line numbers without word wraps
                box = code_container.box()
                box.separator(factor=0.2)
                for line_index, code_line in enumerate(part["content"]):
                    # container
                    code_line_container = box.row(align=True)
                    code_line_container.scale_y = 0.6
                    # line number
                    code_line_number = code_line_container.column(align=True)
                    line_number = line_index + 1
                    code_line_number.label(text=str(line_number))
                    code_line_number.alignment = "LEFT"
                    code_line_number.scale_x = 0.075
                    code_line_number.enabled = False
                    # code text
                    code_line_text = code_line_container.column(align=True)
                    wrapped_code = wrap_string_to_panel(context, code_line)
                    for wr_index, wrapped_line in enumerate(wrapped_code):
                        code_line_text.label(text=wrapped_line)
                        # if len(wrapped_code) > 1 and wr_index == 2:
                        #     code_line_text.scale_y = 2
                        # else:
                        #     code_line_text.scale_y = 1

                    code_line_text.alignment = "EXPAND"
                box.separator(factor=0.2)

                layout.separator(factor=0.2)

        # ! copy complete answer
        copy_answer_button = layout.row(align=True)
        copy_all_props = copy_answer_button.operator(
            operator=CHAT_COMPANION_OT_copy.bl_idname,
            text="Copy Answer",
            icon="DUPLICATE")
        copy_all_props.content_type = "FULL"
        copy_all_props.content = chat_properties.answer
