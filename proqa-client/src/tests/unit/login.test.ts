import { afterAll, afterEach, beforeAll, describe, it, expect, beforeEach } from 'vitest';
import { setupServer } from 'msw/node';
import { rest } from 'msw';
import { get } from 'svelte/store';
import { vi } from 'vitest';
import createFetchMock from 'vitest-fetch-mock';
import {
  username,
  isAdmin,
  fetchCSRFToken,
  logout,
  fetchUsername,
  checkLoginStatus,
  adminLogin
} from '../../logic/login';

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
  rest.get('http://localhost:8080/get-csrf-token/', async (req, res, ctx) => {
    return res(ctx.json({ csrf_token: 'test' }));
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
  // set initial state
  username.set('placeholder');
  isAdmin.set(false);
});

// Reset handlers and stores after each test `important for test isolation`
afterEach(() => {
  // reset mock api handlers
  server.resetHandlers();
});

//// Unit tests
describe('test fetchCSRFToken', () => {
  it('returns CSRF token on success', async () => {
    // call function
    const result = await fetchCSRFToken();

    // check result
    expect(result).toBe('test');
  });

  it('returns undefined on failure', async () => {
    // mock fetch response
    server.use(
      rest.get('http://localhost:8080/get-csrf-token/', async (req, res, ctx) => {
        return res.once(ctx.status(500));
      })
    );

    // call function
    const result = await fetchCSRFToken();

    // check result
    expect(result).toBe(undefined);
  });
});

describe('test logout', () => {
  it('logs out user', async () => {
    // mock fetch response
    let called = false;
    server.use(
      rest.post('http://localhost:8080/logout/', async (req, res, ctx) => {
        called = true;
        return res.once(ctx.status(200));
      })
    );

    // call function
    await logout();

    // check redirect
    // expect(window.location.href).toBe('http://localhost:8080/login'); // hard to do now

    // check api was called
    expect(called).toBe(true);
  });
});

describe('test adminLogin', () => {
  it('changs window location to admin login if admin', async () => {
    isAdmin.set(true);
    // call function
    await adminLogin();
    // expect(window.location.href).toBe('http://localhost:8080/admin');
    // vitest does not support window.location.href
  });

  it('does nothing if not admin', async () => {
    isAdmin.set(false);
    // call function
    await adminLogin();
    // expect(window.location.href).toBe('http://localhost:3000/');
    // vitest does not support window.location.href
  });
});

describe('test fetchUsername', () => {
  it('stores username in store', async () => {
    // mock fetch response
    server.use(
      rest.get('http://localhost:8080/get-username/', async (req, res, ctx) => {
        return res.once(ctx.json({ username: 'test' }));
      })
    );

    // call function
    await fetchUsername();

    // check result
    expect(get(username)).toBe('test');
  });
});

describe('test checkLoginStatus', () => {
  it('returns false if user is not logged in', async () => {
    // mock fetch response
    server.use(
      rest.get('http://localhost:8080/check-login/', async (req, res, ctx) => {
        return res.once(ctx.json({ is_admin: false, is_logged_in: false }));
      })
    );

    // call function
    const loggedIn = await checkLoginStatus();

    // check result
    expect(get(isAdmin)).toBe(false);
    expect(loggedIn).toBe(false);
  });

  it('returns false if user is logged in', async () => {
    // mock fetch response
    server.use(
      rest.get('http://localhost:8080/check-login/', async (req, res, ctx) => {
        return res.once(ctx.json({ is_admin: false, is_logged_in: true }));
      })
    );

    // call function
    const loggedIn = await checkLoginStatus();

    // check result
    expect(loggedIn).toBe(true);
  });

  it('sets admin to false if user is not admin', async () => {
    // mock fetch response
    server.use(
      rest.get('http://localhost:8080/check-login/', async (req, res, ctx) => {
        return res.once(ctx.json({ is_admin: false, is_logged_in: true }));
      })
    );

    // call function
    await checkLoginStatus();

    // check result
    expect(get(isAdmin)).toBe(false);
  });

  it('sets admin to true if user is admin', async () => {
    // mock fetch response
    server.use(
      rest.get('http://localhost:8080/check-login/', async (req, res, ctx) => {
        return res.once(ctx.json({ is_admin: true, is_logged_in: true }));
      })
    );

    // call function
    await checkLoginStatus();

    // check result
    expect(get(isAdmin)).toBe(true);
  });
});
