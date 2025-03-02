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

from bpy.types import AddonPreferences
from bpy import props
from .operator_website import CHAT_COMPANION_OT_website


class ChatCompanionPreferences(AddonPreferences):
    # this must match the addon name, use '__package__'
    # when defining this in a submodule of a python package.
    bl_idname = __package__

    models = (
        ("gpt-3.5-turbo", "GPT-3.5-Turbo (ChatGPT)", "GPT-3.5-Turbo (ChatGPT)"),
        ("gpt-4", "GPT-4", "GPT 4")
    )

    api_key: props.StringProperty(
        name="API Key",
        description="Your openai API key, you can generate it at https://platform.openai.com/account/api-keys.",  # noqa
    )

    model: props.EnumProperty(
        name="OpenAI models",
        description="Choose what OpenAI model you want to use.",
        items=models,
        default="gpt-3.5-turbo"
    )

    def draw(self, context):
        layout = self.layout
        layout.use_property_split = True
        layout.use_property_decorate = False

        api_key_container = layout.column(align=True)
        api_key_container.label(text="Get your API key here:")
        # add button to api key website
        api_website = api_key_container.operator(
            operator=CHAT_COMPANION_OT_website.bl_idname,
            text="https://platform.openai.com/account/api-keys",
            icon="URL")
        api_website.url = "https://platform.openai.com/account/api-keys"
        # enter api key
        api_key_container.label(text="API key:")
        api_key_container.prop(self, "api_key", text="")

        # choose between different models ("gpt-3.5-turbo", "gpt-4", ...)
        model_container = layout.row()
        model_container.prop(self, "model", text="Choose OpenAI model: ")

        # TODO add temperature, top_p, ... to addon preferences
