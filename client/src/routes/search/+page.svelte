<script>
  import { page } from "$app/stores";
  import axios from "axios";
  import { onMount } from "svelte";
  $: query = $page.url.searchParams.get("query");
  $: console.log(query)
  let searchResult = [];
  let flag;

  function getSearchQuery() {
    axios
      .get("http://127.0.0.1:8000/search", { params: { query } })
      .then((res) => {
        console.log("search", res);
        if (res.data.flag == 0) {
          flag = 1;
          searchResult = []
        } else {
          flag = 0;
          searchResult = res.data;

        }
      });
  }

  $: query, flag, getSearchQuery()

  onMount(() => {
    getSearchQuery();
  });
</script>

<div class="w-screen flex flex-col items-center justify-center flex-wrap mt-10">
  <h1 class="text-2xl font-bold">Channels</h1>
  <div class="w-1/2 flex flex-row justify-evenly items-center mt-5">
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
    {#if flag == 1}
    <p class="text-1xl">No Result...</p>
    {/if}
  </div>
</div>
