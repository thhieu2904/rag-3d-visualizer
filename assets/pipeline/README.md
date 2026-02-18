# assets/pipeline/

Chứa toàn bộ raw assets của pipeline 3D — từ model gốc VRoid đến các file animation Mixamo.

> Các file này **không được serve** lên web. Chỉ dùng trong quá trình build bằng script Blender.
> Output cuối cùng là `public/models/character.glb`.

---

## Model gốc

| File | Mô tả |
|---|---|
| `AIC_Female_v1.vrm` | Model nhân vật gốc từ **VRoid Studio**. Chứa toàn bộ textures MToon (skin, cloth, hair, eyes). Đây là nguồn materials để `fix_materials_from_vrm.py` restore lại màu sắc. |
| `upload_Mixamo.fbx` | FBX export từ VRM (T-pose), dùng để **upload lên Mixamo** để auto-rig. Không có materials. |
| `file_new.fbx` | FBX tải về từ Mixamo sau khi auto-rig thành công. Chứa xương Mixamo chuẩn + bind pose. Đây là base character cho `convert_to_glb.py`. |

---

## Animation FBX (tải từ Mixamo — Without Skin)

| File | Tên animation | Mô tả |
|---|---|---|
| `Catwalk Walk Stop Twist R.fbx` | `Catwalk` | Đi catwalk, dừng, xoay |
| `Using A Fax Machine.fbx` | `FaxMachine` | Dùng máy fax |
| `Lengthy Head Nod.fbx` | `HeadNod` | Gật đầu dài |
| `Standing W_Briefcase Idle.fbx` | `Idle` | Đứng idle cầm cặp |
| `Standing Up.fbx` | `StandingUp` | Đứng dậy từ ghế |
| `Texting While Standing.fbx` | `Texting` | Nhắn tin khi đứng |
| `Thankful.fbx` | `Thankful` | Cảm ơn / cúi chào |

---

## Thêm animation mới

1. Vào [mixamo.com](https://mixamo.com), chọn animation
2. Tải về: **Format FBX**, **Skin: Without Skin**, **30 FPS**
3. Đặt file `.fbx` vào thư mục này
4. Mở `scripts/convert_to_glb.py`, thêm vào dict `ANIMATIONS`:
   ```python
   "TenFile.fbx": "TenHienThiTrenWeb",
   ```
5. Chạy lại pipeline:
   ```bash
   blender --background --python scripts/convert_to_glb.py
   blender --background --python scripts/fix_materials_from_vrm.py
   ```
