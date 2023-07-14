import { expect, test } from './baseFixtures.ts';

test('index page has expected h1', async ({ page }) => {
  await page.goto('/');
  await expect(page.getByRole('heading', { name: 'Welcome to SvelteKit' })).toBeVisible();
});
