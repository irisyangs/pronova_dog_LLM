import { SkeletonText, SkeletonCircle } from "@/components/ui/skeleton"
import { HStack, Stack } from "@chakra-ui/react"
import { Icon, Spinner } from "@chakra-ui/react"
import { FaPaw } from "react-icons/fa";
import { useState } from "react";
import {
  ProgressCircleRing,
  ProgressCircleRoot,
} from "@/components/ui/progress-circle"
import pronovaLogo from "@/assets/pronovaLogo.png"

    export const ResponseBubble = () => {
        const [loading, setLoading] = useState(false);

        return (
            <HStack>
                {loading ? (
                    <ProgressCircleRoot value={null} size="sm" pb="20px">
                        <ProgressCircleRing cap="round" color="teal"/>
                    </ProgressCircleRoot>
                ) : (
                    <Icon 
                        fontSize="60px" 
                        color="teal" 
                        pb="20px"
                    >
                        <FaPaw/>
                    </Icon>
                )}
                <SkeletonText noOfLines={3} maxW="33vw" w="30vw" color="lightgrey"/>
            </HStack>
        )
    }
export default ResponseBubble;