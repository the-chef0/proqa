<script>
  import 'bootstrap/dist/css/bootstrap.min.css';
  // import sidebar component
  import SideBar from '../../components/sideBar.svelte';
  import '../../app.scss';
</script>

<!-- layout template for every page -->
<div class="container-fluid g-0 vh-100 vw-100">
  <div class="row g-0">
    <div class="col my-sidebar d-none d-sm-block">
      <SideBar />
    </div>
    <div class="col" id="main-container">
      <slot />
    </div>
  </div>
</div>

<style>
  .my-sidebar {
    /* -ms-flex: 0 0 230px; */
    flex: 0 0 275px;
  }
</style>
