import { useRef, useMemo } from "react";
import { useFrame } from "@react-three/fiber";
import { Float, Environment, RoundedBox, MeshDistortMaterial } from "@react-three/drei";
import * as THREE from "three";

/**
 * FloatingProducts
 *
 * Stand-in "premium electronics" primitives (laptop / phone / watch /
 * earbuds silhouettes) built from basic geometry, since real GLTF
 * product models aren't available in this scaffold. Swap the meshes
 * below for Draco-compressed GLTF models via useGLTF() once assets
 * are ready — the float/parallax rig stays the same.
 */

function Laptop() {
  const group = useRef<THREE.Group>(null!);
  useFrame(({ mouse }) => {
    group.current.rotation.y = THREE.MathUtils.lerp(group.current.rotation.y, mouse.x * 0.25, 0.05);
    group.current.rotation.x = THREE.MathUtils.lerp(group.current.rotation.x, -mouse.y * 0.1, 0.05);
  });
  return (
    <Float speed={1.2} rotationIntensity={0.3} floatIntensity={0.8}>
      <group ref={group} position={[0, 0, 0]}>
        {/* base */}
        <RoundedBox args={[2.4, 0.12, 1.6]} radius={0.05} position={[0, -0.4, 0]}>
          <meshStandardMaterial color="#111318" metalness={0.9} roughness={0.25} />
        </RoundedBox>
        {/* screen */}
        <RoundedBox args={[2.4, 1.5, 0.08]} radius={0.05} position={[0, 0.35, -0.75]} rotation={[-0.15, 0, 0]}>
          <meshStandardMaterial color="#0D1117" metalness={0.7} roughness={0.3} />
        </RoundedBox>
        <mesh position={[0, 0.35, -0.71]} rotation={[-0.15, 0, 0]}>
          <planeGeometry args={[2.15, 1.3]} />
          <MeshDistortMaterial color="#3B82F6" emissive="#3B82F6" emissiveIntensity={0.6} distort={0.15} speed={1.5} />
        </mesh>
      </group>
    </Float>
  );
}

function Phone() {
  return (
    <Float speed={1.6} rotationIntensity={0.6} floatIntensity={1.2}>
      <RoundedBox args={[0.6, 1.25, 0.08]} radius={0.08} position={[2.6, 0.6, 0.6]}>
        <meshStandardMaterial color="#1a1d24" metalness={0.85} roughness={0.2} />
      </RoundedBox>
    </Float>
  );
}

function Watch() {
  return (
    <Float speed={1.8} rotationIntensity={0.8} floatIntensity={1.4}>
      <mesh position={[-2.5, -0.6, 0.8]}>
        <cylinderGeometry args={[0.42, 0.42, 0.14, 48]} />
        <meshStandardMaterial color="#0D1117" metalness={0.9} roughness={0.15} />
      </mesh>
      <mesh position={[-2.5, -0.6, 0.88]}>
        <circleGeometry args={[0.34, 48]} />
        <meshStandardMaterial color="#8B5CF6" emissive="#8B5CF6" emissiveIntensity={0.5} />
      </mesh>
    </Float>
  );
}

function Earbuds() {
  const positions: [number, number, number][] = [
    [1.6, -1.1, 1.4],
    [1.95, -1.3, 1.3],
  ];
  return (
    <Float speed={2} rotationIntensity={1} floatIntensity={1.6}>
      <group>
        {positions.map((pos, i) => (
          <mesh key={i} position={pos}>
            <capsuleGeometry args={[0.09, 0.22, 4, 12]} />
            <meshStandardMaterial color="#f5f5f5" roughness={0.3} />
          </mesh>
        ))}
      </group>
    </Float>
  );
}

function Particles({ count = 200 }: { count?: number }) {
  const positions = useMemo(() => {
    const arr = new Float32Array(count * 3);
    for (let i = 0; i < count; i++) {
      arr[i * 3] = (Math.random() - 0.5) * 14;
      arr[i * 3 + 1] = (Math.random() - 0.5) * 8;
      arr[i * 3 + 2] = (Math.random() - 0.5) * 8 - 2;
    }
    return arr;
  }, [count]);

  const points = useRef<THREE.Points>(null!);
  useFrame((_, delta) => {
    points.current.rotation.y += delta * 0.02;
  });

  return (
    <points ref={points}>
      <bufferGeometry>
        <bufferAttribute attach="attributes-position" args={[positions, 3]} />
      </bufferGeometry>
      <pointsMaterial size={0.02} color="#3B82F6" transparent opacity={0.6} sizeAttenuation />
    </points>
  );
}

export default function FloatingProducts() {
  return (
    <>
      <ambientLight intensity={0.4} />
      <pointLight position={[5, 5, 5]} intensity={40} color="#3B82F6" />
      <pointLight position={[-5, -3, 3]} intensity={20} color="#8B5CF6" />
      <Environment preset="city" />

      <Laptop />
      <Phone />
      <Watch />
      <Earbuds />
      <Particles />
    </>
  );
}
