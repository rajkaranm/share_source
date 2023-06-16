<script>
  import { page } from "$app/stores";
  import axios from "axios";
  import { onMount } from "svelte";
  import Post from "../../../components/Post.svelte";

  let channel_data;
  let posts;

  onMount(async () => {
    function get_channel_data() {
      axios
        .get("http://127.0.0.1:8000/get_channel", {
          params: { channel_name: $page.params.channel_name },
        })
        .then((res) => {
          console.log(res);
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
  <div class="mt-10">
    <h1 class="text-3xl font-bold">{$page.params.channel_name}</h1>
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
