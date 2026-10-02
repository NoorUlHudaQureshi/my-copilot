"use client";

import { useChat } from "@/hooks/useChat";
import { useVoice } from "@/hooks/useVoice";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { ScrollArea } from "@/components/ui/scroll-area";
import { ImageIcon, X, Mic, MicOff, Loader2 } from "lucide-react";
import { useState } from "react";

export default function ChatPage() {
  const {
    messages,
    input,
    setInput,
    sendMessage,
    isLoading,
    selectedImage,
    setSelectedImage,
    handleImageChange
  } = useChat();

  const { isConnected, isConnecting, error: voiceError, connectVoice, disconnectVoice } = useVoice();

  return (
    <div className="flex h-screen w-full items-center justify-center bg-slate-50 p-4 dark:bg-slate-950">
      <Card className="flex h-[80vh] w-full max-w-3xl flex-col overflow-hidden shadow-xl">
        <CardHeader className="border-b p-4 flex flex-row items-center justify-between">
          <CardTitle className="text-2xl font-bold">AI Agent Assistant</CardTitle>
          <div className="flex items-center gap-2">
            {isConnecting && <Loader2 className="animate-spin text-slate-400" size={20} />}
            <Button
              variant={isConnected ? "destructive" : "outline"}
              size="sm"
              onClick={isConnected ? disconnectVoice : connectVoice}
              className="flex items-center gap-2"
            >
              {isConnected ? <MicOff size={16} /> : <Mic size={16} />}
              {isConnected ? "Disconnect Voice" : "Connect Voice"}
            </Button>
          </div>
        </CardHeader>

        <CardContent className="flex flex-1 flex-col p-0">
          {voiceError && (
            <div className="bg-red-100 text-red-600 p-2 text-sm text-center border-b">
              {voiceError}
            </div>
          )}

          <ScrollArea className="flex-1 p-4">
            <div className="flex flex-col gap-4">
              {messages.length === 0 && (
                <div className="text-center text-slate-500 mt-10">
                  Start a conversation with your AI assistant! You can also upload images or use voice.
                </div>
              )}
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`max-w-[80%] rounded-lg px-4 py-2 ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white"
                        : "bg-slate-200 text-slate-900 dark:bg-slate-800 dark:text-slate-100"
                    }`}
                  >
                    {msg.image && (
                      <img
                        src={`data:image/jpeg;base64,${msg.image}`}
                        alt="Uploaded content"
                        className="max-w-full h-auto rounded mb-2 max-h-60"
                      />
                    )}
                    {msg.content}
                  </div>
                </div>
              ))}
              {isLoading && (
                <div className="flex justify-start">
                  <div className="bg-slate-200 rounded-lg px-4 py-2 animate-pulse dark:bg-slate-800 dark:text-slate-100">
                    Thinking...
                  </div>
                </div>
              )}
            </div>
          </ScrollArea>

          <div className="border-t p-4 bg-white dark:bg-slate-900">
            {selectedImage && (
              <div className="mb-2 relative w-20 h-20">
                <img
                  src={selectedImage}
                  alt="Preview"
                  className="w-full h-full object-cover rounded-md border"
                />
                <button
                  onClick={() => setSelectedImage(null)}
                  className="absolute -top-2 -right-2 bg-red-500 text-white rounded-full p-1 hover:bg-red-600 transition-colors"
                >
                  <X size={12} />
                </button>
              </div>
            )}
            <form
              className="flex gap-2"
              onSubmit={(e) => { e.preventDefault(); sendMessage(); }}
            >
              <div className="relative flex-1">
                <Input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Type your message..."
                  disabled={isLoading}
                  className="pr-10"
                />
                <label className="absolute right-2 top-1/2 -translate-y-1/2 cursor-pointer text-slate-400 hover:text-slate-600 transition-colors">
                  <ImageIcon size={20} />
                  <input
                    type="file"
                    className="hidden"
                    accept="image/*"
                    onChange={handleImageChange}
                    disabled={isLoading}
                  />
                </label>
              </div>
              <Button type="submit" disabled={isLoading}>
                Send
              </Button>
            </form>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
