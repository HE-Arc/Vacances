<script setup>
import axios from "axios";
import { ref } from "vue";

const success = ref(false);
const errors = ref(null);

const pokemonType = ref("");
const name = ref("");
const obtainable = ref("");

const submit = async () => {
  try {
    success.value = false;
    errors.value = null;
    
    console.log(obtainable.value);

    await axios.post("http://127.0.0.1:8000/api/pokemons/", {
      pokemon_type: `http://127.0.0.1:8000/api/pokemon-types/${pokemonType.value}/`,
      name: name.value,
      obtainable: true,
    });

    success.value = true;
  } catch (error) {
    console.log(error);
    //errors.value = error.response.data;
  }
};
</script>

<template>
  <q-page padding>

    <q-form class="q-gutter-md" @submit="submit()">
      <div class="row self-center justify-evenly">
        <div class="col-8 col-md-6 q-mt-md">
          <q-card class="q-pa-lg">
            <q-card-section class="">
              <q-btn color="primary" :to="{ name: 'pokemons' }">
                <q-icon left name="mdi-arrow-left-top-bold" />
                <div>Retour</div>
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Créer le Pokémon</div>
            </q-card-section>

            <q-card-section>
              <q-input v-model="name" label="*Nom" class="q-mb-md" outlined />
              <q-input
                v-model="pokemonType"
                type="number"
                label="*Type de Pokémon"
                class="q-mb-md"
                outlined
              />
              <q-input
                v-model="obtainable"
                type="checkbox"
                label="Achetable"
                class="q-mb-md"
                outlined
              />
            </q-card-section>

            <q-banner
              v-if="success"
              inline-actions
              class="q-mb-lg text-white bg-green"
            >
              <div class="text-h6">
                <q-icon left size="md" name="mdi-check-circle-outline" />
                Le Pokémon a été créé!
              </div>
            </q-banner>

            <q-card-section class="q-gutter-y-sm">
              <div class="text-center">
                <q-btn type="submit" color="primary" label="Submit" />
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
