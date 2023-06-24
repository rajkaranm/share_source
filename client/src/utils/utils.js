import axios from "axios";

export function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1);
}

export function joinChannel(user_id, channel_id) {
  axios
    .post("http://127.0.0.1:8000/join_channel", { user_id, channel_id })
    .then((res) => {
      if (res.ok) {
        return true;
      }
    })
    .catch((error) => {
      console.log(error);
      return false;
    });
}

export function leaveChannel(user_id, channel_id) {
  axios
    .post("http://127.0.0.1:8000/leave_channel", { user_id, channel_id })
    .then((res) => {
      if (res.ok) {
        return true;
      }
    })
    .catch((error) => {
      console.log(error);
      return false;
    });
}

export function getUser(user_id, userData) {
  axios
    .get("http://127.0.0.1:8000/get_user", { params: { user_id } })
    .then((res) => {
      userData.update((data) => (data = res.data));
    });
}

export function getSearchQuery(query, searchResult) {
  axios
    .get("http://127.0.0.1:8000/search", { params: { query } })
    .then((res) => {
      console.log("search", res.data);
      searchResult.set(res.data);
    });
}

export function deletePost(post_id) {
  axios
    .post("http://127.0.0.1:8000/delete_post", { post_id: post_id })
    .then((res) => {
      if (res.data.flag === 1) {
        alert("Post Deleted!");
      }
    });
}

export function get_posts(user_id, feeds) {
  axios
    .get("http://127.0.0.1:8000/get_posts", {
      params: { user_id },
    })
    .then((res) => {
      console.log(res);
      feeds.set(res.data);
    })
    .catch((err) => {
      console.log("Error in get_posts", err);
    });
}
