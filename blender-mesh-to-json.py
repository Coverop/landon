# The goal of this addon is to export all of the actions for the active
# armature into a JSON file

bl_info = {
    "name": "Export Mesh to JSON",
    "category": "Import-Export"
}

import bpy
import json
# import sys

# Write our JSON to stdout by default or to a file if specified.
# Stdout mesh JSON is wrapped in a start and end indicators
# to more easily distinguish it from other Blender output.
#
# START_MESH_JSON $BLENDER_FILEPATH $MESH_NAME
# ... mesh json ...
# END_MESH_JSON $BLENDER_FILEPATH $MESH_NAME
class MeshToJSON(bpy.types.Operator):
    """Given an active armature, export it's actions and keyframed bone pose information to a JSON file"""
    # Unique identifier for the addon
    bl_idname = 'import_export.mesh2json'
    # Display name in the interface
    bl_label = 'Export Mesh to JSON'
    bl_options = {'REGISTER'}
    bl_category = 'Import-Export'

    # The filepath to write out JSON to
    # filepath = bpy.props.StringProperty(name='filepath')

    def execute(self, context):
        mesh = bpy.context.active_object
        mesh_json = {
            'vertex_positions': [],
            'num_vertices_in_each_face': [],
            'vertex_position_indices': [],
            'vertex_normals': [],
            'vertex_normal_indices': [],
            'armature_name': None,
        }

        # TODO: Handle triangular polygons, not just quads
        # cube.data.polygons[1].vertices[0]. Check if length
        # of face is 4... Use a triangular face in Blender to unit test.
        index = 0
        for face in mesh.data.polygons:
            num_vertices_in_face = len(face.vertices)
            mesh_json['num_vertices_in_each_face'].append(num_vertices_in_face)

            for i in range(num_vertices_in_face):
                mesh_json['vertex_position_indices'].append(face.vertices[i])
                # TODO: Maintain a dictionary with (x, y, z) => normal index
                # for normals that we've already run into.
                # Re-use an existing normal index wherever possible. Especially important
                # for smoothed models that mostly re-use the same normals. Test this by
                # making a cube with to faces that have the same normal
                mesh_json['vertex_normal_indices'].append(index)

            # TODO: Don't append normals if we've already encountered them
            mesh_json['vertex_normals'].append(face.normal.x)
            mesh_json['vertex_normals'].append(face.normal.y)
            mesh_json['vertex_normals'].append(face.normal.z)
            index += 1

        # TODO: Breadcrumb - iterate over the vertices and add them to mesh_json
        # TODO: Option for # of decimal places to round positions / normals / etc to.
        # Potentially just one option or a separate option for each
        for vert in mesh.data.vertices:
            mesh_json['vertex_positions'].append(vert.co.x)
            mesh_json['vertex_positions'].append(vert.co.y)
            mesh_json['vertex_positions'].append(vert.co.z)

        # TODO: Add unit test for no mesh currently selected
        # if mesh == None or mesh.type != 'MESH':
        #     print("__NO_MESH_SELECTED__", file=sys.stderr)
        #     return {'FINISHED'}

        # Iterate over all of the polygons and get the face data

        print("START_MESH_JSON " + bpy.data.filepath + " " + mesh.name)
        print(json.dumps(mesh_json))
        print("END_MESH_JSON " + bpy.data.filepath + " " + mesh.name)
# START_EXPORT_MESH $BLENDER_FILEPATH $MESH_NAME
# ... mesh json ...
# FINISH_EXPORT_MESH $BLENDER_FILEPATH $MESH_NAME

        return {'FINISHED'}

def register():
    bpy.utils.register_class(MeshToJSON)

def unregister():
    bpy.utils.unregister_class(MeshToJSON)

if __name__ == "__main__":
    register()

# >>> list(o.data.vertices[62].groups)[1].weight
# 0.32011678814888

# >>> list(o.data.vertices[62].groups)[1].group
# 6

# >>> list(o.data.vertices[62].groups)[0].group
# 5

# >>> o.vertex_groups
# bpy.data.objects['temp-player-full-body'].vertex_groups

# >>> o.vertex_groups[5]
# bpy.data.objects['temp-player-full-body']...VertexGroup

# >>> o.vertex_groups[5].name
# 'Lower.Arm.L'

# >>> o.vertex_groups[6].name
# 'Hand.L'
