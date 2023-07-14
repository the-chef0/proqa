<script lang="ts">
  import './chatWindow.scss';
  import { type Session, confirmDeletion, hidePopUpMessage } from '../logic/sessions';

  // import the session to delete
  export let sessionToDelete: Session;
</script>

<!-- Pop-up message that asks for confirmation to delete a chat session -->
<div
  class="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50 deletion-confirmation-container"
  on:click={() => hidePopUpMessage()}
  on:keypress={(e) => {
    if (e.key === 'Escape') {
      hidePopUpMessage();
    }
  }}
>
  <div
    class="position-absolute top-50 start-50 translate-middle rounded-3 pt-3 pb-4 ps-4 pe-4 deletion-confirmation"
    on:click={(e) => e.stopPropagation()}
    on:keypress={(e) => {
      if (e.key === 'Escape') {
        hidePopUpMessage();
      }
    }}
  >
    <div class="d-flex flex-column align-items-left justify-content-center">
      <div class="fs-4 deletion-confirmation-title">Confirm deletion</div>
      <div class="fs-5 deletion-confirmation-subtext text-wrap">
        Are you sure you want to delete this chat? This action cannot be undone.
      </div>
      <div class="mt-3 mb-2 d-flex align-items-center">
        <!-- Icon for the beginning -->
        <div class="vr opacity-100" style="color: {sessionToDelete.color}; width: 5px;" />
        <div class="text-truncate w-75 ms-2 ps-1 pb-1 text-start fs-6">
          {sessionToDelete.title}
        </div>
      </div>
      <div class="d-flex flex-row align-items-center justify-content-center mt-3">
        <button
          class="btn ms-2 px-4 fs-6 deletion-confirmation-cancel"
          on:click={() => hidePopUpMessage()}
        >
          Cancel
        </button>
        <button
          class="btn ms-2 px-4 fs-6 deletion-confirmation-delete"
          on:click={() => confirmDeletion(sessionToDelete)}
        >
          Delete
        </button>
      </div>
    </div>
  </div>
</div>
