<script>
  import { userData, feeds } from "../store.js";

  import { onMount } from "svelte";
  import { goto } from "$app/navigation";

  import Post from "../../components/Post.svelte";
  import Footer from "../../components/Footer.svelte";
  import ChannelList from "../../components/ChannelList.svelte";
  import { getUser, get_posts } from "../../utils/utils.js";

  if (!$userData.email) {
    goto("/login");
  }

  let posts;
  getUser($userData.id, userData);
  get_posts($userData.id, feeds)

  onMount(async () => {
    if (!$userData.email) {
      goto("/login");
    }

    get_posts();
  });
</script>

<div class="w-screen flex flex-row justify-center flex-wrap mt-10">
  <div class="w-1/3 mx-20">
    {#if $feeds}
      {#each $feeds as post}
        <Post {post} />
      {/each}
    {/if}
  </div>
  <div class="flex flex-col">
    <ChannelList />
    <Footer />
  </div>
</div>
