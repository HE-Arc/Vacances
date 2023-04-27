<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import interval from "../views/DaycareView.vue";
import { useRoute } from "vue-router";

const user = ref(null);
const isLogged = ref(false);
const isManager = ref(false);

async function disconnect()
{
  await axios.get("users/logout/").then(() => {
    user.value = null;
    isLogged.value = false;
    localStorage.removeItem("isAuth");
    localStorage.removeItem("isManager");
    window.location.href = "users?logout=true";
  });
}

// OnMounted we check if we are still connected
const fetchConnected = async () => {
  const route = useRoute();
  if (route.query == "users") {
    return;
  }
  await axios
    .get("users/current/")
    .then(async (response) => {
      user.value = response.data;
      isLogged.value = true;
      localStorage.setItem("isAuth", true); // TODO A token will be better

      // Is manager
      await axios.get("players/my-data/").then((response) => {
        isManager.value = response.data.is_manager;
        localStorage.setItem("isManager", isManager.value);
      });
    })
    .catch(() => {
      user.value = null;
      isLogged.value = false;
      localStorage.removeItem("isAuth");
      localStorage.removeItem("isManager");
    });
};

onMounted(() => {
  fetchConnected();
});
</script>

<template>
  <q-header reveal elevated class="bg-grey-10 text-white" height-hint="98">
    <q-toolbar>
      <q-toolbar-title>Vacances ?</q-toolbar-title>

      <q-separator vertical />

      <div v-if="isLogged" class="q-ml-auto">
        <q-toolbar-title>
          {{ user.username }}
          <span v-if="isManager">[manager]</span>
        </q-toolbar-title>
      </div>
    </q-toolbar>

    <q-tabs align="left">
      <q-route-tab :to="{ name: 'home' }" @click="clearInterval(interval)">
        <q-icon name="cottage" />
        Accueil
      </q-route-tab>
      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'pokemons' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="auto_stories" />
        Pokédex
      </q-route-tab>
      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'daycare' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="grass" />
        Pension
      </q-route-tab>
      <q-route-tab
        v-if="isLogged"
        :to="{ name: 'shop' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="storefront" />
        Magasin
      </q-route-tab>

      <q-route-tab
        v-if="isLogged"
        @click="
          disconnect();
          clearInterval(interval);
        "
      >
        <q-icon name="logout" @click="clearInterval(interval)" />
        Deconnexion
      </q-route-tab>

      <q-route-tab
        v-if="!isLogged"
        :to="{ name: 'users' }"
        @click="clearInterval(interval)"
      >
        <q-icon name="login" @click="clearInterval(interval)" />
        Connexion
      </q-route-tab>
    </q-tabs>

    <q-space />
  </q-header>
</template>

<style scoped></style>
