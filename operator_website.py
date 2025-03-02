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


class CHAT_COMPANION_OT_website(Operator):
    bl_idname = "chat_companion.website"
    bl_label = "Open"
    bl_description = "Open Website"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    # properties
    url: bpy.props.StringProperty()

    def execute(self, context):

        bpy.ops.wm.url_open(url=self.url)

        return {'FINISHED'}
