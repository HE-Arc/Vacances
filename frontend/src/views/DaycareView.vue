<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

const pokemons = ref([]);

const fetchPokemons = async () => {
  const result = await axios.get(
    import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemons/"
  );
  pokemons.value = result.data;
};

const pokemonTypes = ref([]);

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (
    await axios.get(
      import.meta.env.VITE_DATABASE_SERVER_NAME + "/api/pokemon-types/"
    )
  ).data;
};

onMounted(() => {
  fetchPokemons();
  fetchPokemonTypes();
});

const imageArray = [
  {
    source: "../assets/images/Beach.jpg",
    alt: "Plage",
  },
  {
    source: "../assets/images/Forest.jpg",
    alt: "Forêt",
  },
  {
    source: "../assets/images/Mountain.jpg",
    alt: "Montagne",
  },
  {
    source: "../assets/images/Town.jpg",
    alt: "Ville",
  },
  {
    source: "../assets/images/Cave.jpg",
    alt: "Grotte",
  },
  {
    source: "../assets/images/PowerPlant.jpg",
    alt: "Centrale",
  },
];
</script>

<template>
  <q-page>
    <h1>La pension</h1>
    <br />

    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Beach.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="Plage"
            ></q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Mountain.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="Montagne"
            ></q-img>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Cave.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="Grotte"
            ></q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Forest.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="Forêt"
            ></q-img>
          </div>
        </div>
        <div class="row">
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/Town.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="Ville"
            ></q-img>
          </div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"></div>
          <div class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm">
            <q-img
              src="../assets/images/PowerPlant.jpg"
              style="outline: solid; max-width: 300px; height: 150px"
              fit="cover"
              alt="Centrale"
            ></q-img>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-12 col-md-3 col-lg-3 q-pl-xl">
        <div class="container" style="outline: solid; outline-offset: 1em">
          <h5>Mes Pokémon</h5>
          <br />
          <!-- Card list -->
          <div class="" v-for="(item, index) in pokemons" :key="index">
            <q-card class="q-mb-sm">
              <div class="flex justify-center">
                <q-card-section>
                  <div class="col justify-center items-center">
                    <div class="text-h7 row justify-center">
                      {{ item.name }}
                    </div>
                    <div
                      class="image-size-daycare row justify-center items-center q-ma-sm"
                    >
                      <q-img
                        :src="item.image_url"
                        :alt="item.name"
                        class="image-max-size-parent"
                        fit="contain"
                      />
                    </div>
                  </div>
                </q-card-section>
              </div>
              <q-separator inset />
            </q-card>
          </div>
        </div>
        <br />
        <div class="text-center q-mb-md q-mt-md">
          <q-btn color="green" :to="{ TODO }">
            <q-icon left size="xl" name="add_circle_outline" />
            <div>Acheter un Pokémon</div>
          </q-btn>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped></style>
