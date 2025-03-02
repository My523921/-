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
from . import global_variables
from .operator_open_prefs import CHAT_COMPANION_OT_open_prefs


class POLYGONINGENIEUR_panel:
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Companion"


class CHAT_COMPANION_PT_main(POLYGONINGENIEUR_panel, Panel):
    bl_idname = "CHAT_COMPANION_PT_main"
    bl_label = "Chat Companion"

    def draw_header(self, context):
        layout = self.layout
        pcoll = global_variables.preview_collections["main"]
        layout.label(text="", icon_value=pcoll["poly_icon"].icon_id)

        layout.operator(
            operator=CHAT_COMPANION_OT_open_prefs.bl_idname,
            text="",
            icon="PREFERENCES")

    def draw(self, context):
        pass
