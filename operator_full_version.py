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

from bpy.types import Operator


class CHAT_COMPANION_OT_full_version(Operator):
    bl_idname = "chat_companion.full_version"
    bl_label = ""
    bl_description = "Please Upgrade to the Full Version of the addon to use all its features"  # noqa
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    def execute(self, context):
        return {'FINISHED'}


class CHAT_COMPANION_OT_context_menu_full(Operator):
    bl_idname = "chat_companion.context_menu_full"
    bl_label = "Ask Chat Companion about this"
    bl_description = "Please Upgrade to the Full Version of the addon to use all its features"  # noqa

    @classmethod
    def poll(cls, context):
        return False

    def execute(self, context):
        return {'FINISHED'}
