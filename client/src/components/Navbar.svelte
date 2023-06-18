<script>
  import { goto } from "$app/navigation";
  import {userData} from "../routes/store.js"

  let search = "";
  let user;

  userData.subscribe((data) => {
    user = data;
  })

  function handleSignOut() {
    userData.set({})
    goto("/login");
  }

  function handleSubmit() {
    goto(`/search?query=${search}`);
  }
</script>

<nav class="bg-white border-gray-200 dark:bg-gray-900">
  <div class="flex h-12 flex-row justify-evenly items-center">
    <a href="/">
      <h1 class="text-white">Share Source</h1>
    </a>
    <div
      class="flex flex-row justify-center items-center bg-white rounded-lg p-0.5"
    >
      <input
        placeholder="Search topic..."
        class="outline-none rounded-lg px-2 py-0.5"
        type="text"
        bind:value={search}
      />
      <button class="m-1" on:click={handleSubmit}>
        <svg
          aria-hidden="true"
          class="w-5 h-5 text-gray-500 dark:text-gray-400"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
          xmlns="http://www.w3.org/2000/svg"
          ><path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"
          /></svg
        >
      </button>
    </div>

    <div class="w-2/12">
      <ul class="">
        {#if !user.email}
          <li><a class="text-white" href="/login">login</a></li>
        {:else}
          <li class="flex flex-row justify-around">
            <a class="text-white" href="/home">Home</a>
            <a class="text-white" href="/login" on:click={handleSignOut}
              >Sign out</a
            >
          </li>
        {/if}
      </ul>
    </div>
  </div>
</nav>
