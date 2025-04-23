import { SentimentResponse } from "@frontend/client/Response"
import { AxiosResponse } from "axios"

export interface PredictSentimentService {
    getReviewSentiment(review:string): Promise<AxiosResponse<SentimentServiceResponse>>
}

type SentimentServiceResponse = {
    isError: boolean, response: SentimentResponse
}