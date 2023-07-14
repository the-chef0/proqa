<script lang="ts">
  import './chatWindow.scss';
  // import error message
  export let message = '';
</script>

<!-- Pop-up that shows the error that it has been given -->
<div class="position-absolute top-10 start-50 translate-middle rounded-3 p-3" id="error-message">
  Error: {message}
</div>
