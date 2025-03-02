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

system_instructions = [
    "You are a helpful assistant.",
    "You are an expert in Blender, in programming in Python and using Blenders Python module bpy.",
    "If no context is given, assume a context of the 3D software Blender and its python bpy module.",
    "If instructions are given, assume that you have to write a python script for Blender bpy."
    # "Explain step by step.",
    # "Put linebreaks with \n wherever appropriate."
]


test_answer_1 = "\n\nAs an AI language model, I am unable to provide you with specific information on your system configuration. However, I can provide you with the general steps to import the bpy module:\n\n1. Ensure that Blender is installed on your system.\n\n2. Open your Python code file or Python interpreter.\n\n3. Import the bpy module using the following command:\n\n``` python\nimport bpy\n```\n\n4. Now you can use the bpy module functions in your Python code."

test_answer_2 = "Here's a short script that adds a cube at a random location within 1 m of the world origin:\n\n``` python\nimport bpy\nimport random\n\n# Define the range of coordinates\nmin_coord = -1.0\nmax_coord = 1.0\n\n# Generate a random location within the range\nx_loc = random.uniform(min_coord, max_coord)\ny_loc = random.uniform(min_coord, max_coord)\nz_loc = random.uniform(min_coord, max_coord)\n\n# Create a new cube object\nbpy.ops.mesh.primitive_cube_add(location=(x_loc, y_loc, z_loc))\n```\n\nIn this script, we first import the bpy module and the random module. We then define the range of coordinates as -1.0 to 1.0. Next, we generate a random location within this range using the random.uniform() function for each axis (x, y, z). Finally, we create a new cube object using the bpy.ops.mesh.primitive_cube_add() function and set its location to the random coordinates generated earlier."

test_answer_3 = "\n\nAs an AI language model, I don't have the ability to write code, but here's an example of how to add two numbers in JavaScript:\n\n```javascript\nvar num1 = 5;\nvar num2 = 10;\nvar sum = num1 + num2;\n\nconsole.log(sum); // Output: 15\n```"


test_answer_4 = """

You can specify multiple locations for your addon panel by providing a list of tuples in the `bl_category` field of your addon's `bl_info` dictionary. Each tuple represents a location and contains the name of the location and an optional icon:

```
bl_info = {
    "name": "My Addon",
    "category": [("Panel Location 1", "ICON_NAME"), ("Panel Location 2", "ICON_NAME")],
    # other addon metadata...
}
```

You can then define your panel's `draw()` method to conditionally display different UI elements based on the panel's location, using the `self.layout.context` attribute:

```
class MYADDON_PT_MyPanel(bpy.types.Panel):
    bl_idname = "MYADDON_PT_my_panel"
    bl_label = "My Panel"

    def draw(self, context):
        if self.layout.context.category == "Panel Location 1":
            # draw Panel Location 1 UI elements
        elif self.layout.context.category == "Panel Location 2":
            # draw Panel Location 2 UI elements
```

When your addon is installed, you should see your panel displayed in both locations you specified."""
