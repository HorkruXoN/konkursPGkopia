import { ref } from 'vue'
const getChatList = () => {
    const chats = ref([])
    const error = ref(null)

    const load = async () => {
        try {
            let data = await fetch("/api/lastMessages")
            if (!data.ok) {
              throw Error('no data available')
            }
            chats.value = await data.json()
          }
          catch(err) {
            error.value = err.message
            console.log(error.value)
          }
    }
    return { chats, error, load }

}

export default getChatList