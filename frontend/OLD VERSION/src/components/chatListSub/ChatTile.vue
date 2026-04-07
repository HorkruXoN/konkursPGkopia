<template>
    <div class="chatTile">
        <div class="sender">
            <div class="senderName"><h3>{{ chat.sender }}</h3></div>
            <div class="senderStatus">
                <span v-if="!chat.lastSeen">online</span>
                <span v-else>{{ chat.lastSeen }}</span>
            </div>
        </div>
        <div class="lastMessage">{{ chat.lastMessage }}</div>
    </div>
</template>

<script>
import computed from 'vue'

export default {
    props: ['chat'],

}
</script>