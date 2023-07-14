<script lang="ts">
  // import clearSessionID function
  import { clearSessionID } from '../logic/sessions';
  import { PlusLg } from 'svelte-bootstrap-icons';
</script>

<div class="d-grid gap-2 p-2 m-1 mt-0 mb-2" id="newChat">
  <button
    class="btn btn-primary btn-lg prodrive-button shadow border-0"
    type="button"
    on:click={clearSessionID}
  >
    <!-- Align icon and text -->
    <div class="d-flex align-items-center justify-content-start">
      <div class="d-flex align-items-center justify-content-center">
        <PlusLg width={22} height={22} fill="white" class="ms-0" />
      </div>
      <div class="ps-3 fs-6">New Chat</div>
    </div>
  </button>
</div>
