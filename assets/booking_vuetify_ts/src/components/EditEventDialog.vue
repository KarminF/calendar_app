
<template>
  <v-dialog v-model="localIsOpen" width="auto">
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

        <v-text-field
          v-model="currentEvent.startStr"
          :active="dialogStart"
          :focused="dialogStart"
          label="Picker in dialog"
          prepend-icon="mdi-clock-time-four-outline"
          readonly
        >
          <v-dialog v-model="dialogStart" activator="parent" width="auto">
            <v-date-picker
              v-if="datePickerStart"
              v-model="selectedDateStart"
              @update:model-value="
                datePickerStart = false;
                timePickerStart = true;
              "
            ></v-date-picker>
            <v-time-picker
              v-if="timePickerStart"
              format="24hr"
              v-model="selectedTimeStart"
              @update:model-value="
                timePickerStart = false;
                dialogStart = false;
              "
            ></v-time-picker>
          </v-dialog>
        </v-text-field>

        <v-text-field
          v-model="currentEvent.endStr"
          :active="dialogEnd"
          :focused="dialogEnd"
          label="Picker in dialog"
          prepend-icon="mdi-clock-time-four-outline"
          readonly
        >
          <v-dialog v-model="dialogEnd" activator="parent" width="auto">
            <v-date-picker
              v-if="datePickerEnd"
              v-model="selectedDateEnd"
              @update:model-value="
                datePickerEnd = false;
                timePickerEnd  = true;
              "
            ></v-date-picker>
            <v-time-picker
              v-if="timePickerEnd"
              format="24hr"
              v-model="selectedTimeEnd "
              @update:model-value="
                timePickerEnd  = false;
                dialogEnd = false;
              "
            ></v-time-picker>
          </v-dialog>
        </v-text-field>

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
      console.log("currentEvent end", currentEvent.value.end);
      console.log("selectedTimeStart", selectedTimeStart.value);
      console.log("selectedTimeEnd", selectedTimeEnd.value);
    };
    const localIsOpen = ref(props.isOpen);
    const currentEvent = ref({ ...props.event });
    const selectedDateStart = ref(new Date());
    const selectedTimeStart = ref("");
    const selectedDateEnd = ref(new Date());
    const selectedTimeEnd = ref("");
    const dialogStart = ref(false);
    const dialogEnd = ref(false);
    const datePickerStart = ref(false);
    const datePickerEnd = ref(false);
    const timePickerStart = ref(false);
    const timePickerEnd = ref(false);
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
    const formatDate = (date: Date) => {
      const year = date.getFullYear();
      const month = String(date.getMonth() + 1).padStart(2, "0"); // months are zero indexed
      const day = String(date.getDate()).padStart(2, "0");
      const hours = String(date.getHours()).padStart(2, "0");
      const minutes = String(date.getMinutes()).padStart(2, "0");

      return `${year}-${month}-${day} ${hours}:${minutes}`;
    };

    const addTimeToDate = (time: string, date: Date, isStart: boolean) => {
      const [hours, minutes] = time.split(":").map(Number);
      date.setHours(hours);
      date.setMinutes(minutes);
      if(isStart) currentEvent.value.start = date;
      else currentEvent.value.end = date;
    };

    watch(
      () => props.isOpen,
      (val) => {
        localIsOpen.value = val;
        console.log("props.isOpen", val);
        console.log("localIsOpen", localIsOpen.value);
      }
    );
    
    watch(
      () => localIsOpen.value,
      (val) => {
        if (!val) {
          emit("close");
        }
      }
    )

    watch(
      () => dialogStart.value,
      (val) => {
        datePickerStart.value = val;
      }
    );

    watch(
      () => dialogEnd.value,
      (val) => {
        datePickerEnd.value = val;
      }
    );

    watch(
      () => selectedTimeStart.value,
      (val) => {
        addTimeToDate(val, selectedDateStart.value, true);
      }
    );

    watch(
      () => selectedTimeEnd.value,
      (val) => {
        addTimeToDate(val, selectedDateEnd.value, false);
      }
    );

    watch(
      () => currentEvent.value.start,
      (newVal) => {
        if (newVal) {
          currentEvent.value.startStr = formatDate(newVal);
        }
      }
    );

    watch(
      () => currentEvent.value.end,
      (newVal) => {
        if (newVal) {
          currentEvent.value.endStr = formatDate(newVal);
        }
      }
    );

    return {
      ...toRefs({
        localIsOpen,
        debug,
        currentEvent,
        selectedDateStart,
        selectedTimeStart,
        selectedDateEnd,
        selectedTimeEnd,
        dialogStart,
        dialogEnd,
        datePickerStart,
        datePickerEnd,
        timePickerStart,
        timePickerEnd,
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
    },
  },
});
</script>
