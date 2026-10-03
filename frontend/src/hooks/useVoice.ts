"use client";

import { useEffect, useRef, useState } from "react";
import { Room, RoomEvent } from "livekit-client";
import { apiFetch } from "@/lib/api-client";

const LIVEKIT_URL = "wss://agent-io30ind4.livekit.cloud";

export function useVoice() {
  const roomRef = useRef<Room | null>(null);

  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const connectVoice = async () => {
    if (roomRef.current) return;

    setIsConnecting(true);
    setError(null);

    try {
      const identity = `user_${Math.random().toString(36).substring(2, 10)}`;

      const response = await apiFetch<{ token: string }>(
        "/api/v1/voice/token",
        {
          method: "POST",
          body: JSON.stringify({
            room: "ai-copilot-room",
            identity,
          }),
        }
      );

      const room = new Room();

      room.on(RoomEvent.Connected, () => {
        setIsConnected(true);
        setIsConnecting(false);
      });

      room.on(RoomEvent.Disconnected, () => {
        setIsConnected(false);
        roomRef.current = null;
      });

      room.on(RoomEvent.ConnectionStateChanged, (state) => {
        if (state === "disconnected") {
          setIsConnected(false);
        }
      });

      roomRef.current = room;

      await room.connect(LIVEKIT_URL, response.token);
    } catch (err) {
      roomRef.current?.disconnect();
      roomRef.current = null;

      setIsConnected(false);
      setError(
        err instanceof Error
          ? err.message
          : "Failed to connect to voice service."
      );
    } finally {
      setIsConnecting(false);
    }
  };

  const disconnectVoice = () => {
    roomRef.current?.disconnect();
    roomRef.current = null;
    setIsConnected(false);
    setIsConnecting(false);
  };

  useEffect(() => {
    return () => {
      roomRef.current?.disconnect();
      roomRef.current = null;
    };
  }, []);

  return {
    isConnected,
    isConnecting,
    error,
    connectVoice,
    disconnectVoice,
  };
}