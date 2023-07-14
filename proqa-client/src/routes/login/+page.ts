export const ssr = false;

import { redirect } from '@sveltejs/kit';
import { checkLoginStatus } from '../../logic/login';
import type { PageLoad } from './$types';

export const load = (async () => {
  // Check if user is logged in
  const isLoggedIn = await checkLoginStatus();

  // If user is logged in, redirect to chat page
  if (isLoggedIn) {
    throw redirect(307, '/chat');
  }
}) satisfies PageLoad;
