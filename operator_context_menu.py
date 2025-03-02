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


class CHAT_COMPANION_OT_context_menu(bpy.types.Operator):
    bl_idname = "chat_companion.context_menu"
    bl_label = "Ask Chat Companion about this"
    bl_description = "Get an explanation for this data path in the addon panel"

    @classmethod
    def poll(cls, context):
        api_key = context.preferences.addons[__package__.split(".")[0]].preferences.api_key  # noqa
        no_api_key = api_key is None or len(api_key) == 0 or api_key == ""
        chat_properties = context.scene.chat_companion_properties
        return not no_api_key and not chat_properties.waiting_for_answer

    def execute(self, context):
        chat_properties = context.scene.chat_companion_properties

        is_splitted = False

        # ! get full data path
        bpy.ops.ui.copy_data_path_button(full_path=True)
        full_path = context.window_manager.clipboard
        prompt = "Explain " + full_path + \
            " briefly and with a short python bpy code example."

        # in 3d view context
        # ! make sure view3d editor is a visible area
        # * and we need the view3d area to overwrite the context
        # editor not visible, split area
        if not any(area.type == 'VIEW_3D' for area in bpy.context.screen.areas):  # noqa
            start_areas = bpy.context.screen.areas[:]

            is_splitted = True

            # If it's not visible, split the current area
            bpy.ops.screen.area_split(direction='VERTICAL', factor=0.0)

            # change space to text editor
            for area in context.screen.areas:
                if area not in start_areas:
                    area.type = 'VIEW_3D'

            # Get the new active area
            view3D_area = next(
                area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')  # noqa
        # view3d visible, get area
        else:
            # If view3d is already visible, just get its area
            view3D_area = next(
                area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')  # noqa

        # ! add data path as prompt
        chat_properties.user_prompt = prompt

        # ! ask
        # # run_text_data_block.use_module = True
        with context.temp_override(area=view3D_area):
            bpy.ops.chat_companion.ask(user_prompt=prompt)
            # ! close created text_area again
            if is_splitted:
                bpy.ops.screen.area_close()

        return {'FINISHED'}
