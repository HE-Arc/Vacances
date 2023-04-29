<script setup>
import NavBar from "./components/NavBar.vue";
import axios from "axios";
import { onDisconnect } from "@/assets/js/persistanceLoginInfo";
import { useRouter } from "vue-router";

const router = useRouter();

// Axios configuration (applied to all axios requests, anywhere in the frontend app)
axios.defaults.baseURL = import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/";
axios.defaults.withCredentials = true;
axios.defaults.xsrfCookieName = "csrftoken";
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";

axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response.status === 401 || error.response.status === 403) {
      console.log("unauthorized action detected");
      console.log("- disconnecting user and redirecting to login page");
      onDisconnect();

      router.push("users");
    }
    return Promise.reject(error);
  }
);
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
