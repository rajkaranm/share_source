<script>
  import { goto } from "$app/navigation";
  import { onMount } from "svelte";

  let count = 0;

  $: if (count >= 10) {
    alert("Count is high");
    count = 1;
  }

  $: console.log("Count changed ", count);

  function incrementCount() {
    count += 1;
  }

  // let user = false;
  // onMount(async () => {
  //   function checkIfUserLoggedInOrNot() {
  //     if (!user) {
  //       goto('/login');
  //     }
  //   }
  //   checkIfUserLoggedInOrNot();
  // });

</script>

<h1 class="text-3xl font-bold underline">Hello world!</h1>
<button on:click={incrementCount}>
  Clicked {count}
</button>
