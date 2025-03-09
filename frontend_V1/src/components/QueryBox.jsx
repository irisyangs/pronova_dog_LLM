import { useState, useEffect } from "react";
import { Textarea, IconButton, Box, Input, Button, VStack, HStack, Stack, Text, Heading } from "@chakra-ui/react";
import { FaArrowAltCircleUp } from "react-icons/fa";

export const QueryBox = ({ onQuerySubmit }) => {
    const [query, setQuery] = useState("");

    const handleSendQuery = () => {
        if (query.trim() !== "") {
            onQuerySubmit(query);
            setQuery("");
        }
    };

    const handleKeyPress = (event) => {
        if (event.key === "Enter") {
            event.preventDefault();
            handleSendQuery();
        }
    };

    useEffect(() => {
        const handleGlobalKeyPress = (event) => {
            if (event.key === "Enter") {
                event.preventDefault();
                handleSendQuery();
            }
        };

        document.addEventListener("keydown", handleGlobalKeyPress);

        return () => {
            document.removeEventListener("keydown", handleGlobalKeyPress);
        };
    }, [query]);

    return (
        <Box 
            position="relative" 
            width="100%"
            display="flex"
            alignItems="center"
            borderRadius="45px"
            border="2px solid #7FFFD4"
            bg="#FFF6E5"
            boxShadow="0px 5px 5px rgba(0, 0, 0, 0.37)"
            p="10px"
        >
            <Textarea 
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                onKeyPress={handleKeyPress}
                autoresize
                maxH="20rem"
                width="100%"
                borderRadius="45px"
                fontSize="18px"
                py="20px"
                pl="30px"
                pr="80px"  // Add padding for button space
                bg="transparent"
                placeholder="Type here to ask a question..."
                _placeholder={{ color: "#29CC96" }}
                color="#29CC96"
                border="none"
                focusBorderColor="transparent"
                _focus={{ outline: "none", boxShadow: "none", border: "none" }}
            />

            <IconButton 
                onClick={handleSendQuery}
                position="absolute"
                right="20px"
                size="lg"
                rounded="full"
                aria-label="Send Query"
                bg="#29CC96"
                _hover={{ bg: "#f5cb42" }}
            >
                <FaArrowAltCircleUp color="black"/>
            </IconButton>
        </Box>
    );
};

export default QueryBox;