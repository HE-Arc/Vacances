<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

import MessageBanner from "@/components/MessageBanner.vue";

const pokemons = ref([]);

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

const fetchPokemons = async () => {
  const result = await axios.get("pokemons/unowned-by-user/");
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (await axios.get("pokemon-types/")).data;
};

const playerCash = ref(0);

const fetchPlayerCash = async () => {
  playerCash.value = (await axios.get("players/my-data/")).data.money;
};

const fetchPokemon = async (id) => {
  const result = await axios.get(`pokemons/${id}/`);
  return result.data;
};

const buyPokemon = async (id) => {
  // Clean messages
  success.value = [];
  successTitle.value = "";
  errors.value = [];
  errorsTitle.value = "";

  // update data of the player (to be sure of the real value)
  // TODO : It is realy necessary ?
  await fetchPlayerCash();
  await fetchPokemons();

  let buyedPokemon = await fetchPokemon(id);

  // 1) Check errors
  // 1.a) Check if enough money
  if (playerCash.value < buyedPokemon.pokemon_type_object.cost) {
    errors.value.push("Vous n'avez pas suffisament d'argent.");
  }

  // 1.b) Check if pokemon is already owned
  if (!pokemons.value.find((pokemon) => pokemon.id === id)) {
    errors.value.push("Vous possédez déjà ce Pokémon.");
  }

  // 1.c) add global error message + handle case
  if (errors.value.length) {
    errorsTitle.value = "Erreur lors de l'achat de " + buyedPokemon.name + " :";

    return; // There is some error, stop the process
  }

  // 2) Process buy (backend)
  await axios
    .post(`pokemons/${id}/buy/`)
    .then((response) => {
      successTitle.value = "Achat réussi !";
      success.value.push(buyedPokemon.name + " vous attend !");
    })
    .catch((error) => {
      errorsTitle.value =
        "Erreur lors de l'achat de " + buyedPokemon.name + " :";
      errors.value.push("Une erreur est survenue lors de l'achat.");
    });

  // 3) Update data with new values
  await fetchPlayerCash();
  await fetchPokemons();
};

let showBuyDialog = ref(false);
let buyItem = ref(null);

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();

  fetchPlayerCash();
});
</script>

<template>
  <q-page>
    <h1>Magasin</h1>

    <br />

    <q-page-sticky
      position="top-right"
      :offset="[18, 18]"
      class="text-h6 bg-info text-black border-info q-pa-sm rounded-borders z-top"
    >
      Vous avez {{ playerCash }} <q-icon name="currency_ruble" />
    </q-page-sticky>

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

    <!-- Card list -->
    <div class="q-pa-md row q-gutter-md justify-center">
      <q-card
        v-for="(item, index) in pokemons"
        :key="index"
        :class="{ 'bg-green-3': item.is_owned, 'bg-grey-4': !item.is_owned }"
        class="col-xs-12 col-sm-5 col-lg-3 column"
      >
        <div class="row q-ma-sm col-grow items-center">
          <!-- Image -->
          <q-img
            :src="item.display_image_url"
            :alt="item.name"
            class="col-2 full-height no-native-menu"
            fit="contain"
            :ratio="1"
          />
          <q-card-section class="col-10">
            <div class="text-h4" style="word-break: break-word">
              {{ item.name }}
            </div>
            <div class="text-subtitle2">
              {{ item.pokemon_type_object.name }}
            </div>
            <div class="text-subtitle2"></div>
            <div class="q-mt-md">
              <p>
                <q-icon name="price_change" size="xs" /> Facteur de gain :
                {{ item.pokemon_type_object.cash_factor }}
              </p>
              <p>
                <q-icon name="sentiment_very_satisfied" size="xs" /> Bonheur max
                : {{ item.pokemon_type_object.max_happiness }}
              </p>
            </div>
          </q-card-section>
        </div>

        <q-separator />

        <!-- Buttons -->
        <q-card-actions class="q-gutter-y-sm" align="around">
          <div class="row justify-center col-12">
            <q-tooltip v-if="playerCash < item.pokemon_type_object.cost">
              Vous n'avez pas assez d'argent pour acheter ce Pokémon.
            </q-tooltip>
            <q-btn
              color="blue"
              push
              @click="
                showBuyDialog = true;
                buyItem = item;
              "
              :disable="playerCash < item.pokemon_type_object.cost"
              class="col-8"
            >
              <div class="q-pa-sm">
                <q-icon left name="price_check" />
                Acheter<br />
                {{ item.pokemon_type_object.cost }}
                <q-icon name="currency_ruble" size="xs" />
              </div>
            </q-btn>
          </div>
        </q-card-actions>
      </q-card>
    </div>

    <!-- Buy dialog -->
    <q-dialog v-model="showBuyDialog">
      <q-card class="confirm-border-information">
        <q-card-section>
          <div class="text-h6 text-blue">
            <q-icon name="error" size="lg" />
            Confirmation d'achat
          </div>
        </q-card-section>

        <hr />

        <q-card-section>
          <p>
            Souhaitez-vous vraiment acheter
            <span class="text-teal">{{ buyItem.name }}</span> ?
          </p>
          <p>
            Il vous coutera
            <span class="text-teal"
              >{{ buyItem.pokemon_type_object.cost }}
              <q-icon name="currency_ruble" size="xs" /></span
            >.
          </p>
          <p>
            Votre nouveau solde sera de
            <span class="text-teal"
              >{{ playerCash - buyItem.pokemon_type_object.cost }}
              <q-icon name="currency_ruble" size="xs" />
            </span>
            .
          </p>
        </q-card-section>

        <hr />

        <q-card-actions align="right">
          <q-btn color="blue-grey" v-close-popup>
            <q-icon left size="xs" name="cancel" />
            Annuler
          </q-btn>
          <q-btn color="blue" @click="buyPokemon(buyItem.id)" v-close-popup>
            <q-icon left size="xs" name="price_check" />
            Acheter
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped></style>
