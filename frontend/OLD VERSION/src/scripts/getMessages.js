// import { ref } from 'vue'
// const getMessages = (id) => {
//     const mess = ref([])
//     const error = ref(null)

//     const load = async () => {
//         try {
//             let data = await fetch("http://localhost:3000/messages"+id)
//             if (!data.ok) {
//               throw Error('no data available')
//             }
//             mess.value = await data.json()
//           }
//           catch(err) {
//             error.value = err.message
//             console.log(error.value)
//           }
//     }
//     return { mess, error, load }

// }

// export default getMessages