import { Box } from "@chakra-ui/react";

export const QuestionBubble = (props) => {
    return (
        <Box
            borderRadius="40px 5px 40px 40px"
            bg="teal.500"
            color="white"
            maxW="20vw"
            p={5}
            boxShadow="0px 2px 2px rgba(0, 0, 0, 0.37)"
        >
            {props.content}
        </Box>
    );
}

export default QuestionBubble;