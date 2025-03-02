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


class ChatCompanionProperties(bpy.types.PropertyGroup):

    full_variant: bpy.props.BoolProperty(
        name="Full Variant",
        description="If Addon is Full Variant (True) or Free (False)",
        default=True
    )

    waiting_for_answer: bpy.props.BoolProperty(
        name="Waiting",
        description="Waiting for an answer from ChatGPT",
        default=False
    )

    waiting_string: bpy.props.StringProperty(
        name="Waiting String",
        description="The string that is being printed while waiting for the ChatGPT answer",  # noqa
        default=""
    )

    waiting_icon: bpy.props.StringProperty(
        name="Waiting Icon",
        default="ALIGN_TOP"
    )

    user_prompt: bpy.props.StringProperty(
        name="ChatGPT user prompt",
        description="Talk with ChatGPT through here",
        options={'TEXTEDIT_UPDATE'}
    )

    answer: bpy.props.StringProperty(
        name="Answer from ChatGPT",
        description="Answer from ChatGPT",
        default="..."
    )

    pretty_answer: bpy.props.StringProperty(
        name="Answer from ChatGPT",
        description="Answer from ChatGPT",
        default="..."
    )

    answer_parts: bpy.props.StringProperty(
        name="Answer in Parts",
        description="Array of Answer in parts serialized",
        default=""
    )

    used_token_session: bpy.props.IntProperty(
        name="Used Tokens in this session",
        default=0
    )

    used_token_current: bpy.props.IntProperty(
        name="Used Tokens of current prompt",
        default=0
    )
