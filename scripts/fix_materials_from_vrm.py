"""
Blender Script: Khôi phục materials/textures từ VRM gốc vào character.glb

Vấn đề: FBX export từ VRM → Mixamo không giữ materials → character.glb bị trắng xóa
Giải pháp: Import VRM gốc, lấy materials, transfer vào character.glb, export lại

Chạy: blender --background --python fix_materials_from_vrm.py
"""

import bpy
import os

# ============================================================
# CẤU HÌNH - chỉnh đường dẫn nếu cần
# ============================================================
BASE_DIR      = r"d:\Personal\3D_Blender"
VRM_FILE      = os.path.join(BASE_DIR, "assets", "pipeline", "AIC_Female_v1.vrm")
GLB_INPUT     = os.path.join(BASE_DIR, "public", "models", "character.glb")
GLB_OUTPUT    = os.path.join(BASE_DIR, "public", "models", "character.glb")   # ghi đè
# ============================================================

def log(msg): print(msg, flush=True)

# ----------------------------------------------------------
# Bước 0: Reset scene
# ----------------------------------------------------------
log("\n🧹 Reset scene...")
bpy.ops.wm.read_homefile(use_empty=True)

# ----------------------------------------------------------
# Bước 1: Import character.glb (armature + animations)
# ----------------------------------------------------------
log(f"\n📦 Import GLB: {GLB_INPUT}")
bpy.ops.import_scene.gltf(filepath=GLB_INPUT)

glb_meshes    = [o for o in bpy.context.scene.objects if o.type == 'MESH']
glb_armatures = [o for o in bpy.context.scene.objects if o.type == 'ARMATURE']
log(f"   GLB meshes   : {[o.name for o in glb_meshes]}")
log(f"   GLB armatures: {[o.name for o in glb_armatures]}")

# Lưu lại đối tượng GLB để sau còn phân biệt
glb_objects = set(bpy.context.scene.objects)

# ----------------------------------------------------------
# Bước 2: Import VRM (dưới dạng GLTF vì VRM = GLTF + ext)
# ----------------------------------------------------------
log(f"\n🎨 Import VRM: {VRM_FILE}")
try:
    bpy.ops.import_scene.gltf(filepath=VRM_FILE)
    vrm_imported_ok = True
except Exception as e:
    log(f"   ⚠️  GLTF importer lỗi: {e}")
    vrm_imported_ok = False

vrm_objects = set(bpy.context.scene.objects) - glb_objects
vrm_meshes  = [o for o in vrm_objects if o.type == 'MESH']
log(f"   VRM meshes: {[o.name for o in vrm_meshes]}")

# ----------------------------------------------------------
# Bước 3: Xây dựng bảng materials từ VRM (key = tên material)
# ----------------------------------------------------------
vrm_material_map = {}   # { mat_name_lower : material_object }
for mesh_obj in vrm_meshes:
    for slot in mesh_obj.material_slots:
        if slot.material:
            key = slot.material.name.lower()
            vrm_material_map[key] = slot.material
            log(f"   📌 VRM mat: {slot.material.name}")

log(f"\n   Tổng {len(vrm_material_map)} materials từ VRM")

# ----------------------------------------------------------
# Bước 4: Assign materials VRM → GLB mesh slots
# ----------------------------------------------------------
log("\n🔗 Transfer materials...")

assigned = 0
for glb_mesh in glb_meshes:
    log(f"\n   Mesh: '{glb_mesh.name}'  ({len(glb_mesh.material_slots)} slots)")
    for slot in glb_mesh.material_slots:
        if not slot.material:
            continue
        old_name = slot.material.name
        old_key  = old_name.lower()

        # Tìm material VRM phù hợp nhất
        matched = None

        # 1) Khớp chính xác
        if old_key in vrm_material_map:
            matched = vrm_material_map[old_key]

        # 2) Khớp một phần (GLB mat name nằm trong VRM mat name hoặc ngược lại)
        if not matched:
            for vkey, vmat in vrm_material_map.items():
                if old_key in vkey or vkey in old_key:
                    matched = vmat
                    break

        # 3) Fuzzy: so sánh token chung
        if not matched:
            old_tokens = set(old_key.replace("_", " ").replace(".", " ").split())
            best_score = 0
            best_mat   = None
            for vkey, vmat in vrm_material_map.items():
                v_tokens = set(vkey.replace("_", " ").replace(".", " ").split())
                score = len(old_tokens & v_tokens)
                if score > best_score and score >= 1:
                    best_score = score
                    best_mat   = vmat
            if best_mat:
                matched = best_mat

        if matched:
            slot.material = matched
            log(f"      ✅  '{old_name}'  →  '{matched.name}'")
            assigned += 1
        else:
            log(f"      ❌  '{old_name}'  — không tìm được VRM mat tương ứng")

log(f"\n   Tổng assigned: {assigned} slots")

# ----------------------------------------------------------
# Bước 5: Xóa VRM objects (mesh + armature từ VRM không cần nữa)
# ----------------------------------------------------------
log("\n🗑️  Xóa VRM objects...")
for obj in list(vrm_objects):
    try:
        bpy.data.objects.remove(obj, do_unlink=True)
    except:
        pass

# Dọn mesh/armature data không dùng
for mesh in list(bpy.data.meshes):
    if mesh.users == 0:
        bpy.data.meshes.remove(mesh)

# ----------------------------------------------------------
# Bước 6: Verify NLA animations vẫn còn nguyên
# ----------------------------------------------------------
log("\n🎬 Kiểm tra animations...")
for arm in glb_armatures:
    if arm.animation_data:
        tracks = arm.animation_data.nla_tracks
        log(f"   Armature '{arm.name}': {len(tracks)} NLA tracks")
        for t in tracks:
            log(f"      - {t.name}")
    else:
        log(f"   ⚠️  '{arm.name}' không có animation_data")

# ----------------------------------------------------------
# Bước 7: Export GLB với materials + animations
# ----------------------------------------------------------
log(f"\n💾 Export: {GLB_OUTPUT}")
os.makedirs(os.path.dirname(GLB_OUTPUT), exist_ok=True)

bpy.ops.object.select_all(action='SELECT')

bpy.ops.export_scene.gltf(
    filepath=GLB_OUTPUT,
    export_format='GLB',
    # Textures & materials
    export_image_format='JPEG',
    export_image_quality=85,
    export_texcoords=True,
    export_normals=True,
    export_materials='EXPORT',
    # Animations
    export_animations=True,
    export_nla_strips=True,
    export_animation_mode='NLA_TRACKS',
    # Compression (bỏ draco để tránh lỗi ở một số viewer)
    export_draco_mesh_compression_enable=False,
)

size_mb = os.path.getsize(GLB_OUTPUT) / 1024 / 1024
log(f"\n🎉 DONE!  Output: {GLB_OUTPUT}  ({size_mb:.1f} MB)")
log("   Model bây giờ nên có đầy đủ màu sắc/textures rồi nhé!")
