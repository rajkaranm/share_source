<script>
  import { userData } from "../store.js";

  import { onMount } from "svelte";
  import { goto } from "$app/navigation";
  import axios from "axios";

  onMount(async () => {
    if (!$userData.email) {
      goto("/login");
    } else {
      axios.get("")
    }
  });
</script>

<div>
  {$userData.email}
  <br />
  {$userData.id}

  <div class="max-w-sm rounded overflow-hidden shadow-lg">
    <!-- <img class="w-full" src="/img/card-top.jpg" alt="Sunset in the mountains" /> -->
    <div class="px-6 py-4">
      <div class="font-bold text-xl mb-2">The Coldest Sunset</div>
      <p class="text-gray-700 text-base">
        Lorem ipsum dolor sit amet, consectetur adipisicing elit. Voluptatibus
        quia, nulla! Maiores et perferendis eaque, exercitationem praesentium
        nihil.
      </p>
    </div>
    <div class="px-6 pt-4 pb-2">
      <span
        class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
        >#photography</span
      >
      <span
        class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
        >#travel</span
      >
      <span
        class="inline-block bg-gray-200 rounded-full px-3 py-1 text-sm font-semibold text-gray-700 mr-2 mb-2"
        >#winter</span
      >
    </div>
  </div>
</div>
