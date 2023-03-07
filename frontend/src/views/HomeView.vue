<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
// TODO-2-3 Récupérer tous les users de l'API (ref var, async func, axios, onMounted)
const users = ref([]);

const fetchUsers = async () => {
  const res = await axios.get(import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/users/");
  users.value = res.data;
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <main>
    <q-page padding>
      <div>
        <img src="../img/Logo.png" alt="Vacances ?" />
        <p>Oui, mais pas pour vous !</p>
        <img src="../img/Pika.gif" alt="Pikachu at the beach" />
        <h1>But du projet</h1>
        <br>
        <p>Le projet choisi consiste à créer un jeu sur navigateur.</p>
        <p>
          Le joueur est le gérant d'une pension Pokémon. Son rôle est de veiller
          que ses pensionnaires soient satisfaits et ainsi obtenir de l'argent
          pour accueillir de nouveaux Pokémon. Pour veiller à ce bonheur, le
          joueur devra répondre aux demandes des Pokémon qui souhaiteront être
          placés dans différents endroits à tout moment.
        </p>
        <p>
          Le but en tant que joueur est de remplir le pokédex disponible en
          rendant ses Pokémon heureux et ainsi en gagnant de l'argent pour
          acheter de nouveaux Pokémon.
        </p>
        <p>
          Le site est accompagné d'une partie Administrateur. C'est dans cette
          section que de nouveaux Pokémon pourront être ajoutés au jeu.
        </p>
      </div>
    </q-page>
  </main>
</template>
