<template>
  <q-banner
    v-if="title || items.length"
    inline-actions
    :class="`q-mb-lg text-${fontColor} bg-${color}`"
  >
    <template v-slot:avatar>
      <q-icon left size="md" :name="icon" />
    </template>
    <div class="text-h6">
      {{ title }}

      <q-list dense class="text-subtitle2">
        <q-item v-for="(item, index) in items" :key="index">
          {{ item }}
        </q-item>
      </q-list>
    </div>
  </q-banner>
</template>

<script>
export default {
  props: {
    title: String,
    items: {
      type: Array,
      default: () => [],
    },
    icon: {
      type: String,
      default: "info",
    },
    color: {
      type: String,
      default: "blue",
    },
    fontColor: {
      type: String,
      default: "white",
    },
  },
};
</script>
