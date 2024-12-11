import { useState } from 'react'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
// import ReactTypingEffect from 'react-typing-effect'
import './App.css'
import { FaArrowCircleUp } from "react-icons/fa";

function App() {
  const [queryField, setQueryField] = useState('')
  const [queries, setQueries] = useState([])
  const [contexts, setContexts] = useState([])
  const [responses, setResponses] = useState([])
  const [isLoading, setIsLoading] = useState(false)

  const handleQuery = async () => {
    console.log('QueryField:', queryField)
    const currentQuery = queryField
    setQueryField("")
    console.log('New Query:', currentQuery)
    setIsLoading(true)
    try {
      const res = await axios.post('http://127.0.0.1:5000/query', {
        new_query: currentQuery,
        queries: queries,
        contexts: contexts,
        responses: responses
      })
      console.log('Response:', res.data)
      setQueries(res.data.queries)
      setContexts(res.data.contexts)
      setResponses(res.data.responses)
    } catch (error) {
      console.error('Error querying the LLM:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const handleKeyPress = (event) => {
    if (event.key === 'Enter') {
      event.preventDefault()
      handleQuery()
    }
  }

  return (
    <div className="App">
       <img src="/Pronova-green-logo.jpg" alt="Pronova Logo" />
      <h1>AI Vet Support</h1>
      <div>
      <div style={{ display: 'flex', alignItems: 'center', height: '70vh'}}>
      <textarea
        value={queryField}
        onChange={(e) => setQueryField(e.target.value)}
        placeholder="Enter your query here"
        style={{ width: '800px', height: '100px', marginRight: '5px' }} 
      />
      <button onClick={handleQuery} disabled={isLoading} style={{ cursor: 'pointer' }}>
        <FaArrowCircleUp color = "#29CC96"/>
      </button>
    </div>
        <div className="response" style={{maxHeight: '400px', overflowY: 'auto', marginTop: '20px' }}>
          {responses.map((response, index) => (
            <div key={index} style={{ marginBottom: '20px' }}>
              <h3>Query:</h3>
              <ReactMarkdown>{queries[index]}</ReactMarkdown>
              <h3>Response:</h3>
              <ReactMarkdown>{responses[index]}</ReactMarkdown>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default App