export interface IMessageService {
  getMessageFromSentiment: (
    sentiment: "negative" | "positive"
  ) => string ;
}
