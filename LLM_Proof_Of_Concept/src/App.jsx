import { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import ReactTypingEffect from 'react-typing-effect'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')

  const handleQuery = async () => {
    try {
      const res = await axios.post('http://127.0.0.1:5000/query', { query })
      setResponse(res.data.response)
    } catch (error) {
      console.error('Error querying the LLM:', error)
      setResponse('Error querying the LLM')
    }
  }

  return (
    <div className="App">
      <h1>Query the LLM</h1>
      <textarea
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Enter your query here"
      />
      <button onClick={handleQuery}>Submit</button>
      <div className="response">
        {response && (
          <ReactTypingEffect
            text={response}
            speed={10}
            eraseSpeed={1}
            typingDelay={100}
            eraseDelay={10000}
            displayTextRenderer={(text, i) => {
              return <ReactMarkdown>{text}</ReactMarkdown>
            }}
          />
        )}
      </div>
    </div>
  )
}

export default App