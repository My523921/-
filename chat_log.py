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

# conversations list, begins with initial prompts to train the ai
# FIFO, list of:
# (
#     {"role": "user", "content": "q 1"},
#     {"role": "assistant", "content": "a1"}
# ), ...
conversations = [
    (
        {"role": "user", "content": "In blender bpy, how do I import the bpy module?"},
        {"role": "assistant", "content": """
To access bpy from an external Python script, you will need to add Blender's Python interpreter to your system's PATH variable, and then use it to run your script. Here's an example of how you can import bpy from an external Python script:
``` python
import bpy

# Your code goes here...
```
"""}
    ),
    (
        {"role": "user", "content": "How can I convert a curve into a mesh?"},
        {"role": "assistant", "content": """
        To convert a curve into a mesh in Blender, follow these steps:
1. Select the curve you want to convert to a mesh by right-clicking on it.
2. Press "Alt+C" on your keyboard or go to "Object" > "Convert To" > "Mesh from Curve/Meta/Surf/Text" in the top menu.
3. In the pop-up menu, select "Mesh from Curve" and click "OK".
4. The curve will now be converted into a mesh.
"""}
    )
]
