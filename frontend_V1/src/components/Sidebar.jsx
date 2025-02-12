import { Button } from "@chakra-ui/react"
import { SlMenu } from "react-icons/sl";
import { IconButton } from "@chakra-ui/react"
import {
    DrawerActionTrigger,
    DrawerBackdrop,
    DrawerBody,
    DrawerCloseTrigger,
    DrawerContent,
    DrawerFooter,
    DrawerHeader,
    DrawerRoot,
    DrawerTitle,
    DrawerTrigger,
} from "@/components/ui/drawer"

const Sidebar = () => {
    return (
        <DrawerRoot size="sm" placement="start">
            <DrawerBackdrop />
            <DrawerTrigger asChild>
                <IconButton aria-label="Open Sidebar" size="md" backgroundColor = "tan">
                    <SlMenu />
                </IconButton>
            </DrawerTrigger>
            <DrawerContent offset="0" style={{ backgroundColor: 'tan' }}>
                <DrawerHeader>
                    <DrawerTitle>Chat History</DrawerTitle>
                </DrawerHeader>
                <DrawerBody>
                    
                </DrawerBody>
                <DrawerFooter>
                    <DrawerActionTrigger asChild>
                        <Button variant="outline">New Chat</Button>
                    </DrawerActionTrigger>
                </DrawerFooter>
                <DrawerCloseTrigger />
            </DrawerContent>
        </DrawerRoot>
    )
}

export default Sidebar
