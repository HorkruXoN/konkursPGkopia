<template>
    <div id="container">
        <div class="navigation">
            <Navigation />
        </div>
        <div class="chatList">
            <ChatList />
        </div>
        <div class="messages">
            <!-- <Messages id="1"/> -->
        </div>
    </div>
</template>
<!--http://localhost:3000/users
http://localhost:3000/messages-->
<script>
import Navigation from '../components/Navigation.vue';
import ChatList from '../components/ChatList.vue';
import Messages from '../components/Messages.vue';
export default {
    components: {Navigation, ChatList, Messages }
}
</script>

<style>
body
{
    margin: 0;
    background-color: #444;
    color: #efefef;
    font-family:Verdana, Geneva, Tahoma, sans-serif;
}
#container
{
    width: 95%;
    margin-inline: auto;
}
.navigation {
    width: 5%;
    border: 1px solid #efefef;
    margin: 5px 2px 0 5px;
    height: 95vh;
    float: left;
    padding: 2px 5px;
    border-radius: 10px;
}

.chatList {
    float:left;
    width: 26%;
    border: 1px solid #efefef;
    margin: 5px 2px;
    padding: 2px 5px;
    border-radius: 10px;
    height: 95vh;
}
.messages {
    float:left;
    width: 66%;
    border: 1px solid #efefef;
    margin: 5px 2px;
    padding: 2px 5px;
    border-radius: 10px;
    height: 95vh;
}

</style>
