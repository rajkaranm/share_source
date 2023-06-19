<script>
  import { page } from "$app/stores";
  import axios from "axios";
  import { onMount } from "svelte";
  import Post from "../../../components/Post.svelte";
  import { capitalizeFirstLetter } from "../../../utils/utils.js";

  import { userData } from "../../store.js";

  import { joinChannel } from "../../../utils/utils";

  let channel_data;
  let posts;
  let user;

  userData.subscribe((data) => (user = data));

  onMount(async () => {
    function get_channel_data() {
      axios
        .get("http://127.0.0.1:8000/get_channel", {
          params: { channel_name: $page.params.channel_name },
        })
        .then((res) => {
          console.log(res.data.channel_name);
          channel_data = res.data;
          posts = channel_data.posts;
        })
        .catch((err) => {
          console.log("Error in get_posts", err);
        });
    }
    get_channel_data();
  });
</script>

<div class="w-full flex flex-col justify-center items-center first-letter">
  <div class="mt-10 w-1/3 flex flex-row justify-evenly items-center">
    {#if channel_data?.channel_name}
      <h1 class="text-3xl font-bold">
        {capitalizeFirstLetter(channel_data.channel_name)}
      </h1>

      {#if user.email}
        {#if user.channels.find((channels) => channels.channel_id === channel_data.channel_id)}
          <button
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            >Leave</button
          >
        {:else}
          <button
            on:click={() => joinChannel(user.id, channel_data.channel_id)}
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >Join</button
          >
        {/if}
      {/if}
    {/if}
  </div>
  <h1 class="text-2xl mt-10">All Posts</h1>
  <div class="w-1/3 mt-5">
    {#if channel_data}
      {#each posts as post}
        <Post {post} />
      {/each}
    {/if}
  </div>
</div>
