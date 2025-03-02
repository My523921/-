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

import bpy
from . import global_variables
from .operator_full_version import CHAT_COMPANION_OT_context_menu_full


class WM_MT_button_context(bpy.types.Menu):
    # class to add a context menu entry
    bl_label = ""

    @classmethod
    def poll(cls, context):
        return bpy.ops.ui.copy_data_path_button.poll()

    def draw(self, context):
        pass


def menu_func(self, context):

    chat_properties = context.scene.chat_companion_properties

    layout = self.layout
    layout.separator()
    pcoll = global_variables.preview_collections["main"]

    if chat_properties.full_variant:
        from .full.operator_context_menu import CHAT_COMPANION_OT_context_menu
        layout.operator(CHAT_COMPANION_OT_context_menu.bl_idname,
                        icon_value=pcoll["poly_icon"].icon_id)
    else:
        layout.operator(CHAT_COMPANION_OT_context_menu_full.bl_idname,
                        icon_value=pcoll["poly_icon"].icon_id)
