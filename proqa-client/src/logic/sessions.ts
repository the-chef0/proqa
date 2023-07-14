import { get, writable, type Writable } from 'svelte/store';
import { MessageType, type Message, type Source, RatingState, type FAQEntry } from './types';
import { env } from '$env/dynamic/public';

/**
 * All statusses for whether a session is shown
 */
export enum SessionStatus {
  Pinned,
  Normal,
  Archived
}

/**
 * Keeps track of sessions and their relevant parts
 */
export type Session = {
  title: string;
  sessionID: string;
  type: SessionStatus;
  color: string;
};

/**
 * Dictionary mapping sessions to messages.
 */
export const chatSessions: Writable<Record<string, Message[]>> = writable({});

/**
 * Indicates either that there is no selected chat session or it's session id
 */
export const chatSessionID: Writable<null | string> = writable(null);

/**
 * Tracks all known sessions for the user
 */
export const knownSessions: Writable<Session[]> = writable([]);

/**
 * FAQ entries
 */
export const faqEntries: Writable<FAQEntry[]> = writable([]);

/**
 * Tracks title shown in chat window.
 */
export const chatTitle: Writable<string> = writable('');

/**
 * Tracks whether the confirmation dialog for deletion should be shown.
 */
export const errorMessage: Writable<string> = writable('');

/**
 * Tracks whether the confirmation dialog for deletion should be shown.
 */
export const sessionToDelete: Writable<Session | null> = writable(null);

/**
 * Stores if stream is in progress.
 */
export const isStreaming: Writable<boolean> = writable(false);

/**
 * Resets current session ID so a new one can be created. Also clears the chat title.
 */
export function clearSessionID() {
  chatTitle.set('');
  chatSessionID.set(null);
}

/**
 * Sets the current active chat to the ID given.
 * @param sessionID id of the session to change to
 * @returns nothing
 */
export async function setActiveChatSession(sessionID: string): Promise<void> {
  chatSessionID.set(sessionID);

  // set chat title
  let title = 'Title not found'; //placeholder
  get(knownSessions).every((session) => {
    if (session.sessionID === sessionID) {
      title = session.title;
      return false;
    }
    return true;
  });
  chatTitle.set(title);

  // get previous questions from API
  const sessionDict: Record<string, Message[]> = get(chatSessions);

  if (sessionDict[sessionID] === undefined) {
    const url = env.PUBLIC_API_URL + '/api/chat/messages/';
    const headers = {
      'Content-Type': 'application/json'
    };
    const body = JSON.stringify({ session: sessionID });

    return fetch(url, {
      method: 'POST',
      headers,
      body,
      credentials: 'include'
    })
      .then((res) => res.json())
      .then((res) => {
        // Get all messages
        const messages: Message[] = [];
        for (const message_json of res.messages) {
          // Set sources
          const sources: Source[] = [];
          if (message_json.source != undefined) {
            // Check if source is defined
            const source: Source = {
              name: message_json.source.title,
              link: message_json.source.filepath,
              context: message_json.source.context
            };
            sources.push(source);
          }

          // Set message
          const message: Message = {
            messageID: message_json.id,
            type: message_json.is_answer ? MessageType.Answer : MessageType.Question,
            content: message_json.content,
            streaming: false,
            sources: sources,
            rating: message_json.is_answer ? ratingToState(message_json.rating) : undefined
          };
          messages.push(message);
        }

        chatSessions.update((dict) => {
          dict[sessionID] = messages;
          return dict;
        });
      })
      .catch((error) => {
        setErrorMessage('Could not retrieve chat messages for chat: ' + sessionID, error);
      });
  }
}

/**
 * Get FAQ entries from the API and save them in the fAQEntries
 * @param messageNumber upperbound of number of messages to get
 * @returns nothing
 */
export async function getFAQEntries(messageNumber: number): Promise<void> {
  const url = env.PUBLIC_API_URL + '/api/faq/entries/';
  const headers = {
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({ number: messageNumber });

  return fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) => res.json())
    .then((res) => {
      // Get all FAQ entries
      const faqEntryList: FAQEntry[] = [];
      for (const faqEntry_json of res.faq_entries) {
        // Set faqQuestion
        const faqEntry: FAQEntry = {
          faqID: faqEntry_json.id,
          question: faqEntry_json.question,
          answer: faqEntry_json.answer
        };
        faqEntryList.push(faqEntry);
      }

      faqEntries.set(faqEntryList);
    })
    .catch((error) => {
      setErrorMessage('Could not retrieve FAQ entries', error);
    });
}

/**
 * Converts a rating number to a rating state.
 * @param rating rating number
 * @returns rating state
 */
export function ratingToState(rating: number): RatingState {
  switch (rating) {
    case 1:
      return RatingState.Positive;
    case -1:
      return RatingState.Negative;
    default:
      return RatingState.Neutral;
  }
}

/**
 * Converts a hiding and pinned status to a session status.
 * @param is_hidden whether the session is hidden
 * @param is_pinned whether the session is pinned
 * @returns session status
 */
export function statusToState(is_hidden: boolean, is_pinned: boolean): SessionStatus {
  if (is_hidden && is_pinned) {
    setErrorMessage('Session cannot be both hidden and pinned', null);
    return SessionStatus.Normal;
  }

  if (is_hidden) {
    return SessionStatus.Archived;
  } else if (is_pinned) {
    return SessionStatus.Pinned;
  } else {
    return SessionStatus.Normal;
  }
}

/**
 * Generates a random light color
 * @returns random color in rgb format
 */
export function getRandomColor(): string {
  // Create a color with minimum values to avoid very dark colors
  const minColorValue = 100;

  // Generate each of the three parts (red, green, blue) of the color
  const redPart = Math.floor(Math.random() * (255 - minColorValue) + minColorValue);
  const greenPart = Math.floor(Math.random() * (255 - minColorValue) + minColorValue);
  const bluePart = Math.floor(Math.random() * (255 - minColorValue) + minColorValue);

  // Return the color as an RGB string
  return `rgb(${redPart},${greenPart},${bluePart})`;
}

/**
 * Set error message for 10 seconds
 * @param message message of the error
 * @param error error object if available
 * @returns nothing
 */
export async function setErrorMessage(message: string, error: Error | null): Promise<void> {
  // Log the error message
  console.error(message);

  if (error != null) console.error(error);

  // Update the error message
  await errorMessage.update(() => message);

  // Clear the error message after 10 seconds
  setTimeout(() => {
    errorMessage.update(() => '');
  }, 10000);
}

/**
 * Generate chat title from question
 * @param questionInput the question itself
 * @param length length of the title
 * @returns chat title
 */
export function generateChatTitle(questionInput: string, length: number): string {
  const dots = questionInput.length > length ? '...' : '';
  const title = questionInput.substring(0, length) + dots;
  return title;
}

/**
 * Creates a new chat session and sets the current session to the new one using its ID.
 * Question title is passed to generate an appropriate title for the session.
 * @param questionInput the question itself
 * @returns nothing
 */
export async function createNewChatSession(questionInput: string): Promise<void> {
  const url = env.PUBLIC_API_URL + '/api/chat/creation/';
  const headers = {
    'Content-Type': 'application/json'
  };

  const chatColor = getRandomColor();

  // Get question input and convert it to title by truncating it to 50 characters
  // Add '...' if the question is longer than 50 characters
  const title = generateChatTitle(questionInput, 50);
  const body = JSON.stringify({ title: title, color: chatColor });

  return fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) => res.json())
    .then((res) => {
      if (typeof res.id !== 'string') {
        setErrorMessage('Could not retrieve new chat session ID', null);
        return;
      }

      const sessionID: string = res.id as string;

      chatSessionID.set(sessionID);
      const session: Session = {
        title: title,
        sessionID: sessionID,
        type: SessionStatus.Normal,
        color: chatColor
      };
      knownSessions.update((arr) => [session, ...arr]);

      chatTitle.set(title);
    })
    .catch((error) => {
      setErrorMessage('Could not retrieve new chat session ID', error);
    });
}

/**
 * Gets all previous session IDs of the user and stores it in global state.
 * @returns nothing.
 */
export async function getChatSessions(): Promise<void> {
  const url = env.PUBLIC_API_URL + '/api/chat/history/';
  const headers = {
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({});

  return fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) => res.json())
    .then((res) => {
      const arrayOfSessions: Session[] = res.chats.map(
        (obj: {
          session_id: number;
          title: string;
          hidden: boolean;
          pinned: boolean;
          color: string;
        }) => ({
          sessionID: obj.session_id,
          title: obj.title,
          type: statusToState(obj.hidden, obj.pinned),
          color: obj.color
        })
      );

      knownSessions.set(arrayOfSessions);
    })
    .catch((error) => {
      setErrorMessage('Could not retrieve chat session IDs', error);
    });
}

/**
 * Hide chat session from the user.
 * @param session which to hide
 * @returns nothing
 */
export async function hideChatSession(session: Session): Promise<void> {
  const sessionID = session.sessionID;

  // Get the session status
  const visibility =
    session.type == SessionStatus.Archived ? SessionStatus.Normal : SessionStatus.Archived;

  // Send the change to the API
  const url = env.PUBLIC_API_URL + '/api/chat/hiding/';
  const headers = {
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({
    hide: visibility == SessionStatus.Archived,
    chat_session_id: sessionID
  });
  await fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) =>
      // check for failure
      res.json()
    )
    .catch((error) => {
      setErrorMessage('Could not save hiding the chat session', error);
    });

  // Update the session status
  knownSessions.update((arr) => {
    const index = arr.findIndex((s) => s.sessionID == sessionID);
    if (index == -1) {
      setErrorMessage('Could not hide chat session: session not found', null);
      return arr;
    }
    arr[index].type = visibility;
    return arr;
  });
}

/**
 * Pin chat session from the user.
 * @param session which to pin
 * @returns nothing
 */
export async function pinChatSession(session: Session): Promise<void> {
  const sessionID = session.sessionID;

  // Get the session status
  const pinned = session.type == SessionStatus.Pinned ? SessionStatus.Normal : SessionStatus.Pinned;

  // Send the change to the API
  const url = env.PUBLIC_API_URL + '/api/chat/pinning/';
  const headers = {
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({
    pin: pinned == SessionStatus.Pinned,
    chat_session_id: sessionID
  });
  await fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) =>
      // check for failure
      res.json()
    )
    .catch((error) => {
      setErrorMessage('Could not save pining the chat session', error);
    });

  // Update the session status
  knownSessions.update((arr) => {
    const index = arr.findIndex((s) => s.sessionID == sessionID);
    if (index == -1) {
      setErrorMessage('Could not pin chat session: session not found', null);
      return arr;
    }
    arr[index].type = pinned;
    return arr;
  });
}

/**
 * Delete chat session from the user.
 * @param session which to delete
 * @returns nothing
 */
export async function deleteChatSession(session: Session): Promise<void> {
  const sessionID = session.sessionID;

  // Send the change to the API
  const url = env.PUBLIC_API_URL + '/api/chat/deletion/';
  const headers = {
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({ chat_session_id: sessionID });
  await fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) =>
      // check for failure
      res.json()
    )
    .catch((error) => {
      setErrorMessage('Could not save deleting the chat session', error);
    });

  // Update the session status
  knownSessions.update((arr) => {
    const index = arr.findIndex((s) => s.sessionID == sessionID);
    if (index == -1) {
      setErrorMessage('Could not delete chat session: session not found', null);
      return arr;
    }
    arr.splice(index, 1);
    return arr;
  });

  // Get active chat session id
  let activeSessionID: null | string = null;
  const unsub = chatSessionID.subscribe((id) => (activeSessionID = id));
  unsub();

  // If the deleted session is the active session, clear the active session
  if (activeSessionID === sessionID) {
    clearSessionID();
  }
}

/**
 * Call to show the pop up message
 * @param session session to delete
 * @returns nothing
 */
export async function deleteConfirmation(session: Session): Promise<void> {
  sessionToDelete.update(() => session);
}

/**
 * Call to delete the chat session and hide the pop-up
 * @param session session to delete
 * @returns nothing
 */
export async function confirmDeletion(session: Session): Promise<void> {
  await deleteChatSession(session);
  await hidePopUpMessage();
}

/**
 * Call to hide the pop up message
 * @returns nothing
 */
export async function hidePopUpMessage(): Promise<void> {
  sessionToDelete.update(() => null);
}

/**
 * Send a rating of a chat session to the backend.
 * @param answerID id of the answer to rate
 * @param rating rating to give to the answer
 * @returns nothing
 */
export async function rateAnswer(answerID: string, rating: RatingState): Promise<void> {
  // Send the change to the API
  const url = env.PUBLIC_API_URL + '/api/answer/rating/';
  const headers = {
    'Content-Type': 'application/json'
  };

  const positive: string = RatingState.Positive.toString();
  const neutral: string = RatingState.Neutral.toString();
  const negative: string = RatingState.Negative.toString();
  const conversion: { [rating: string]: number } = {};
  conversion[positive] = 1;
  conversion[neutral] = 0;
  conversion[negative] = -1;

  const body = JSON.stringify({ answer_id: answerID, rating: conversion[rating] });
  await fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) =>
      // check for failure
      res.json()
    )
    .catch((error) => {
      setErrorMessage('Could not save rating the answer', error);
    });
}

/**
 * Finds a session by its ID in known sessions.
 * @param sessionID to look up
 * @returns session with that ID
 */
export function getSessionByID(sessionID: string): Session {
  const session: Session | undefined = get(knownSessions).find((s) => s.sessionID === sessionID);

  if (session === undefined) {
    throw Error('Could not find session with ID' + sessionID);
  } else {
    return session;
  }
}

/**
 * Sets the rating of the answer to given state.
 * If positive or negative is passed while this is the current state, it will set it neutral instead.
 * @param message what message to change the rating of
 * @param ratingChange what to update the answer rating to
 */
export function changeRating(message: Message, ratingChange: RatingState) {
  switch (ratingChange) {
    case RatingState.Neutral:
      message.rating = ratingChange;
      break;
    case RatingState.Positive:
      message.rating =
        message.rating != RatingState.Positive ? RatingState.Positive : RatingState.Neutral;
      break;
    case RatingState.Negative:
      message.rating =
        message.rating != RatingState.Negative ? RatingState.Negative : RatingState.Neutral;
      break;
  }

  // Update the rating in the database
  rateAnswer(message.messageID, message.rating);
}

/**
 * Generates a UUID. Not cryptographically strong.
 * @returns UUID
 */
export function generateID(): string {
  const arr = new Uint8Array(20);
  window.crypto.getRandomValues(arr);
  return Array.from(arr, (dec) => dec.toString(16).padStart(2, '0')).join('');
}

/**
 * Sends question to back end and adds it to internal message store.
 * @param messageID ID of the chat message
 * @param sessionID ID of the chat session
 * @param question text of the question
 * @param callback what function to execute after the question is sent
 */
export async function addQuestion(
  messageID: string,
  sessionID: string,
  question: string,
  callback: (sessionID: string, message: Message) => void
) {
  const message: Message = {
    messageID: messageID,
    type: MessageType.Question,
    content: question,
    streaming: true
  };

  chatSessions.update((rec) => {
    if (rec[sessionID] === undefined) {
      // new chat session
      rec[sessionID] = [];
    }

    // add message to session
    rec[sessionID].push(message);

    return rec;
  });

  const url = env.PUBLIC_API_URL + '/api/question/';
  const headers = {
    'Content-Type': 'application/json' // Set the appropriate Content-Type for your API
  };
  const body = JSON.stringify({ question: question, session: sessionID }); // Replace with your request payload
  await fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((response) => response.json())
    .then(
      (response: { context: string; source: string; question_id: string; answer_id: string }) => {
        message.messageID = response.question_id;

        const source: Source = {
          name: response.source,
          link: response.source,
          context: response.context
        };

        const answer: Message = {
          messageID: response.answer_id,
          type: MessageType.Answer,
          content: '',
          sources: [source],
          rating: RatingState.Neutral,
          streaming: true
        };

        callback(sessionID, answer);
      }
    )
    .catch((error) => {
      setErrorMessage('Could not send question', error);
    });
}

/**
 * Save message to the backend
 * @param message_content Content of the message
 * @param message_type Type of the message
 * @param question_id ID of the question
 * @returns Message ID of the saved message or null if an error occurred
 */
export async function saveMessage(
  message_content: string,
  message_type: MessageType,
  question_id: string | null
): Promise<Message | null> {
  const url = env.PUBLIC_API_URL + '/api/chat/saving/';
  const headers = {
    'Content-Type': 'application/json'
  };
  const body = JSON.stringify({
    session: get(chatSessionID),
    content: message_content,
    is_answer: message_type,
    question_id: question_id
  });

  return fetch(url, {
    method: 'POST',
    headers,
    body,
    credentials: 'include'
  })
    .then((res) => res.json())
    .then((res) => {
      const message: Message = {
        messageID: res.message_id,
        type: message_type,
        content: message_content,
        streaming: false
      };

      return message;
    })
    .catch((error) => {
      setErrorMessage('Could not save message', error);
      return null;
    });
}
