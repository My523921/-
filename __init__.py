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
import os

from . import global_variables
from .async_loop import *

# classes that need to be registered
from .addon_preferences import ChatCompanionPreferences
from .properties import ChatCompanionProperties
from .panel import CHAT_COMPANION_PT_main
from .panel_prompt import CHAT_COMPANION_PT_prompt
from .panel_output import CHAT_COMPANION_PT_output
from .panel_info import CHAT_COMPANION_PT_info
from .operator_ask import CHAT_COMPANION_OT_ask
from .operator_copy import CHAT_COMPANION_OT_copy
from .operator_open_prefs import CHAT_COMPANION_OT_open_prefs
from .operator_website import CHAT_COMPANION_OT_website
from .operator_full_version import CHAT_COMPANION_OT_full_version
from .operator_full_version import CHAT_COMPANION_OT_context_menu_full
from .button_context import WM_MT_button_context
from .button_context import menu_func

# ! variant enable/disable
# classes of full variant the need to be registered
from .full.operator_copy_code_clipboard import CHAT_COMPANION_OT_copy_code_clipboard  # noqa
from .full.operator_copy_code_cursor import CHAT_COMPANION_OT_copy_code_cursor
from .full.operator_copy_code_text import CHAT_COMPANION_OT_copy_code_text
from .full.operator_run_code import CHAT_COMPANION_OT_run_code
from .full.operator_context_menu import CHAT_COMPANION_OT_context_menu

bl_info = {
    "name": "Chat Companion",
    "author": "Polygoningenieur Gustav Hahn",
    "description": "Let AI help you in using Blender and writing scripts.",  # noqa
    "blender": (3, 4, 0),
    "version": (1, 0, 1),
    "location": "View3D",
    "warning": "",
    "doc_url": "https://blendermarket.com/creators/polygoningenieur",
    "support": "COMMUNITY",
    "category": "AI"
}

classes = (
    AsyncLoopModalOperator,
    ChatCompanionPreferences,
    ChatCompanionProperties,
    CHAT_COMPANION_PT_main,
    CHAT_COMPANION_PT_prompt,
    CHAT_COMPANION_PT_output,
    CHAT_COMPANION_PT_info,
    CHAT_COMPANION_OT_ask,
    CHAT_COMPANION_OT_copy,
    CHAT_COMPANION_OT_open_prefs,
    CHAT_COMPANION_OT_website,
    CHAT_COMPANION_OT_full_version,
    CHAT_COMPANION_OT_context_menu_full,
    WM_MT_button_context
)

# ! variant enable/disable
classes_full_variant = (
    CHAT_COMPANION_OT_copy_code_clipboard,
    CHAT_COMPANION_OT_copy_code_cursor,
    CHAT_COMPANION_OT_copy_code_text,
    CHAT_COMPANION_OT_run_code,
    CHAT_COMPANION_OT_context_menu
)

# ! variant enable/disable
classes += classes_full_variant


def register():

    print("................Chat.Companion.Registering.................")

    # Note that preview collections returned by bpy.utils.previews
    # are regular py objects - you can use them to store custom data.
    import bpy.utils.previews
    pcoll = bpy.utils.previews.new()
    # path to the folder where the icon is
    # the path is calculated relative to this py file inside the addon folder
    chat_comp_icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    # load a preview thumbnail of a file and store in the previews collection
    pcoll.load("poly_icon", os.path.join(
        chat_comp_icons_dir, "poly_icon.png"), 'IMAGE')

    global_variables.preview_collections["main"] = pcoll

    async_loop.setup_asyncio_executor()

    for c in classes:
        bpy.utils.register_class(c)

    bpy.types.Scene.chat_companion_properties = bpy.props.PointerProperty(
        type=ChatCompanionProperties)

    bpy.types.WM_MT_button_context.append(menu_func)
    # bpy.types.TEXT_MT_context_menu.append(menu_func)
    # bpy.types.TEXT_MT_edit.append(menu_func)

    print("..............Chat.Companion.Registration..DONE............")


def unregister():

    del bpy.types.Scene.chat_companion_properties

    for pcoll in global_variables.preview_collections.values():
        bpy.utils.previews.remove(pcoll)
    global_variables.preview_collections.clear()

    bpy.types.WM_MT_button_context.remove(menu_func)
    # bpy.types.TEXT_MT_edit.remove(menu_func)
    # bpy.types.TEXT_MT_context_menu.remove(menu_func)

    from bpy.utils import unregister_class
    for c in reversed(classes):
        if c.is_registered:
            unregister_class(c)
