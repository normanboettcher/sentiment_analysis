import { SentimentResponse } from "@frontend/client/Response";
import { ResponseValidator, useResponseValidator } from "@frontend/client/ResponseValidator";
import { useRestClient } from "@frontend/client/RestClient";
import { useRestClientConfig } from "@frontend/client/RestClientConfig";

export type ReviewPost = {review: string}

export class SentimentPredService {

    constructor(){}

    public async getReviewSentiment(review: string): Promise<{isError: boolean, response: SentimentResponse}> {
        const postRequest: ReviewPost = {review: review};
        //use default hostname and port
        const responseValidator: ResponseValidator = useResponseValidator()
        
        try {
            const res  = await this.postReview(postRequest);
            return Promise.resolve({
                isError: responseValidator.isErrorResponse(res),
                response: res
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