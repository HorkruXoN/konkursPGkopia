<template>
    <Settings />
    <div id="nav">
    <button @click="logout()">Wyloguj się</button>
    
    <select name="koloryWybór" id="SColors"  @change="changeTheme">
            <option value="rgb(122,186,255);rgb(17,84,156);black;white">Bezchmurne niebo</option>
            <option value="#fafae7;#eba49c;black;white">Łososiowy staw</option>
            <option value="#5ea037;#034b0a;black;white">Świerkowy las</option>
            <option value="#edbacd;#880f3b;black;white">Wiśniowy sad</option>
            <option value="yellow;black;#8080FF;yellow">Dla słabowidzących</option>
    </select>
    <button @click="resetPass()">Zresetuj hasło</button>
    </div>
</template>

<script>

import Settings from './Settings.vue';
import router from '@/router';
export default {
    components: {Settings},
    methods: {
        logout() {
            localStorage.clear()
            router.push('/login')
        },
        changeTheme() {
            let value = document.getElementById("SColors").value;
            value = value.split(';')
            document.documentElement.style.setProperty('--mainColor', value[0]);
            document.documentElement.style.setProperty('--extraColor', value[1]);
            document.documentElement.style.setProperty('--textMainColor', value[2]);
            document.documentElement.style.setProperty('--textExtraColor', value[3]);
        },
        resetPass() {
            router.push('/resetPassword')
        }
    }
}
</script>