<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

import { varToString, sessionGetAndRemove } from "@/assets/js/utils.js";
import MessageBanner from "@/components/MessageBanner.vue";

const users = ref([]);

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

successTitle.value = sessionGetAndRemove(varToString({ successTitle }));
success.value = sessionGetAndRemove(varToString({ success }), true);
errorsTitle.value = sessionGetAndRemove(varToString({ errorsTitle }));
errors.value = sessionGetAndRemove(varToString({ errors }), true);

const fetchUsers = async () => {
  const res = await axios.get("users/");
  users.value = res.data;
};

onMounted(() => {
  fetchUsers();
});
</script>

<template>
  <main>
    <q-page padding>
      <MessageBanner
        :title="successTitle"
        :items="success"
        icon="check_circle"
        color="green"
      />

      <MessageBanner
        :title="errorsTitle"
        :items="errors"
        icon="emoji_nature"
        color="red"
      />

      <!-- "Catch phrase" -->
      <div class="text-center">
        <img src="../assets/images/Logo.png" alt="Vacances ?" class="mw-100" />
        <p>Oui, mais pas pour vous !</p>
        <img src="../assets/images/Pika.gif" alt="Pikachu at the beach" />
      </div>

      <!-- "Project information" -->
      <div>
        <h1>But du projet</h1>
        <br />
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
