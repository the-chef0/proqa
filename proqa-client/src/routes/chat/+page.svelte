<script lang="ts">
  import Chatwindow from '../../components/chatWindow.svelte';
  import ChatTitle from '../../components/chatTitle.svelte';
  import '../../app.scss';
</script>

<div
  class="overflow-auto bg-light vh-100 hideScrollbarChrome hideScrollbarFirefox rounded-3 position-relative"
  id="chat-page"
>
  <ChatTitle />
  <div class="" id="container-page">
    <Chatwindow />
  </div>
</div>
