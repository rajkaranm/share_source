<script>
  import { page } from "$app/stores";
  import axios from "axios";
  import { onMount } from "svelte";
  import Post from "../../../components/Post.svelte";
  import { capitalizeFirstLetter } from "../../../utils/utils.js";

  import { userData } from "../../store.js";

  import { joinChannel, leaveChannel, getUser } from "../../../utils/utils";

  let channel_data;
  let posts;

  let title;
  let content;

  function handleLeaveSubmit() {
    leaveChannel($userData.id, channel_data.channel_id);
    getUser($userData.id, userData);
  }

  function handleJoinSubmit() {
    joinChannel($userData.id, channel_data.channel_id);
    getUser($userData.id, userData);
  }

  function addPost() {
    axios
      .post("http://127.0.0.1:8000/add_post", {
        user_id: $userData.id,
        channel_id: channel_data.channel_id,
        message: content,
        title: title,
      })
      .then((res) => {
        if (res.data.flag === 1) {
          console.log(res.data);
          get_channel_data();
          alert("Post Added!");
          title = "";
          content = "";
        }
      });
  }
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

  onMount(async () => {
    get_channel_data();
  });
</script>

<div class="w-full flex flex-col justify-center items-center first-letter">
  <div class="mt-10 w-1/3 flex flex-row justify-evenly items-center">
    {#if channel_data?.channel_name}
      <h1 class="text-3xl font-bold">
        {capitalizeFirstLetter(channel_data?.channel_name)}
      </h1>

      {#if $userData.email}
        {#if $userData.channels.find((channels) => channels.channel_id === channel_data?.channel_id)}
          <button
            on:click={() => handleLeaveSubmit()}
            class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded"
            >Leave</button
          >
        {:else}
          <button
            on:click={() => handleJoinSubmit()}
            class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded"
            >Join</button
          >
        {/if}
      {/if}
    {/if}
  </div>
  <h1 class="text-2xl mt-10">All Posts</h1>
  <div class="w-1/3 mt-5">
    {#if $userData.email}
      <div class="flex flex-col my-5 p-5 bg-white border">
        <label for="">Title</label>
        <input
          bind:value={title}
          class="border rounded outline-none"
          type="text"
        />
        <label for="">Content</label>
        <textarea
          bind:value={content}
          class="h-32 border rounded outline-none"
          name=""
          id=""
          cols="30"
          rows="10"
        />
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded mt-3"
          on:click={addPost}>Post</button
        >
      </div>
    {/if}
    {#if posts}
      {#each posts as post}
        <Post {post} />
      {/each}
    {/if}
  </div>
</div>
