# proqa-client

This repository houses the front-end of the ProQA service. Users use this front-end interface to interact with the service. The client is setup as a Single-page app.

## Overview used technologies

Versions for used packages can be found in `./package.json`

- npm, package manager for managing and installing dependencies for development
- Vite, for the development server and production bundler
- Typescript, a language that is a superset of JavaScript that is strongly typed
- Svelte, JavaScript framework for developing user interfaces
  - SvelteKit, framework around Svelte to handle routing and potentially hosting
- Bootstrap, a library to build and style user interfaces
- Vitest, unit testing library
- Playwright, integration testing library

## Getting started

To develop for this project you need to have [Node JS](https://nodejs.org/en) installed. Once you've cloned this project, you can install the dependencies with `npm install`.

Visual Studio Code has an extension for Svelte which might aid in development.

A development server can be started with

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

## Building

To create a production version of the app:

```bash
npm run build
```

## Useful commands

Run tests using:

```bash
npm run test
```

Preview production build:

```bash
npm run preview
```

Do formatting:

```bash
npm run format
```
