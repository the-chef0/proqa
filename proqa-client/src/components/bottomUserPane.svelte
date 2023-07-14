<script lang="ts">
  import { PersonSquare } from 'svelte-bootstrap-icons';
  import { GearWideConnected } from 'svelte-bootstrap-icons';
  import { BoxArrowLeft } from 'svelte-bootstrap-icons';
  import { onMount } from 'svelte';
  import { adminLogin, fetchUsername, logout, isAdmin, username } from '../logic/login';

  // on mount execute fetchUsername
  onMount(() => {
    // Fetch username on mount
    fetchUsername();
  });
</script>

<div>
  <!-- Collapsible tray -->
  <div class="collapse" id="collapseExample">
    <div class="d-grid p-2 mx-1 pb-1">
      <!-- Tray components -->
      <div class="btn-group-vertical shadow">
        {#if $isAdmin}
          <button
            class="btn btn-secondary user-bottom-pane btn-lg fs-6 border-0"
            style="border-radius: 0.25rem 0.25rem 0px 0px;"
            on:click={adminLogin}
          >
            <!-- Align icon and text -->
            <div class="d-flex align-items-center justify-content-start">
              <div class="d-flex align-items-center justify-content-center">
                <GearWideConnected width={15} height={15} class="ms-0" />
              </div>
              <div class="text-truncate ps-3 tray-btn-text">Admin page</div>
            </div>
          </button>
        {/if}

        <button
          class="btn btn-secondary user-bottom-pane btn-lg fs-6 border-0"
          style="border-radius: 0px 0px 0.25rem 0.25rem;"
          on:click={logout}
        >
          <!-- Align icon and text -->
          <div class="d-flex align-items-center justify-content-start">
            <div class="d-flex align-items-center justify-content-center">
              <BoxArrowLeft width={15} height={15} class="ms-0" />
            </div>
            <div class="text-truncate ps-3 tray-btn-text">Log Out</div>
          </div>
        </button>
      </div>
    </div>
  </div>
  <!-- Bottom pane -->
  <div class="d-grid p-2 mx-1" id="UserBottomPane">
    <button
      class="btn btn-secondary btn-lg shadow user-bottom-pane border-0"
      type="button"
      data-bs-toggle="collapse"
      data-bs-target="#collapseExample"
      aria-expanded="false"
      aria-controls="collapseExample"
    >
      <div class="d-flex align-items-center justify-content-start">
        <div class="d-flex align-items-center justify-content-center">
          <PersonSquare width={22} height={22} class="" />
        </div>
        <div class="text-truncate ps-3 fs-6">{$username}</div>
      </div>
    </button>
  </div>
</div>
