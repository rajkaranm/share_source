<script>
  export let post;
  import moment from "moment";
  import { capitalizeFirstLetter } from "../utils/utils";
  import MdDelete from "svelte-icons/md/MdDelete.svelte";
  import GiSaveArrow from "svelte-icons/gi/GiSaveArrow.svelte";
  import MdShare from "svelte-icons/md/MdShare.svelte";
  import { userData, feeds } from "../routes/store"
  import { deletePost, get_posts } from "../utils/utils";
  
  let option = false;

  function handleDelete() {
    deletePost(post.id)
    get_posts($userData.id, feeds)
    option = false;
  }

</script>

<div class="mb-5 relative">
  <div class="w-full flex flex-col border bg-white rounded">
    <!-- <img class="w-full" src="/img/card-top.jpg" alt="Sunset in the mountains" /> -->
    <div class="px-6 py-4">
      <p class="text-gray-700 text-base">
        <a href={`/channel/${post.channel}`}
          >{capitalizeFirstLetter(post.channel)}</a
        >
        - {moment(post.date).startOf("ss").fromNow()}
        <!-- {post.date.slice(0, 10)} -->
      </p>
      <div class="font-bold text-xl mb-2">
        {capitalizeFirstLetter(post.title)}
      </div>
      <div class="text-lg mb-2">{capitalizeFirstLetter(post.content)}</div>
      <div class="flex flex-row justify-between">
        <button on:click={() => console.log("Comment")}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            ><path
              fill="currentColor"
              d="M6 14h12v-2H6v2Zm0-3h12V9H6v2Zm0-3h12V6H6v2Zm16 14l-4-4H4q-.825 0-1.413-.588T2 16V4q0-.825.588-1.413T4 2h16q.825 0 1.413.588T22 4v18ZM4 16V4v12Zm14.85 0L20 17.125V4H4v12h14.85Z"
            /></svg
          >
        </button>
        <button on:click={() => (option = !option)}>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            width="24"
            height="24"
            viewBox="0 0 24 24"
            ><path
              fill="currentColor"
              d="M7 12a2 2 0 1 1-4 0a2 2 0 0 1 4 0Zm7 0a2 2 0 1 1-4 0a2 2 0 0 1 4 0Zm7 0a2 2 0 1 1-4 0a2 2 0 0 1 4 0Z"
            /></svg
          >
        </button>
      </div>
    </div>
  </div>
  {#if option}
    <div
      class="w-28 absolute left-[28rem] bottom-10 flex flex-col justify-center p-1 bg-white border transition"
    >
      {#if $userData.post_ids.find((id) => id === post.id)}
      <button on:click={handleDelete} class="flex p-1"> <div class="w-6 h-6"><MdDelete /> </div>  Delete</button>
      {/if}
      <button class="flex p-2"> <div class="w-6 h-6"><GiSaveArrow /> </div>  Save</button>
      <button class="flex p-2"> <div class="w-6 h-6"> <MdShare /> </div>  Share</button>

    </div>
  {/if}
</div>
