import { useState, useEffect, useRef, Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { useGLTF, useAnimations, OrbitControls, Environment, ContactShadows } from "@react-three/drei";
import * as THREE from "three";
import "./App.css";

// --- NHÂN VẬT ---
function Avatar({
  action,
  onNamesReady,
}: {
  action: string;
  onNamesReady?: (n: string[]) => void;
}) {
  const group = useRef<THREE.Group>(null!);
  const namesReported = useRef(false);

  const { scene, animations } = useGLTF("/models/character.glb");
  const { actions, names } = useAnimations(animations, group);

  // Fix materials nếu model không có texture
  useEffect(() => {
    scene.traverse((child) => {
      if ((child as THREE.Mesh).isMesh) {
        const mesh = child as THREE.Mesh;
        if (mesh.material) {
          const material = mesh.material as THREE.MeshStandardMaterial;
          // Nếu màu trắng thuần, đổi sang màu da tự nhiên
          if (material.color && material.color.getHex() === 0xffffff) {
            material.color.setHex(0xffdbac); // Màu da
          }
          material.roughness = 0.8;
          material.metalness = 0.2;
          material.needsUpdate = true;
        }
      }
    });
  }, [scene]);

  // Báo tên animations — CHỈ 1 LẦN
  useEffect(() => {
    if (names.length > 0 && !namesReported.current) {
      namesReported.current = true;
      console.log("🎬 Animations:", names);
      const clean = names.filter(
        (n) => !n.includes("collider") && !n.includes("Layer0"),
      );
      onNamesReady?.(clean);
    }
  }, [names]);

  // Chuyển animation
  useEffect(() => {
    if (names.length === 0 || !action) return;
    Object.values(actions).forEach((a) => a?.stop());
    const target = actions[action] || actions[names[0]];
    if (target) {
      target.reset().fadeIn(0.3).play();
    }
  }, [action, actions, names]);

  return (
    <group ref={group} dispose={null} position={[0, 0.5, 0]}>
      <primitive object={scene} scale={0.8} />
    </group>
  );
}

// --- APP ---
export default function App() {
  const [currentAction, setAction] = useState("");
  const [animNames, setAnimNames] = useState<string[]>([]);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleNamesReady = (names: string[]) => {
    setAnimNames(names);
    if (names.length > 0) setAction(names[0]);
  };

  return (
    <div className="app-container">
      {/* NÚT HAMBURGER - chỉ hiện trên mobile */}
      <button
        className="sidebar-toggle"
        onClick={() => setSidebarOpen((o) => !o)}
        aria-label="Toggle animations"
      >
        {sidebarOpen ? "✕" : "☰"}
      </button>

      {/* OVERLAY - đóng sidebar khi tap ngoài */}
      {sidebarOpen && (
        <div className="sidebar-overlay" onClick={() => setSidebarOpen(false)} />
      )}

      {/* SIDEBAR */}
      <aside className={`sidebar ${sidebarOpen ? "open" : ""}` }>
        <div className="sidebar-header">
          <h2>🎭 Animations</h2>
          <span className="badge">{animNames.length}</span>
        </div>
        <div className="animation-list">
          {animNames.map((name) => (
            <button
              key={name}
              onClick={() => { setAction(name); setSidebarOpen(false); }}
              className={`anim-btn ${currentAction === name ? "active" : ""}`}
            >
              <span className="anim-icon">▶</span>
              <span className="anim-name">{name}</span>
            </button>
          ))}
          {animNames.length === 0 && (
            <p className="loading-text">⏳ Đang tải animations...</p>
          )}
        </div>
      </aside>

      {/* KHUNG 3D */}
      <main className="canvas-container">
        <Suspense fallback={<div className="loading-screen">⏳ Đang tải nhân vật 3D...</div>}>
          <Canvas
            camera={{ position: [0, 1.2, 3], fov: 40 }}
            shadows
            gl={{ 
              antialias: true, 
              alpha: false,
              toneMapping: THREE.ACESFilmicToneMapping,
              toneMappingExposure: 1.2
            }}
            dpr={[1, 2]}
          >
            {/* Lighting */}
            <ambientLight intensity={0.5} />
            <directionalLight
              position={[5, 8, 5]}
              intensity={0.8}
              castShadow
              shadow-mapSize-width={1024}
              shadow-mapSize-height={1024}
            />
            <pointLight position={[-5, 5, -5]} intensity={0.3} color="#a78bfa" />
            <pointLight position={[5, 2, 5]} intensity={0.2} color="#60a5fa" />
            
            {/* Environment */}
            <Environment preset="sunset" background={false} />
            <color attach="background" args={['#1a1625']} />
            
            {/* Model */}
            <Avatar action={currentAction} onNamesReady={handleNamesReady} />
            
            {/* Ground Shadow */}
            <ContactShadows
              position={[0, -1, 0]}
              opacity={0.4}
              scale={10}
              blur={2}
              far={4}
            />
            
            {/* Controls */}
            <OrbitControls
              enablePan={false}
              enableZoom={true}
              minDistance={2}
              maxDistance={8}
              maxPolarAngle={Math.PI / 2}
              target={[0, 1, 0]}
            />
          </Canvas>
        </Suspense>

        {/* CHAT INPUT */}
        <div className="chat-container">
          <input
            type="text"
            placeholder="💬 Nhập tin nhắn..."
            className="chat-input"
          />
          <button className="chat-btn">Gửi</button>
        </div>

        {/* INFO BADGE */}
        <div className="info-badge">
          <span>🖱️ Click &amp; Drag để xoay • Scroll để zoom</span>
        </div>
      </main>
    </div>
  );
}
