<script>
  import { page } from "$app/stores";
  import { postCommentData } from "../../store";
  import { onMount } from "svelte";
  import { getPostWithComment } from "../../../utils/utils";
  import Post from "../../../components/Post.svelte";

  let post_id = $page.params.id;
  let comment_length = 0;

  onMount(() => {
    getPostWithComment(post_id, postCommentData);
    console.log($postCommentData);
    comment_length = $postCommentData.comments?.length
  });
</script>

<p>{post_id}</p>
<div class="mt-10 w-full flex flex-col justify-center items-center">
  <div class="w-96">
    {#if $postCommentData.title}
      <Post post={$postCommentData} />
      <h1>Comments ({comment_length})</h1>
      {#each $postCommentData.comments as comment}
        <div class="bg-white p-5 m-1">

        <p class="text-black">{comment.comment}</p>
        </div>
      {/each}
    {/if}
  </div>
</div>
