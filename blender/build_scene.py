"""Build the Mist presentation scene: a dark room, the Halo still projected on the
back wall as an emissive screen, and a rigged placeholder presenter standing in
its light. Run with:  Blender --background --python build_scene.py

Optional: put a rigged human at blender/models/presenter.glb (or .fbx) and it
is imported in place of the capsule mannequin.
"""
import bpy, math, os, glob
from mathutils import Vector, Matrix

HERE = os.path.dirname(os.path.abspath(__file__))
STILL = os.path.abspath(os.path.join(HERE, "..", "stills", "halo-speaking.png"))
OUT = os.path.join(HERE, "mist-presentation.blend")
HUMAN = (glob.glob(os.path.join(HERE, "models", "presenter.*")) + [None])[0]

# ---------------------------------------------------------------- reset
bpy.ops.wm.read_factory_settings(use_empty=True)
scene = bpy.context.scene
scene.name = "Mist Presentation"

def mat(name, color=(0.02, 0.02, 0.022), rough=0.6, spec=0.5):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (*color, 1)
    bsdf.inputs["Roughness"].default_value = rough
    if "Specular IOR Level" in bsdf.inputs:
        bsdf.inputs["Specular IOR Level"].default_value = spec
    return m

def box(name, size, loc, material, rot=(0, 0, 0)):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object; o.name = name; o.scale = size
    o.data.materials.append(material)
    return o

# ---------------------------------------------------------------- room
SCREEN_W, SCREEN_H = 16.0, 9.0         # 16:9, meters (keynote LED wall)
STAGE_H = 0.9
SCREEN_Z0 = STAGE_H                    # the LED wall stands on the stage
WALL_Y = 0.0                           # back wall plane
ROOM_W, ROOM_D, ROOM_H = 32, 34, 15

dark = mat("Room Dark", (0.05, 0.05, 0.052), rough=0.9, spec=0.2)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -ROOM_D / 2, 0))
floor = bpy.context.object; floor.name = "Floor"; floor.scale = (ROOM_W, ROOM_D, 1)
floor.data.materials.append(mat("Floor", (0.03, 0.03, 0.032), rough=0.32, spec=0.6))
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, WALL_Y, ROOM_H / 2), rotation=(math.pi / 2, 0, 0))
wall = bpy.context.object; wall.name = "Back Wall"; wall.scale = (ROOM_W, ROOM_H, 1); wall.data.materials.append(dark)
for sx, nm in ((-1, "Left Wall"), (1, "Right Wall")):
    bpy.ops.mesh.primitive_plane_add(size=1, location=(sx * ROOM_W / 2, -ROOM_D / 2, ROOM_H / 2), rotation=(math.pi / 2, 0, math.pi / 2))
    o = bpy.context.object; o.name = nm; o.scale = (ROOM_D, ROOM_H, 1); o.data.materials.append(dark)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, -ROOM_D / 2, ROOM_H), rotation=(math.pi, 0, 0))
ceil = bpy.context.object; ceil.name = "Ceiling"; ceil.scale = (ROOM_W, ROOM_D, 1); ceil.data.materials.append(dark)

# a low stage riser and a lectern so the space reads as a presentation room
stage_mat = mat("Stage", (0.02, 0.02, 0.022), rough=0.5, spec=0.5)
box("Stage Riser", (24, 7.5, STAGE_H), (0, -3.75, STAGE_H / 2), stage_mat)
lectern = mat("Lectern", (0.06, 0.06, 0.065), rough=0.4, spec=0.6)
box("Lectern Body", (0.55, 0.45, 1.05), (7.5, -4.2, STAGE_H + 0.525), lectern)
box("Lectern Top", (0.62, 0.5, 0.04), (7.5, -4.2, STAGE_H + 1.07), lectern, rot=(math.radians(12), 0, 0))
# a few rows of audience chairs, silhouettes only
chair = mat("Chair", (0.04, 0.04, 0.045), rough=0.7, spec=0.3)
for row in range(8):
    for i in range(18):
        x = -10.2 + i * 1.2 + (0.6 if row % 2 else 0); y = -10.5 - row * 1.4
        box(f"Chair {row}-{i} seat", (0.5, 0.5, 0.06), (x, y, 0.45), chair)
        box(f"Chair {row}-{i} back", (0.5, 0.06, 0.5), (x, y + 0.22, 0.72), chair)

# ---------------------------------------------------------------- screen (projected image)
bpy.ops.mesh.primitive_plane_add(size=1, location=(0, WALL_Y - 0.01, SCREEN_Z0 + SCREEN_H / 2), rotation=(math.pi / 2, 0, 0))
screen = bpy.context.object; screen.name = "Screen"; screen.scale = (SCREEN_W, SCREEN_H, 1)
sm = bpy.data.materials.new("Screen Emission"); sm.use_nodes = True
nt = sm.node_tree; nt.nodes.clear()
out = nt.nodes.new("ShaderNodeOutputMaterial")
emit = nt.nodes.new("ShaderNodeEmission")
tex = nt.nodes.new("ShaderNodeTexImage")
img = bpy.data.images.load(STILL); img.name = "mist-halo-speaking"
tex.image = img; tex.interpolation = "Closest"       # keep the pixels crisp
emit.inputs["Strength"].default_value = 22.0          # the screen is the room's key light
nt.links.new(tex.outputs["Color"], emit.inputs["Color"])
nt.links.new(emit.outputs["Emission"], out.inputs["Surface"])
screen.data.materials.append(sm)
img.pack()

# the projected image is mostly black, so this area light stands in for the projector's wash on the presenter
bpy.ops.object.light_add(type="AREA", location=(0, -0.6, SCREEN_Z0 + SCREEN_H / 2), rotation=(math.pi / 2, 0, 0))
fill = bpy.context.object; fill.name = "Screen Fill"
fill.data.shape = "RECTANGLE"; fill.data.size = SCREEN_W; fill.data.size_y = SCREEN_H
fill.data.energy = 2600; fill.data.color = (0.8, 0.85, 1.0); fill.data.spread = math.radians(90)

# dim warm stage spot from behind the audience so the presenter isn't pure silhouette
bpy.ops.object.light_add(type="SPOT", location=(-6, -20, 9))
spot = bpy.context.object; spot.name = "Stage Spot"
spot.data.energy = 6000; spot.data.color = (1.0, 0.86, 0.7); spot.data.spot_size = math.radians(26); spot.data.spot_blend = 0.6
spot.data.shadow_soft_size = 0.6
PRESENTER_AT = Vector((3.5, -3.0, STAGE_H))
spot.rotation_euler = (PRESENTER_AT + Vector((0, 0, 1.1)) - spot.location).to_track_quat("-Z", "Y").to_euler()

# ---------------------------------------------------------------- presenter
pres_col = bpy.data.collections.new("Presenter"); scene.collection.children.link(pres_col)
parts = []
skin_mat = mat("Presenter", (0.32, 0.32, 0.34), rough=0.7, spec=0.35)

if HUMAN:
    # user-supplied rigged human (glTF/FBX): import, scale to ~1.8 m, place on stage facing the screen
    before = set(bpy.data.objects)
    if HUMAN.lower().endswith((".glb", ".gltf")): bpy.ops.import_scene.gltf(filepath=HUMAN)
    else: bpy.ops.import_scene.fbx(filepath=HUMAN)
    new = [o for o in bpy.data.objects if o not in before]
    roots = [o for o in new if o.parent is None]
    for o in new:
        for c in o.users_collection: c.objects.unlink(o)
        pres_col.objects.link(o)
        if o.type == "MESH": parts.append(o)
    zs = [(o.matrix_world @ Vector(c)).z for o in new if o.type == "MESH" for c in o.bound_box]
    h = (max(zs) - min(zs)) or 1
    for r in roots:
        r.scale = r.scale * (1.8 / h)
        r.location = PRESENTER_AT
        r.rotation_euler = (r.rotation_euler.x, r.rotation_euler.y, math.radians(-135))
else:
    # capsule mannequin: one capsule per bone, each parented to its bone, so the
    # figure poses with the rig and every limb stays readable
    bpy.ops.preferences.addon_enable(module="rigify")
    bpy.ops.object.armature_human_metarig_add()
    rig = bpy.context.object; rig.name = "Presenter Rig"
    rig.location = PRESENTER_AT
    rig.rotation_euler = (0, 0, math.radians(-135))     # front toward the screen, three-quarter to the camera
    bpy.context.view_layer.update()
    KEEP = ("spine", "shoulder", "upper_arm", "forearm", "hand", "thigh", "shin", "foot", "toe")
    bones = [b for b in rig.data.bones if b.name.split(".")[0] in KEEP and not b.name.startswith("face")]
    RADIUS = {"spine": 0.11, "spine.001": 0.115, "spine.002": 0.12, "spine.003": 0.125, "spine.004": 0.05, "spine.005": 0.05,
              "shoulder": 0.045, "upper_arm": 0.05, "forearm": 0.042, "hand": 0.035, "thigh": 0.075, "shin": 0.058, "foot": 0.04, "toe": 0.03}
    def part(obj, bone):
        obj.data.materials.append(skin_mat)
        for c in obj.users_collection: c.objects.unlink(obj)
        pres_col.objects.link(obj)
        # bone parenting: the parent frame sits at the bone tail, so bake the rest-pose offset
        parent_mat = rig.matrix_world @ bone.matrix_local @ Matrix.Translation((0, bone.length, 0))
        obj.parent = rig; obj.parent_type = "BONE"; obj.parent_bone = bone.name
        obj.matrix_parent_inverse = parent_mat.inverted()
        parts.append(obj)
    for b in bones:
        base = b.name.split(".")[0]
        r = RADIUS.get(b.name, RADIUS.get(base, 0.05))
        head, tail = rig.matrix_world @ b.head_local, rig.matrix_world @ b.tail_local
        if b.name == "spine.006":                                   # head: one ellipsoid
            bpy.ops.mesh.primitive_uv_sphere_add(radius=1, location=(head + tail) / 2 + Vector((0, 0, 0.02)), segments=32, ring_count=16)
            o = bpy.context.object; o.name = "Presenter Head"; o.scale = (0.095, 0.115, 0.125)
            o.rotation_euler = rig.rotation_euler
            bpy.ops.object.shade_smooth(); part(o, b); continue
        d = tail - head
        bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=d.length, location=(head + tail) / 2, vertices=24)
        o = bpy.context.object; o.name = f"Presenter {b.name}"; o.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
        bpy.ops.object.shade_smooth(); part(o, b)
        for j, p in ((0, head), (1, tail)):                         # rounded joints
            bpy.ops.mesh.primitive_uv_sphere_add(radius=r * 1.02, location=p, segments=24, ring_count=12)
            o = bpy.context.object; o.name = f"Presenter {b.name} joint{j}"
            bpy.ops.object.shade_smooth(); part(o, b)
    # pose: right arm gestures toward the screen, left arm relaxed, slight head turn
    pb = rig.pose.bones
    def rot(name, x=0, y=0, z=0):
        if name in pb:
            pb[name].rotation_mode = "XYZ"
            pb[name].rotation_euler = (math.radians(x), math.radians(y), math.radians(z))
    rot("upper_arm.R", x=-75, z=-30)
    rot("forearm.R", x=25)
    rot("upper_arm.L", x=12, z=22)
    rot("forearm.L", x=35)
    rot("spine.004", z=-10)   # neck
    rot("spine.006", z=-15)   # head
    rot("thigh.L", z=6)
    rot("thigh.R", z=-6)

# light linking: the stand-in wash hits the presenter, stage and floor only (the wall stays dark like a real projection)
lit = bpy.data.collections.new("Lit by Screen"); scene.collection.children.link(lit)
for o in parts + [floor, bpy.data.objects["Stage Riser"], bpy.data.objects["Lectern Body"], bpy.data.objects["Lectern Top"]]:
    lit.objects.link(o)
if hasattr(fill, "light_linking"):
    fill.light_linking.receiver_collection = lit

# ---------------------------------------------------------------- camera
bpy.ops.object.camera_add(location=(-9, -19, 2.2), rotation=(math.radians(88), 0, math.radians(-28)))
cam = bpy.context.object; cam.name = "Audience Camera"
cam.data.lens = 28; cam.data.sensor_width = 36
scene.camera = cam

# ---------------------------------------------------------------- world + render
world = bpy.data.worlds.new("Dark Room"); scene.world = world
world.use_nodes = True
bg = world.node_tree.nodes["Background"]
bg.inputs["Color"].default_value = (0.012, 0.013, 0.02, 1); bg.inputs["Strength"].default_value = 1

scene.render.engine = "CYCLES"
scene.cycles.samples = 256
scene.cycles.use_denoising = True
scene.render.resolution_x = 1920; scene.render.resolution_y = 1080
scene.view_settings.view_transform = "AgX"
scene.view_settings.look = "AgX - Medium High Contrast"
scene.render.filepath = os.path.join(HERE, "renders", "mist-presentation.png")

for area in bpy.context.screen.areas if bpy.context.screen else []:
    if area.type == "VIEW_3D":
        for sp in area.spaces:
            if sp.type == "VIEW_3D":
                sp.shading.type = "RENDERED"; sp.region_3d.view_perspective = "CAMERA"

bpy.ops.wm.save_as_mainfile(filepath=OUT)
print("SAVED", OUT, "human:", HUMAN, "objects:", len(scene.objects))
