import { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, Environment, RoundedBox, ContactShadows } from "@react-three/drei";

interface ProductViewerProps {
  color?: string;
}

/**
 * ProductViewer — interactive 3D product presentation for the PDP.
 *
 * Drag to rotate (OrbitControls), auto-rotates when idle, zoom with
 * mouse wheel. Renders a stylized device silhouette colored by the
 * selected variant — swap for a real GLTF model (useGLTF + Draco) once
 * product-specific 3D assets are available; the control rig is
 * asset-agnostic.
 */
function DeviceModel({ color = "#111318" }: { color?: string }) {
  return (
    <group>
      <RoundedBox args={[1.8, 3.6, 0.16]} radius={0.18} smoothness={6}>
        <meshStandardMaterial color={color} metalness={0.6} roughness={0.25} />
      </RoundedBox>
      <mesh position={[0, 0, 0.09]}>
        <planeGeometry args={[1.6, 3.3]} />
        <meshStandardMaterial color="#0a0a0a" metalness={0.3} roughness={0.5} />
      </mesh>
      <mesh position={[0, 0, 0.1]}>
        <planeGeometry args={[1.5, 3.2]} />
        <meshStandardMaterial color="#3B82F6" emissive="#3B82F6" emissiveIntensity={0.35} />
      </mesh>
    </group>
  );
}

export default function ProductViewer({ color = "#111318" }: ProductViewerProps) {
  return (
    <div className="relative h-[420px] w-full overflow-hidden rounded-2xl bg-gradient-to-b from-surface/60 to-black/40 md:h-[520px]">
      <Canvas camera={{ position: [0, 0, 6], fov: 40 }} dpr={[1, 1.5]}>
        <Suspense fallback={null}>
          <ambientLight intensity={0.5} />
          <pointLight position={[4, 4, 4]} intensity={30} color="#3B82F6" />
          <pointLight position={[-4, -2, 2]} intensity={15} color="#8B5CF6" />
          <Environment preset="studio" />

          <DeviceModel color={color} />
          <ContactShadows position={[0, -2, 0]} opacity={0.5} scale={8} blur={2.5} far={4} />

          <OrbitControls
            enablePan={false}
            enableZoom
            minDistance={3.5}
            maxDistance={9}
            autoRotate
            autoRotateSpeed={1.2}
            makeDefault
          />
        </Suspense>
      </Canvas>
      <p className="pointer-events-none absolute bottom-3 left-1/2 -translate-x-1/2 text-xs text-white/30">
        Drag to rotate · Scroll to zoom
      </p>
    </div>
  );
}
