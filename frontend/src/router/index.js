import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: HomeView,
    },
    {
      path: "/about",
      name: "about",
      component: () => import("../views/AboutView.vue"),
    },
    {
      path: "/pokemons:success?",
      name: "pokemons",
      props: true,
      component: () => import("../views/PokemonView.vue"),
    },
    {
      path: "/pokemons/create",
      name: "pokemons.create",
      component: () => import("../views/CreatePokemonView.vue"),
    },
  ],
});

export default router;
