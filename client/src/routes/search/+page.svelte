<script>
  import { page } from "$app/stores";
  import axios from "axios";
  import { onMount } from "svelte";
  let query = $page.url.searchParams.get("query");
  let searchResult;

  onMount(() => {
    function getSearchQuery() {
      axios
        .get("http://127.0.0.1:8000/search", { params: { query } })
        .then((res) => {
          console.log("search", res);
          searchResult = res.data;
        });
    }
    getSearchQuery();
  });
</script>

<div class="w-screen flex flex-col items-center justify-center flex-wrap mt-10">
  <h1 class="text-2xl">Channels</h1>
  <div class="w-1/2 flex flex-row justify-evenly items-center">
    {#if searchResult}
      {#each searchResult as query}
      <p class="text-xl">
        <a href="/channel/{query.channel_name}">{query.channel_name}</a>
        
      </p>
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
          >Join</button
        >
      {/each}
    {/if}
  </div>
</div>
