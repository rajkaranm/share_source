<script>
  import { page } from "$app/stores";
  import axios from "axios";
  import { onMount } from "svelte";

  import { userData } from "../store.js";
  import { capitalizeFirstLetter } from "../../utils/utils.js";

  let user;
  userData.subscribe((data) => (user = data));

  let query = $page.url.searchParams.get("query");

  let searchResult = [];
  let flag;

  function getSearchQuery() {
    axios
      .get("http://127.0.0.1:8000/search", { params: { query } })
      .then((res) => {
        console.log("search", res.data);
        if (res.data.flag == 0) {
          flag = 1;
          searchResult = [];
        } else {
          flag = 0;
          searchResult = res.data;
        }
      });
  }

  $: query, flag, getSearchQuery();

  onMount(() => {
    getSearchQuery();
  });
</script>

<div class="w-screen flex flex-col items-center justify-center flex-wrap mt-10">
  <h1 class="text-2xl font-bold">Channels</h1>
  <div class="w-1/2 flex flex-row justify-evenly items-center mt-5">
    {#if !user.email}
      {#if searchResult}
        {#each searchResult as query}
          <p class="text-xl">
            <a href="/channel/{query.channel_name}"
              >{capitalizeFirstLetter(query.channel_name)}</a
            >
          </p>
        {/each}
      {/if}
    {:else if user.email}
      {#if searchResult}
        {#each searchResult as query}
          <p class="text-xl">
            <a href="/channel/{query.channel_name}"
              >{capitalizeFirstLetter(query.channel_name)}</a
            >
          </p>
          {#if user.channels?.find((channels) => channels.channel_id === query.channel_id)}
            <button
              class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
              >Leave</button
            >
          {:else}
            <button
              class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
              >Join</button
            >
          {/if}
        {/each}
      {/if}
    {/if}
    {#if flag == 1}
      <p class="text-1xl">No Result...</p>
    {/if}
  </div>
</div>
