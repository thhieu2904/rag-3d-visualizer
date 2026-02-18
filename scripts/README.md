# scripts/

Chứa các Blender Python scripts để xây dựng `character.glb` từ VRM + FBX animations.

> Yêu cầu: **Blender 4.2** cài tại `C:\Program Files\Blender Foundation\Blender 4.2\`

---

## convert_to_glb.py

**Mục đích:** Gộp base character FBX + nhiều animation FBX → một file `character.glb` với NLA tracks.

**Chạy:**
```bash
blender --background --python scripts/convert_to_glb.py
```

**Luồng xử lý:**
1. Import `assets/pipeline/file_new.fbx` (xương Mixamo + bind pose)
2. Lần lượt import từng FBX animation trong `assets/pipeline/`
3. Lấy Action từ mỗi FBX, đặt tên ngắn, push vào NLA Tracks
4. Export → `public/models/character.glb`

**Khi nào dùng:** Thêm animation mới hoặc rebuild model từ đầu.

---

## fix_materials_from_vrm.py

**Mục đích:** Khôi phục materials/textures từ VRM gốc vào `character.glb` (fix model bị trắng xóa).

**Chạy:**
```bash
blender --background --python scripts/fix_materials_from_vrm.py
```

**Luồng xử lý:**
1. Import `public/models/character.glb`
2. Import `assets/pipeline/AIC_Female_v1.vrm` (nguồn materials MToon gốc)
3. Transfer 18 material slots từ VRM → GLB meshes (Body, Face, Hair) theo tên
4. Xóa VRM objects, giữ NLA animations
5. Export lại `public/models/character.glb`

**Khi nào dùng:** Luôn chạy **sau** `convert_to_glb.py`.

---

## Thứ tự chạy

```bash
# Bước 1
blender --background --python scripts/convert_to_glb.py

# Bước 2
blender --background --python scripts/fix_materials_from_vrm.py
```
