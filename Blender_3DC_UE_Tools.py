# SPDX-License-Identifier: GPL-2.0-or-later
# testing codespaces right now
import bpy
from bpy.types import bpy_prop_collection
print("test")
print('------------------------------------------------------------------------------------')

class TEST_OT_poll():
    @classmethod
    def poll(cls, context):
        if context.space_data.type == 'NODE_EDITOR' and context.space_data.tree_type == 'ShaderNodeTree':
            return True
        else:
            return False
#----------------------------------------------------------------------
class TEST_OT_del_double_mats(bpy.types.Operator, TEST_OT_poll):
    bl_idname = "node.doublemats"
    bl_label = "3DC_Tools"
    bl_description = "Delete duplicate Materials"
    bl_options = {'REGISTER', 'UNDO'}    
    

    def execute(self, context):
        
        def replace_material(bad_mat, good_mat):
            bad_mat.user_remap(good_mat)
            bpy.data.materials.remove(bad_mat)
            
            
        def get_duplicate_materials(og_material):
            
            common_name = og_material.name
            
            if common_name[-3:].isnumeric():
                common_name = common_name[:-4]
            
            duplicate_materials = []
            
            for material in bpy.data.materials:
                if material is not og_material:
                    name = material.name
                    if name[-3:].isnumeric() and name[-4] == ".":
                        name = name[:-4]
                    
                    if name == common_name:
                        duplicate_materials.append(material)
            
            text = "{} duplicate materials found"
            print(text.format(len(duplicate_materials)))
            
            return duplicate_materials


        def remove_all_duplicate_materials():
            i = 0
            while i < len(bpy.data.materials):
                
                og_material = bpy.data.materials[i]
                
                print("og material: " + og_material.name)
                
                # get duplicate materials
                duplicate_materials = get_duplicate_materials(og_material)
                
                # replace all duplicates
                for duplicate_material in duplicate_materials:
                    replace_material(duplicate_material, og_material)
                
                # adjust name to no trailing numbers
                if og_material.name[-3:].isnumeric() and og_material.name[-4] == ".":
                    og_material.name = og_material.name[:-4]
                    
                i = i+1
            

        remove_all_duplicate_materials()
        bpy.ops.outliner.orphans_purge()       
        
        return {'FINISHED'}
  
#----------------------------------------------------------------------
class TEST_OT_make_group(bpy.types.Operator, TEST_OT_poll):
    bl_idname = "node.3dc_ungroup"
    bl_label = "3DC_Tools"
    bl_description = "Clears 3DCoat group"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        
        print('----------------------------------------------------------------------------------------------')
        getmat = bpy.context.object.active_material.name
        
        node_tree = bpy.data.materials[getmat].node_tree
        node=bpy.data.materials[getmat].node_tree.nodes["3DC_Applink"]
        node.select=True
        node_tree.nodes.active = node
        bpy.ops.node.select_all(action='DESELECT')
        bpy.ops.node.group_ungroup()
        print('Ready.')
        #active_area.type = active_area_type

        return {'FINISHED'}
  
#----------------------------------------------------------------------
class TEST_OT_make_group1(bpy.types.Operator, TEST_OT_poll):
    bl_idname = "node.removal"
    bl_label = "3DC_Tools"
    bl_description = ""
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        
        #Get the material you want (replace the name below)
        getmat = bpy.context.object.active_material.name
        mat = bpy.data.materials[getmat]
        material_name = (getmat)

        #Get the node in its node tree (replace the name below)
        node_to_delete =  mat.node_tree.nodes['3DC_HueSaturation']
        node_to_delete1 =  mat.node_tree.nodes['3DC_HueSaturation.001']
        node_to_delete2 =  mat.node_tree.nodes['3DC_HueSaturation.002']
        node_to_delete3 =  mat.node_tree.nodes['3DC_RGBCurve']
        node_to_delete4 =  mat.node_tree.nodes['3DC_RGBCurve.001']
        node_to_delete5 =  mat.node_tree.nodes['3DC_RGBCurve.002']
        node_to_delete6 =  mat.node_tree.nodes['3DC_ColorRamp']
        node_to_delete7 =  mat.node_tree.nodes['3DC_ColorRamp.001']

        #Remove it
        mat.node_tree.nodes.remove( node_to_delete )
        mat.node_tree.nodes.remove( node_to_delete1 )
        mat.node_tree.nodes.remove( node_to_delete2 )
        mat.node_tree.nodes.remove( node_to_delete3 )
        mat.node_tree.nodes.remove( node_to_delete4 )
        mat.node_tree.nodes.remove( node_to_delete5 )
        mat.node_tree.nodes.remove( node_to_delete6 )
        mat.node_tree.nodes.remove( node_to_delete7 )

        print('Remove Done.')
        
        
        return {'FINISHED'}

#----------------------------------------------------------------------
class TEST_OT_make_group2(bpy.types.Operator, TEST_OT_poll):
    bl_idname = "node.3dc_reroute"
    bl_label = "3DC_Tools"
    bl_description = "Connect to Unreal_FBX"
    bl_options = {'REGISTER', 'UNDO'}
    

    def execute(self, context):
        
        getmat = bpy.context.object.active_material.name
        mat = bpy.data.materials[getmat]
        material_name = (getmat)
        
        # Create a material
        mts = bpy.data.materials.get(material_name)
        mts.use_nodes = True

        nodes = mts.node_tree.nodes
        links = mts.node_tree.links

        def reconnect(fname):
  
            texture_list = []

            for obj in bpy.context.selected_objects:
                for s in obj.material_slots:
                    if s.material and s.material.use_nodes:
                        for n in s.material.node_tree.nodes:
                            if n.type == 'TEX_IMAGE':
                                texture_list += [n.image]
                                # print(obj.name,'uses',n.image.name,'saved at',n.image.filepath)
                    
                    
                                if n.image.name.endswith(fname):       #If Imagename endswith
                                    dodo=n.image.name                  #Name of Image
                                    dofdof=n.image                     #Image in Memory
                                    goz=n                              #the Image_Node
                                    print(dodo)                        #print image name
                                    return goz
        #print(texture_list)

        # GET Principled BSDF and the Material Output node of Material
        #principled_bsdf = nodes.get("Principled BSDF")
        principled_bsdf = bpy.data.materials[getmat].node_tree.nodes["Principled BSDF"]
        print(principled_bsdf)

        gol=reconnect('diffuse.png')
        links.new(principled_bsdf.inputs["Base Color"], gol.outputs["Color"])
        gol=reconnect('metalness.png')
        links.new(principled_bsdf.inputs["Metallic"], gol.outputs["Color"])
        gol=reconnect('roughness.png')
        links.new(principled_bsdf.inputs["Roughness"], gol.outputs["Color"])

        #----------------------------------------------------------------------------
        links.remove(principled_bsdf.inputs["Metallic"].links[0])
        links.remove(principled_bsdf.inputs["Roughness"].links[0])

        gol=reconnect('metalness.png')
        links.new(principled_bsdf.inputs["Roughness"], gol.outputs["Color"])
        gol=reconnect('roughness.png')
        links.new(principled_bsdf.inputs["Specular"], gol.outputs["Color"])

        
        return {'FINISHED'}
  

#-------------------------------------------------------------------------------------------------------      
class TEST_PT_panel(bpy.types.Panel):
    bl_idname = "TEST_PT_panel"
    bl_label = "3DCoat Tools"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = "UI"
    bl_category = "Tool"

    @classmethod  
    def poll(cls, context):                                           # What is Polling?
        if context.space_data.tree_type == 'ShaderNodeTree':
            return True
        else:
            return False
#--------------------------------------------------------------------------------------------------
    def draw(self, context):
        
        layout = self.layout
        column = layout.column()
        column.operator("node.doublemats", text = "Delete duplicate Mats") #Buttons drawing
        column.operator("node.3dc_ungroup", text = "Ungroup")
        column.operator("node.removal", text = "Remove 3DCoat Nodes")
        column.operator("node.3dc_reroute", text = "Reroute to Unreal")
#----------------------------------------------------------------------        
# Register------------------------------------------------------------
classes = (              
    TEST_PT_panel,
    TEST_OT_del_double_mats,
    TEST_OT_make_group,
    TEST_OT_make_group1,
    TEST_OT_make_group2,
)

#-----------------------------------------------------------------------
def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
        
        
if __name__ == "__main__":
    register()
