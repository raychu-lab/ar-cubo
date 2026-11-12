"""Generate cube.glb: a 20 cm low-poly cube with soft rounded edges and a glowing gradient.

Run from this folder (Blender on macOS is not on PATH):
    /Applications/Blender.app/Contents/MacOS/Blender --background --python make_cube.py

How the look works (so it survives glTF, three.js and iPhone Quick Look alike):
- The cube is bevelled, so its edges are thin slanted faces.
- A tiny 64x64 texture holds two vertical gradients: the left half is the face colour,
  the right half a lighter "glow" version used only on the bevelled edges.
- Every face corner gets a UV: u picks face or edge column, v = height in the cube,
  so the gradient runs bottom -> top on every side.
- The same texture is used as emission (at low strength), so the cube never goes
  black in a dark room and its edges read as softly lit.

To use your own model instead: export any mesh as GLB (units in metres, origin at
its centre) and replace cube.glb, or change MODEL_URL in index.html.
"""
from pathlib import Path

import bpy

SIZE = 0.20          # cube edge length in metres (20 cm)
BEVEL = 0.025        # rounded edge width in metres
TEX = 64             # texture resolution (tiny on purpose)
BOTTOM = (0.36, 0.25, 0.85)   # violet (sRGB 0..1)
TOP = (0.25, 0.88, 0.82)      # mint cyan
GLOW = 0.45          # how far the edge colour is pushed toward white
EMISSION = 0.45      # emission strength (0 = no glow)
OUT = Path(__file__).resolve().parent / "cube.glb"


def lerp(a, b, t):
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def make_texture():
    """Left half: face gradient. Right half: lighter edge gradient."""
    image = bpy.data.images.new("cube_gradient", TEX, TEX, alpha=False)
    pixels = []
    for row in range(TEX):                      # row 0 is the bottom of the image
        t = row / (TEX - 1)
        face = lerp(BOTTOM, TOP, t)
        edge = lerp(face, (1.0, 1.0, 1.0), GLOW)
        for col in range(TEX):
            pixels += [*(face if col < TEX // 2 else edge), 1.0]
    image.pixels = pixels
    image.pack()                                # keep it inside the .blend / export
    return image


def make_material(image):
    mat = bpy.data.materials.new("cube_mat")
    mat.use_nodes = True
    nodes, links = mat.node_tree.nodes, mat.node_tree.links
    bsdf = nodes["Principled BSDF"]
    tex = nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = "Linear"
    links.new(tex.outputs["Color"], bsdf.inputs["Base Color"])
    links.new(tex.outputs["Color"], bsdf.inputs["Emission Color"])
    bsdf.inputs["Emission Strength"].default_value = EMISSION
    bsdf.inputs["Roughness"].default_value = 0.55
    bsdf.inputs["Metallic"].default_value = 0.0
    return mat


def make_cube(mat):
    bpy.ops.mesh.primitive_cube_add(size=SIZE)
    cube = bpy.context.active_object
    cube.name = "cube"
    bevel = cube.modifiers.new("bevel", "BEVEL")
    bevel.width = BEVEL
    bevel.segments = 2          # low-poly but still rounded
    bpy.ops.object.modifier_apply(modifier=bevel.name)
    bpy.ops.object.shade_smooth()

    mesh = cube.data
    mesh.materials.append(mat)
    uv = mesh.uv_layers.active.data
    half = SIZE / 2
    for poly in mesh.polygons:
        is_edge = max(abs(c) for c in poly.normal) < 0.99   # slanted = bevel face
        u = 0.80 if is_edge else 0.20
        for loop in poly.loop_indices:
            z = mesh.vertices[mesh.loops[loop].vertex_index].co.z
            v = min(max((z + half) / SIZE, 0.02), 0.98)
            uv[loop].uv = (u, v)
    return cube


def main():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    cube = make_cube(make_material(make_texture()))
    bpy.ops.object.select_all(action="DESELECT")
    cube.select_set(True)
    bpy.ops.export_scene.gltf(
        filepath=str(OUT),
        export_format="GLB",
        use_selection=True,
        export_yup=True,         # glTF / three.js convention
        export_apply=True,
    )
    print(f"CUBE_OK {OUT} {OUT.stat().st_size / 1024:.1f} KB, {len(cube.data.polygons)} faces")


if __name__ == "__main__":
    main()
