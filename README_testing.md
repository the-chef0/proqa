# Files to be included in testing

The files that need to be included in the code quality tests are mentioned below. They're grouped by the subdirectories they lie under. We've excluded files such as configuration files, test files, boilerplate files etc. There are no client files so everything that hasn't been included is either a configuration file or auto-generated boilerplate code. Note we use the [Svelte](https://svelte.dev/) framework for our front-end but [SciTools Understand](https://scitools.com/) doesn't recognize files with `.svelte` extension. As a remedy, the javascript (logic) from these files can be extracted in a seperate `.js` file. The logic is present between `<script>` and `</script>` tags at the top of these files. Happy Testing!

## proqa-ai-service

### proqa_ai/controllers

- embedding.py
- text.py
- tokenize.py

### proqa_ai/routers

- embedding.py
- text.py
- tokenize.py

### proqa_ai/schemas

- embedding.py
- text.py
- tokenize.py

### proqa_ai/server

- config.py
- main.py

### proqa_ai/utilities

- callback.py
- model_manager.py

## proqa-back-end

### api

- exceptions.py
- tasks.py

### api/admin

- chat.py
- collection.py
- model.py

### api/models

- abstract.py
- chat.py
- choices.py
- collection.py
- model.py

### api/utils

- aiservice_embedding.py
- aiservice_text.py
- aiservice_tokenize.py
- aiservice.py
- chat_session.py
- context.py
- csrf_exempt.py
- faq.py
- vectordb.py

### api/views

- aiservice.py
- chat_session.py
- context.py
- faq.py
- home.py
- login.py
- text_stream.py

## proqa-client

### src/components

- bottomUserPane.svelte
- chatAnswer.svelte
- chatList.svelte
- chatTitle.svelte
- chatWindow.svelte
- deletionConfirmation.svelte
- errorMessage.svelte
- largeSideBarButton.svelte
- newChatButton.svelte
- sectionHeading.svelte
- sessionButton.svelte
- sideBar.svelte

### src/logic

- login.ts
- sessions.ts
- types.ts

### src/routes

- +layout.svelte
- +page.ts

### src/routes/chat

- +layout.svelte
- +page.svelte
- +page.ts
- +layout.ts

### src/routes/login

- +page.svelte
- +page.ts
