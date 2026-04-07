<template>
    <div class="userFoto"><img v-if="userImage" :src="userImage" alt="User Avatar" class="userAvatar"/></div>
    <div v-if="!chat.is_group">
        <div class="activeStatus" v-if="isActive">Aktywny</div>
        <div class="offlineStatus" v-else>
            Widziano {{ lastSeen }}
        </div>
    </div>
    <div class="info"><div class="chatName"><h3>{{ chat.name }}</h3></div>
    <div class="lastMessage">
        <span class="lastGroupMessageSender" v-if="chat.is_group">
            <span class="lastMessageSenderYou" v-if="isSender">Ty: </span>
            <span v-else>{{ userName }}:&nbsp;</span>
        </span>
        <span v-else><span class="lastMessageSenderYou" v-if="isSender">Ty: </span></span>
        <span class="lastMessageContent">{{ chat.last_message.content }}&nbsp;</span>
    </div>
    <div class="lastMessageDate">
        <span class="lastMessageDateSpan">{{ lastMessageTime }} </span>
    </div>
    </div>
    <div style="clear: both;"></div>
</template>

<script>
import { ref, onMounted, computed } from 'vue';
import config from '../config.js';
export default {
    props: ['chat', 'id_user'],
    setup(props) {
        const userImage = ref(null);

        onMounted(async () => {
            if(!props.chat.is_group)
            {
                try {
                    const response = await fetch(config.API_URL+`users/image?id_user=${props.chat.members[0]}`);
                    if (response.ok) {
                        const imageURL = URL.createObjectURL(await response.blob());
                        userImage.value = imageURL;
                    } else {
                        console.error('Error fetching user image:', response.status, response.statusText);
                    }
                } catch (error) {
                    console.error('Error fetching user image:', error);
                }
            }
            else
            {
                try {
                    const response = await fetch(config.API_URL+`chats/image?id_chat=${props.chat.id_chat}&id_user_asking=${localStorage.getItem('id_user')}`);
                    if (response.ok) {
                        const imageURL = URL.createObjectURL(await response.blob());
                        userImage.value = imageURL;
                    } else {
                        console.error('Error fetching user image:', response.status, response.statusText);
                    }
                } catch (error) {
                    console.error('Error fetching user image:', error);
                }
            }
            
        });
        const lastMessageTime = computed(() => {
            let date = new Date(props.chat.last_message.date)
            let today = new Date()
            let timeDiff = today - date;
            let seconds = Math.floor(timeDiff / 1000);
            let minutes = Math.floor(seconds / 60);
            let hours = Math.floor(minutes / 60);
            let days = Math.floor(hours / 24);
            let weeks = Math.floor(days / 7);
            let months = Math.floor(days / 30.44);  // average days in a month
            let years = Math.floor(days / 365.25);  // average days in a year

            if (years > 0) {
                return `${years} ${years === 1 ? 'rok' : 'lata'} temu`;
            } else if (months > 0) {
                return `${months} ${months === 1 ? 'miesiąc' : 'miesiące'} temu`;
            } else if (weeks > 0) {
                return `${weeks} ${weeks === 1 ? 'tydzień' : 'tygodnie'} temu`;
            } else if (days > 0) {
                return `${days} ${days === 1 ? 'dzień' : 'dni'} temu`;
            } else if (hours > 0) {
                return `${hours} ${hours === 1 ? 'godzinę' : 'godziny'} temu`;
            } else if (minutes > 0) {
                return `${minutes} ${minutes === 1 ? 'minutę' : 'minuty'} temu`;
            } else {
                return 'mniej niż minutę temu';
            }
        })

        const isSender= computed(() => {
            return props.chat.last_message.id_user === localStorage.getItem('id_user')
        })
        const userName = computed(() => {
            // Retrieve the users data from local storage and parse it
            const storedUsers = localStorage.getItem('users');
            const users = JSON.parse(storedUsers).users || [];

            // Assuming props.chat.last_message.id_user is available
            const messageIdUser = props.chat.last_message.id_user;

            // Initialize the default value
            let matchedUserFullName = 'Unknown User';

            for (const user of users) {
                if (user.id_user === messageIdUser) {
                    matchedUserFullName = user.full_name;
                    break; // Exit the loop once a match is found
                }
            }

            // Return the full_name
            return matchedUserFullName;
        });

        const isActive = computed(() => {
            const storedUsers = localStorage.getItem('users');
            const users = JSON.parse(storedUsers).users || [];

            // Assuming props.chat.last_message.id_user is available
            const messageIdUser = props.chat.members[0];

            // Initialize the default value

            for (const user of users) {
                if (user.id_user === messageIdUser) {
                    return user.is_active
                }
            }
        })
        const lastSeen = computed(() => {

            const storedUsers = localStorage.getItem('users');
            const users = JSON.parse(storedUsers).users || [];
            const messageIdUser = props.chat.members[0];
            
            for (const user of users) {
                
                if (user.id_user === messageIdUser) {
                    let date = new Date(user.last_seen)
                    let today = new Date()
                    let timeDiff = today - date;
                    let seconds = Math.floor(timeDiff / 1000);
                    let minutes = Math.floor(seconds / 60);
                    let hours = Math.floor(minutes / 60);
                    let days = Math.floor(hours / 24);
                    let weeks = Math.floor(days / 7);
                    let months = Math.floor(days / 30.44);  // average days in a month
                    let years = Math.floor(days / 365.25);  // average days in a year
                    
                    

                    if (years > 0) {
                        return `${years} ${years === 1 ? 'rok' : 'lata'} temu`;
                    } else if (months > 0) {
                        return `${months} ${months === 1 ? 'miesiąc' : 'miesiące'} temu`;
                    } else if (weeks > 0) {
                        return `${weeks} ${weeks === 1 ? 'tydzień' : 'tygodnie'} temu`;
                    } else if (days > 0) {
                        return `${days} ${days === 1 ? 'dzień' : 'dni'} temu`;
                    } else if (hours > 0) {
                        return `${hours} ${hours === 1 ? 'godzinę' : 'godziny'} temu`;
                    } else if (minutes > 0) {
                        return `${minutes} ${minutes === 1 ? 'minutę' : 'minuty'} temu`;
                    } else {
                        return 'mniej niż minutę temu';
                    }
                }
            }

            
        })


        return { lastMessageTime, isSender, userName, userImage, isActive, lastSeen }
    }
}
        
</script>