/**
 * Possible types of messages in the chat window.
 */
export enum MessageType {
  Question,
  Answer
}

/**
 * Is a source where the backend has found information regarding user query.
 */
export type Source = {
  name: string;
  link: string;
  context: string;
};

/**
 * Possible states a rating can be in.
 */
export enum RatingState {
  Positive,
  Neutral,
  Negative
}

/**
 * Any type of message that is used in the chat window.
 */
export type Message = {
  messageID: string;
  type: MessageType;
  content: string;
  streaming: boolean;
  sources?: Source[];
  rating?: RatingState;
};

/**
 * FAQ message
 */
export type FAQEntry = {
  faqID: string;
  question: string;
  answer: string;
};
