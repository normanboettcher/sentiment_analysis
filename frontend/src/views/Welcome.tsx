import { useSentimentPredService } from '@frontend/services/SentimentPredService';
import { Box, Stack, TextField, Typography } from '@mui/material';
import React from 'react';

const Welcome: React.FC = () => {
    const predService = useSentimentPredService();

    return (
        <Box>
            <Stack direction={'row'} spacing={2} width='100%' >
                <Box sx={{flex:1}}></Box>
                <Box sx={{flex: 1}}>
                    <Stack spacing={2}>
                        <Typography>Please enter your review here:</Typography>
                        <TextField></TextField>
                    </Stack>
                </Box>
                <Box sx={{flex: 1}}></Box>
            </Stack>
        </Box>
    )
}
export default Welcome;