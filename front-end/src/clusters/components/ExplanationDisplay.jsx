import React from 'react'

const ExplanationDisplay = ({ explanation }) => {
  const formattedText = explanation.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                                   .replace(/\*(.*?)\*/g, '<em>$1</em>')
                                   .replace(/\n/g, '<br>');

  return (
    <div className="p-6 bg-gray-100 rounded-md shadow-md">
      <div 
        className="prose prose-lg text-gray-800 leading-relaxed"
        dangerouslySetInnerHTML={{ __html: formattedText }}>
      </div>

    </div>
  )
}

export default ExplanationDisplay;
