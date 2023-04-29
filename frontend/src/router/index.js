import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../views/HomeView.vue";
import { ref } from "vue";

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
      path: "/daycare",
      name: "daycare",
      component: () => import("../views/DaycareView.vue"),
      meta: { auth: true },
    },
    {
      path: "/pokemons:success?",
      name: "pokemons",
      props: true,
      component: () => import("../views/pokedex/PokemonView.vue"),
      meta: { auth: true },
    },
    {
      path: "/pokemons/create",
      name: "pokemons.create",
      component: () => import("../views/pokedex/CreatePokemonView.vue"),
      meta: {
        auth: true,
        manager: true,
      },
    },
    {
      path: "/pokemons/:id/edit",
      name: "pokemons.edit",
      component: () => import("../views/pokedex/CreatePokemonView.vue"),
      meta: {
        auth: true,
        manager: true,
      },
    },

    /* ====== SHOP ====== */
    {
      path: "/shop",
      name: "shop",
      component: () => import("../views/ShopView.vue"),
      meta: { auth: true },
    },

    /* ====== USERS ====== */
    {
      path: "/users/create",
      name: "users.create",
      component: () => import("../views/users/CreateUserView.vue"),
    },
    {
      path: "/users:success?:logout?",
      name: "users",
      component: () => import("../views/users/UserView.vue"),
    },
  ],
});

router.beforeEach((to, from, next) => {
  player.value = {
    isLogged: localStorage.getItem("isAuth") == "true",
    isManager: localStorage.getItem("isManager") == "true",
    // !xStorage.get => item is null or undefined
    // Note : another way to check if boolean would be using !JSON.parse(...)

    name: localStorage.getItem("playerName"),
  };

  const auth = to.matched.some((record) => record.meta.auth);
  const manager = to.matched.some((record) => record.meta.manager);

  if (auth && !player.value.isLogged) {
    next({ name: "users" });
    return;
  }

  if (manager && !player.value.isManager) {
    next({ name: "pokemons" });
    return;
  }

  next();
});

export const player = ref({});
export default router;
