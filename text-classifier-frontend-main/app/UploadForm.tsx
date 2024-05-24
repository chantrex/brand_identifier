'use client'
import { use, useEffect, useState } from 'react';
import { 
    Flex,
    Box,
    Button,
    Input,
    Text,
    FormHelperText,
    Heading,
    InputGroup,
    InputRightElement,
    Divider,
    CheckboxIcon,
    HStack,
    FormControl,
} from "@chakra-ui/react";
import axios from 'axios';

const UploadForm = () => {
    const [isInputFocused, setIsInputFocused] = useState(false);
    const [description, setDescription] = useState<string | null>('')
    const [response, setResponse] = useState<any | null>();
    const [isLoading, setIsloading] = useState<boolean>(false)
    const [delayMessage, setDelayMessage] = useState<string | null>(null);


    const handleFocus = () => {
        setIsInputFocused(true);
      };
    
    const handleBlur = () => {
    setIsInputFocused(false);
    };

    const handleDescriptionChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        setDescription(e.target.value)
    }

    const handleCleanInput = () => {
        setDescription('')
    }

    // Logic when form data is submitted
    const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        setIsloading(true)
        setDelayMessage(null)

        const timeout5 = setTimeout(() => {
            setDelayMessage('Connecting to the API service ...');
          }, 5000);
      
          const timeout15 = setTimeout(() => {
            setDelayMessage('Still processing, please stay tight...');
          }, 15000);
      
          const timeout20 = setTimeout(() => {
            setDelayMessage('Spinning up the connection, almost there!');
          }, 20000);

        // The API url should be in an ENV variable
        try {
            const res = await axios.post("https://clasify-text-from-product-tmb.onrender.com/process-text/", {text: description}, {
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            setResponse(res.data);
            clearTimeout(timeout5)
            clearTimeout(timeout15)
            clearTimeout(timeout20)
        } catch (error) {
            alert(`Error sending text:\n ${error}`);
        } finally {
            setIsloading(false)
            clearTimeout(timeout5)
            clearTimeout(timeout15)
            clearTimeout(timeout20)
        }
        console.log('Response', response)
    };

    const messageOutput = (
        <Flex
            my={'4'}
            bg={'#1a202c'}
            w={'90%'}
            p={'4'}
            alignSelf={'end'}
            color={'white'}
            borderRadius={'5'}
        >
            <HStack>
                <Text 
                    as={'b'}
                    mr={'4'}
                    p={'1'}
                    bg={'white'}
                    textAlign={'center'}
                    borderRadius={'2'}
                    color={'#1a202c'}
                >
                    Response
                </Text>
                <Text>{response && response.text_result}</Text>
            </HStack>
        </Flex>
    );

    const loadingMessage = (
        <Box
            bg={'yellow.500'}
            w={delayMessage ? '100%' : '150px'}
            mt={'2'}
            p={'4'}
            rounded={'lg'}
            color={'white'}
            alignSelf={'center'}
            fontWeight={'bold'}
        >
            <Text>Loading...</Text>
            {delayMessage && <Text mt={2} color={'#1a202c'}>{delayMessage}</Text>}
        </Box>
    )

    const cleanButton = (
        <Button 
            type="submit"
            h={'2.5rem'}
            my={'4'}
            size={'sm'}
            borderRadius={'10px'}
            fontSize={'large'}
            transition={'0.1s all ease-in-out'}
            _hover={{bg: 'cyan'}}
            _active={{
                transform: "scale(.9)",
                bg: "#1a202c",
                color: 'white'
            }}
            onClick={handleCleanInput}
        >
            Clean Input
        </Button>
    )

    return (
        <Flex
            w={{ base: '90%', md: '600px' }}
            p={'4'}
            direction={'column'}
            bg={'rgba(255, 255, 255, 0.05)'}
            borderRadius={'10px'}
            boxShadow={isInputFocused ? '10px 10px white' : '0px'}
            transition={'0.3s all ease-in'}
        >
            <Heading as={'h1'} color={'rgba(255, 255, 255, 0.8)'} textAlign={'center'} my={'2'}>
                Product Brand Identifier
            </Heading>
            <Divider mb={'4'} />

            {description && cleanButton}
            <form onSubmit={handleSubmit}>
                <FormControl textAlign={'center'}>
                    <FormHelperText fontWeight={'bold'} mb={'2'}>Example: Great Value Hazelnut Milk Chocolate, 100 g</FormHelperText>
                    <InputGroup size={'md'}>
                        <Input 
                            type='text'
                            color={'rgba(255, 255, 255, 0.8)'}
                            borderRadius={'30px'}
                            h={'3rem'}
                            pr={'4.5rem'}
                            placeholder={'Type your description ...'}
                            focusBorderColor='lime'
                            onChange={handleDescriptionChange}
                            value={description || ''}
                            onFocus={handleFocus}
                            onBlur={handleBlur}
                            required
                        />
                        <InputRightElement w={'4.5rem'} h={'100%'}>
                            <Button 
                                type="submit"
                                h={'2.5rem'}
                                w={'2.5rem'}
                                ml={'23px'}
                                size={'sm'}
                                borderRadius={'50%'}
                                fontSize={'large'}
                                transition={'0.2s all ease-in-out'}
                                _hover={{bg: 'lime'}}
                                _active={{
                                    transform: "scale(1.1)",
                                    bg: "#1a202c",
                                    color: 'white'
                                }}
                            >
                                Go
                            </Button>
                        </InputRightElement>
                    </InputGroup>
                </FormControl>
            </form>
            
            {isLoading ? loadingMessage : response ? messageOutput : null}

        </Flex>
    );
};

export default UploadForm;
