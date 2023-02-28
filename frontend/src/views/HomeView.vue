<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
// TODO-2-3 Récupérer tous les users de l'API (ref var, async func, axios, onMounted)
const users = ref([]);

const fetchUsers = async () => {
  const res = await axios.get("http://localhost:8000/api/users/");
  users.value = res.data;
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <main>
    <q-page padding>
      <div>Hello World</div>
    </q-page>
  </main>
</template>
