<script>
  import { PinAngleFill, ChatFill, ArchiveFill } from 'svelte-bootstrap-icons';

  // import the section heading
  export let sectionHeading = '';
</script>

<div class="d-flex px-2 py-1 align-items-center">
  {#if sectionHeading === 'Pinned'}
    <PinAngleFill width={20} height={20} class="heading-icon m-2" />
  {:else if sectionHeading === 'Chats'}
    <ChatFill width={20} height={20} class="heading-icon m-2" />
  {:else}
    <ArchiveFill width={20} height={20} class="heading-icon m-2" />
  {/if}
  <div class="d-flex p-2 justify-content-between align-items-center" style="width: 100%;">
    <div class="fs-6 section-heading">{sectionHeading}</div>
    <!-- Slot for the icon which acts toggle for the visibility -->
    <div class="d-flex justify-content-center align-items-center">
      <slot />
    </div>
  </div>
</div>
