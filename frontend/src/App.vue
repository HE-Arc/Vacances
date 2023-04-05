<script setup>
import NavBar from "./components/NavBar.vue";
import axios from "axios";

// Axios configuration (applied to all axios requests, anywhere in the frontend app)
axios.defaults.baseURL = import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/";
</script>

<template>
  <q-layout>
    <!-- navbar -->
    <NavBar />

    <q-page-container>
      <router-view />
    </q-page-container>
  </q-layout>
</template>
