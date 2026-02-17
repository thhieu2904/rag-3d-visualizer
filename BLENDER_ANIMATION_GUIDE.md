# 🎬 Hướng Dẫn Nhanh: Tạo Animations trong Blender

## ⚠️ Vấn Đề Hiện Tại
Model `test.glb` của bạn **KHÔNG CÓ ANIMATIONS** → Cần tạo trong Blender.

---

## 📋 Các Bước Cơ Bản

### 1️⃣ Mở File GLB trong Blender
```
1. Mở Blender
2. File → Import → glTF 2.0 (.glb/.gltf)
3. Chọn file test.glb → Import
```

### 2️⃣ Chuyển Sang Animation Workspace
- **Top menu** → Click **Animation**
- Hoặc chọn **Dope Sheet** editor type

### 3️⃣ Tạo Action Đầu Tiên: "Idle"

**Bước 1: Tạo Action**
```
1. Trong Dope Sheet, chọn mode: Action Editor (dropdown)
2. Bấm nút "+" (New Action)
3. ĐẶT TÊN: "Idle"
```

**Bước 2: Tạo Keyframes**
```
Frame 1:
  - Chọn model trong 3D Viewport
  - Bấm phím I → chọn "Location"
  
Frame 30:
  - Kéo timeline đến frame 30
  - Di chuyển model lên 0.1m (bấm G → Z → 0.1 → Enter)
  - Bấm I → Location
  
Frame 60:
  - Kéo đến frame 60
  - Di chuyển về vị trí ban đầu (G → Z → -0.1 → Enter)
  - Bấm I → Location
```

**Test Animation:**
- Bấm **Space** → Xem animation chạy

### 4️⃣ Tạo Action Thứ 2: "Talking"

```
1. Trong Action Editor, bấm "+" → Tạo Action mới
2. Đặt tên: "Talking"
3. Tạo keyframes xoay đầu hoặc mở miệng (nếu có rigging)

Ví dụ đơn giản:
Frame 1:   I → Rotation
Frame 15:  Xoay model (R → Z → 10 → Enter) → I → Rotation
Frame 30:  Xoay ngược lại (R → Z → -10 → Enter) → I → Rotation
Frame 45:  Về vị trí ban đầu → I → Rotation
```

### 5️⃣ Tạo Action Thứ 3: "Waving"

```
1. Action Editor → "+" → Tên: "Waving"
2. Tạo animation vẫy tay

Ví dụ:
Frame 1:   I → Rotation
Frame 20:  Xoay model sang phải (R → Z → 45 → Enter) → I → Rotation
Frame 40:  Xoay về giữa → I → Rotation
Frame 60:  Xoay sang trái (R → Z → -45 → Enter) → I → Rotation
Frame 80:  Về vị trí ban đầu → I → Rotation
```

---

## 💾 Export GLB với Animations

### ⚠️ CỰC KỲ QUAN TRỌNG

```
1. File → Export → glTF 2.0 (.glb)

2. BÊN PHẢI cửa sổ Export, tìm mục "Animation":
   ✅ CHECK "Animation" checkbox
   ✅ Animation Mode: "Actions" hoặc "NLA Tracks"
   ✅ Always Sample Animations
   
3. Format: glTF Binary (.glb)

4. Đặt tên: test.glb

5. Bấm "Export glTF 2.0"
```

### ❌ Lỗi Thường Gặp

**Quên check Animation checkbox:**
→ File GLB sẽ không chứa animations

**Không đặt tên Actions:**
→ Animations không được export

**Chọn sai Animation Mode:**
→ Chọn "Actions" là đơn giản nhất

---

## 🔄 Sau Khi Export

```bash
1. Copy file test.glb mới
2. Paste vào: D:\Personal\3D_Blender\public\models\
3. Reload trang web (Ctrl + R)
4. Mở Console (F12) → Xem log animations
```

---

## 📝 Checklist Trước Export

- [ ] Đã tạo ít nhất 1 Action
- [ ] Action đã được đặt tên (Idle, Talking, Waving)
- [ ] Mỗi Action có ít nhất 2 keyframes
- [ ] Test animation trong Blender (Space)
- [ ] Export: ✅ Animation checkbox
- [ ] Format: glTF Binary (.glb)

---

## 🎥 Video Hướng Dẫn (Tham Khảo)

YouTube Search: "Blender create animation export glb"

Hoặc xem docs:
- https://docs.blender.org/manual/en/latest/animation/actions.html
- https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html

---

## 💡 Tips Nhanh

**Phím tắt Blender:**
- `I` = Insert Keyframe
- `Space` = Play/Pause animation
- `G` = Move (Grab)
- `R` = Rotate
- `S` = Scale
- `Z` = Constrain to Z-axis

**Animation đơn giản không cần rigging:**
- Location (di chuyển)
- Rotation (xoay)
- Scale (phóng to/thu nhỏ)

**Nếu có character rigged:**
- Animate bones/armature
- Pose Mode → Di chuyển bones → Insert keyframes

---

## ✅ Khi Nào Thành Công?

Sau khi export đúng và reload web, Console sẽ hiển thị:

```
🎬 Số animations tìm thấy: 3
📋 Danh sách actions: ['Idle', 'Talking', 'Waving']
```

Và các nút sẽ hoạt động khi bấm! 🎉

---

**Chúc bạn thành công!** 🚀
