<script>
  // import name of button
  export let btnName = '';
</script>

<div class="d-grid gap-2 p-2 m-1 mt-0 mb-2" id="newChat">
  <button class="btn btn-primary btn-lg prodrive-button shadow" type="button">
    <!-- Align icon and text -->
    <div class="d-flex align-items-center justify-content-start">
      <div class="d-flex align-items-center justify-content-center">
        <slot />
      </div>
      <div class="ps-3 fs-6">{btnName}</div>
    </div>
  </button>
</div>
