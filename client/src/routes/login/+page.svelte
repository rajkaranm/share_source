<script>

  import {userData } from '../store.js';
  import axios from "axios";

  import { goto } from "$app/navigation";
  // import goto from "$app/navigation"
  
  let email = ""
  let password = ""

  function handleSubmit() {
    axios.post(
      "http://localhost:8000/login", 
      {"email": email, "password": password}, 
      { headers: { "Access-Control-Allow-Origin": "https://localhost:8000"},
        withCredentials: true
      }
    )
    .then((res) => {
      console.log(res);
      if (res.data.flag == 1){
        return alert("Wrong Password")
      }
      userData.update((value) => value = res.data);
      goto("/home")
    })

	}
</script>

<div class="flex flex-col justify-center items-center m-20">
  <div class="w-full max-w-xs">
    <form class="bg-white shadow-md rounded px-8 pt-6 pb-8 mb-4">
      <div class="mb-4">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="username"
        >
          Username
        </label>
        <input
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline"
          id="username"
          type="text"
          placeholder="Username"
          bind:value={email}
        />
      </div>
      <div class="mb-6">
        <label
          class="block text-gray-700 text-sm font-bold mb-2"
          for="password"
        >
          Password
        </label>
        <input
          class="shadow appearance-none border rounded w-full py-2 px-3 text-gray-700 mb-3 leading-tight focus:outline-none focus:shadow-outline"
          id="password"
          type="password"
          placeholder="password"
          bind:value={password}
        />
        <!-- <p class="text-red-500 text-xs italic">Please choose a password.</p> -->
      </div>
      <div class="flex items-center justify-between">
        <button
          class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded focus:outline-none focus:shadow-outline"
          type="button"
          on:click={handleSubmit}
        >
          Sign In
        </button>
        <a
          class="inline-block align-baseline font-bold text-sm text-blue-500 hover:text-blue-800"
          href="/"
        >
          Forgot Password?
        </a>
      </div>
    </form>
    <p class="text-center text-gray-500 text-xs">
      &copy;2020 Acme Corp. All rights reserved.
    </p>
  </div>
</div>
