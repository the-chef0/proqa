import { afterAll, afterEach, beforeAll, describe, it, expect, beforeEach, test } from 'vitest';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import {
  chatSessions,
  chatSessionID,
  knownSessions,
  chatTitle,
  clearSessionID,
  setActiveChatSession,
  type Session,
  SessionStatus,
  ratingToState,
  statusToState,
  errorMessage,
  getRandomColor,
  setErrorMessage,
  createNewChatSession,
  getChatSessions,
  hideChatSession,
  pinChatSession,
  deleteChatSession,
  deleteConfirmation,
  confirmDeletion,
  hidePopUpMessage,
  sessionToDelete,
  rateAnswer,
  generateID,
  getSessionByID,
  changeRating,
  addQuestion,
  saveMessage,
  faqEntries,
  getFAQEntries
} from '../../logic/sessions';
import { get } from 'svelte/store';
import { vi } from 'vitest';
import createFetchMock from 'vitest-fetch-mock';
import { RatingState, type Message, MessageType } from '../../logic/types';
import crypto from 'crypto';

const fetchMocker = createFetchMock(vi);
fetchMocker.enableMocks();

// mock environment variables
vi.mock('$env/dynamic/public', async () => {
  const env: {
    PUBLIC_EVENT_STREAM_URL: string;
    PUBLIC_API_URL: string;
    PUBLIC_APP_URL: string;
    [key: `PUBLIC_${string}`]: string | undefined;
  } = {
    PUBLIC_EVENT_STREAM_URL: 'http://localhost:8080',
    PUBLIC_API_URL: 'http://localhost:8080',
    PUBLIC_APP_URL: 'http://localhost:8080'
  };
  return { env };
});

export const restHandlers = [
  // setup history of chat sessions
  rest.post('http://localhost:8080/api/chat/messages/', async (req, res, ctx) => {
    // const request: { session: string } = await req.json();

    const messages: {
      id: string;
      created_at: string;
      is_answer: boolean;
      content: string;
      rating: number;
    }[] = [
      {
        id: '1',
        created_at: '2021-08-24T15:00:00.000Z',
        is_answer: false,
        content: 'Hello, I am a bot',
        rating: 0
      },
      {
        id: '2',
        created_at: '2021-09-24T15:00:00.000Z',
        is_answer: true,
        content: 'Hello, I am also a bot',
        rating: 0
      }
    ];
    return res(ctx.json({ messages }));
  }),

  // sample response for setting up a new chat session
  rest.post('http://localhost:8080/api/chat/creation/', async (req, res, ctx) => {
    return res(ctx.json({ id: crypto.randomUUID() }));
  }),

  // sample response for getting all previous chat sessions
  rest.post('http://localhost:8080/api/chat/history/', async (req, res, ctx) => {
    const sessions: {
      session_id: number;
      title: string;
      hidden: boolean;
      pinned: boolean;
      color: string;
    }[] = [
      {
        session_id: 1,
        title: 'Hello',
        hidden: false,
        pinned: false,
        color: 'rgb(100, 200, 123)'
      },
      {
        session_id: 2,
        title: 'Hidden hi',
        hidden: true,
        pinned: false,
        color: 'rgb(200, 100, 123)'
      },
      {
        session_id: 3,
        title: 'Pinned greeting',
        hidden: false,
        pinned: true,
        color: 'rgb(100, 123, 200)'
      }
    ];
    return res(ctx.json({ chats: sessions }));
  }),

  // sample response for hiding a chat session
  rest.post('http://localhost:8080/api/chat/hiding/', async (req, res, ctx) => {
    return res(ctx.json({}));
  }),

  // sample response for pinning a chat session
  rest.post('http://localhost:8080/api/chat/pinning/', async (req, res, ctx) => {
    return res(ctx.json({}));
  }),

  // sample response for deleting a chat session
  rest.post('http://localhost:8080/api/chat/deletion/', async (req, res, ctx) => {
    return res(ctx.json({}));
  }),

  // sample response for ratings
  rest.post('http://localhost:8080/api/answer/rating/', async (req, res, ctx) => {
    return res(ctx.json({}));
  }),

  // sample response for adding a question
  rest.post('http://localhost:8080/api/question/', async (req, res, ctx) => {
    return res(ctx.json({}));
  })
];

const server = setupServer(...restHandlers);

// Start server before all tests
beforeAll(() =>
  server.listen({
    onUnhandledRequest: (e) => {
      throw new Error('Unhandled request' + e);
    }
  })
);

// Close server after all tests
afterAll(() => server.close());

// set initial state before each test
beforeEach(() => {
  const s: Session = {
    sessionID: 'hello-123',
    title: 'Hello',
    type: SessionStatus.Normal,
    color: 'rgb(100, 200, 123)'
  };
  knownSessions.set([s]);
  chatSessions.set({});
  chatSessionID.set(null);
  chatTitle.set('');
  errorMessage.set('');
  sessionToDelete.set(null);
});

// Reset handlers and stores after each test `important for test isolation`
afterEach(() => {
  // reset mock api handlers
  server.resetHandlers();

  // reset stores
  chatSessions.set({});
  chatSessionID.set(null);
  knownSessions.set([]);
  chatTitle.set('');
  errorMessage.set('');
  sessionToDelete.set(null);
});

/**
 * Regular expression to check if a string is a valid rgb color
 */
const colorRegex = /^rgb\(\d{1,3}, ?\d{1,3}, ?\d{1,3}\)$/;

/**
 * Sets a new active chat session
 * @returns a promise that resolves to a session object
 */
const createActiveChatSession: () => Promise<Session> = async () => {
  const id = 'hello-123';
  await setActiveChatSession(id);
  const session = get(knownSessions).find((session) => session.sessionID === id);

  if (!session) {
    throw new Error('Session not found?');
  }

  return session;
};

//// Unit tests

describe('test clearSessionID', () => {
  it('clears session id', () => {
    chatSessionID.set('123');
    expect(get(chatSessionID)).toBe('123');
    clearSessionID();
    expect(get(chatSessionID)).toBe(null);
  });

  it('clears chat title', () => {
    chatTitle.set('test title');
    expect(get(chatTitle)).toBe('test title');
    clearSessionID();
    expect(get(chatTitle)).toBe('');
  });
});

describe('test setActiveChatSession', () => {
  it('sets active chat session', async () => {
    await setActiveChatSession('hello-123');
    expect(get(chatSessionID)).toBe('hello-123');
  });

  it('sets chat title', async () => {
    await setActiveChatSession('hello-123');
    expect(get(chatTitle)).toBe('Hello');
  });

  it('messages are loaded', async () => {
    expect(get(chatSessions)['hello-123']).toBeFalsy();
    await setActiveChatSession('hello-123');
    expect(get(chatSessions)['hello-123']).toBeTruthy();
    expect(get(chatSessions)['hello-123'].length).toBe(2);
  });

  it('sets error message on failure', async () => {
    // mock error response once
    server.use(
      rest.post('http://localhost:8080/api/chat/messages/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    await setActiveChatSession('hello-123');
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test ratingToState', () => {
  it('returns correctly positive', () => {
    expect(ratingToState(1)).toBe(RatingState.Positive);
    expect(get(errorMessage)).toBeFalsy();
  });
  it('returns correctly neutral', () => {
    expect(ratingToState(0)).toBe(RatingState.Neutral);
    expect(get(errorMessage)).toBeFalsy();
  });
  it('returns correctly negative', () => {
    expect(ratingToState(-1)).toBe(RatingState.Negative);
    expect(get(errorMessage)).toBeFalsy();
  });
});

describe('test statusToState', () => {
  it('returns correctly normal', async () => {
    expect(statusToState(false, false)).toBe(SessionStatus.Normal);
    expect(get(errorMessage)).toBeFalsy();
  });
  it('returns correctly pinned', async () => {
    expect(statusToState(true, false)).toBe(SessionStatus.Archived);
    expect(get(errorMessage)).toBeFalsy();
  });
  it('returns correctly hidden', async () => {
    expect(statusToState(false, true)).toBe(SessionStatus.Pinned);
    expect(get(errorMessage)).toBeFalsy();
  });
});

describe('test getRandomColor', () => {
  it('returns a color', () => {
    const color = getRandomColor();
    expect(color).toBeTruthy();
    expect(color).toMatch(colorRegex);
  });
});

describe('test setErrorMessage', () => {
  it('sets error message', async () => {
    await setErrorMessage('hello', null);
    expect(get(errorMessage)).toBe('hello');
  });
});

describe('test createNewChatSession', () => {
  it('creates a new chat session and sets variables ', async () => {
    const title = 'New session!'; // might fail with a very long title, as it might be cut off
    await createNewChatSession(title);

    // current session should be set to the new one
    expect(get(chatSessionID)).toBeTruthy();

    // known sessions should contain the new session
    const session = get(knownSessions).find((session) => (session.title = title));
    expect(session).toBeTruthy();

    // chat sessions should contain the new session with the right details
    expect(session?.sessionID).toBe(get(chatSessionID));
    expect(session?.title).toBe(title);
    expect(session?.type).toBe(SessionStatus.Normal);
    expect(session?.color).toMatch(colorRegex);
  });

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/chat/creation/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );
    await createNewChatSession('New session!');
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test getChatSessions', () => {
  it('gets previous chat sessions', async () => {
    await getChatSessions();

    // known sessions should be populated
    expect(get(knownSessions)).toBeTruthy();
  });

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/chat/history/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );
    await getChatSessions();
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test hideChatSession', () => {
  it('hides chat session', async () => {
    const session = await createActiveChatSession();

    await hideChatSession(session);
    const session_after = get(knownSessions).find((session) => session.sessionID === 'hello-123');
    expect(session_after?.type).toBe(SessionStatus.Archived);
  });
  // We could test for sending a request to the server, but that would be maybe too implementation specific

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/chat/hiding/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    const session = await createActiveChatSession();

    await hideChatSession(session);
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test pinChatSession', () => {
  it('pin chat session', async () => {
    const session = await createActiveChatSession();

    await pinChatSession(session);
    const session_after = get(knownSessions).find((session) => session.sessionID === 'hello-123');
    expect(session_after?.type).toBe(SessionStatus.Pinned);
  });
  // We could test for sending a request to the server, but that would be maybe too implementation specific

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/chat/pinning/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    const session = await createActiveChatSession();

    await pinChatSession(session);
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test deleteChatSession', () => {
  it('deletes chat session', async () => {
    const session = await createActiveChatSession();

    await deleteChatSession(session);
    const session_after = get(knownSessions).find((session) => session.sessionID === 'hello-123');
    expect(session_after).toBeFalsy();
  });
  // We could test for sending a request to the server, but that would be maybe too implementation specific

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/chat/deletion/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    const session = await createActiveChatSession();

    await deleteChatSession(session);
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test deleteConfirmation', async () => {
  it('sets the variable correctly', async () => {
    const session = await createActiveChatSession();

    expect(get(sessionToDelete)).toBeFalsy();
    await deleteConfirmation(session);
    expect(get(sessionToDelete)).toBe(session);
  });
});

describe('test hidePopUpMessage', async () => {
  it('sets the variable correctly', async () => {
    const session = await createActiveChatSession();

    expect(get(sessionToDelete)).toBeFalsy();
    await deleteConfirmation(session);
    expect(get(sessionToDelete)).toBe(session);
    await hidePopUpMessage();
    expect(get(sessionToDelete)).toBeFalsy();
  });
});

describe('test confirmDeletion', () => {
  it('deletes chat session', async () => {
    const session = await createActiveChatSession();

    await confirmDeletion(session);
    const session_after = get(knownSessions).find((session) => session.sessionID === 'hello-123');
    expect(session_after).toBeFalsy();
  });

  it('hides pop up', async () => {
    const session = await createActiveChatSession();

    expect(get(sessionToDelete)).toBeFalsy();
    await deleteConfirmation(session);
    expect(get(sessionToDelete)).toBe(session);
    await confirmDeletion(session);
    expect(get(sessionToDelete)).toBeFalsy();
  });
});

describe('test rateAnswer', async () => {
  it('sets positive rating correctly', async () => {
    server.use(
      rest.post('http://localhost:8080/api/answer/rating/', async (req, res, ctx) => {
        const reqBody: { id: string; rating: number } = await req.json();
        if (reqBody.rating != 1) {
          return res.once(ctx.status(500));
        }
        return res.once(ctx.json({}));
      })
    );

    await rateAnswer('987', RatingState.Positive);
    expect(get(errorMessage)).toBeFalsy();
  });

  it('sets positive neutral correctly', async () => {
    server.use(
      rest.post('http://localhost:8080/api/answer/rating/', async (req, res, ctx) => {
        const reqBody: { id: string; rating: number } = await req.json();
        if (reqBody.rating != 0) {
          return res.once(ctx.status(500));
        }
        return res.once(ctx.json({}));
      })
    );

    await rateAnswer('987', RatingState.Neutral);
    expect(get(errorMessage)).toBeFalsy();
  });

  it('sets positive negative correctly', async () => {
    server.use(
      rest.post('http://localhost:8080/api/answer/rating/', async (req, res, ctx) => {
        const reqBody: { id: string; rating: number } = await req.json();
        if (reqBody.rating != -1) {
          return res.once(ctx.status(500));
        }
        return res.once(ctx.json({}));
      })
    );

    await rateAnswer('987', RatingState.Negative);
    expect(get(errorMessage)).toBeFalsy();
  });

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/answer/rating/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    await rateAnswer('987', RatingState.Negative);
    expect(get(errorMessage)).toBeTruthy();
    errorMessage.set('');
  });
});

describe('test generateID', () => {
  it('generates a random ID', () => {
    const id = generateID();
    expect(id).toBeTruthy();
  });
});

describe('test getSessionByID', () => {
  it('returns the correct session', async () => {
    const session = await createActiveChatSession();

    const session_after = getSessionByID(session.sessionID);
    expect(session_after).toBe(session);
  });

  it('throws an error if the session does not exist', async () => {
    await expect(() => getSessionByID('123')).toThrowError();
  });
});

describe('test changeRating', () => {
  test.each([
    // format: rating before, what to change, rating after
    [RatingState.Neutral, RatingState.Positive, RatingState.Positive],
    [RatingState.Neutral, RatingState.Negative, RatingState.Negative],
    [RatingState.Neutral, RatingState.Neutral, RatingState.Neutral],
    [RatingState.Positive, RatingState.Positive, RatingState.Neutral],
    [RatingState.Positive, RatingState.Negative, RatingState.Negative],
    [RatingState.Positive, RatingState.Neutral, RatingState.Neutral],
    [RatingState.Negative, RatingState.Positive, RatingState.Positive],
    [RatingState.Negative, RatingState.Negative, RatingState.Neutral],
    [RatingState.Negative, RatingState.Neutral, RatingState.Neutral]
  ])(
    'changes the rating correctly',
    async (before: RatingState, change: RatingState, after: RatingState) => {
      const message: Message = {
        messageID: 'answer-123',
        type: MessageType.Answer,
        content: '',
        streaming: false
      };
      message.rating = before;
      changeRating(message, change);
      expect(message.rating).toBe(after);
    }
  );
});

describe('test addQuestion', () => {
  it('adds a question to the session', async () => {
    const session = await createActiveChatSession();

    let idOfMessage = '';

    await addQuestion(
      'question-123',
      session.sessionID,
      'A very interesting question',
      (sessionID: string, answer: Message) => {
        idOfMessage = answer.messageID;
        console.log('executed callback');
      }
    );

    const messages = get(chatSessions)[session.sessionID];
    expect(messages).toBeTruthy();

    // it should contain the new question
    const question = messages.find((message) => message.messageID === idOfMessage);
    expect(question).toBeTruthy();
    expect(question?.type).toBe(MessageType.Question);
    expect(question?.content).toBe('A very interesting question');

    expect(get(errorMessage)).toBeFalsy();
  });

  it('sends the question to the server', async () => {
    const question = 'Some question';
    server.use(
      rest.post('http://localhost:8080/api/question/', async (req, res, ctx) => {
        const reqBody: { question: string; sessionID: string } = await req.json();
        if (reqBody.question != question) {
          return res.once(ctx.status(500));
        }
        return res.once(ctx.json({}));
      })
    );

    const session = await createActiveChatSession();

    await addQuestion('some-id', session.sessionID, question, () => {
      console.log('executed callback');
    });

    expect(get(errorMessage)).toBeFalsy();
  });

  it('creates a new chat if one does not exist already', async () => {
    await addQuestion('new-id', 'new-session-id', 'new question', () => {
      console.log('executed callback');
    });

    // look for the session in message data structure
    const messages = get(chatSessions)['new-session-id'];
    expect(messages).toBeTruthy();
    expect(messages.length).toBe(1);

    expect(get(errorMessage)).toBeFalsy();
  });

  it('sets error message on failure', async () => {
    server.use(
      rest.post('http://localhost:8080/api/question/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    const session = await createActiveChatSession();

    await addQuestion('some-id', session.sessionID, 'some question', () => {
      console.log('executed callback');
    });

    expect(get(errorMessage)).toBeTruthy();
  });

  it('executes the callback on success', async () => {
    const session = await createActiveChatSession();

    const callback = vi.fn();
    await addQuestion('some-id', session.sessionID, 'some question', callback);
    expect(callback).toBeCalledTimes(1);
  });
});

describe('test saveMessage', async () => {
  it('saves a message to a session', async () => {
    const session = await createActiveChatSession();

    let called = false;
    server.use(
      rest.post('http://localhost:8080/api/chat/saving/', async (req, res, ctx) => {
        called = true;
        return res.once(ctx.json({}));
      })
    );

    await saveMessage(session.sessionID, MessageType.Question, 'some message');

    expect(called).toBeTruthy();
  });
});

describe('test getFAQEntries', async () => {
  it('returns the FAQ entries', async () => {
    server.use(
      rest.post('http://localhost:8080/api/faq/entries/', async (req, res, ctx) => {
        return res.once(
          ctx.json({
            faq_entries: [
              { id: '1', question: 'q1', answer: 'a1' },
              { id: '2', question: 'q2', answer: 'a2' }
            ]
          })
        );
      })
    );

    await getFAQEntries(2);

    expect(get(faqEntries)).toBeTruthy();
    expect(get(faqEntries).length).toBe(2);
  });
});
