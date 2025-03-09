import { useState } from "react";
import axios from 'axios';
import { Box, Input, Button, VStack, HStack, Stack, Text, Heading } from "@chakra-ui/react";
import ResponseBubble from './components/ResponseBubble';
import Sidebar from './components/Sidebar';
import QueryBox from './components/QueryBox';
import QuestionBubble from './components/QuestionBubble';

const Chatbot = () => {

  const [queries, setQueries] = useState([])
  const [contexts, setContexts] = useState([])
  const [responses, setResponses] = useState([])
  const [isLoading, setIsLoading] = useState(false)
  const [allMessages, setAllMessages] = useState([])

  const handleSend = async (input) => {
    if (input.trim()) {
      try {
        setIsLoading(true);
        const messagesBeforeSending = [
          ...allMessages,
          { text: input, sender: "user" },
          { text: "", sender: "bot" }
        ];
        setAllMessages(messagesBeforeSending);
        // console.log('All messages before sending:', messagesBeforeSending);
        const res = await axios.post('http://127.0.0.1:5000/query', {
          new_query: input,
          queries: queries,
          contexts: contexts,
          responses: responses
        });
        console.log('Response:', res.data);
        setQueries(res.data.queries);
        setContexts(res.data.contexts);
        setResponses(res.data.responses);

        setAllMessages((prevMessages) => {
          let updatedMessages = [...prevMessages];
          updatedMessages[updatedMessages.length - 1].text = res.data.responses[res.data.responses.length - 1];
        //   console.log('Updated messages:', updatedMessages);
          return updatedMessages;
        });

      } catch (error) {
        console.error('Error querying the LLM:', error);
        setAllMessages((prevMessages) => {
          let updatedMessages = [...prevMessages];
          updatedMessages[updatedMessages.length - 1].text = "Error querying the LLM";
          return updatedMessages;
        });

      } finally {
        setIsLoading(false);
        setAllMessages((prevMessages) => {
        //   console.log('All messages finally:', prevMessages);
          return prevMessages;
        });
      }
    }
  };

    return (
        <Box
            display="flex"
            flexDirection="column"
            justifyContent="center" // Always starts centered
            alignItems="center"
            height="100vh"
            padding="10px"
            backgroundColor="#FFFFFF"
        >
            <Box
                width="95%"
                maxWidth="800px"
                border="1px"
                borderRadius="md"
                padding="10px"
                display="flex"
                flexDirection="column"
                height={allMessages.length > 0 ? "100vh" : "auto"} // Expands when messages appear
            >
                {allMessages.length > 0 && (
                    <Box
                        flex="1" // Pushes input box down
                        overflowY="auto"
                        padding="10px"
                        borderRadius="md"
                    >
                        {allMessages.map((msg, idx) => (
                            <HStack key={idx} justify={msg.sender === "user" ? "flex-end" : "flex-start"}>
                                {msg.sender === "user" ? (
                                    <QuestionBubble content={msg.text} />
                                ) : (
                                    <ResponseBubble content={msg.text} />
                                )}
                            </HStack>
                        ))}
                    </Box>
                )}
                {/* <Stack display="flex" justifyContent="center">
                    <Box background="blue" color="black">How Can I Help You Today?</Box>
                    <Box>
                        <QueryBox onQuerySubmit={handleSend} />
                    </Box>
                </Stack> */}

                {/* Input and Send Button */}
                <VStack gap="30px">
                  <Heading color="black" size="4xl">How can I help you today?</Heading>

                  <QueryBox onQuerySubmit={handleSend} />

                </VStack>
            </Box>
        </Box>
    );
};

export default Chatbot;