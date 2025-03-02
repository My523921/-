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

from bpy.types import Panel
from .panel import POLYGONINGENIEUR_panel
from .operator_ask import CHAT_COMPANION_OT_ask
from .utils import wrap_string_to_panel
from .operator_open_prefs import CHAT_COMPANION_OT_open_prefs
from .operator_website import CHAT_COMPANION_OT_website


class CHAT_COMPANION_PT_prompt(POLYGONINGENIEUR_panel, Panel):
    bl_idname = "CHAT_COMPANION_PT_prompt"
    bl_label = "Prompt"
    bl_parent_id = "CHAT_COMPANION_PT_main"
    bl_order = 0
    bl_options = {"HIDE_HEADER"}

    def draw_header(self, context):
        self.layout.label(
            text="", icon="VIEWZOOM")

    def draw(self, context):

        addon_props = context.scene.chat_companion_properties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # ! API key info
        api_key = context.preferences.addons[__package__].preferences.api_key
        no_api_key = api_key is None or len(api_key) == 0 or api_key == ""
        if no_api_key:
            api_info_container = layout.column(align=True)

            # api info text
            api_info_text = api_info_container.column(align=False)
            api_info_text.alert = True
            api_info_text.scale_y = 0.8
            text_list = wrap_string_to_panel(context, "Please enter your API key in the addon preferences.")  # noqa
            for index, line in enumerate(text_list):
                if index == 0:
                    api_info_text.label(text=line, icon="KEYINGSET")
                else:
                    api_info_text.label(text=line)

            # add button to api key website
            api_website_container = api_info_container.row(align=True)
            api_website_button = api_website_container.column(align=True)
            api_website = api_website_button.operator(
                operator=CHAT_COMPANION_OT_website.bl_idname,
                text="",
                icon="URL")
            api_website.url = "https://platform.openai.com/account/api-keys"
            api_website_text = api_website_container.column(align=True)
            api_website_text.alignment = "LEFT"
            api_website_text.label(text=" Get your API key here")

            # add button to get to preferences directly
            api_prefs_container = api_info_container.row(align=True)
            api_prefs_button = api_prefs_container.column(align=True)
            api_prefs_button.operator(
                operator=CHAT_COMPANION_OT_open_prefs.bl_idname,
                text="",
                icon="PREFERENCES")
            api_prefs_text = api_prefs_container.column(align=True)
            api_prefs_text.alignment = "LEFT"
            api_prefs_text.label(text=" And enter it here", )

            layout.separator()

        prompt = layout.row(align=True)
        prompt.enabled = not no_api_key
        prompt_text = prompt.column(align=True)
        prompt_text.scale_y = 1.2
        prompt_text.enabled = not addon_props.waiting_for_answer
        prompt_text.prop(addon_props, "user_prompt", text="")

        prompt_icon = prompt.column(align=True)
        prompt_icon.scale_y = 1.2
        prompt_icon.scale_x = 1.1
        prompt_icon.enabled = not addon_props.waiting_for_answer
        props = prompt_icon.operator(
            operator=CHAT_COMPANION_OT_ask.bl_idname, text="", icon="RIGHTARROW_THIN")  # noqa
        props.user_prompt = addon_props.user_prompt

        promt_full = layout.column(align=True)
        wrapped_prompt = wrap_string_to_panel(
            context, addon_props.user_prompt, 13)
        # show prompt below text field when it is multiline only
        if len(wrapped_prompt) > 1:
            for line in wrapped_prompt:
                line_col = promt_full.column()
                line_col.label(text=line)
                line_col.scale_y = 0.8
