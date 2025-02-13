import { useState } from 'react'
// import axios from 'axios'
import ReactMarkdown from 'react-markdown'
// import ReactTypingEffect from 'react-typing-effect'
import './App.css'

function App() {
  const [queryField, setQueryField] = useState('')
  const [queries, setQueries] = useState([])
  const [contexts, setContexts] = useState([])
  const [responses, setResponses] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [files, setFiles] = useState([]) // i want files to be an array of strings:
  const [showFiles, setShowFiles] = useState(false);

  


  const handleQuery = async () => {
    console.log('QueryField:', queryField)
    const currentQuery = queryField
    setQueryField("")
    console.log('New Query:', currentQuery)
    setIsLoading(true)
  
    try {
      const res = await fetch('https://pronova-llm-1-c672684149ef.herokuapp.com/query', {
        method: 'POST', // Use POST, not GET
        headers: {
          'Content-Type': 'application/json', // Set the content type
        },
        body: JSON.stringify({
            new_query: currentQuery,
            queries: queries,
            contexts: contexts,
            responses: responses,
            files: files
        }),
      });
      
      if (!res.ok) {
        throw new Error(`HTTP error! Status: ${res.status}`);
      }
  
      const data = await res.json();

      console.log('Response:', data);
      // setQueries(res.data.queries)
      // setContexts(res.data.contexts)
      // setResponses(res.data.responses)
      setQueries(data.queries || []);
      setContexts(data.contexts || []);
      setResponses(data.responses || []);
      setFiles(data.files || []);
      console.log('files:', data.files)
      const flattenedFiles = data.files.flat();
      setFiles(flattenedFiles);




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
      <h1>Pronova AI Vet Support - Temporarily Down!</h1>
      <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column', height: '70vh' }}>
        <textarea
          value={queryField}
          onChange={(e) => setQueryField(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Enter your query here"
          style={{ width: '800px', height: '100px', marginBottom: '20px' }}
        />
        <button onClick={handleQuery} disabled={isLoading}>Submit</button>
        <div className="response" style={{ width: '800px', maxHeight: '400px', overflowY: 'auto', marginTop: '20px' }}>
          {responses.map((response, index) => (
            <div key={index} style={{ marginBottom: '20px' }}>
              <h3>Query:</h3>
              <ReactMarkdown>{queries[index]}</ReactMarkdown>
              <h3>Response:</h3>
              <ReactMarkdown>{responses[index]}</ReactMarkdown>
            </div>
          ))}
        </div>
        <button onClick={() => setShowFiles(!showFiles)} style={{ marginTop: '20px' }}>
          {showFiles ? 'Hide Files' : 'Show Files'}
        </button>
        {showFiles && (
          <div style={{ width: '800px', marginTop: '20px' }}>
            <h3>Files Used:</h3>
            <ul style={{ listStyleType: 'none', paddingLeft: '0' }}>
              {files.map((file, fileIndex) => (
                <li key={fileIndex}>
                  <ReactMarkdown>{file}</ReactMarkdown>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  )
}

export default App