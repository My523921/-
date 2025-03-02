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
from .operator_website import CHAT_COMPANION_OT_website


class CHAT_COMPANION_PT_info(POLYGONINGENIEUR_panel, Panel):
    bl_idname = "CHAT_COMPANION_PT_info"
    bl_label = "Information"
    bl_parent_id = "CHAT_COMPANION_PT_main"
    bl_order = 3
    # bl_options = {'DEFAULT_CLOSED'}

    def draw_header(self, context):
        self.layout.label(text="", icon="INFO")

    def draw(self, context):
        addon_props = context.scene.chat_companion_properties

        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        # ! used tokens
        layout.label(text="Used Tokens:")
        tokens = layout.column_flow(columns=2, align=True)
        current_tokens = tokens.row(align=True)
        current_text = "Last prompt: " + str(addon_props.used_token_current)
        current_tokens.label(text=current_text)
        session_tokens = tokens.row(align=True)
        session_text = "Session: " + str(addon_props.used_token_session)
        session_tokens.label(text=session_text)

        # ! add button to api key website and usage site
        usage_website = layout.column(align=True)
        api_website = usage_website.operator(
            operator=CHAT_COMPANION_OT_website.bl_idname,
            text="Your Usage",
            icon="URL")
        api_website.url = "https://platform.openai.com/account/usage"
        # Pricing button
        api_website = usage_website.operator(
            operator=CHAT_COMPANION_OT_website.bl_idname,
            text="OpenAI Pricing",
            icon="URL")
        api_website.url = "https://openai.com/pricing"
