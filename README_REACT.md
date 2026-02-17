# ⚛️ React Three Fiber - 3D Model Viewer

[![React](https://img.shields.io/badge/React-19-blue.svg)](https://react.dev/)
[![Vite](https://img.shields.io/badge/Vite-7.3-purple.svg)](https://vitejs.dev/)
[![Three.js](https://img.shields.io/badge/Three.js-0.182-black.svg)](https://threejs.org/)

3D Model Viewer với React Three Fiber để hiển thị và điều khiển animations GLB/GLTF.

---

## 🚀 Quick Start

```bash
# Cài đặt dependencies
npm install

# Chạy dev server
npm run dev

# Mở browser
http://localhost:5173
```

---

## 📁 Cấu Trúc Project

```
3D_Blender/
├── public/
│   └── models/
│       └── test.glb          # ← Đặt file GLB tại đây
├── src/
│   ├── App.tsx               # Main component
│   ├── index.css             # Styles
│   └── main.tsx              # Entry point
├── BLENDER_ANIMATION_GUIDE.md # Hướng dẫn tạo animations
└── package.json
```

---

## ⚠️ BẮT BUỘC: Model Phải Có Animations

### Hiện Tại: Model Chưa Có Animations

Console log hiển thị:
```
🎬 Số animations tìm thấy: 0
⚠️ Model không có animations
```

### ✅ Giải Pháp: Tạo Animations trong Blender

Xem chi tiết: **[BLENDER_ANIMATION_GUIDE.md](BLENDER_ANIMATION_GUIDE.md)**

**Tóm tắt:**
1. Mở `test.glb` trong Blender
2. Tạo 3 **Actions** (Idle, Talking, Waving)
3. Thêm keyframes cho mỗi action
4. Export GLB với checkbox **✅ Animation**
5. Copy file mới vào `public/models/`
6. Reload trang

---

## 🎮 Features

✅ Load model GLB/GLTF  
✅ Hiển thị và điều khiển animations  
✅ Auto-rotate khi không có animations  
✅ Smooth transitions (fade in/out)  
✅ OrbitControls (xoay, zoom model)  
✅ Environment lighting & shadows  
✅ TypeScript support  
✅ Hot Module Replacement (HMR)  

---

## 🎨 Tùy Chỉnh

### Đổi Tên Animations

Mở Console (F12) để xem tên animations thực tế:
```
📋 Danh sách actions: ['Animation1', 'Animation2']
```

Sửa trong [src/App.tsx](src/App.tsx):
```tsx
<button onClick={() => setAction("Animation1")}>
  Hành động 1
</button>
```

### Thay Đổi Camera Position
```tsx
<Canvas camera={{ position: [x, y, z], fov: 50 }}>
```

### Thay Đổi Background
```tsx
<div style={{ background: "#yourcolor" }}>
```

### Lighting Presets
```tsx
<Environment preset="sunset" /> 
// Options: city, sunset, dawn, night, warehouse, forest, etc.
```

---

## 🛠️ Tech Stack

| Package | Version | Mô Tả |
|---------|---------|-------|
| React | 19.2.0 | UI Framework |
| Vite | 7.3.1 | Build tool |
| Three.js | 0.182.0 | 3D engine |
| @react-three/fiber | 9.5.0 | React renderer cho Three.js |
| @react-three/drei | 10.7.7 | Helpers & components |
| TypeScript | 5.9.3 | Type safety |

---

## 📝 Component Structure

### `Avatar` Component
```tsx
function Avatar({ action }: { action: string }) {
  const { scene, animations } = useGLTF('/models/test.glb');
  const { actions, names } = useAnimations(animations, group);
  
  // Auto-rotate if no animations
  // Fade in/out between animations
  // Log animation debug info
}
```

### `App` Component
```tsx
export default function App() {
  const [currentAction, setAction] = useState("");
  const [hasAnimations, setHasAnimations] = useState(false);
  
  return (
    <Canvas>
      <Avatar action={currentAction} />
      <OrbitControls />
      <Environment preset="city" />
    </Canvas>
  );
}
```

---

## 🐛 Troubleshooting

### ❌ Model không hiển thị
**Nguyên nhân:** File GLB không tồn tại hoặc đường dẫn sai

**Giải pháp:**
```bash
# Kiểm tra file tồn tại
ls public/models/test.glb

# Nếu không có, copy file vào
Copy-Item test.glb public/models/
```

### ❌ Animations không hoạt động
**Nguyên nhân:** Model không có animations hoặc tên sai

**Giải pháp:**
1. Check Console (F12): `Số animations tìm thấy: 0`
2. Đọc [BLENDER_ANIMATION_GUIDE.md](BLENDER_ANIMATION_GUIDE.md)
3. Export lại từ Blender với checkbox **Animation**

### ⚠️ WebGL warnings
```
THREE.WebGLProgram: Program Info Log: warning X4122...
```
**Đây là warning bình thường của GPU**, không ảnh hưởng.

### 🐌 Performance chậm
- Giảm `resolution` của ContactShadows
- Dùng Environment preset đơn giản hơn ("apartment" thay vì "city")
- Optimize model trong Blender (reduce polycount)

---

## 🔌 Tích Hợp API/RAG

### Fetch Animation từ Backend
```tsx
const [currentAction, setAction] = useState("");

useEffect(() => {
  fetch('/api/get-animation')
    .then(res => res.json())
    .then(data => setAction(data.animationName));
}, []);
```

### Voice Input → Animation
```tsx
const handleVoice = async (transcript: string) => {
  const response = await fetch('/api/rag', {
    method: 'POST',
    body: JSON.stringify({ text: transcript })
  });
  const { animation } = await response.json();
  setAction(animation);
};
```

---

## 📚 Resources

- [React Three Fiber Docs](https://docs.pmnd.rs/react-three-fiber/)
- [Drei Components](https://github.com/pmndrs/drei)
- [Three.js Manual](https://threejs.org/manual/)
- [Blender glTF Export](https://docs.blender.org/manual/en/latest/addons/import_export/scene_gltf2.html)

---

## 🎓 Learning Path

1. ✅ Setup React + Vite project
2. ✅ Install React Three Fiber
3. ✅ Load GLB model
4. ⏳ **Create animations in Blender** ← BẠN Ở ĐÂY
5. Control animations via buttons
6. Integrate with backend API
7. Add voice control
8. Deploy to production

---

## 🎯 Next Steps

1. **Tạo animations trong Blender** - Đọc [BLENDER_ANIMATION_GUIDE.md](BLENDER_ANIMATION_GUIDE.md)
2. Export file GLB mới
3. Copy vào `public/models/`
4. Reload trang → Check Console
5. Test các nút điều khiển

---

## 📧 Support

Nếu có vấn đề:
1. Check Console (F12) xem lỗi gì
2. Đọc Troubleshooting section
3. Đọc BLENDER_ANIMATION_GUIDE.md

---

## ✨ Credits

Built with ❤️ using:
- React Three Fiber by Poimandres
- Three.js
- Vite

---

**Happy Coding! 🚀**
