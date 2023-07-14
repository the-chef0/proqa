<script lang="ts">
  import './sideBar.scss';
  import { ThreeDotsVertical, PinAngleFill, ArchiveFill, Trash3Fill } from 'svelte-bootstrap-icons';
  import {
    type Session,
    setActiveChatSession,
    hideChatSession,
    pinChatSession,
    SessionStatus,
    deleteConfirmation
  } from '../logic/sessions';

  /**
   * Import session details
   */
  export let session: Session;

  /**
   * Tracks whether three dot menu should be visible.
   */
  let threeDotsVisivility = false;

  /**
   * Toggles visbility for the three dot menu.
   */
  function toggleThreeDots() {
    threeDotsVisivility = !threeDotsVisivility;
  }
</script>

<button
  class="btn m-2 text-truncate chat-btn"
  on:mouseenter={toggleThreeDots}
  on:mouseleave={toggleThreeDots}
  on:click={() => setActiveChatSession(session.sessionID)}
>
  <!-- Flex div to put the text and icon side by side -->
  <div class="d-flex align-items-center justify-content-start">
    <!-- Icon for the beginning -->
    <div class="vr opacity-100" style="color: {session.color}; width: 6px;" />
    <!-- Chat title (possibly truncated) -->
    <div class="text-truncate w-100 ms-2 ps-1 text-start chat-btn-title fs-6">
      {session.title}
    </div>
    <!-- Three dot menu -->
    {#if threeDotsVisivility}
      <button
        class="btn btn-sm three-dot-menu align-items-end justify-content-center"
        style="padding-left:5px; padding-right:5px; margin-right:-5px;"
        type="button"
        id="dropdownMenuButton1"
        data-bs-toggle="dropdown"
        aria-expanded="false"
        data-bs-boundary="viewport"
        on:click={(e) => e.stopPropagation()}
      >
        <div class="d-flex align-items-center justify-content-center">
          <ThreeDotsVertical class="text-light" />
        </div>
      </button>
      <ul class="dropdown-menu float-end" aria-labelledby="dropdownMenuButton1">
        <li>
          <a
            class="dropdown-item"
            href="./"
            on:click={() => pinChatSession(session)}
            style="border-radius: 0.25rem 0.25rem 0 0;"
          >
            <div class="d-flex align-items-center justify-content-start">
              <PinAngleFill class="m-2 ms-0 me-3" />
              {#if session.type == SessionStatus.Pinned}
                Unpin
              {:else}
                Pin
              {/if}
            </div>
          </a>
        </li>
        <li>
          <a class="dropdown-item" href="./" on:click={() => hideChatSession(session)}>
            <div class="d-flex align-items-center justify-content-start">
              <ArchiveFill class="m-2 ms-0 me-3" />
              {#if session.type == SessionStatus.Archived}
                Unarchive
              {:else}
                Archive
              {/if}
            </div>
          </a>
        </li>
        <li>
          <a
            class="dropdown-item"
            href="./"
            on:click={() => deleteConfirmation(session)}
            style="border-radius: 0 0 0.25rem 0.25rem;"
          >
            <div class="d-flex align-items-center justify-content-start">
              <Trash3Fill class="m-2 ms-0 me-3" />Delete
            </div>
          </a>
        </li>
      </ul>
    {:else}
      <!-- invisible button to keep the button from moving when the three dots appear -->
      <button
        class="btn btn-sm three-dot-menu invisible"
        style="padding-left:5px; padding-right:5px; margin-right:-5px"
        type="button"
      >
        <div class="d-flex align-items-center justify-content-center">
          <ThreeDotsVertical class="text-muted" />
        </div>
      </button>
    {/if}
  </div>
</button>
