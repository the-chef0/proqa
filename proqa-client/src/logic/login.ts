import { env } from '$env/dynamic/public';
import { get, writable, type Writable } from 'svelte/store';
import { setErrorMessage } from './sessions';

/**
 * Tracks username of logged in user.
 */
export const username: Writable<string> = writable('admin');

/**
 * Keeps track of whether the logged in user is an administrator.
 */
export const isAdmin: Writable<boolean> = writable(false);

/**
 * Fetches user login token from back end.
 * @returns CSRF token, or undefined for failure
 */
// todo: type response better
export async function fetchCSRFToken(): Promise<string | undefined> {
  try {
    const response = await fetch(env.PUBLIC_API_URL + '/get-csrf-token/', {
      method: 'GET',
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      const csrfToken = data.csrf_token;
      return csrfToken;
    } else {
      throw new Error('Failed to fetch CSRF token');
    }
  } catch (error) {
    console.error(error);
    return undefined;
  }
}

/**
 * Logs out user
 */
export async function logout() {
  try {
    const csrfToken = await fetchCSRFToken();

    if (csrfToken === undefined) {
      console.error('Failed to fetch CSRF token');
      return;
    }

    const response = await fetch(env.PUBLIC_API_URL + '/logout/', {
      method: 'POST',
      credentials: 'include',
      headers: {
        'X-CSRFToken': csrfToken
      }
    });

    if (response.ok) {
      // Logout successful
      // You can perform any additional actions here (e.g., updating the UI, redirecting, etc.)
      window.location.href = env.PUBLIC_APP_URL + '/login';
      console.log('User logged out');
    } else {
      // Logout failed
      throw new Error('Logout failed with status ' + response.status);
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Gets user name from back end and sets it in username store.
 * Does not return username!
 */
export async function fetchUsername() {
  try {
    const response = await fetch(env.PUBLIC_API_URL + '/get-username/', {
      method: 'GET',
      credentials: 'include'
    });

    if (response.ok) {
      const data = await response.json();
      const retrievedUsername = data.username;
      // Update the username store with the retrieved username
      username.set(retrievedUsername);
    } else {
      throw new Error('Failed to fetch username');
    }
  } catch (error) {
    console.error(error);
  }
}

/**
 * Sets current page to admin page if the user is an administrator.
 */
export async function adminLogin() {
  if (get(isAdmin)) {
    const url = env.PUBLIC_API_URL + '/admin/';
    const win = window.open(url, '_blank');
    if (win) {
      // Browser has allowed it to be opened
      win.focus();
    } else {
      // Browser has blocked it
      setErrorMessage('Browser disallowed opening new window', null);
    }
  }
}

/**
 * Checks login status with back end. If a user is an admin this is saved accordingly.
 * @returns true if logged in, false otherwise
 */
export async function checkLoginStatus(): Promise<boolean> {
  const response = await fetch(env.PUBLIC_API_URL + '/check-login/', {
    method: 'GET',
    headers: {
      'Content-Type': 'application/json'
    },
    credentials: 'include'
  });

  if (response.ok) {
    const data = await response.json();
    console.log(data.is_admin ? 'User is admin' : 'User is NOT an admin');
    isAdmin.set(data.is_admin);
    return data.is_logged_in;
  } else {
    throw new Error('Request failed with status ' + response.status);
  }
}
