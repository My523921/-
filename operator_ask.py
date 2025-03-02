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

import asyncio
import requests
import json
from bpy import props
from bpy.types import Operator
from . import async_loop
from .chat_setup import system_instructions
from .chat_log import conversations
from .utils import parse_chatgpt_content


class CHAT_COMPANION_OT_ask(Operator, async_loop.AsyncModalOperatorMixin):
    bl_idname = "chat_companion.ask"
    bl_label = "Send"
    bl_description = "Send prompt to ChatGPT"
    bl_options = {'REGISTER', 'UNDO', 'INTERNAL'}

    # properties
    user_prompt: props.StringProperty()

    async def async_execute(self, context):
        chat_properties = context.scene.chat_companion_properties
        addon_preferences = context.preferences.addons[__package__].preferences

        # * https://platform.openai.com/account/api-keys
        api_key = addon_preferences.api_key

        # check if api key and the userpromt
        # are not none and if it is not an empty string
        api_key_go = api_key is not None and api_key
        user_prompt_go = self.user_prompt is not None and self.user_prompt

        if not api_key_go and not user_prompt_go:
            report_icon = 'WARNING'
            report_message = "No API key and no prompt to answer. Enter your API key in the addons preferences and enter a prompt into the text field."  # noqa
            self.report({report_icon}, report_message)
        elif not api_key_go and user_prompt_go:
            report_icon = 'WARNING'
            report_message = "No API key. Did you enter your API key in the addons preferences?"  # noqa
            self.report({report_icon}, report_message)
        elif not user_prompt_go and api_key_go:
            report_icon = 'WARNING'
            report_message = "No prompt entered."
            self.report({report_icon}, report_message)
        else:
            report_icon = 'INFO'
            report_message = "Your prompt was sent. Generating answer..."

            # setting answering status to waiting
            chat_properties.waiting_for_answer = True

            self.report({report_icon}, report_message)

            async_return = await asyncio.gather(
                self.query_openai(context, api_key),
                self.print_waiting_string(context)
            )

            # ! query chatGPT with http request
            # response = await self.query_openai(context, api_key)
            response = async_return[0]
            if response is not None:
                print("RESPONSE: ", response)
                content = response["choices"][0]["message"]["content"]

                # add answer to ui
                chat_properties.answer = content

                # parse ChatGPT content into parts of text/code/lists/...
                # serialize answer and add to property
                answer_parts = parse_chatgpt_content(context, content)
                chat_properties.answer_parts = json.dumps(
                    answer_parts)

                # tokens
                used_tokens = response["usage"]["total_tokens"]
                chat_properties.used_token_current = used_tokens
                chat_properties.used_token_session += used_tokens

                # add answer to conversation log
                conversations.append((
                    {"role": "user", "content": self.user_prompt},
                    {"role": "assistant", "content": content}
                ))
                # remove first item if conversation is longer than 4 prompts
                if len(conversations) > 4:
                    conversations.pop(0)

                report_icon = 'INFO'
                report_message = "Answer generated."
            else:
                report_icon = 'ERROR'
                report_message = "The response returned None."

            self.report({report_icon}, report_message)

        # update view_3d (where addon is located in (context))
        # TODO old answer still visible for a second
        context.area.tag_redraw()

        self.quit()

    async def query_openai(self, context, api_key):
        try:
            addon_preferences = context.preferences.addons[__package__].preferences  # noqa

            # http request session
            session = requests.Session()
            url = "https://api.openai.com/v1/chat/completions"
            # put together all messages
            all_messages = [
                {"role": "system", "content": " ".join(system_instructions)},
            ]
            # add previous conversations
            for previous_conversation in conversations:
                # question
                all_messages.append(previous_conversation[0])
                # answer
                all_messages.append(previous_conversation[1])
            # add current prompt
            all_messages.append({"role": "user", "content": self.user_prompt})

            payload = {
                "model": addon_preferences.model,
                "messages": all_messages,
                "temperature": 1.0,
                "top_p": 1.0,
                "n": 1,
                "stream": False,
                "presence_penalty": 0,
                "frequency_penalty": 0
            }
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            }

        # send the API request
            loop = asyncio.get_event_loop()
            future = loop.run_in_executor(
                None, lambda: session.post(
                    url,
                    headers=headers,
                    json=payload,
                    stream=False,
                    timeout=100))
            response = await future

            # to have http errors also raise exceptions
            response.raise_for_status()

            # setting answering status
            context.scene.chat_companion_properties.waiting_for_answer = False

        except requests.ConnectionError as e:
            self.showError(context, "Connection Error.", e)
        except requests.exceptions.HTTPError as e:
            if response.status_code == 429:
                self.showError(context, "Too Many Requests.", e)
            elif response.status_code == 401:
                self.showError(context,
                               "Unauthorized. Is your API key correct?", e)
            else:
                self.showError(context, "HTTP Error.", e)
        except requests.exceptions.Timeout as e:
            # Maybe set up for a retry, or continue in a retry loop
            self.showError(context, "Timeout.", e)
        except requests.exceptions.TooManyRedirects:
            # Tell the user their URL was bad and try a different one
            self.showError(context, "Too Many Redirects.", e)
        except requests.exceptions.RequestException as e:
            # catastrophic error. bail.
            self.showError(context, "Request Exception.", e)
        except Exception as e:
            print(e)
        else:
            return response.json()
        finally:
            # setting answering status
            context.scene.chat_companion_properties.waiting_for_answer = False

    # cancel the search if error occured during one of the requests
    # TODO show errors somewhere permanent and better visible
    def showError(self, context, message, error):
        chat_properties = context.scene.chat_companion_properties
        print(error)
        chat_properties.answer = message
        parts = json.dumps([{"type": "text", "content": [message]}])
        chat_properties.answer_parts = parts
        context.area.tag_redraw()
        self.report({'ERROR'}, message)
        self.quit()

    async def print_waiting_string(self, context):
        interval = 0.35
        prefix = "Generating"
        suffix = "."
        icons = ["ALIGN_TOP", "ALIGN_MIDDLE", "ALIGN_BOTTOM"]
        while context.scene.chat_companion_properties.waiting_for_answer:
            for iteration in range(1, len(icons) + 1):
                context.scene.chat_companion_properties["waiting_string"] = \
                    prefix + iteration*suffix  # noqa
                context.scene.chat_companion_properties["waiting_icon"] = icons[iteration-1]  # noqa
                context.area.tag_redraw()
                await asyncio.sleep(interval)
