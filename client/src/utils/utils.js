import axios from "axios";

export function capitalizeFirstLetter(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

export function joinChannel(user_id, channel_id) {
    axios.post("http://127.0.0.1:8000/join_channel", {user_id, channel_id})
    .then((res) => {
        if (res.ok){
            return true
        }
    }) 
    .catch((error) => {
        console.log(error)
        return false
    })   
}