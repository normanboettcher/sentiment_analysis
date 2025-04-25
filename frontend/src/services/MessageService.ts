import { IMessageService } from "./IMessageService";
import MessageFactory from "./MessageFactory";

export class SentimentMessageService implements IMessageService {
  public getMessageFromSentiment = (sentiment: "negative" | "positive"): string => {
      return MessageFactory.getMessage(sentiment);
  };
}

export const useSentimentMessageService = () => new SentimentMessageService();
