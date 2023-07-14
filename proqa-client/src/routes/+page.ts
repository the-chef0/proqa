export const ssr = false;
import { redirect } from '@sveltejs/kit';
import type { PageLoad } from './$types';
import { checkLoginStatus } from '../logic/login';

export const load = (async () => {
  const isLoggedIn = await checkLoginStatus();
  if (isLoggedIn) {
    // redirect to chat if logged in
    throw redirect(307, '/chat');
  } else {
    // redirect to login if not logged in
    throw redirect(307, '/login');
  }
}) satisfies PageLoad;
