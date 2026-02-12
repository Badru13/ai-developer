/**
 * MessageBubble Component
 *
 * Displays a single chat message with markdown support.
 * Different styling for user vs assistant messages.
 */

import ReactMarkdown from 'react-markdown'

function MessageBubble({ message }) {
  const isUser = message.role === 'user'

  // Don't render empty messages
  if (!message.content) return null

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-[80%] rounded-2xl px-5 py-3 shadow-sm ${
          isUser
            ? 'bg-blue-600 text-white'
            : 'bg-white border border-gray-200 text-gray-800'
        }`}
      >
        {isUser ? (
          // User messages: plain text
          <p className="whitespace-pre-wrap">{message.content}</p>
        ) : (
          // Assistant messages: render markdown
          <div className="markdown-content">
            <ReactMarkdown>{message.content}</ReactMarkdown>
          </div>
        )}
      </div>
    </div>
  )
}

export default MessageBubble
