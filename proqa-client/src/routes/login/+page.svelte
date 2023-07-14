<script lang="ts">
  import { env } from '$env/dynamic/public';

  /**
   * Navigates to login page.
   */
  async function goToLogin() {
    window.location.href = env.PUBLIC_API_URL + '/login/oidc'; // Replace with the desired Django view UR
  }
</script>

<div
  class="container-fluid d-flex flex-column align-items-center justify-content-center vh-100 bg-dark"
>
  <div class="row flex-column align-items-center justify-content-center flex-grow-1">
    <div class="col text-center">
      <h1 class="display-1 text-light custom-proqa">ProQA</h1>
    </div>
    <div class="col text-center">
      <h2 class="text-light custom-slogan">Answers at your fingertips</h2>
      <button
        class="btn btn-primary btn-lg custom-button"
        style="margin-top: 45%;"
        on:click={goToLogin}>Login with Prodrive</button
      >
    </div>
  </div>
</div>

<style>
  .custom-proqa {
    position: absolute;
    width: 372px;
    height: 142px;
    left: calc(50% - 372px / 2);
    top: 283px;

    font-family: 'Podkova Variable' !important;
    font-style: normal;
    font-weight: 700;
    font-size: 128px;
    line-height: 142px;
    color: #0167b1 !important;
  }

  .custom-slogan {
    position: absolute;
    width: 393px;
    height: 35px;
    left: calc(50% - 393px / 2 - 0.27px);
    top: 422.99px;

    font-family: 'Podkova Variable' !important;
    font-style: normal;
    font-weight: 500;
    font-size: 32px;
    line-height: 35px;

    color: #8c969f !important;
  }

  .custom-button {
    padding: 15px 60px !important;
    font-style: normal;
    font-weight: 400;
    line-height: 22px;
    letter-spacing: 1px;
    color: #eceeef !important;
  }
</style>
