import { ref } from 'vue'
import config from '../config.js';
const getImg = () => {
    const resp = ref([])
    const error = ref(null)
    const load = async (id) => {
        try {
            let response = await fetch(config.API_URL+'img/'+id, {
                method: 'GET',
                body: JSON.stringify({ 'token': 'string' }),
                headers: {
                    "Accept": "application/json",
                    "Content-Type": "application/json"
                }
            });
            if (!response.ok) {
                throw Error('fetching data error') 
            }
            resp.value = await response.json()
            
        }
        catch(err) {
            error.value = err.message;
        }
    }
    return { resp, error, load }
}
export default getImg