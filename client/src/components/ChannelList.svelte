<script>
  import { userData } from "../routes/store";
  import { capitalizeFirstLetter } from "../utils/utils.js";

</script>

<div class="flex flex-col items-center border-2 bg-white py-5">
  <h1 class="text-xl font-semibold">Your Channels</h1>
  <div class="flex flex-col mt-2">
    {#if $userData.email}
      {#each $userData?.channels as channels, id}
        <a href="/channel/{channels.channel_name}"
          >{id + 1}. {capitalizeFirstLetter(channels.channel_name)}
        </a>
      {/each}
    {/if}
  </div>
</div>
