<template>
        
</template>


<script>
import getMessages from '../scripts/getMessages.js'
import ChatTile from './chatListSub/ChatTile.vue'

export default {
    components: {ChatTile},
    props: ['id'],
    setup() {
        const {mess, error, load} = getMessages(id)

        load()      

        return { mess, error}
    }
}
</script>