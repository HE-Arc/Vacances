<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const errors = ref(false);

const pokemonType = ref("");
const name = ref("");

let options = ref([]);
const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (
    await axios.get("pokemon-types/")
  ).data;

  for(var i = 0; i < pokemonTypes.value.length; i++) {
    options.value.push({label:pokemonTypes.value[i].name, value:pokemonTypes.value[i].url});
  }
  
};


const submit = async () => {
  try {
    errors.value = false;
    
    await axios.post("pokemons/", {
      pokemon_type: pokemonType.value.value,
      name: name.value,
      obtainable: true,
    });
    location.href = "/pokemons?success=true";

  } catch (error) {
    errors.value = true;
  }
};

onMounted(() => {
  fetchPokemonTypes();
});
</script>

<template>
  <q-page padding>

    <q-form class="q-gutter-md" @submit="submit()">
      <div class="row self-center justify-evenly">
        <div class="col-8 col-md-6 q-mt-md">
          <q-card class="q-pa-lg">
            <q-card-section class="">
              <q-btn color="blue-grey" :to="{ name: 'pokemons' }">
                <q-icon left name="arrow_back_ios" />
                Retour
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Créer le Pokémon</div>
            </q-card-section>

            <q-card-section>
              <q-input v-model="name" label="*Nom" class="q-mb-md" outlined />
              
              <q-select
                v-model="pokemonType"
                :options="options"
                label="Sélectionnez un type"
              />
              
            </q-card-section>

            <q-banner
              v-if="errors"
              inline-actions
              class="q-mb-lg text-white bg-red"
            >
              <div class="text-h6">
                <q-icon left size="md" name="emoji_nature" />
                Erreur lors de la création du Pokémon!
              </div>
            </q-banner>

            <q-card-section class="q-gutter-y-sm">
              <div class="text-center">
                <q-btn type="submit" color="green">
                  <q-icon left name="fact_check" />
                  <div>Créer</div>
                </q-btn>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
