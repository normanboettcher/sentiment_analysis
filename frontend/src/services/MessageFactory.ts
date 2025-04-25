type MessageType = 'positive' | 'negative';

class MessageFactory {
  private static messages: Record<MessageType, string> = {
    positive: "Thank you for your positive Feedback",
    negative: "We are sorry to hear that you did not like the movie"
  };

  static getMessage(type: MessageType): string {
    return this.messages[type];
  }
}

export default MessageFactory;
