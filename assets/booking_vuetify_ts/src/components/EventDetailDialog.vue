<!-- eslint-disable vue/no-mutating-props -->
<template>
  <v-dialog v-model="isOpen" width="auto">
    <v-sheet class="mx-auto" width="400">
      <v-card-title>
        <span class="headline">Details</span>
      </v-card-title>
      <v-text-field
        v-model="currentEvent.title"
        label="title"
        readonly
      ></v-text-field>
      <v-textarea
        v-model="currentEvent.desc"
        label="description"
        readonly
      ></v-textarea>
      <v-text-field
        v-model="currentEvent.startStr"
        label="from"
        readonly
      ></v-text-field>
      <v-text-field
        v-model="currentEvent.endStr"
        label="to"
        readonly
      ></v-text-field>
      <v-btn class="mt-1" @click="editEvent" block>Edit</v-btn>
      <v-btn class="mt-1" @click="deleteEvent" block>Delete</v-btn>
      <v-btn class="mt-1" @click="closeDialog" block>Cancel</v-btn>
    </v-sheet>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { EventInput } from "@fullcalendar/core";

interface Event extends EventInput {
  desc?: string;
}

export default defineComponent({
  props: {
    isOpen: {
      type: Boolean,
      required: true,
    },
    event: {
      type: Object as PropType<Event>,
      required: true,
    },
  },
  emits: ["close", "edit", "delete"],
  data() {
    return {
      currentEvent: { ...this.event },
    };
  },
  watch: {
    isOpen(val) {
      if (val) {
        this.currentEvent = { ...this.event };
      }
    },
  },
  methods: {
    editEvent() {
      this.$emit("edit");
    },
    closeDialog() {
      this.$emit("close");
    },
    deleteEvent() {
      this.$emit("delete");
    },
  },
});
</script>
