<script lang="ts">
  import { PinAngleFill, ArchiveFill, Trash3Fill } from 'svelte-bootstrap-icons';
  import {
    chatSessionID,
    chatTitle,
    deleteConfirmation,
    pinChatSession,
    hideChatSession,
    getSessionByID,
    type Session,
    setErrorMessage,
    SessionStatus
  } from '../logic/sessions';
  import './chatWindow.scss';

  /**
   * Variable is false if title is empty, is reactive.
   */
  $: titleExists = $chatTitle != '';

  /**
   * Variable containing chat session pinning status, is reactive.
   */
  $: sessionPinned = $chatSessionID && getSessionByID($chatSessionID).type == SessionStatus.Pinned;

  /**
   * Function updating pinned UI and calling backend update
   * @param session to pin
   */
  function pinChat(session: Session) {
    if (session.type === SessionStatus.Pinned) {
      sessionPinned = false;
    } else {
      sessionPinned = true;
      sessionArchived = false;
    }
    pinChatSession(session);
  }

  /**
   * Variable containing chat session pinning status, is reactive.
   */
  $: sessionArchived =
    $chatSessionID && getSessionByID($chatSessionID).type === SessionStatus.Archived;

  /**
   * Function updating pinned UI and calling backend update
   * @param session to pin
   */
  function archiveChat(session: Session) {
    if (session.type === SessionStatus.Archived) {
      sessionArchived = false;
    } else {
      sessionArchived = true;
      sessionPinned = false;
    }
    hideChatSession(session);
  }
</script>

{#if titleExists}
  <nav class="navbar chat-title-bg mb-3 sticky-top">
    <div class="d-flex p-2">
      {#if $chatSessionID}
        <div
          class="vr opacity-100 ms-2 me-1"
          style="color: {getSessionByID($chatSessionID).color}; width: 5px;"
        />
      {/if}
      <h4 class="fw-bold text-start ps-2 pt-2 text-truncate text-break text-wrap chat-title">
        {$chatTitle}
      </h4>
    </div>
    <div class="d-flex flex-row align-items-center justify-content-between" id="iconTray">
      {#if sessionPinned}
        <button
          class="border-0 pin-active"
          on:click={() =>
            $chatSessionID
              ? pinChat(getSessionByID($chatSessionID))
              : setErrorMessage('Could not find session', null)}
        >
          <PinAngleFill width={20} height={20} class="heading-icon m-3 pin-active" />
        </button>
      {:else}
        <button
          class="border-0 pin-inactive"
          on:click={() =>
            $chatSessionID
              ? pinChat(getSessionByID($chatSessionID))
              : setErrorMessage('Could not find session', null)}
        >
          <PinAngleFill width={20} height={20} class="heading-icon m-3 pin-inactive" />
        </button>
      {/if}

      {#if sessionArchived}
        <button
          class="border-0 archive-active"
          on:click={() =>
            $chatSessionID
              ? archiveChat(getSessionByID($chatSessionID))
              : setErrorMessage('Could not find session', null)}
        >
          <ArchiveFill width={20} height={20} class="heading-icon m-3 archive-active" />
        </button>
      {:else}
        <button
          class="border-0 archive-inactive"
          on:click={() =>
            $chatSessionID
              ? archiveChat(getSessionByID($chatSessionID))
              : setErrorMessage('Could not find session', null)}
        >
          <ArchiveFill width={20} height={20} class="heading-icon m-3 archive-inactive" />
        </button>
      {/if}

      <button
        class="border-0 trash-inactive me-2"
        on:click={() =>
          $chatSessionID
            ? deleteConfirmation(getSessionByID($chatSessionID))
            : setErrorMessage('Could not find session', null)}
      >
        <Trash3Fill width={20} height={20} class="heading-icon m-3 trash-inactive" />
      </button>
    </div>
  </nav>
{/if}

<style>
  button {
    background-color: transparent;
  }
</style>
