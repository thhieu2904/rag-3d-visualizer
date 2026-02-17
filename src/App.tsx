import { useState, useEffect, useRef, Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { useGLTF, useAnimations, Center } from "@react-three/drei";
import * as THREE from "three";

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
    <group ref={group} dispose={null}>
      <primitive object={scene} />
    </group>
  );
}

// --- APP ---
export default function App() {
  const [currentAction, setAction] = useState("");
  const [animNames, setAnimNames] = useState<string[]>([]);

  const handleNamesReady = (names: string[]) => {
    setAnimNames(names);
    if (names.length > 0) setAction(names[0]);
  };

  return (
    <div
      style={{
        width: "100vw",
        height: "100vh",
        background: "#1a1a2e",
        display: "flex",
      }}
    >
      {/* SIDEBAR */}
      <div
        style={{
          width: "220px",
          padding: "20px",
          background: "rgba(255,255,255,0.05)",
          borderRight: "1px solid rgba(255,255,255,0.1)",
          display: "flex",
          flexDirection: "column",
          gap: "8px",
        }}
      >
        <h2
          style={{ color: "white", marginBottom: "15px", fontSize: "1.1rem" }}
        >
          🎭 Animation
        </h2>
        {animNames.map((name) => (
          <button
            key={name}
            onClick={() => setAction(name)}
            style={{
              padding: "10px 14px",
              background:
                currentAction === name
                  ? "linear-gradient(135deg, #667eea, #764ba2)"
                  : "rgba(255,255,255,0.08)",
              color: "white",
              border:
                currentAction === name
                  ? "none"
                  : "1px solid rgba(255,255,255,0.1)",
              borderRadius: "10px",
              cursor: "pointer",
              textAlign: "left",
              fontSize: "0.9rem",
              transition: "all 0.2s",
            }}
          >
            {name}
          </button>
        ))}
        {animNames.length === 0 && (
          <p style={{ color: "#666", fontSize: "0.8rem" }}>Đang tải...</p>
        )}
      </div>

      {/* KHUNG 3D */}
      <div style={{ flex: 1, position: "relative" }}>
        <Suspense
          fallback={
            <div
              style={{
                color: "white",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                height: "100%",
              }}
            >
              ⏳ Đang tải nhân vật...
            </div>
          }
        >
          <Canvas camera={{ position: [0, 1, 3], fov: 35 }}>
            <ambientLight intensity={0.8} />
            <directionalLight position={[5, 5, 5]} intensity={1} />
            <Center>
              <Avatar action={currentAction} onNamesReady={handleNamesReady} />
            </Center>
          </Canvas>
        </Suspense>

        {/* CHAT */}
        <div
          style={{
            position: "absolute",
            bottom: "20px",
            left: "50%",
            transform: "translateX(-50%)",
            width: "55%",
            background: "rgba(0,0,0,0.5)",
            padding: "12px 20px",
            borderRadius: "30px",
            display: "flex",
            alignItems: "center",
            gap: "10px",
            backdropFilter: "blur(8px)",
            border: "1px solid rgba(255,255,255,0.1)",
          }}
        >
          <input
            type="text"
            placeholder="Nhập tin nhắn..."
            style={{
              flex: 1,
              background: "transparent",
              border: "none",
              color: "white",
              outline: "none",
              fontSize: "0.95rem",
            }}
          />
          <button
            style={{
              background: "linear-gradient(135deg, #667eea, #764ba2)",
              border: "none",
              color: "white",
              padding: "8px 20px",
              borderRadius: "20px",
              cursor: "pointer",
            }}
          >
            Gửi
          </button>
        </div>
      </div>
    </div>
  );
}
