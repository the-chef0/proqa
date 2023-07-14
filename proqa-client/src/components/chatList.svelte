<script lang="ts">
  import ChatBtn from './sessionButton.svelte';
  // import Session type
  import type { Session } from '../logic/sessions';

  // import sessions array
  export let sessions: Session[];
</script>

<!-- Div for the chat history -->
<div class="overflow-auto hideScrollbarChrome hideScrollbarFirefox">
  <!-- History Questions go here -->
  <!-- Create a grid so that each button has uniform width -->
  <div class="d-grid">
    {#each sessions as session}
      <!-- export the history question -->
      <ChatBtn {session} />
    {/each}
  </div>
</div>
