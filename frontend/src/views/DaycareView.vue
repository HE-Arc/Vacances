<script setup>
import axios from "axios";
import { ref, onMounted, onUnmounted } from "vue";

import { areas } from "@/assets/js/areasData.js";
import transparentImg from "@/assets/images/transparent.png";

const ownedPokemons = ref([]);
const interval = ref(null);

const isReceived = ref(true);

const tag = ref("");

const pokemonTypes = ref([]);

const areasPairs = ref([]);

const tempImage = ref(null);

var imageElement = ref(null);

var listPokemonMoved = ref([]);

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
var randomIndexZone = null;

function pokemonRequest() {
  if (listPokemonMoved.value.length > 0) {
    randomIndexPokemon = Math.floor(
      Math.random() * listPokemonMoved.value.length
    );
    randomIndexZone = Math.floor(Math.random() * areas.length);

    document.getElementById("Request").innerText =
      listPokemonMoved.value[randomIndexPokemon].pokemon_object.name +
      " aimerait aller à la " +
      areas[randomIndexZone].name +
      ".";
  }
}

function coroutine() {
  interval.value = setInterval(pokemonRequest, 5000); // 30000
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

function receiveImage(event, image) {
  if (imageElement.value != "") {
    if (tag.value == "pokemon") {
      event.target.src = imageElement.value.src;

      tag.value = "";

      isReceived.value = true;

      imageElement.value.style.filter = "grayscale(100%)";
      imageElement.value.style.cursor = "default";

      listPokemonMoved.value.push(pokemonCurrent);
    } else {
      if (isReceived.value) {
        if (event.target.src != transparentImg) {
          imageElement.value = event.target;
          isReceived.value = false;
        }
      } else {
        tempImage.value = event.target.src;
        event.target.src = imageElement.value.src;

        isReceived.value = true;

        imageElement.value.src = tempImage.value;

        if (randomIndexZone != null) {
          if (areas[randomIndexZone].image == image) {
            const id = listPokemonMoved.value[randomIndexPokemon].id;
            axios
              .post(`owned-pokemons/${id}/increment-happiness/`)
              .then((ownedpkm) => {
                listPokemonMoved.value[randomIndexPokemon].current_happiness =
                  ownedpkm.data.current_happiness;
                randomIndexZone = null;
                document.getElementById("Request").innerText = "";

                if (
                  listPokemonMoved.value[randomIndexPokemon]
                    .current_happiness == 0
                ) {
                  document.getElementsByClassName("money")[0].innerText =
                    "Vous avez gagné " +
                    listPokemonMoved.value[randomIndexPokemon].pokemon_object
                      .pokemon_type_object.cash_factor *
                      10 +
                    " ₽ grâce au bonheur de " +
                    listPokemonMoved.value[randomIndexPokemon].pokemon_object
                      .name +
                    " !";
                } else {
                  document.getElementsByClassName("money")[0].innerText = "";
                }
              });
          }
        }
      }
    }
  } else {
    imageElement.value = event.target;
    isReceived.value = false;
  }
}

function takeAbreak() {
  if (!isReceived.value) {
    var elements = document.getElementsByClassName("rightImages");
    for (var i = 0; i < elements.length; i++) {
      if (elements[i].children[1].children[0].src == imageElement.value.src) {
        let styleElem = elements[i].children[1].children[0].style;
        styleElem.filter = "grayscale(0%)";
        styleElem.cursor = "pointer";
      }
    }

    for (var j = 0; j < listPokemonMoved.value.length; j++) {
      if (
        listPokemonMoved.value[j].display_image_url == imageElement.value.src
      ) {
        listPokemonMoved.value.splice(j, 1);
        document.getElementById("Request").innerText = "";
      }
    }
    imageElement.value.src = transparentImg;

    imageElement = ref(transparentImg);
    isReceived.value = true;
  }
}

onMounted(() => {
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
    <p class="money"></p>
    <br />
    <p id="Request" style="color: deeppink; font-size: 2em"></p>
    <div class="row">
      <div class="col-xs-12 col-sm-12 col-md-9 col-lg-9">
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
                @click="receiveImage($event, item.image)"
                class="hover-image"
              ></q-img>
            </q-img>
          </div>
        </div>
      </div>
      <div class="col-xs-12 col-sm-12 col-md-3 col-lg-3 q-pl-xl">
        <div
          id="scrolltarget"
          class="container"
          style="outline: solid; outline-offset: 2em; margin-top: 3em"
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
                      <div class="text-h7 row justify-center">
                        {{ item.pokemon_object.name }}
                      </div>
                      <div class="text-h7 row justify-left">
                        {{ item.current_happiness }} /
                        {{
                          item.pokemon_object.pokemon_type_object.max_happiness
                        }}
                      </div>
                      <div
                        class="image-size-daycare row justify-center items-center q-ma-sm"
                      >
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
        <br />
        <div>
          <br />
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
