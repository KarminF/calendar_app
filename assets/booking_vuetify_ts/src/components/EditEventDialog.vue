<!-- eslint-disable vue/no-mutating-props -->
<template>
  <v-dialog v-model="isOpen" width="auto">
    <v-btn @click="debug">debug</v-btn>
    <v-sheet width="400">
      <v-card-title>
        <span>Edit Event</span>
      </v-card-title>
      <v-form @submit.prevent="submitEvent">
        <v-text-field v-model="currentEvent.title" label="title"></v-text-field>
        <v-textarea
          v-model="currentEvent.desc"
          label="description"
        ></v-textarea>

        <v-menu v-model="datePickerStart" :close-on-content-click="false">
          <template v-slot:activator="{ props }">
            <v-text-field
              v-model="currentEvent.startStr"
              label="from"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="props"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="currentEvent.start"
            @update:model-value="datePickerStart = false"
          ></v-date-picker>
        </v-menu>

        <v-menu v-model="datePickerEnd" :close-on-content-click="false">
          <template v-slot:activator="{ props }">
            <v-text-field
              v-model="currentEvent.endStr"
              label="to"
              prepend-icon="mdi-calendar"
              readonly
              v-bind="props"
            ></v-text-field>
          </template>
          <v-date-picker
            v-model="currentEvent.end"
            @update:model-value="datePickerEnd = false"
          ></v-date-picker>
        </v-menu>

        <v-switch
          v-model="currentEvent.allDay"
          label="All Day Event?"
        ></v-switch>
        <v-btn class="mt-1" type="submit" block>Submit</v-btn>
        <v-btn class="mt-1" @click="deleteEvent" block>Delete</v-btn>
        <v-btn class="mt-1" @click="closeDialog" block>Cancel</v-btn>
      </v-form>
    </v-sheet>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, toRefs, watch } from "vue";
import { EventInput } from "@fullcalendar/core";
import { VTimePicker } from "vuetify/labs/VTimePicker";

interface Event extends EventInput {
  start: Date;
  end?: Date;
  desc?: string;
}

export default defineComponent({
  components: {
    VTimePicker,
  },
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
  emits: ["close", "submit", "delete"],
  setup(props, { emit }) {
    const debug = () => {
      console.log("currentEvent start", currentEvent.value.start);
      console.log("instanceof Date", currentEvent.value.start instanceof Date);
    };
    const currentEvent = ref({ ...props.event });
    const selectedDate = ref(null);
    const selectedTime = ref(null);
    const datePickerStart = ref(false);
    const datePickerEnd = ref(false);
    const timePicker = ref(false);
    const dateSelection = ref("");
    const timeSelection = ref("");
    const submitEvent = () => {
      emit("submit", currentEvent.value);
    };
    const closeDialog = () => {
      emit("close");
    };
    const deleteEvent = () => {
      emit("delete");
    };
    const formatDate = (date: Date) =>{
      console.log("dateeeeeee", date);
      console.log(date instanceof Date);
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0"); // months are zero indexed
      const day = String(date.getDate()).padStart(2, "0");
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");

      return `${year}-${month}-${day} ${hours}:${minutes}`;
    }

    watch(
      () => currentEvent.value.start,
      (newVal) => {
        if (newVal) {
          currentEvent.value.startStr = formatDate(newVal);
        }
      }
    )

    watch(
      () => currentEvent.value.end,
      (newVal) => {
        if (newVal) {
          currentEvent.value.endStr = formatDate(newVal);
        }
      }
    )

    return {
      ...toRefs({
        debug,
        currentEvent,
        selectedDate,
        selectedTime,
        datePickerStart,
        datePickerEnd,
        timePicker,
        dateSelection,
        timeSelection,
        submitEvent,
        closeDialog,
        deleteEvent,
      }),
    };
  },
  watch: {
    isOpen(val) {
      if (val) {
        this.currentEvent = { ...this.event };
      }
    }
  },
});
</script>
