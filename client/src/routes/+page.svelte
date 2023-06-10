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

<h1 class="text-3xl font-bold mt-10 text-center">Welcome to Share Source</h1>
<p class="text-center" >Explore, Learn and Interact.</p>
