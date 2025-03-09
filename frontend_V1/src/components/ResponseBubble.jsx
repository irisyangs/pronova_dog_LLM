import { SkeletonText, SkeletonCircle } from "@/components/ui/skeleton"
import { HStack, Stack, Box } from "@chakra-ui/react"
import { Icon, Spinner } from "@chakra-ui/react"
import { FaPaw } from "react-icons/fa";
import { useState, useEffect } from "react";
import {
  ProgressCircleRing,
  ProgressCircleRoot,
} from "@/components/ui/progress-circle"
import pronovaLogo from "@/assets/pronovaLogo.png"
import ReactMarkdown from 'react-markdown';
import { CSSTransition } from 'react-transition-group';
import './ResponseBubble.css'; // Import the CSS file for transitions

export const ResponseBubble = (props) => {
    const [loading, setLoading] = useState(true);
    const [content, setContent] = useState("");

    // When the incoming content changes, update the content and loading state.
    // The loading state is true when the content is empty, and false otherwise.
    useEffect(() => {
        console.log(props.content);
        setContent(props.content);
        if (props.content === "") {
            setLoading(true);
        } else {
            setLoading(false);
        }
    }, [props.content]);

    return (
        <Box>
            <style>
                @import url('https://fonts.googleapis.com/css2?family=Montserrat:ital,wght@0,100..900;1,100..900&display=swap');
            </style>
            {/* If the content is empty, show a loading spinner
            Otherwise, show the content */}
            {loading ? (
                <HStack m={4} align="start">
                    <ProgressCircleRoot value={null} size="sm" pb="20px">
                        <ProgressCircleRing cap="round" color="teal"/>
                    </ProgressCircleRoot>
                    <SkeletonText noOfLines={3} maxW="33vw" w="30vw" color="lightgrey"/>
                </HStack>
            ) : (
                <HStack m={4} align="start">
                    <Icon 
                        fontSize="60px" 
                        color="teal" 
                        pb="20px"
                    >
                        <FaPaw/>
                    </Icon>
                    <Box 
                        fontFamily="'Montserrat', sans-serif" 
                        fontSize="18px" 
                        color="teal" 
                        backgroundColor="#FFF6E5" 
                        padding="20px" 
                        borderRadius="5px 40px 40px 40px"
                        boxShadow="0px 5px 5px rgba(0, 0, 0, 0.37)"
                    >
                        <ReactMarkdown>{content}</ReactMarkdown>
                    </Box>
                </HStack>
            )}
        </Box>
    )
}
export default ResponseBubble;