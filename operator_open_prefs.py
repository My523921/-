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
from bpy.types import Operator


class CHAT_COMPANION_OT_open_prefs(Operator):
    bl_idname = "chat_companion.open_prefs"
    bl_label = "Open Preferences"
    bl_description = "Open the preferences for Chat Companion"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):

        bpy.ops.screen.userpref_show()
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.data.window_managers["WinMan"].addon_search = "Chat Companion"

        return {'FINISHED'}
