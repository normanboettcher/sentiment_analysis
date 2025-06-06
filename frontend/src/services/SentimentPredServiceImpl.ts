import { SentimentResponse } from "@frontend/client/Response";
import {
  ResponseValidator,
  useResponseValidator,
} from "@frontend/client/ResponseValidator";
import { useRestClient } from "@frontend/client/RestClient";
import { PredictSentimentService } from "./PredictSentimentService";
import { AxiosError } from "axios";

export type ReviewPost = { review: string };

export class SentimentPredService implements PredictSentimentService {
  public async getReviewSentiment(review: string) {
    const postRequest: ReviewPost = { review: review };
    const responseValidator: ResponseValidator = useResponseValidator();

    try {
      const res = await this.postReview(postRequest);
      return Promise.resolve({
        isError: responseValidator.isErrorResponse(res.data),
        response: { sentiment: res.data.sentiment, error: res.data.error },
      });
    } catch (e) {
      if (e instanceof AxiosError) {
        return Promise.resolve({
          isError: true,
          response: { error: `request failed: ${e.response?.data.error ?? e.message}` }
        });
      }
      throw e;
    }
  }

  private async postReview(request: ReviewPost) {
    const restClient = useRestClient();
    return await restClient.doPost<SentimentResponse, ReviewPost>(
      "predict",
      request
    );
  }
}

export const useSentimentPredService = () => new SentimentPredService();
