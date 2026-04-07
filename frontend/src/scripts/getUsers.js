// autoFetchUserData.js
import { ref } from 'vue';
import getMe from '@/scripts/getMe.js';
import router from '@/router';
import config from '../config.js';
export default function autoFetchUserData() {
  const id_user = ref(localStorage.getItem('token'));
  const { load } = getMe();
  const fetchInterval = ref(null);

  // Function to fetch user data and save to localStorage
  async function fetchUserData() {
    id_user.value = localStorage.getItem('token');
    try {
      const response = await fetch(config.API_URL+'users', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          token: id_user.value,
        }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('users', JSON.stringify(data));
      } else {
        handleFailure();
      }
    } catch (apiError) {
      handleFailure();
    }
  }

  // Function to initialize the fetchUserData interval
  function initFetchInterval() {
    fetchUserData(); // Initial call

    // Set interval to run fetchUserData every 1 minute
    fetchInterval.value = setInterval(fetchUserData, 60000); // 60,000 milliseconds = 1 minute
  }

  // Function to start the autoFetch
  function startAutoFetch() {
    initFetchInterval();
  }

  // Function to stop the autoFetch
  function stopAutoFetch() {
    clearInterval(fetchInterval.value);
  }

  // Handle failure by redirecting to login
  function handleFailure() {
    stopAutoFetch(); // Stop the interval on failure
    router.push('/login');
  }

  // Load user data using the getMe function
  load(id_user.value);

  return { id_user, startAutoFetch, stopAutoFetch };
}
