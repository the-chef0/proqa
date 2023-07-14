<script lang="ts">
  import { RatingState, type Message, type Source } from '../logic/types';
  import { ArrowUpShort, ArrowDownShort, ChevronRight, ChevronDown } from 'svelte-bootstrap-icons';
  import { isStreaming, changeRating } from '../logic/sessions';
  import './chatWindow.scss';

  /**
   * Content of the answer, the body of text.
   */
  export let content = '';

  /**
   * Update when content is streamed.
   */
  $: containsContent = content;

  /**
   * Update when rating is changed.
   */
  $: rating = message.rating;

  /**
   * Relevant context.
   */
  export let sources: Source[] = [];

  /**
   * Message of the answer.
   */
  export let message: Message;

  /**
   * Whether the session is shown.
   */
  let showSource = false;
</script>

<div class="mb-2">
  <div class="chat-answer rounded text-break text-wrap">
    <div class="d-flex align-items-center">
      <div class="d-flex flex-column">
        {#if $isStreaming && message.streaming}
          <div style="margin: 3px 10px;">
            <div class="spinner-grow" role="status" style="width: 1rem; height: 1rem;">
              <span class="visually-hidden">Loading...</span>
            </div>
          </div>
        {:else}
          <button
            class:upvote={rating == RatingState.Positive}
            class:vote={rating != RatingState.Positive}
            class="border-0"
            style="background-color: transparent;"
            on:click={() => {
              changeRating(message, RatingState.Positive);
              rating = message.rating;
            }}
          >
            <ArrowUpShort width={24} height={24} class="mb-1" />
          </button>
          <button
            class:downvote={rating == RatingState.Negative}
            class:vote={rating != RatingState.Negative}
            class="border-0"
            style="background-color: transparent;"
            on:click={() => {
              changeRating(message, RatingState.Negative);
              rating = message.rating;
            }}
          >
            <ArrowDownShort width={24} height={24} class="mt-1" />
          </button>
        {/if}
      </div>
      <div class="ms-3">
        {#if containsContent}
          {content}
        {/if}
      </div>
    </div>
    <div class="d-inline">
      {#if sources}
        {#each sources as s}
          <button
            class="border-0 bg-transparent"
            on:click={() => {
              showSource = !showSource;
            }}
          >
            <div
              class:source-unavailable={!s.link}
              class="bg-light px-2 mt-2 d-flex justify-content-start source-button"
              style="border-radius: 5px; max-width: 100%; width: fit-content;"
            >
              <div
                class:source-unavailable-title={!s.link}
                class="source text-break text-wrap text-start text-decoration-none text-dark"
                title={s.link}
              >
                {s.name}
              </div>
              <div class="d-flex align-items-center">
                {#if showSource}
                  <ChevronDown style="margin: 0px 0px 0px 6px" />
                {:else}
                  <ChevronRight style="margin: 0px 0px 0px 6px" />
                {/if}
              </div>
            </div>
            {#if showSource}
              <div
                class="source bg-light px-2 mx-1 mt-2 text-break text-wrap text-start text-decoration-none text-dark"
                style="border-radius: 5px;"
              >
                {s.context}
              </div>
            {/if}
          </button>
        {/each}
      {/if}
    </div>
  </div>
</div>
