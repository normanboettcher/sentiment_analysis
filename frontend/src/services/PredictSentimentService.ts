import { SentimentResponse } from "@frontend/client/Response"

export interface PredictSentimentService {
    getReviewSentiment(review:string): Promise<SentimentServiceResponse>
}

type SentimentServiceResponse = {
    isError: boolean, response: SentimentResponse
}