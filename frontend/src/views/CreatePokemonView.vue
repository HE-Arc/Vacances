<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute } from "vue-router";

const errors = ref(false);

const name = ref("");
const imageUrl = ref("");

let options = ref([]);
const pokemonTypes = ref([]);

const selectedPokemonType = ref("");

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (await axios.get("pokemon-types/")).data;

  for (var i = 0; i < pokemonTypes.value.length; i++) {
    options.value.push({
      label: pokemonTypes.value[i].name,
      value: pokemonTypes.value[i].url,
    });
  }

  selectedPokemonType.value = options.value[0];
};

// Is edit == route.params.id defined
const isEdit = useRoute().params.id !== undefined;
const pokemonEditId = ref(-1);

const getPokemonForEdit = async () => {
  pokemonEditId.value = useRoute().params.id;
  const pokemon = (await axios.get(`pokemons/${pokemonEditId.value}/`)).data;
  selectedPokemonType.value = options.value.find((option) => {
    return option.value === pokemon.pokemon_type;
  });
  name.value = pokemon.name;
  imageUrl.value = pokemon.image_url;
};


const submit = async () => {
  try {
    errors.value = false;
    if (!isEdit)
    {
      await axios.post("pokemons/", {
        pokemon_type: selectedPokemonType.value.value,
        name: name.value,
        obtainable: true,
        image_url: imageUrl.value,
      });
    }
    else {
      await axios.put(`pokemons/${pokemonEditId.value}/update/`, {
        pokemon_type: selectedPokemonType.value.value,
        name: name.value,
        //obtainable: ..., // TODO When obtainable is implemented
        image_url: imageUrl.value,
      });
    }
    location.href = "/pokemons?success=true";
  } catch (error) {
    errors.value = true;
  }
};

onMounted(() => {
  fetchPokemonTypes();
  if (isEdit) {
    getPokemonForEdit();
  }
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
              <div class="text-h5">
                {{ isEdit ? "Modifier" : "Créer" }} un Pokémon
              </div>
            </q-card-section>

            <q-card-section>
              <q-input v-model="name" label="*Nom" class="q-mb-md" outlined />

              <q-select
                v-model="selectedPokemonType"
                :options="options"
                label="Sélectionnez un type"
                class="q-mb-md"
              />

              <div>
                <q-input
                  v-model="imageUrl"
                  label="URL d'une image"
                  class="q-mb-md"
                  outlined
                />
              </div>
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
                  <div>{{ isEdit ? "Modifier" : "Créer" }}</div>
                </q-btn>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
