<script>
  export let post;
  
</script>

<div class="w-11/12 max-w-sm rounded overflow-hidden shadow-lg pt-2">
  <!-- <img class="w-full" src="/img/card-top.jpg" alt="Sunset in the mountains" /> -->
  <div class="px-6 py-4">
    <div class="font-bold text-xl mb-2">{post.content}</div>
    <p class="text-gray-700 text-base">
      {post.channel} - At {post.date.slice(0,10)}
    </p>
  </div>
</div>
