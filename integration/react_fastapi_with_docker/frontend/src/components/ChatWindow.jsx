/**
 * ChatWindow Component
 *
 * Main container for the chat interface.
 * Displays list of messages and auto-scrolls to bottom.
 */

import { useEffect, useRef } from 'react'
import MessageBubble from './MessageBubble'

function ChatWindow({ messages, isLoading }) {
  const messagesEndRef = useRef(null)

  // Auto-scroll when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  return (
    <div className="flex-1 overflow-y-auto px-6 py-6 chat-scrollbar bg-gray-50">
      {/* Welcome message when no messages */}
      {messages.length === 0 && (
        <div className="flex items-center justify-center h-full">
          <div className="text-center text-gray-500 max-w-md">
            <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 10h.01M12 10h.01M16 10h.01M9 16H5a2 2 0 01-2-2V6a2 2 0 012-2h14a2 2 0 012 2v8a2 2 0 01-2 2h-5l-5 5v-5z" />
              </svg>
            </div>
            <h2 className="text-xl font-semibold text-gray-700 mb-3">Welcome!</h2>
            <p className="text-gray-500 mb-4">I'm your AI Research Assistant. I can help you with:</p>
            <div className="space-y-2 text-left bg-white rounded-lg p-4 shadow-sm">
              <div className="flex items-center gap-2">
                <span className="text-blue-500">🔍</span>
                <span>Search the web for information</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-blue-500">🌤️</span>
                <span>Get weather for any city</span>
              </div>
              <div className="flex items-center gap-2">
                <span className="text-blue-500">🔢</span>
                <span>Do calculations</span>
              </div>
            </div>
            <p className="mt-4 text-sm text-gray-400">Try asking me something!</p>
          </div>
        </div>
      )}

      {/* Messages list */}
      <div className="space-y-4">
        {messages.map((message, index) => (
          <MessageBubble key={index} message={message} />
        ))}

        {/* Loading indicator */}
        {isLoading && messages[messages.length - 1]?.content === '' && (
          <div className="flex justify-start">
            <div className="bg-white border border-gray-200 rounded-lg px-4 py-3 shadow-sm">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                  <div className="w-2 h-2 bg-blue-500 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                </div>
                <span className="text-sm text-gray-500">Thinking...</span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Auto-scroll anchor */}
      <div ref={messagesEndRef} />
    </div>
  )
}

export default ChatWindow
