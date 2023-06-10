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

<div class="w-screen flex flex-row justify-center flex-wrap mt-10">
  {#if searchResult}
    {#each searchResult as query}
      {query.channel_name}
    {/each}
  {/if}
</div>
