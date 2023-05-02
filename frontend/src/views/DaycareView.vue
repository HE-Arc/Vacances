<!-- eslint-disable prettier/prettier -->
<script setup>
import axios from "axios";
import { ref, onMounted, onUnmounted } from "vue";

import { areas } from "@/assets/js/areasData.js";
const transparentImg = "transparent.png"; // Syntax for public folder
// import transparentImg from "@/transparent.png"; // Syntax for assets folder
// Note : We use the public folder to avoid the rename of the image when build (we use it's name for checks)

const lblRequestEmpty = "Aucune demande pour le moment.";
const lblMoneyDefault =
  "Montez un Pokémon à son bonheur max pour gagner de l'argent !";

let lblRequest = null;
let lblMoney = null;

const colorNoRequest = "blue-grey-13";
const colorRequest = "pink-14";
const colorMoneyDefault = "blue-grey-13";
const colorEarnMoney = "green-14";

const currentColorRequest = ref(colorNoRequest);
const currentColorMoney = ref(colorMoneyDefault);

const ownedPokemons = ref([]);
const interval = ref(null);

const isReceived = ref(true);

const tag = ref("");

const pokemonTypes = ref([]);

const areasPairs = ref([]);

const tempImage = ref(null);

var imageElement = ref(null);
const lastAreaClicked = ref(null);
const mapAreaPokemon = new Map();

var pokemonCurrent = null;

const pokemonAlt = "pokemon";

const fetchPokemonTypes = async () => {
  pokemonTypes.value = (await axios.get("pokemon-types/")).data;
};

const fetchOwnedPokemons = async () => {
  ownedPokemons.value = (await axios.get("owned-pokemons/my-pokemons")).data;
};

const placeAreas = async () => {
  let odd = true;
  for (let i = 0; i + 1 < areas.length; i += 2) {
    if (odd == true) {
      areasPairs.value.push([areas[i], 0, areas[i + 1]]);
    } else {
      areasPairs.value.push([0, areas[i], 0, areas[i + 1]]);
    }
    odd = !odd;
  }
};

var randomIndexPokemon = null;
var randomPokemon = null;
var randomIndexZone = null;

function pokemonRequest() {
  if (mapAreaPokemon.size > 0) {
    let keys = Array.from(mapAreaPokemon.keys());

    randomIndexPokemon = Math.floor(Math.random() * mapAreaPokemon.size);

    randomPokemon = mapAreaPokemon.get(keys[randomIndexPokemon]);

    randomIndexZone = Math.floor(Math.random() * areas.length);

    while (mapAreaPokemon.get(areas[randomIndexZone].name) == pokemonCurrent) {
      randomIndexZone = Math.floor(Math.random() * areas.length);
    }

    lblRequest.innerText =
      randomPokemon.pokemon_object.name +
      " aimerait aller à la " +
      areas[randomIndexZone].name +
      ".";

    currentColorRequest.value = colorRequest;

    let randomwait = Math.floor(Math.random() * 10000) + 5000;
    clearInterval(interval.value);
    interval.value = setInterval(pokemonRequest, randomwait);
  } else {
    lblRequest.innerText = lblRequestEmpty;
    currentColorRequest.value = colorNoRequest;
  }
}

function coroutine() {
  interval.value = setInterval(pokemonRequest, 5000);
}

function changeTag() {
  const cursorStyle = window.getComputedStyle(event.target).cursor;

  if (cursorStyle === "pointer") {
    tag.value = "pokemon";
  }
}

function sendImage(event, item) {
  const cursorStyle = window.getComputedStyle(event.target).cursor;

  if (cursorStyle === "pointer") {
    imageElement.value = event.target;
    isReceived.value = false;
    pokemonCurrent = item;
  } else {
    imageElement.value = "";
    isReceived.value = true;
    tag.value = "";
  }
}

function receiveImage(event, area) {
  if (imageElement.value != "") {
    if (tag.value == "pokemon") {
      if (event.target.src.includes(transparentImg)) {
        event.target.src = imageElement.value.src;

        tag.value = "";

        isReceived.value = true;

        imageElement.value.style.filter = "grayscale(100%)";
        imageElement.value.style.cursor = "default";

        mapAreaPokemon.set(area.name, pokemonCurrent);
      }
    } else {
      if (isReceived.value) {
        if (!event.target.src.includes(transparentImg)) {
          imageElement.value = event.target;
          lastAreaClicked.value = area;
          isReceived.value = false;
        }
      } else {
        tempImage.value = event.target.src;
        event.target.src = imageElement.value.src;

        isReceived.value = true;

        imageElement.value.src = tempImage.value;

        let tempPokemon = mapAreaPokemon.get(lastAreaClicked.value.name);
        mapAreaPokemon.set(
          lastAreaClicked.value.name,
          mapAreaPokemon.get(area.name)
        );
        mapAreaPokemon.set(area.name, tempPokemon);
        if (mapAreaPokemon.get(area.name) == null) {
          mapAreaPokemon.delete(area.name);
        }
        if (mapAreaPokemon.get(lastAreaClicked.value.name) == null) {
          mapAreaPokemon.delete(lastAreaClicked.value.name);
        }

        //lastAreaClicked.value = area;

        if (randomIndexZone != null) {
          if (
            areas[randomIndexZone].name == area.name &&
            mapAreaPokemon.get(area.name) == randomPokemon
          ) {
            const id = mapAreaPokemon.get(area.name).id;
            axios
              .post(`owned-pokemons/${id}/increment-happiness/`)
              .then((ownedpkm) => {
                mapAreaPokemon.get(area.name).current_happiness =
                  ownedpkm.data.current_happiness;
                randomIndexZone = null;
                currentColorRequest.value = colorNoRequest;

                if (mapAreaPokemon.get(area.name).current_happiness == 0) {
                  lblMoney.innerText =
                    "Vous avez gagné " +
                    mapAreaPokemon.get(area.name).pokemon_object
                      .pokemon_type_object.cash_factor *
                      10 +
                    " ₽ grâce au bonheur de " +
                    mapAreaPokemon.get(area.name).pokemon_object.name +
                    " !";
                  currentColorMoney.value = colorEarnMoney;
                } else {
                  lblMoney.innerText = lblMoneyDefault;
                  currentColorMoney.value = colorMoneyDefault;
                }
                pokemonRequest();
              });
          }
        }
      }
    }
  } else {
    imageElement.value = event.target;
    lastAreaClicked.value = area;
    isReceived.value = false;
  }
}

function takeAbreak() {
  if (!isReceived.value) {
    var elements = document.getElementsByClassName("rightImages");
    var nameElements = document.getElementsByClassName("pokemonName");
    var pokemonToSleep = mapAreaPokemon.get(lastAreaClicked.value.name);
    for (var i = 0; i < elements.length; i++) {
      if (nameElements[i].textContent == pokemonToSleep.pokemon_object.name) {
        let styleElem = elements[i].children[1].children[0].style;
        styleElem.filter = "grayscale(0%)";
        styleElem.cursor = "pointer";
      }
    }
    if (mapAreaPokemon.get(lastAreaClicked.value.name) != null) {
      mapAreaPokemon.delete(lastAreaClicked.value.name);
    }

    imageElement.value.src = transparentImg;

    imageElement = ref(transparentImg);
    isReceived.value = true;
  }
}

onMounted(() => {
  lblRequest = document.getElementById("request");
  lblMoney = document.getElementById("money");
  fetchOwnedPokemons();
  fetchPokemonTypes();
  placeAreas();
  coroutine();
});

onUnmounted(() => {
  clearInterval(interval.value);
});
</script>

<template>
  <q-page>
    <h1>La pension</h1>
    <br />
    <p id="money" :class="`text-${currentColorMoney} text-h6`">
      {{ lblMoneyDefault }}
    </p>
    <q-page-sticky
      position="top-right"
      :offset="[18, 18]"
      class="text-h6 bg-white text-black border-info q-pa-sm rounded-borders z-top"
    >
      <span id="request" :class="`text-${currentColorRequest} text-h5`">
        {{ lblRequestEmpty }}
      </span>
    </q-page-sticky>
    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
        <div class="q-mr-md">
          <div v-for="(items, index) in areasPairs" :key="index" class="row">
            <div
              v-for="(item, index) in items"
              :key="index"
              class="col-xs-12 col-sm-12 col-md-9 col-lg-3 q-pa-sm"
            >
              <q-img
                v-if="item != 0"
                :src="item.image"
                style="outline: solid; max-width: 300px; height: 150px"
                fit="cover"
                :alt="item.name"
              >
                <q-img
                  style="
                    outline: solid;
                    max-width: 100px;
                    height: 100px;
                    margin-top: 2em;
                    margin-left: 7em;
                  "
                  fit="contain"
                  :src="transparentImg"
                  @click="receiveImage($event, item)"
                  class="hover-image"
                ></q-img>
              </q-img>
            </div>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-12 col-md-3 col-lg-3 column">
        <div
          id="scrolltarget"
          class="container q-pa-md"
          style="outline: solid; margin-top: 3em"
        >
          <q-scroll-area style="height: 20em">
            <h5>Mes Pokémon</h5>
            <br />
            <!-- Card list -->
            <div class="" v-for="(item, index) in ownedPokemons" :key="index">
              <q-card class="q-mb-sm">
                <div class="flex justify-center">
                  <q-card-section>
                    <div class="col justify-center items-center">
                      <div class="text-h7 row justify-center pokemonName">
                        {{ item.pokemon_object.name }}
                      </div>
                      <div class="text-h7 row justify-center">
                        <q-icon
                          name="sentiment_very_satisfied"
                          size="xs"
                          class="q-mr-sm"
                        />
                        {{ item.current_happiness }} /
                        {{
                          item.pokemon_object.pokemon_type_object.max_happiness
                        }}
                      </div>
                      <div
                        class="image-size-daycare row justify-center items-center q-my-sm q-mx-auto"
                      >
                        <!-- q-mx-auto is required to center fixed (max-)size content -->
                        <q-img
                          :src="item.pokemon_object.display_image_url"
                          :alt="pokemonAlt"
                          class="image-max-size-parent hover-image rightImages"
                          fit="contain"
                          @click="
                            sendImage($event, item);
                            changeTag($event);
                          "
                        />
                      </div>
                    </div>
                  </q-card-section>
                </div>
                <q-separator inset />
              </q-card>
            </div>
          </q-scroll-area>
        </div>

        <div class="column items-center q-mt-sm" style="order: -1">
          <h5>Zone de repos</h5>
          <q-img
            style="outline: solid; max-width: 300px; height: 100px"
            fit="contain"
            @click="takeAbreak"
            src="https://www.digitaltrends.com/wp-content/uploads/2023/02/Pokemon-sleep-art.jpg?p=1"
          >
          </q-img>
        </div>
        <div class="text-center q-mb-md q-mt-md">
          <q-btn color="green" :to="{ name: 'shop' }">
            <q-icon left size="xl" name="add_circle_outline" />
            <div>Acheter un Pokémon</div>
          </q-btn>
        </div>
      </div>
    </div>
  </q-page>
</template>

<style scoped></style>
