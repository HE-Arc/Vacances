<script setup>
import { varToString } from "@/assets/js/utils.js"; // IMPORTANT : Need to be in { } to work !
import axios from "axios";
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
// useRoute is to get data like params or query from the route
// useRouter is to redirect to another route with some data
//    sample :  obj = "abc"
//              router.push({ path: "/a", query: { obj } });
//          => Will redirect to /a?obj=abc

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

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

const router = useRouter();
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
  errors.value = [];
  errorsTitle.value = "";

  // Validation
  if (!name.value) {
    errors.value.push("Le nom est obligatoire.");
  }

  // selectedPokemonType.value not in options ?
  if (
    !options.value.find(
      (option) => option.value === selectedPokemonType.value.value
    )
  ) {
    errors.value.push("Le type de Pokémon est invalide.");
  }

  if (errors.value.length) {
    errorsTitle.value =
      "Erreur avec les données du formulaire, veuillez les corriger :";

    return; // There is some error, stop the buy process
  }

  // Send to backend
  const data = {
    pokemon_type: selectedPokemonType.value.value,
    name: name.value,
    obtainable: true, // TODO When obtainable is implemented
    image_url: imageUrl.value,
  };

  const uri = isEdit ? `pokemons/${pokemonEditId.value}/update/` : "pokemons/";
  const axiosMethod = isEdit ? axios.put : axios.post;

  await axiosMethod(uri, data)
    .then(() => {
      successTitle.value = "Le Pokémon a été sauvegardé avec succès.";

      sessionStorage.setItem(varToString({ successTitle }), successTitle.value);
      sessionStorage.setItem(
        varToString({ success }),
        JSON.stringify(success.value)
      );

      router.push({ path: "/pokemons" });
    })
    .catch((error) => {
      errorsTitle.value = "Erreur avec lors de la sauvegarde des données.";
      errors.value.push(
        "Une des cause possible est que l'URL de l'image n'est pas valide"
      );
    });
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
              v-if="errorsTitle || errors.length"
              inline-actions
              class="q-mb-lg text-white bg-red"
            >
              <div class="text-h6 flex">
                <q-icon left size="md" name="emoji_nature" />
                <div>
                  {{ errorsTitle }}

                  <q-list dense class="text-subtitle2">
                    <q-item v-for="(item, index) in errors" :key="index">
                      {{ item }}
                    </q-item>
                  </q-list>
                </div>
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
