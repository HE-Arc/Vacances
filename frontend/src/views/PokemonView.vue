<!-- eslint-disable prettier/prettier -->
<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

import { varToString, sessionGetAndRemove } from "@/assets/js/utils.js";
import MessageBanner from "@/components/MessageBanner.vue";

const pokemons = ref([]);

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

const isManager = ref(false);

successTitle.value = sessionGetAndRemove(varToString({ successTitle }));
success.value = sessionGetAndRemove(varToString({ success }), true);
errorsTitle.value = sessionGetAndRemove(varToString({ errorsTitle }));
errors.value = sessionGetAndRemove(varToString({ errors }), true);

const fetchPlayer = async () => {
  const result = await axios.get("players/my-data/");
  isManager.value = result.data.is_manager;
};

const fetchPokemons = async () => {
  const result = await axios.get("pokemons/is-owned-by-user/");
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (await axios.get("pokemon-types/")).data;
};

const removePokemon = async (id) => {
  await axios
    .delete(`pokemons/${id}/delete-with-refund`)
    .then(() => {
      successTitle.value = "Succès";
      success.value = ["Le Pokémon a été supprimé avec succès."];
    })
    .catch(() => {
      errorsTitle.value = "Erreur";
      errors.value = ["Une erreur est survenue lors de la suppression."];
    });

  await fetchPokemons();
};

let showDelDialog = ref(false);
let removeItem = ref(null);

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
  fetchPlayer();
});
</script>

<template>
  <q-page>
    <h1>Pokédex</h1>
    <br />

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

    <div v-if="isManager" class="text-center q-mb-md q-mt-md">
      <q-btn color="green" :to="{ name: 'pokemons.create' }">
        <q-icon left size="xl" name="add_circle_outline" />
        <div>Créer un Pokémon</div>
      </q-btn>
    </div>

    <!-- Card list -->
    <div class="" v-for="(item, index) in pokemons" :key="index">
      <q-card
        class="q-mb-sm"
        :class="{ 'bg-green-3': item.is_owned, 'bg-grey-4': !item.is_owned }"
      >
        <div>
          <div class="flex justify-between">
            <div class="flex items-center q-ma-sm">
              <!-- Image -->
              <div
                class="image-size-pokedex row justify-center items-center q-mr-sm"
              >
                <q-img
                  :src="item.display_image_url"
                  :alt="item.name"
                  class="image-max-size-parent"
                  fit="contain"
                />
              </div>
              <q-card-section class="flex-auto">
                <div class="text-h4 flex">
                  <div class="flex items-center q-mr-sm icon-size-pokedex">
                    <q-img
                      v-if="item.is_owned"
                      src="../assets/images/pokeball-icon.png"
                    />
                    <q-img
                      v-if="!item.is_owned"
                      src="../assets/images/pokeball-icon-white.png"
                    />
                  </div>
                  {{ item.name }}
                </div>
                <div class="text-subtitle2">
                  {{ item.pokemon_type_object.name }}
                </div>
                <div class="text-subtitle2"></div>
              </q-card-section>
            </div>
            <!-- Buttons -->
            <div v-if="isManager" class="flex column">
              <div class="flex normal-btn-size">
                <q-btn
                  color="orange-8"
                  push
                  :to="{ name: 'pokemons.edit', params: { id: item.id } }"
                  class="q-ma-xs"
                  style="width: 100%"
                  dense
                >
                  <div>
                    <q-icon left size="xs" name="edit" />
                    Modifier
                  </div>
                </q-btn>
              </div>
              <div class="flex normal-btn-size">
                <q-btn
                  color="red"
                  push
                  @click="
                    showDelDialog = true;
                    removeItem = item;
                  "
                  class="q-ma-xs"
                  style="width: 100%"
                  dense
                >
                  <div>
                    <q-icon left size="xs" name="delete_outline" />
                    Supprimer
                  </div>
                </q-btn>
              </div>
            </div>
          </div>
        </div>

        <q-separator inset />
      </q-card>
    </div>

    <!-- Delete dialog -->
    <q-dialog v-model="showDelDialog">
      <q-card class="confirm-border-attention">
        <q-card-section>
          <div class="text-h6 text-red">
            <q-icon name="error" size="lg" />
            Confirmation de suppression
          </div>
        </q-card-section>

        <hr />

        <q-card-section>
          <p>
            Souhaitez-vous réellement supprimer le pokémon
            <span class="text-teal">{{ removeItem.name }}</span>
          </p>
          <p>
            Si vous le supprimez, toutes les données associées le seront
            également.
          </p>
          <p>
            <q-icon name="redeem" size="sm" />
            Les joueurs seront remboursé.
          </p>
          <p class="text-red">
            <q-icon name="crisis_alert" size="sm" />
            Attention, cette action est irréversible.
          </p>
        </q-card-section>

        <hr />

        <q-card-actions align="right">
          <q-btn color="blue-grey" v-close-popup>
            <q-icon left size="xs" name="cancel" />
            Annuler
          </q-btn>
          <q-btn
            color="red"
            @click="removePokemon(removeItem.id)"
            v-close-popup
          >
            <q-icon left size="xs" name="delete_outline" />
            Supprimer
          </q-btn>
        </q-card-actions>
      </q-card>
    </q-dialog>
  </q-page>
</template>

<style scoped></style>
