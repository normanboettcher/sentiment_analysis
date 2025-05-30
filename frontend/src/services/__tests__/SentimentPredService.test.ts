import { vi, it, expect, describe } from "vitest";
import * as rest_client from "../../client/RestClient";
import { useSentimentPredService } from "../SentimentPredServiceImpl";

vi.mock("axios");
const restClientSpy = vi.spyOn(rest_client, "useRestClient");

describe("negative testcases for getReviewSentiment", () => {
  it(
    "should throw an error if post request fails and error is not of type " +
      "AxiosError",
    async () => {
      const thrownError = new Error();
      const doPostMock = vi.fn().mockRejectedValue(thrownError);
      restClientSpy.mockReturnValue({
        doPost: doPostMock,
      } as unknown as rest_client.RestClient);

      const underTest = useSentimentPredService();

      await expect(underTest.getReviewSentiment("some_review")).rejects.toThrow(
        thrownError
      );
      expect(doPostMock).toHaveBeenCalledWith("predict", {
        review: "some_review",
      });
    }
  );
});
