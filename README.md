# 3D Character Viewer with Animations

Dự án demo xem nhân vật 3D với animations realtime trên web, xây dựng trên **React + Three.js**. Nhân vật được tạo từ VRoid Studio, xử lý qua Blender + Mixamo, và hiển thị với đầy đủ materials/textures + nhiều animations.

---

## Chạy nhanh

```bash
npm install
npm run dev
# Mở http://localhost:5173
```

**Điều khiển:**
- **Click & Drag** để xoay nhân vật
- **Scroll** để zoom in/out
- **Sidebar trái** để chọn animation

---

## Tech Stack

| Layer | Công nghệ |
|---|---|
| UI Framework | React 19 + TypeScript |
| Build Tool | Vite 7 |
| 3D Rendering | Three.js + @react-three/fiber |
| 3D Helpers | @react-three/drei (OrbitControls, GLTF, Animations) |
| 3D Pipeline | VRoid Studio → Blender 4.2 → Mixamo → GLB |

---

## Cấu trúc thư mục

```
3D_Blender/
├── src/
│   ├── App.tsx              # Component chính: Canvas 3D + Sidebar animations + Chat UI
│   ├── App.css              # Styling dark theme, sidebar, chat input
│   ├── main.tsx             # Entry point React
│   └── index.css            # Global styles
│
├── public/
│   └── models/
│       └── character.glb    # Model 3D cuối cùng (materials + 7 animations)
│
├── scripts/                 # Blender Python scripts — xem scripts/README.md
│   ├── convert_to_glb.py    # Gộp FBX base + animation FBX → character.glb
│   ├── fix_materials_from_vrm.py  # Transfer materials từ VRM vào GLB
│   └── README.md
│
├── assets/
│   └── pipeline/            # Raw assets pipeline — xem assets/pipeline/README.md
│       ├── AIC_Female_v1.vrm      # Model gốc VRoid (nguồn materials MToon)
│       ├── upload_Mixamo.fbx      # FBX dùng để upload lên Mixamo
│       ├── file_new.fbx           # FBX tải từ Mixamo (xương chuẩn + bind pose)
│       ├── Catwalk Walk Stop Twist R.fbx
│       ├── Using A Fax Machine.fbx
│       ├── Lengthy Head Nod.fbx
│       ├── Standing W_Briefcase Idle.fbx
│       ├── Standing Up.fbx
│       ├── Texting While Standing.fbx
│       ├── Thankful.fbx
│       └── README.md
│
├── ThamKhao/                # Tài liệu tham khảo
├── vite.config.ts
├── tsconfig.json
└── package.json
```

---

## Pipeline tạo model 3D

Quy trình đầy đủ từ thiết kế nhân vật đến hiển thị web:

```
[1] VRoid Studio
    └─> Tạo nhân vật, export AIC_Female_v1.vrm

[2] Blender 4.2
    └─> Import VRM → Export upload_Mixamo.fbx
        (FBX chuẩn T-pose để Mixamo nhận diện xương)

[3] Mixamo (mixamo.com)
    ├─> Upload upload_Mixamo.fbx → Auto-rig
    └─> Tải file_new.fbx (T-pose + xương Mixamo chuẩn)
    └─> Tải từng animation FBX (Without Skin) → lưu vào assets/pipeline/

[4] scripts/convert_to_glb.py  ← chạy 1 lần
    └─> Import assets/pipeline/file_new.fbx làm base character
    └─> Import từng FBX animation, lấy Action, push vào NLA tracks
    └─> Export → public/models/character.glb  (có animations nhưng materials chưa đúng)

[5] scripts/fix_materials_from_vrm.py  ← chạy sau bước 4
    └─> Import character.glb + assets/pipeline/AIC_Female_v1.vrm
    └─> Transfer 18 material slots từ VRM → GLB meshes (Body, Face, Hair)
    └─> Export lại → public/models/character.glb  ✅ đầy đủ materials + animations

[6] React App
    └─> Load character.glb qua useGLTF
    └─> useAnimations → 7 NLA tracks hiện trong sidebar
```

---

## Scripts Blender

### `scripts/convert_to_glb.py` — Gộp animations

Dùng khi **thêm animation mới** hoặc rebuild model từ đầu.

```bash
blender --background --python scripts/convert_to_glb.py
```

Thêm/bớt animations bằng cách chỉnh dict `ANIMATIONS` trong file:

```python
ANIMATIONS = {
    "TenFile.fbx": "TenHienThiTrenWeb",
    ...
}
```

---

### `scripts/fix_materials_from_vrm.py` — Khôi phục materials

Dùng khi model bị **trắng xóa** sau khi qua FBX pipeline. Luôn chạy sau `convert_to_glb.py`.

```bash
blender --background --python scripts/fix_materials_from_vrm.py
```

---

## Animations có sẵn

| Tên | Mô tả |
|---|---|
| `Catwalk` | Đi catwalk, dừng, xoay |
| `FaxMachine` | Dùng máy fax |
| `HeadNod` | Gật đầu |
| `Idle` | Đứng idle cầm cặp |
| `StandingUp` | Đứng dậy từ ghế |
| `Texting` | Nhắn tin khi đứng |
| `Thankful` | Cảm ơn / cúi chào |

---

## Thêm animation mới

1. Lên [Mixamo](https://mixamo.com), tìm animation, tải FBX (**Without Skin**)
2. Đặt file vào `assets/pipeline/`
3. Thêm vào dict `ANIMATIONS` trong `scripts/convert_to_glb.py`
4. Chạy lại cả 2 scripts:
   ```bash
   blender --background --python scripts/convert_to_glb.py
   blender --background --python scripts/fix_materials_from_vrm.py
   ```
5. Reload trình duyệt — animation mới tự động xuất hiện trong sidebar

---

## Hướng phát triển

### Tích hợp AI Chatbot / RAG
Avatar phản ứng theo câu hỏi người dùng — chat input đã có sẵn trong UI:

```
User input → RAG API → { answer, emotion, animation_name }
           → Avatar chạy animation tương ứng + TTS đọc câu trả lời
```

Map ví dụ: `greeting → Thankful`, `thinking → HeadNod`, `idle → Idle`

### Lip Sync & Facial Expressions
- VRM hỗ trợ BlendShapes (biểu cảm khuôn mặt)
- Tích hợp [three-vrm](https://github.com/pixiv/three-vrm) thay vì GLTF thuần để khai thác đầy đủ MToon shader + viseme

### Nhiều nhân vật / Environment
- Load nhiều GLB, chuyển nhân vật qua UI
- Thay `Environment preset` bằng custom HDRI hoặc background 3D

---

## Yêu cầu

- **Node.js** 18+
- **Blender 4.2** — chỉ cần nếu rebuild hoặc thêm animation mới

---

## Ghi chú kỹ thuật

**Tại sao pipeline VRM → FBX → Mixamo → GLB?**

VRM dùng **MToon shader** (toon-style) không được hỗ trợ bởi Mixamo. Mixamo yêu cầu FBX với xương Humanoid chuẩn. Pipeline này:
1. VRM → FBX: lấy mesh + xương, mất materials
2. Mixamo: auto-rig + download animations
3. `fix_materials_from_vrm.py`: ghép lại materials từ VRM gốc vào GLB cuối

**Tại sao GLB thay vì GLTF?**

GLB là binary, gộp textures + mesh + animations vào 1 file → load nhanh hơn, deploy đơn giản.
