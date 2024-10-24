<!-- eslint-disable vue/no-mutating-props -->
<template>
  <v-dialog v-model="isOpen" width="auto">
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
        <v-text-field
          v-model="currentEvent.start"
          label="from"
          readonly
          @click="startClick"
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
        <v-btn class="mt-1" @click="deleteEvent" block>Delete</v-btn>
        <v-btn class="mt-1" @click="closeDialog" block>Cancel</v-btn>
        <v-dialog v-model="datePicker">
          <v-date-picker
            v-model="dateSelection"
            @change="datePicker = false"
          ></v-date-picker>
        </v-dialog>
        <v-dialog v-model="timePicker">
          <v-time-picker v-model="startObj"></v-time-picker>
        </v-dialog>
      </v-form>
    </v-sheet>
  </v-dialog>
</template>

<script lang="ts">
import { defineComponent, PropType, ref, toRefs } from "vue";
import { EventInput } from "@fullcalendar/core";
import { VTimePicker } from "vuetify/labs/VTimePicker";

interface Event extends EventInput {
  start: string;
  end?: string;
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
    const currentEvent = ref({ ...props.event });
    const startObj = ref(new Date());
    const endObj = ref(new Date());
    const datePicker = ref(false);
    const timePicker = ref(false);
    const dateSelection = ref("");
    const timeSelection = ref("");
    const startClick = () => {
      datePicker.value = true;
    };
    const submitEvent = () => {
      emit("submit", currentEvent.value);
    };
    const closeDialog = () => {
      emit("close");
    };
    const deleteEvent = () => {
      emit("delete");
    };
    return {
      ...toRefs({
        currentEvent,
        startObj,
        endObj,
        datePicker,
        timePicker,
        dateSelection,
        timeSelection,
        startClick,
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
        this.startObj = new Date(this.event.start.replace("T", " "));
        this.startObj.getDate();
      }
    },
  },
});
</script>
