<script>
  import { searchResult } from "../store";
  import { capitalizeFirstLetter } from "../../utils/utils.js";
</script>

<div class="w-screen flex flex-col items-center justify-center flex-wrap mt-10">
  <h1 class="text-2xl font-bold">Channels</h1>
  <div class="w-1/2 flex flex-row justify-evenly items-center mt-5">
    {#if $searchResult.flag === 0}
      <p class="text-1xl">No Result...</p>
    {:else if $searchResult}
      {#each $searchResult as query}
        <p class="text-xl">
          <a href="/channel/{query.channel_name}"
            >{capitalizeFirstLetter(query.channel_name)}</a
          >
        </p>
      {/each}
    {/if}
  </div>
</div>
