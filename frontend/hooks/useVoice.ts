import { useState, useEffect } from "react";
import { apiFetch } from "@/lib/api-client";

export function useVoice() {
  const [isConnected, setIsConnected] = useState(false);
  const [isConnecting, setIsConnecting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const connectVoice = async () => {
    setIsConnecting(true);
    setError(null);
    try {
      const response = await apiFetch<{ token: string }>("/api/v1/voice/token", {
        method: "POST",
        body: JSON.stringify({
          room: "ai-copilot-room",
          identity: `user_${Math.random().toString(36).substring(7)}`
        }),
      });

      // In a full implementation, we would now use the token to connect
      // using livekit-client. Here we simulate the connection for the UI.
      console.log("LiveKit Token acquired:", response.token);
      setIsConnected(true);
    } catch (err: any) {
      setError(err.message || "Failed to connect to voice service.");
    } finally {
      setIsConnecting(false);
    }
  };

  const disconnectVoice = () => {
    setIsConnected(false);
  };

  return { isConnected, isConnecting, error, connectVoice, disconnectVoice };
}
