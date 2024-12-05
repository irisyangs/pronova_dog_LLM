import { useState, useEffect } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import ReactTypingEffect from 'react-typing-effect'
import './App.css'

function App() {
  const [query, setQuery] = useState('')
  const [response, setResponse] = useState('')

  useEffect(() => {
  setResponse('')
}, [])

  const [isLoading, setIsLoading] = useState(false)

  const handleQuery = async () => {
    setIsLoading(true)
    try {
      const res = await axios.post('http://127.0.0.1:5000/query', { query })
      setResponse(res.data.response)
    } catch (error) {
      console.error('Error querying the LLM:', error)
      setResponse('Error querying the LLM')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="App">
      <h1>Pronova AI Vet Support</h1>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', height: '70vh' }}>
        <div className="response" style={{ width: '800px', maxHeight: '400px', overflowY: 'auto' }}>
          <ReactMarkdown>{response}</ReactMarkdown>
        </div>
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Hi, I'm your AI assistant Kora! How can I assist you today?"
          style={{ width: '300px', height: '100px', marginBottom: '20px', resize: 'none', color: 'white'}}
        />
        <button 
          onClick={handleQuery} 
          style={{ marginBottom: '20px' }} 
          disabled={isLoading || query.trim() === ''}
          className={isLoading || query.trim() === '' ? 'disabled-button' : ''}
        >
          {isLoading ? 'Loading...' : 'Submit'}
        </button>
      </div>
    </div>
  )
}

export default App