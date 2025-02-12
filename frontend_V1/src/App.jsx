import { useState } from 'react';
import { Stack, Box } from '@chakra-ui/react';
import ResponseBubble from './components/ResponseBubble';
import Sidebar from './components/Sidebar';
import QueryBox from './components/QueryBox';
import QuestionBubble from './components/QuestionBubble';

function App() {
  const [questions, setQuestions] = useState([]);

  const handleQuerySubmit = (query) => {
    setQuestions([...questions, query]);
  };

  return (
    <div style={{ backgroundColor: '#fae8d2', height: '100vh', display: 'flex', flexDirection: 'column', justifyContent: 'space-between', alignItems: 'center' }}>
      <Sidebar></Sidebar>
      <Box width="40vw" mt="20px" display="flex" flexDirection="column" justifyContent="space-between" alignItems="center">
        {questions.map((question, index) => (
          <div key={index} style={{ width: '100%', alignSelf: 'flex-start'}}>
            <QuestionBubble content={question}/>
          </div>
        ))}
        <ResponseBubble/>
      </Box>

      <div style={{ width: '100%', display: 'flex', justifyContent: 'center', marginBottom: '20px', backgroundColor: 'blue' }}>
        <QueryBox onQuerySubmit={handleQuerySubmit} />
      </div>

    </div>
  );
}

export default App;
