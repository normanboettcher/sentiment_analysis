import { SentimentResponse } from "@frontend/client/Response";
import { ResponseValidator, useResponseValidator } from "@frontend/client/ResponseValidator";
import { useRestClient } from "@frontend/client/RestClient";
import { useRestClientConfig } from "@frontend/client/RestClientConfig";
import { PredictSentimentService } from "./PredictSentimentService";

export type ReviewPost = {review: string}

export class SentimentPredService implements PredictSentimentService {

    public async getReviewSentiment(review: string) {
        const postRequest: ReviewPost = {review: review};
        const responseValidator: ResponseValidator = useResponseValidator()
        
        try {
            const res  = await this.postReview(postRequest);
            return Promise.resolve({
                isError: responseValidator.isErrorResponse(res.data),
                response: {sentiment: res.data.sentiment, error: res.data.error}
            });
        } catch(e) {
            throw e;
        }
    }

    private async postReview(request: ReviewPost) {
        const clientConfig = useRestClientConfig();
        const restClient = useRestClient(clientConfig);
        return await restClient.doPost<SentimentResponse, ReviewPost>('predict', request);
    }
}

export const useSentimentPredService = () => new SentimentPredService();