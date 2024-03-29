<!-- eslint-disable prettier/prettier -->
<script setup>
import axios from "axios";
import { ref, onMounted } from "vue";

import { onConnect, onDisconnect } from "@/assets/js/persistanceLoginInfo";
import { varToString, sessionGetAndRemove } from "@/assets/js/utils.js"; // IMPORTANT : Need to be in { } to work !
import MessageBanner from "@/components/MessageBanner.vue";

import { useRouter } from "vue-router";

let successTitle = ref("");
let success = ref([]);
let errorsTitle = ref("");
let errors = ref([]);

const router = useRouter();

successTitle.value = sessionGetAndRemove(varToString({ successTitle }));
success.value = sessionGetAndRemove(varToString({ success }), true);

const username = ref("");
const password = ref("");

const submit = async () => {
  errors.value = [];
  errorsTitle.value = "";

  // Validation
  if (!username.value) {
    errors.value.push("Le nom est obligatoire.");
  }
  if (!password.value) {
    errors.value.push("Le mot de passe est obligatoire.");
  }

  if (errors.value.length) {
    errorsTitle.value =
      "Erreur avec les données du formulaire, veuillez les corriger :";

    return; // There is some error, stop the process
  }

  // Send to backend
  await axios
    .post("users/login/", {
      username: username.value,
      password: password.value,
    })
    .then(async () => {
      successTitle.value = "Connexion réussie !";
      success.value.push("Vous êtes connecté avec le pseudo " + username.value);

      sessionStorage.setItem(varToString({ successTitle }), successTitle.value);
      sessionStorage.setItem(
        varToString({ success }),
        JSON.stringify(success.value)
      );

      await axios.get("players/my-data/").then((response) => {
        const isManager = response.data.is_manager;
        const playerName = response.data.username;

        onConnect(true, isManager, playerName);
      });

      router.push({ name: "home" });
    })
    .catch(() => {
      errorsTitle.value = "Identification échouée";
      errors.value.push("Est-ce le bon nom d'utilisateur et mot de passe ?");

      onDisconnect();
    });
};

onMounted(() => {
  const logout = router.currentRoute.value.query.logout;

  if (logout == "true") {
    successTitle.value = "Déconnexion réussie !";
    success.value = [];
    success.value.push("Vous êtes déconnecté.");

    sessionStorage.setItem(varToString({ successTitle }), successTitle.value);
    sessionStorage.setItem(
      varToString({ success }),
      JSON.stringify(success.value)
    );
  }
});
</script>

<template>
  <q-page padding>
    <q-form class="q-gutter-md" @submit="submit()">
      <div class="row self-center justify-evenly">
        <div class="col-12 col-sm-10 col-md-8">
          <q-card class="q-pa-lg">
            <q-card-section class="">
              <q-btn color="blue-grey" :to="{ name: 'home' }">
                <q-icon left name="arrow_back_ios" />
                Retour
              </q-btn>
            </q-card-section>

            <q-card-section class="text-center">
              <div class="text-h5">Se connecter</div>
            </q-card-section>

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

            <q-card-section>
              <q-input
                v-model="username"
                label="*Nom"
                class="q-mb-md"
                outlined
                autofocus
                maxlength="30"
                :rules="[(val) => !!val || 'Champs requis']"
              >
                <template v-slot:prepend>
                  <q-icon name="badge" />
                </template>
              </q-input>
              <q-input
                v-model="password"
                type="password"
                label="*Mot de passe"
                class="q-mb-md"
                outlined
                maxlength="50"
                :rules="[(val) => !!val || 'Champs requis']"
              >
                <template v-slot:prepend>
                  <q-icon name="password" />
                </template>
              </q-input>
            </q-card-section>

            <q-card-section class="q-gutter-y-sm">
              <div class="row justify-center q-gutter-sm">
                <q-btn
                  type="submit"
                  color="green"
                  class="col-12 col-sm-8 col-md-6"
                >
                  <q-icon left name="fact_check" />
                  <div>Se connecter</div>
                </q-btn>

                <!-- using query to keep the username on the "create page" -->
                <q-btn
                  color="indigo"
                  :to="{
                    name: 'users.create',
                    query: { username: username },
                  }"
                  class="col-12 col-sm-8 col-md-6"
                >
                  <q-icon left name="person_add" />
                  Créer un compte
                </q-btn>
              </div>
            </q-card-section>
          </q-card>
        </div>
      </div>
    </q-form>
  </q-page>
</template>
