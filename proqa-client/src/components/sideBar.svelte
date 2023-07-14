<script lang="ts">
  import './sideBar.scss';
  import 'bootstrap';
  import NewChatBtn from './newChatButton.svelte';
  import SectionHeading from './sectionHeading.svelte';
  import ChatList from './chatList.svelte';
  import BottomUserPane from './bottomUserPane.svelte';

  import { EyeSlashFill, EyeFill } from 'svelte-bootstrap-icons';
  import { SessionStatus, knownSessions, type Session } from '../logic/sessions';

  /**
   * Toggles visibility of that part of the pinned sessions.
   */
  let pinnedVisibility = true;

  /**
   * Toggles visibility of that part of the general history of sessions.
   */
  let historyVisibility = true;

  /**
   * Toggles visibility of that part of the archived sessions.
   */
  let archiveVisibility = false;

  /**
   * The known sessions split into pinned, history and archived
   */
  $: pinnedChats = $knownSessions.filter((sesh) => sesh.type === SessionStatus.Pinned);
  $: historyChats = $knownSessions.filter((sesh) => sesh.type === SessionStatus.Normal);
  $: archivedChats = $knownSessions.filter((sesh) => sesh.type === SessionStatus.Archived);

  /**
   * How many chats are shown before its scrollable
   * @param chats the chats to check
   * @returns true if the chats should be scrollable
   */
  function shouldScrollChats(chats: Session[]) {
    return chats.length > 2; //
  }
</script>

<div class="d-flex flex-column bg-dark vh-100 justify-content-start sidebar prodrive-font">
  <!-- Heading -->
  <div class="d-flex align-items-center pt-1" id="title">
    <h2 class="fw-bold text-light text-start p-3 heading-font">ProQA</h2>
  </div>

  <!-- New Chat Button -->
  <NewChatBtn />

  <!-- Pinned Chats -->
  {#if pinnedChats.length > 0}
    <SectionHeading sectionHeading="Pinned">
      <a
        href="#0"
        on:click={() => {
          pinnedVisibility = !pinnedVisibility;
        }}
      >
        {#if pinnedVisibility}
          <EyeFill class="section-heading mt-1" />
        {:else}
          <EyeSlashFill class="section-heading mt-1" />
        {/if}
      </a>
    </SectionHeading>

    <div class={shouldScrollChats(pinnedChats) ? 'scrollable' : ''}>
      {#if pinnedVisibility}
        <div class="scrollable-content">
          <ChatList sessions={pinnedChats} />
        </div>
      {/if}
    </div>
  {/if}

  <!-- History Chats -->
  <SectionHeading sectionHeading="Chats">
    <a
      href="#0"
      on:click={() => {
        historyVisibility = !historyVisibility;
      }}
    >
      {#if historyVisibility}
        <EyeFill class="section-heading mt-1" />
      {:else}
        <EyeSlashFill class="section-heading mt-1" />
      {/if}
    </a>
  </SectionHeading>

  <div class={shouldScrollChats(historyChats) ? 'scrollable' : ''}>
    {#if historyVisibility}
      <div class="scrollable-content">
        <ChatList sessions={historyChats} />
      </div>
    {/if}
  </div>

  <!-- Archived Chats -->
  {#if archivedChats.length > 0}
    <div class="mt-auto">
      <SectionHeading sectionHeading="Archive">
        <a
          href="#0"
          on:click={() => {
            archiveVisibility = !archiveVisibility;
          }}
        >
          {#if archiveVisibility}
            <EyeFill class="section-heading mt-1" />
          {:else}
            <EyeSlashFill class="section-heading mt-1" />
          {/if}
        </a>
      </SectionHeading>
    </div>

    <div class={shouldScrollChats(archivedChats) ? 'scrollable' : ''}>
      {#if archiveVisibility}
        <div class="scrollable-content">
          <ChatList sessions={archivedChats} />
        </div>
      {/if}
    </div>
  {/if}

  {#if archivedChats.length > 0}
    <hr class="text-light mx-2 mb-2" />
  {:else}
    <hr class="text-light mx-2 mb-2 mt-auto" />
  {/if}

  <!-- Bottom User Pane -->
  <BottomUserPane />
</div>
