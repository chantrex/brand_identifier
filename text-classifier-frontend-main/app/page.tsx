import { Box } from "@chakra-ui/react";
import UploadForm from "./UploadForm";

export default function Home() {
  return (
    <Box 
      as='main'
      w={'100vw'}
      h={'100vh'}
      display={'flex'}
      justifyContent={'center'}
      alignItems={'center'}
      flexDirection={'column'}
      bg={'#1a202c'}
    >
      <UploadForm />
    </Box>
  );
}
