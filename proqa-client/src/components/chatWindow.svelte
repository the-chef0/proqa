<script lang="ts">
  import './chatWindow.scss';
  import { SendFill } from 'svelte-bootstrap-icons';
  import {
    sessionToDelete,
    errorMessage,
    chatSessions,
    chatSessionID,
    createNewChatSession,
    getChatSessions,
    getFAQEntries,
    setErrorMessage,
    faqEntries,
    generateID,
    addQuestion,
    isStreaming,
    saveMessage
  } from '../logic/sessions';
  import { MessageType, type Message, type FAQEntry } from '../logic/types';
  import ChatAnswer from './chatAnswer.svelte';
  import { onMount } from 'svelte';
  import { env } from '$env/dynamic/public';
  import DeletionConfirmation from './deletionConfirmation.svelte';
  import ErrorMessage from './errorMessage.svelte';

  /**
   * Disclaimer displayed under text bar.
   */
  const disclaimer =
    'ProQA is an AI-powered platform. Answers may be inaccurate. Verify information from cited sources for accuracy.';

  /**
   * Dynamic value of question text input field
   */
  let questionInput = '';
  const maxQuestionLength = 500;

  var eventStream = new EventSource(env.PUBLIC_EVENT_STREAM_URL + '/', { withCredentials: true });
  let allowStream = false;
  let blockInput = false;

  const token = {
    START: '[START]',
    END: '[END]'
  };

  eventStream.addEventListener('message', function (event) {
    const data: string = event.data.replace(/'/g, '"');

    let streamPacket: { token: string; sessionID: string; messageID: string } = JSON.parse(data);

    let messagePart = decodeURIComponent(streamPacket.token);
    let messageID = decodeURIComponent(streamPacket.messageID);
    let sessionID = decodeURIComponent(streamPacket.sessionID);

    // Only allow tokens between [START] and [END] to be added to the message.
    // If [START] is not received, it means a broken stream.
    if (messagePart === token.START) {
      allowStream = true;

      $chatSessions[sessionID].every((msg) => {
        if (msg.messageID === messageID) {
          msg.streaming = true;
          isStreaming.set(true);
          return false;
        }
        return true;
      });

      return;
    } else if (messagePart === token.END) {
      allowStream = false;
      blockInput = false;

      $chatSessions[sessionID].every((msg) => {
        if (msg.messageID === messageID) {
          msg.streaming = false;
          isStreaming.set(false);
          return false;
        }
        return true;
      });

      return;
    }

    if (!allowStream) return;

    // use sessionID and messageID to put the streamed part where it should be
    if ($chatSessions[sessionID] === undefined) {
      // can seemingly (only) happen if user refreshes while stream is in progress
      setErrorMessage('Session for message with ID: ' + sessionID + ' is undefined.', null);
      return;
    }

    $chatSessions[sessionID].every((msg) => {
      if (msg.messageID === messageID) {
        msg.content += messagePart;
        return false;
      }
      return true;
    });

    $chatSessions = $chatSessions;
  });

  /**
   * Show FAQ entry
   * @param faq_entry FAQ entry to show
   */
  async function showFAQEntry(faq_entry: FAQEntry) {
    // Create chat
    await createNewChatSession(faq_entry.question);

    // Check if chat session was created
    if ($chatSessionID === null) {
      setErrorMessage('Could not create FAQ chat session', null);
      return;
    }

    // Block input while FAQ is being shown
    blockInput = true;

    // Check if chat session is already in store
    if ($chatSessions[$chatSessionID] === undefined) {
      // new chat session
      $chatSessions[$chatSessionID] = [];
    }

    // Save FAQ question and add it to chat session
    const faqQuestion = await saveMessage(faq_entry.question, MessageType.Question, null);
    if (faqQuestion === null) {
      // Unblock input if saving faq question failed
      blockInput = false;
      return;
    }
    $chatSessions[$chatSessionID].push(faqQuestion);

    // Update chat session after adding question
    $chatSessions = $chatSessions;
    scrollToLatest();

    // Save FAQ answer and add it to chat session
    const faqAnswer = await saveMessage(
      faq_entry.answer,
      MessageType.Answer,
      faqQuestion.messageID
    );
    if (faqAnswer === null) {
      // Unblock input if saving faq answer failed
      blockInput = false;
      return;
    }
    $chatSessions[$chatSessionID].push(faqAnswer);

    // Update chat session after adding answer
    $chatSessions = $chatSessions;
    scrollToLatest();

    // Unblock input after FAQ is shown
    blockInput = false;
  }

  /**
   * Detects whether 'enter' key was put into the question bar, if so it submits the question.
   * @param event the keyboard event triggering this
   */
  function onQuestionBarInput(event: KeyboardEvent) {
    if (event.key !== 'Enter') return;
    handleQuestionSubmit();
  }

  /**
   * Clears question bar of any inputted text.
   */
  function clearInput() {
    questionInput = '';
  }

  /**
   * Submits a question to the back, if it is non-empty.
   * Creates a new session if one is not set yet.
   */
  async function handleQuestionSubmit() {
    if (questionInput == '') return;

    // create a new chat if one is not set
    if ($chatSessionID === null) {
      // on resolve to ones below
      await createNewChatSession(questionInput);
    }

    if ($chatSessionID === null) {
      setErrorMessage('Could not create new session', null);
      return;
    }

    blockInput = true;
    addQuestion(
      generateID(),
      $chatSessionID,
      questionInput,
      (sessionID: string, answer: Message) => {
        $chatSessions[sessionID].push(answer);
        $chatSessions = $chatSessions;
        scrollToLatest();
      }
    );

    clearInput();

    isStreaming.set(true);
  }

  /**
   * Scrolls the chat window down to the latest message.
   */
  function scrollToLatest() {
    setTimeout(() => {
      const chats = document.getElementsByTagName('p');
      const latest = chats[chats.length - 1];
      if (!latest) return;
      latest.scrollIntoView({
        behavior: 'smooth'
      });
    }, 20);
  }

  /**
   * Function to handle getting sessions when the page is loaded.
   */
  async function handlePageRefresh() {
    await getChatSessions();
    await getFAQEntries(6);
  }

  onMount(() => {
    // Call the function on component mount (page load)
    // TODO: call this only when logged in
    handlePageRefresh();
  });
</script>

{#if $sessionToDelete !== null}
  <DeletionConfirmation sessionToDelete={$sessionToDelete} />
{/if}
{#if $errorMessage}
  <ErrorMessage message={$errorMessage} />
{/if}
<div class="d-flex flex-column overflow-auto" id="chat-window">
  <div class="flex-grow-1">
    <!-- questions and answers -->
    <!-- chat window content -->
    {#if $chatSessionID}
      <!-- checks if session ID is set -->
      {#if $chatSessions[$chatSessionID]}
        <!-- to check if there is an array defined for this ID-->
        <!-- questions and answers -->
        {#each $chatSessions[$chatSessionID] as m}
          {#if m.type === MessageType.Question}
            <div class="d-flex justify-content-end">
              <p class="chat-question rounded text-break text-wrap">{m.content}</p>
            </div>
          {:else}
            <ChatAnswer content={m.content} sources={m.sources} message={m} />
          {/if}
        {/each}
      {/if}
    {:else}
      <!-- Show FAQ of 6 questions fetched from backend -->
      <div class="d-flex justify-content-md-center">
        <h3 class="text-center faq-title">Frequently Asked Questions</h3>
      </div>
      <!-- Display the FAQ as tiles in a 3 by 2 grid, first fill the first row, then the second -->
      <div class="faq-grid">
        {#each $faqEntries as faq_entry}
          <button
            class="faq-entry m-2"
            title={faq_entry.question}
            on:click={() => showFAQEntry(faq_entry)}
          >
            <div style="width: 100%; height: 100%;">
              <p style="width: 100%; height: 100%; text-overflow: ellipsis; overflow: hidden;">
                {faq_entry.question}
              </p>
            </div>
          </button>
        {/each}
      </div>
    {/if}
  </div>

  <!--room for the question bar-->
  <br /><br />

  <!-- question bar -->
  <div class="position-fixed bottom-0 px-5 question-box-style" id="question-box">
    <div class="input-group">
      <input
        type="text"
        class="form-control"
        placeholder="Ask me a question..."
        aria-label="Ask a question"
        aria-describedby="basic-addon2"
        bind:value={questionInput}
        on:keydown={onQuestionBarInput}
        maxlength={maxQuestionLength}
        disabled={blockInput}
      />
      <button class="btn border-0" type="button" on:click={handleQuestionSubmit}>
        <SendFill width={22} height={22} fill="#0167B1" class="pb-1" />
      </button>
      <span class="character-count">{questionInput.length}/{maxQuestionLength}</span>
    </div>
    <!-- Disclaimer -->
    <div class="disclaimer mt-1 mb-1 text-center">{disclaimer}</div>
  </div>
</div>
