<template>
  <h3 style="text-align: center">Booking Calendar for: {{ deviceName }}</h3>
  <v-divider></v-divider>

  <v-dialog v-model="addEventDialog" width="auto">
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
        <v-switch
          v-model="currentEvent.allDay"
          label="All Day Event?"
        ></v-switch>
        <v-btn class="mt-1" type="submit" block>Submit</v-btn>
        <v-btn
          class="mt-1"
          @click="
            addEventDialog = false;
            clearCurrentEvent();
          "
          block
          >Cancel</v-btn
        >
      </v-form>
    </v-sheet>
  </v-dialog>

  <v-dialog v-model="eventDetailDialog" width="auto">
    <v-sheet class="mx-auto" width="400">
      <v-card-title>
        <span class="headline">Details</span>
      </v-card-title>
      <v-form>
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
        <v-btn
          class="mt-1"
          @click="
            editEventDialog = true;
            eventDetailDialog = false;
          "
          block
          >Edit</v-btn
        >
        <v-btn
          class="mt-1"
          @click="
            deleteEvent();
            eventDetailDialog = false;
          "
          block
          >Delete</v-btn
        >
        <v-btn
          class="mt-1"
          @click="
            eventDetailDialog = false;
            clearCurrentEvent();
          "
          block
          >Cancel</v-btn
        >
      </v-form>
    </v-sheet>
  </v-dialog>

  <v-dialog v-model="editEventDialog">
    <v-sheet class="mx-auto" max-width="800">
      <v-card width="785">
        <v-card-title>
          <span class="title-center">Edit Event</span>
        </v-card-title>
        <v-form @submit.prevent="submitEditEvent">
          <v-row>
            <v-col cols="6">
              <v-text-field
                v-model="currentEvent.title"
                label="title"
              ></v-text-field>
              <v-textarea
                v-model="currentEvent.desc"
                label="description"
              ></v-textarea>
              <v-switch
                v-model="currentEvent.allDay"
                label="All Day Event?"
              ></v-switch>
              <v-btn class="mt-1" type="submit" block>Submit</v-btn>
              <v-btn
                class="mt-1"
                @click="
                  deleteEvent();
                  editEventDialog = false;
                "
                block
                >Delete</v-btn
              >
              <v-btn
                class="mt-1"
                @click="
                  editEventDialog = false;
                  clearCurrentEvent();
                "
                block
                >Cancel</v-btn
              >
            </v-col>
            <v-col cols="4">
              <v-date-picker></v-date-picker>
              <v-time-picker></v-time-picker>
            </v-col>
          </v-row>
        </v-form>
      </v-card>
    </v-sheet>
  </v-dialog>

  <FullCalendar ref="fullCalendar" class="calendar" :options="calendarOptions">
    <template v-slot:eventContent="arg">
      <b>{{ arg.timeText }}</b>
      <i>{{ arg.event.title }}</i>
    </template>
  </FullCalendar>
</template>

<script lang="ts">
import { defineComponent, ref, reactive, toRefs, onMounted } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { EventApi, EventInput } from "@fullcalendar/core";
import { VTimePicker } from 'vuetify/labs/VTimePicker'

interface CurrentEvent extends EventInput {
  desc?: string;
}

export default defineComponent({
  props: {
    deviceName: {
      type: String,
      required: true,
    },
  },
  components: {
    FullCalendar,
    VTimePicker,
  },
  setup(props) {
    console.log("props", props);
    const addEventDialog = ref(false);
    const editEventDialog = ref(false);
    const eventDetailDialog = ref(false);
    const fullCalendar = ref<InstanceType<typeof FullCalendar> | null>(null);
    const calendarApi = ref<ReturnType<
      InstanceType<typeof FullCalendar>["getApi"]
    > | null>(null);
    const currentEvent = reactive<CurrentEvent>({
      title: "",
      desc: "",
      start: undefined,
      end: undefined,
      allDay: false,
    });
    const currentEvents = ref<EventApi[]>([]);
    const rules = {
      required: (value: string | boolean) => !!value || "Required.",
    };
    onMounted(() => {
      if (fullCalendar.value) {
        calendarApi.value = fullCalendar.value.getApi();
      }
    });
    const calendarOptions = reactive({
      plugins: [dayGridPlugin, timeGridPlugin, interactionPlugin],
      headerToolbar: {
        left: "prev,next today",
        center: "title",
        right: "dayGridMonth,timeGridWeek,timeGridDay",
      },
      initialView: "timeGridWeek",
      initialEvents: [
        {
          id: "1",
          title: "All-day event",
          start: new Date().toISOString().replace(/T.*$/, ""),
        },
        {
          id: "2",
          title: "Timed event",
          start: new Date().toISOString().replace(/T.*$/, "") + "T12:00:00",
        },
      ],
      editable: true,
      selectable: true,
      selectMirror: true,
      dayMaxEvents: true,
      weekends: true,
      eventResizableFromStart: true,
      select: handleDateSelect,
      eventClick: handleEventClick,
      eventsSet: handleEvents,
      eventAdd: handleEventAdd,
      eventRemove: handleEventRemove,
      eventDrop: handleEventDrop,
      eventResize: handleEventResize,
    });

    function submitAddEvent(): void {
      addEventDialog.value = false;
      if (calendarApi.value === null) return; // should not happen
      calendarApi.value.addEvent({
        id: (calendarApi.value.getEvents().length + 1).toString(),
        title: currentEvent.title,
        start: currentEvent.start,
        end: currentEvent.end,
        allDay: currentEvent.allDay,
        extendedProps: {
          description: currentEvent.desc,
        },
      });
    }

    function submitEditEvent(): void {
      editEventDialog.value = false;
      if (calendarApi.value === null) return; // should not happen
      const event = currentEvent.id
        ? calendarApi.value.getEventById(currentEvent.id)
        : null;
      if (event) {
        event.setProp("title", currentEvent.title);
        event.setExtendedProp("description", currentEvent.desc);
        event.setAllDay(currentEvent.allDay ?? false);
        handleEventChange(event);
      } else {
        console.error("submitEditEvent: event not found");
      }
    }

    function deleteEvent(): void {
      if (!confirm("Are you sure you want to delete this event?")) return;
      if (calendarApi.value === null) return; // should not happen
      const event = currentEvent.id
        ? calendarApi.value.getEventById(currentEvent.id)
        : null;
      if (event) {
        event.remove();
      } else {
        console.error("deleteEvent: event not found");
      }
      clearCurrentEvent();
    }

    function clearCurrentEvent(): void {
      Object.assign(currentEvent, {
        title: "",
        desc: "",
        start: undefined,
        end: undefined,
        allDay: false,
      });
    }

    function handleDateSelect(selectInfo: any): void {
      currentEvent.start = selectInfo.startStr;
      currentEvent.end = selectInfo.endStr;
      addEventDialog.value = true;
    }

    function handleEventClick(clickInfo: any): void {
      Object.assign(currentEvent, {
        id: clickInfo.event.id,
        title: clickInfo.event.title,
        desc: clickInfo.event.extendedProps.description,
        start: clickInfo.event.start,
        end: clickInfo.event.end,
        allDay: clickInfo.event.allDay,
      });
      eventDetailDialog.value = true;
    }

    function handleEventDrop(arg: { event: EventApi }): void {
      console.log("dropped:", arg.event);
      handleEventChange(arg.event);
    }

    function handleEventResize(arg: { event: EventApi }): void {
      console.log("resized:", arg.event);
      handleEventChange(arg.event);
    }

    function handleEvents(events: EventApi[]): void {
      currentEvents.value = events;
      console.log("handleEvents");
    }

    function handleEventAdd(arg: { event: EventApi }): void {
      console.log("adding to database:", arg.event);
    }

    function handleEventChange(event: EventApi): void {
      console.log("changing in database:", event);
    }

    function handleEventRemove(arg: { event: EventApi }): void {
      console.log("removing from database:", arg.event);
    }

    return {
      ...toRefs(
        reactive({
          fullCalendar,
          deviceName: props.deviceName,
          addEventDialog,
          editEventDialog,
          eventDetailDialog,
          currentEvent,
          currentEvents,
          rules,
          calendarOptions,
          submitAddEvent,
          submitEditEvent,
          deleteEvent,
          clearCurrentEvent,
          handleDateSelect,
          handleEventClick,
          handleEventDrop,
          handleEventResize,
          handleEvents,
          handleEventAdd,
          handleEventChange,
          handleEventRemove,
        })
      ),
    };
  },
});
</script>

<style lang="css" scoped>
.title-center {
  justify-content: center;
}
</style>
