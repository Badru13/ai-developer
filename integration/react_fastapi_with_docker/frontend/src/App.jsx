/**
 * App Component - Main Application
 *
 * Manages chat state and handles streaming communication
 * with the FastAPI backend using Server-Sent Events (SSE).
 */

import { useState } from 'react'
import ChatWindow from './components/ChatWindow'
import InputBox from './components/InputBox'

// Backend API URL
const API_URL = 'http://localhost:8000'

function App() {
  // State for chat messages
  const [messages, setMessages] = useState([])
  // State for loading indicator
  const [isLoading, setIsLoading] = useState(false)

  /**
   * Send a message to the backend and handle streaming response.
   */
  const handleSendMessage = async (userMessage) => {
    // Add user message to chat
    setMessages((prev) => [...prev, { role: 'user', content: userMessage }])
    setIsLoading(true)

    // Add empty assistant message that we'll update with streamed content
    setMessages((prev) => [...prev, { role: 'assistant', content: '' }])

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: userMessage }),
      })

      const reader = response.body.getReader()
      const decoder = new TextDecoder()

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        const chunk = decoder.decode(value)
        const lines = chunk.split('\n')

        for (const line of lines) {
          if (line.startsWith('data:')) {
            const dataStr = line.slice(5).trim()
            if (!dataStr) continue

            try {
              const data = JSON.parse(dataStr)

              if (data.content) {
                setMessages((prev) => {
                  const updated = [...prev]
                  const lastMsg = updated[updated.length - 1]
                  if (lastMsg.role === 'assistant') {
                    lastMsg.content += data.content
                  }
                  return updated
                })
              }

              if (data.error) {
                setMessages((prev) => {
                  const updated = [...prev]
                  const lastMsg = updated[updated.length - 1]
                  if (lastMsg.role === 'assistant') {
                    lastMsg.content = `Error: ${data.error}`
                  }
                  return updated
                })
              }
            } catch (e) {
              // Skip invalid JSON
            }
          }
        }
      }
    } catch (error) {
      setMessages((prev) => {
        const updated = [...prev]
        const lastMsg = updated[updated.length - 1]
        if (lastMsg.role === 'assistant') {
          lastMsg.content = `Connection error: ${error.message}`
        }
        return updated
      })
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100">
      {/* Centered container with max width */}
      <div className="max-w-4xl mx-auto h-screen flex flex-col shadow-xl bg-white">
        {/* Header */}
        <header className="bg-gradient-to-r from-blue-600 to-blue-700 text-white py-5 px-8">
          <h1 className="text-2xl font-bold">AI Research Assistant</h1>
          <p className="text-sm opacity-80 mt-1">
            Search the web, check weather, or calculate anything
          </p>
        </header>

        {/* Chat area */}
        <ChatWindow messages={messages} isLoading={isLoading} />

        {/* Input area */}
        <div className="border-t bg-gray-50 p-6">
          <InputBox onSend={handleSendMessage} isLoading={isLoading} />
        </div>
      </div>
    </div>
  )
}

export default App
