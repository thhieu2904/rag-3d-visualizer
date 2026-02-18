"""
Blender Script: Gộp file_new.fbx + 3 animation -> Export character.glb
Chạy bằng: blender --background --python convert_to_glb.py
"""
import bpy
import os

# === CẤU HÌNH ===
BASE_DIR = r"d:\Personal\3D_Blender"
BASE_FBX = os.path.join(BASE_DIR, "assets", "pipeline", "file_new.fbx")
ANIM_DIR = os.path.join(BASE_DIR, "assets", "pipeline")
OUTPUT_GLB = os.path.join(BASE_DIR, "public", "models", "character.glb")

# Tất cả animation
ANIMATIONS = {
    "Thankful.fbx": "Thankful",
    "Catwalk Walk Stop Twist R.fbx": "Catwalk",
    "Using A Fax Machine.fbx": "FaxMachine",
    "Standing Up.fbx": "StandingUp",
    "Standing W_Briefcase Idle.fbx": "Idle",
    "Lengthy Head Nod.fbx": "HeadNod",
    "Texting While Standing.fbx": "Texting",
}

# === BƯỚC 1: Xóa scene ===
print("\n🧹 Xóa scene...")
bpy.ops.wm.read_homefile(use_empty=True)

# === BƯỚC 2: Import Base Character ===
print(f"\n📦 Import base: {BASE_FBX}")
bpy.ops.import_scene.fbx(filepath=BASE_FBX)

# Xóa collider objects (rác từ VRM)
colliders = [obj for obj in bpy.context.scene.objects if "collider" in obj.name.lower()]
for obj in colliders:
    bpy.data.objects.remove(obj, do_unlink=True)
print(f"   🗑️ Xóa {len(colliders)} collider objects")

# Tìm Armature chính
base_armature = None
for obj in bpy.context.scene.objects:
    if obj.type == 'ARMATURE':
        base_armature = obj
        break

if not base_armature:
    print("❌ Không tìm thấy Armature!")
    exit(1)

print(f"✅ Armature: {base_armature.name} ({len(base_armature.data.bones)} bones)")

# === BƯỚC 3: Import animations ===
for anim_file, anim_name in ANIMATIONS.items():
    anim_path = os.path.join(ANIM_DIR, anim_file)
    if not os.path.exists(anim_path):
        print(f"⚠️ Bỏ qua: {anim_file}")
        continue

    print(f"\n🎬 Import: {anim_file} -> '{anim_name}'")
    before_objects = set(bpy.context.scene.objects)
    bpy.ops.import_scene.fbx(filepath=anim_path)
    new_objects = set(bpy.context.scene.objects) - before_objects

    new_armature = None
    for obj in new_objects:
        if obj.type == 'ARMATURE':
            new_armature = obj
            break

    if new_armature and new_armature.animation_data and new_armature.animation_data.action:
        action = new_armature.animation_data.action
        action.name = anim_name
        action.use_fake_user = True
        frames = action.frame_range[1] - action.frame_range[0]
        print(f"   ✅ '{anim_name}' ({frames:.0f} frames)")

    for obj in new_objects:
        bpy.data.objects.remove(obj, do_unlink=True)

# === BƯỚC 4: Xóa action rác ===
junk = [a for a in bpy.data.actions if "collider" in a.name.lower() or "Layer0" in a.name]
for a in junk:
    bpy.data.actions.remove(a)
print(f"\n🗑️ Xóa {len(junk)} action rác")

# === BƯỚC 5: Push NLA tracks ===
print("\n📼 Push NLA tracks...")
if not base_armature.animation_data:
    base_armature.animation_data_create()

for track in list(base_armature.animation_data.nla_tracks):
    base_armature.animation_data.nla_tracks.remove(track)

for action in bpy.data.actions:
    if action.use_fake_user:
        track = base_armature.animation_data.nla_tracks.new()
        track.name = action.name
        strip = track.strips.new(action.name, int(action.frame_range[0]), action)
        strip.name = action.name
        print(f"   ✅ {action.name}")

base_armature.animation_data.action = None

# === BƯỚC 6: Export GLB ===
print(f"\n💾 Export: {OUTPUT_GLB}")
bpy.ops.object.select_all(action='SELECT')
os.makedirs(os.path.dirname(OUTPUT_GLB), exist_ok=True)

bpy.ops.export_scene.gltf(
    filepath=OUTPUT_GLB,
    export_format='GLB',
    export_animations=True,
    export_nla_strips=True,
    export_animation_mode='NLA_TRACKS',
    export_texcoords=True,
    export_normals=True,
    export_image_format='JPEG',
    export_image_quality=50,
    export_draco_mesh_compression_enable=True,
    export_draco_mesh_compression_level=6,
)

size_mb = os.path.getsize(OUTPUT_GLB) / 1024 / 1024
print(f"\n🎉 DONE! Size: {size_mb:.1f} MB")
