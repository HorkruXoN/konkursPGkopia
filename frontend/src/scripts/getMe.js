import { ref, onUnmounted } from 'vue';
import { useRouter } from 'vue-router';
import config from '../config.js';
const getMe = () => {
  const resp = ref([]);
  const error = ref(null);
  const router = useRouter();
  const user_id = ref('');

  const load = async (id_user) => {
    user_id.value = id_user;
    try {
      let response = await fetch(config.API_URL+'me', {
        method: 'POST',
        body: JSON.stringify({ 'token': id_user }),
        headers: {
          "Accept": "application/json",
          "Content-Type": "application/json"
        }
      });

      if (!response.ok) {
        throw Error('fetching data error');
      }

      resp.value = await response.json();
      error.value = null; // Reset error on successful response
      localStorage.setItem('id_user', resp.value.id_user)
    } catch (err) {
      error.value = err.message;
      handleFailure();
    }
  };

  const handleFailure = () => {
    // Redirect to /login on failure
    router.push('/login');

    // Stop the interval on failure
    clearInterval(intervalId);
  };

  // Set up an interval to run every 1 minute
  const intervalId = setInterval(() => {
    load(user_id.value);
  }, 60000); // 60000 milliseconds = 1 minute

  // Clear the interval on component unmount to avoid memory leaks
  onUnmounted(() => clearInterval(intervalId));

  return { resp, error, load };
};

export default getMe;
