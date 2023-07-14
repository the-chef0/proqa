// import adapter from '@sveltejs/adapter-auto';
// import adapter from '@sveltejs/adapter-static';
import adapter from '@sveltejs/adapter-node';
import { vitePreprocess } from '@sveltejs/kit/vite';

// eslint-disable-next-line
/** @type {import('@sveltejs/kit').Config} */
const config = {
  // Consult https://kit.svelte.dev/docs/integrations#preprocessors
  // for more information about preprocessors
  preprocess: vitePreprocess(),

  kit: {
    // static adapter
    // adapter: adapter({
    //   // default options are shown. On some platforms
    //   // these options are set automatically — see below
    //   pages: 'build',
    //   assets: 'build',
    //   // fallback: '/',
    //   precompress: false,
    //   strict: true
    // })

    // node adapter
    adapter: adapter({
      // default options are shown
      out: 'build',
      precompress: false,
      envPrefix: '',
      polyfill: true
    })
  }
};

export default config;
