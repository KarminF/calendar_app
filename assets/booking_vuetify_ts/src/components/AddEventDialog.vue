<template>
<v-dialog v-model="isOpen" width="auto">
    <v-sheet class="mx-auto" width="400">
      <v-card-title>
        <span class="headline">New Event</span>
      </v-card-title>
      <v-form @submit.prevent="submitAddEvent">
        <v-text-field v-model="currentEvent.title" label="title"></v-text-field>
        <v-textarea
          v-model="currentEvent.desc"
          label="description"
        ></v-textarea>
        <v-text-field
          v-model="currentEvent.start"
          label="from"
          readonly
        ></v-text-field>
        <v-text-field
          v-model="currentEvent.end"
          label="to"
          readonly
        ></v-text-field>
        <v-switch
          v-model="currentEvent.allDay"
          label="All Day Event?"
        ></v-switch>
        <v-btn class="mt-1" type="submit" block>Submit</v-btn>
        <v-btn
          class="mt-1"
          @click="closeDialog"
          block
          >Cancel</v-btn
        >
      </v-form>
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
  emits: ["submit", "close"],
  data() {
    return {
      currentEvent: { ...this.event }
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
    submitAddEvent() {
      this.$emit("submit", this.currentEvent);
    },
    closeDialog() {
      this.$emit("close");
    },
  },
});
</script>
