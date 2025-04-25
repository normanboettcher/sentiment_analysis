import { useSentimentMessageService } from '@frontend/services/MessageService';
import { PredictSentimentService } from '@frontend/services/PredictSentimentService';
import { useSentimentPredService } from '@frontend/services/SentimentPredService';
import { Box, Button, Stack, TextField, Typography } from '@mui/material';
import React, { useEffect, useState } from 'react';

const Welcome: React.FC = () => {
    const predService: PredictSentimentService = useSentimentPredService();
    const [review, setReview] = useState<string | undefined>();
    const [sentiment, setSentiment] = useState<'positive' | 'negative' | undefined>();
    const [error, setError] = useState<string | undefined>();
    const messageService = useSentimentMessageService();
    const [infoMessage, setInfoMessage] = useState<string | undefined>();

    useEffect(() => {
        sentiment && setInfoMessage(messageService.getMessageFromSentiment(sentiment));
    }, [sentiment])

    const onClick = async () => {
        const response = await predService.getReviewSentiment(review ?? '');
        console.log(`${response}`)
        if(response.isError) {
            setError(response.response.error)
        } else {
            setSentiment(response.response.sentiment)
        }
    }

    return (
        <Box>
            <Stack direction={'row'} spacing={2} width='100%' >
                <Box sx={{flex: 1}}></Box>
                <Box sx={{flex: 1}}>
                    <Stack spacing={2}>
                        <Typography>Please enter your review here:</Typography>
                        <TextField
                            data-testid={'review-textfield'}
                            onChange={(e) => setReview(e.target.value)}
                        />
                            <Box sx={{flex: 1}}>
                                {infoMessage && <Typography>{infoMessage}</Typography>}
                                {error && <Typography>{error}</Typography>}
                            </Box>
                       <Button
                            data-testid={'send-review-button'}
                            onClick={onClick}
                        >
                            Send Review
                        </Button>
                    </Stack>
                </Box>
                <Box sx={{flex: 1}}></Box>
            </Stack>
        </Box>
    )
}
export default Welcome;