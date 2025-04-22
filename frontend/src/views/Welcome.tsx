import { PredictSentimentService } from '@frontend/services/PredictSentimentService';
import { useSentimentPredService } from '@frontend/services/SentimentPredService';
import { Box, Button, Stack, TextField, Typography } from '@mui/material';
import React, { useState } from 'react';

const Welcome: React.FC = () => {
    const predService: PredictSentimentService = useSentimentPredService();
    const [review, setReview] = useState<string | undefined>();
    const [sentiment, setSentiment] = useState<'positive' | 'negative' | undefined>();
    const [error, setError] = useState<string | undefined>();

    const onClick = async () => {
        const response = await predService.getReviewSentiment(review ?? '');
        if(response.isError) {
            setError(response.response.error)
        } else {
            setSentiment(response.response.sentiment)
        }
    }

    const generateReviewMessage = (): string => {
        if (sentiment === 'negative') {
            return 'We are sorry to hear that you did not like the movie'
        } 
        if (sentiment === 'positive') {
            return 'Thank you for your positive Feedback'
        }
        return error  !== undefined ? error : ''
    }
    console.log(`review: ${review}`)
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
                        {(sentiment || error) &&
                            <Box sx={{flex: 1}}>
                                <Typography>${generateReviewMessage()}</Typography>
                            </Box>
                        }
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