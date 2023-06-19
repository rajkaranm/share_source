<script>
  import { userData } from "../store.js";

  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import axios from "axios";

  import Post from "../../components/Post.svelte";
  import Footer from "../../components/Footer.svelte";
  import ChannelList from "../../components/ChannelList.svelte";
  import { getUser } from "../../utils/utils.js";


  if (!$userData.email) {
    goto('/login')
  }
  
  let posts;
  getUser($userData.id, userData)

  onMount(async () => {
    if (!$userData.email) {
      goto("/login");
    }

    function get_posts() {
      axios
        .get("http://127.0.0.1:8000/get_posts", {
          params: { user_id: $userData.id },
        })
        .then((res) => {
          console.log(res);
          posts = res.data;
        })
        .catch((err) => {
          console.log("Error in get_posts", err);
        });
    }
    get_posts();
  });
</script>

<div class="w-screen flex flex-row justify-center flex-wrap mt-10">
  <div class="w-1/3 mx-20">
    {#if posts}
      {#each posts as post}
        <Post {post} />
      {/each}
    {/if}
  </div>
  <div class="flex flex-col">
    <ChannelList />
    <Footer />
  </div>
</div>
