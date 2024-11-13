<template>
  <h3 style="text-align: center">Booking Calendar for: {{ deviceName }}</h3>
  <p style="text-align: center">Id: {{ deviceId }}</p>
  <v-divider></v-divider>

  <AddEventDialog
    :event="currentEvent"
    :isOpen="addEventDialog"
    @submit="submitAddEvent"
    @close="
      addEventDialog = false;
    "
  />

  <EventDetailDialog
    :event="currentEvent"
    :isOpen="eventDetailDialog"
    @edit="
      eventDetailDialog = false;
      editEventDialog = true;
    "
    @delete="
      deleteEvent();
      eventDetailDialog = false;
    "
    @close="eventDetailDialog = false"
  />

  <EditEventDialog
    :event="currentEvent"
    :isOpen="editEventDialog"
    @submit="submitEditEvent"
    @close="editEventDialog = false"
    @delete="
      deleteEvent();
      editEventDialog = false;
    "
  />

  <FullCalendar ref="fullCalendar" class="calendar" :options="calendarOptions">
    <template v-slot:eventContent="arg">
      <b>{{ arg.timeText }}</b>
      <i>{{ arg.event.title }}</i>
    </template>
  </FullCalendar>
</template>

<script lang="ts">
import { useRoute } from 'vue-router';
import { defineComponent, ref, reactive, toRefs, onMounted, toRaw } from "vue";
import FullCalendar from "@fullcalendar/vue3";
import dayGridPlugin from "@fullcalendar/daygrid";
import timeGridPlugin from "@fullcalendar/timegrid";
import interactionPlugin from "@fullcalendar/interaction";
import { EventApi, EventInput } from "@fullcalendar/core";

interface CurrentEvent extends EventInput {
  desc?: string;
  // for displaying date in dialog, not for storing, it's different from the startStr from FullCalendar
  startStr?: string;
  endStr?: string;
}

interface Booking {
  title: string,
  description: string,
  datetime_start: Date | null,
  datetime_end: Date | null,
  user: string | null,
  device_instance: string,
}



export default defineComponent({
  props: {
    deviceName: {
      type: String,
      required: true,
    }
  },
  components: {
    FullCalendar,
  },
  setup() {
    const route = useRoute();
    const deviceName = ref(route.query.deviceName || '');
    const deviceId = ref(route.query.deviceId as string || '');
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
    const currentEvents = ref<EventInput[]>([]);
    const rules = {
      required: (value: string | boolean) => !!value || "Required.",
    };
    onMounted(() => {
      if (fullCalendar.value) {
        calendarApi.value = fullCalendar.value.getApi();
        fetchEvents();
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
      // initialEvents: toRaw(currentEvents.value),
      events: currentEvents,
      editable: true,
      selectable: true,
      selectMirror: true,
      dayMaxEvents: true,
      weekends: true,
      eventResizableFromStart: true,
      locale: "de",
      slotLabelFormat: {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      },
      eventTimeFormat: {
        hour: "2-digit",
        minute: "2-digit",
        hour12: false,
      },
      select: handleDateSelect,
      eventClick: handleEventClick,
      eventsSet: handleEvents,
      eventAdd: handleEventAdd,
      eventRemove: handleEventRemove,
      eventDrop: handleEventDrop,
      eventResize: handleEventResize,
    });

    function submitAddEvent(event: CurrentEvent): void {
      addEventDialog.value = false;
      if (calendarApi.value === null) return; // should not happen
      calendarApi.value.addEvent({
        id: (calendarApi.value.getEvents().length + 1).toString(),
        title: event.title,
        start: event.start,
        end: event.end,
        allDay: event.allDay,
        extendedProps: {
          description: event.desc,
        },
      });
    }

    function submitEditEvent(newEvent: CurrentEvent): void {
      console.log("submitedit", newEvent.endStr);
      console.log("typeof newEvent");
      editEventDialog.value = false;
      if (calendarApi.value === null) return; // should not happen
      const event = currentEvent.id
        ? calendarApi.value.getEventById(currentEvent.id)
        : null;
      if (event) {
        event.setProp("title", newEvent.title);
        event.setExtendedProp("description", newEvent.desc);
        if (newEvent.start) event.setStart(newEvent.start);
        if (newEvent.end) event.setEnd(newEvent.end);
        event.setAllDay(newEvent.allDay ?? false);
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
    }

    function handleDateSelect(selectInfo: any): void {
      currentEvent.title = "";
      currentEvent.desc = "";
      currentEvent.start = selectInfo.start;
      currentEvent.end = selectInfo.end ? selectInfo.end : selectInfo.start;
      currentEvent.startStr = dateStrToReadable(selectInfo.startStr);
      currentEvent.endStr = dateStrToReadable(selectInfo.endStr);
      currentEvent.allDay = selectInfo.allDay;
      addEventDialog.value = true;
    }

    function handleEventClick(clickInfo: any): void {
      Object.assign(currentEvent, {
        id: clickInfo.event.id,
        title: clickInfo.event.title,
        desc: clickInfo.event.extendedProps.description,
        start: clickInfo.event.start,
        end: clickInfo.event ? clickInfo.event.end : clickInfo.event.start,
        startStr: dateStrToReadable(clickInfo.event.startStr),
        endStr: dateStrToReadable(clickInfo.event.endStr),
        allDay: clickInfo.event.allDay,
      });
      // console.log("handleEventClick,ce:", currentEvent);
      eventDetailDialog.value = true;
    }

    function dateStrToReadable(date: string): string {
      return date.slice(0, 10) + " " + date.slice(11, 16);
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
      console.log("handleEvents");
    }

    async function handleEventAdd(arg: { event: EventApi }): Promise<void> {
      console.log("adding to database:", arg.event);
      console.log("currentEvent:", currentEvent);
      const booking: Booking = {
        title: arg.event.title,
        description: arg.event.extendedProps.description,
        datetime_start: arg.event.start,
        datetime_end: arg.event.end,
        user: null, // todo: provide a valid user value
        device_instance: deviceId.value,
      };
      fetch('http://127.0.0.1:8000/api/bookings/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(booking),
      })
        .then(response => response.json())
        .then(data => {
          console.log('Success:', data);
        })
        .catch((error) => {
          console.error('Error:', error);
        });
    }

    function handleEventChange(event: EventApi): void {
      console.log("changing in database:", event);
    }

    function handleEventRemove(arg: { event: EventApi }): void {
      console.log("removing from database:", arg.event);
    }

    async function fetchEvents(): Promise<void> {
  try {
    const response = await fetch('http://localhost:8000/api/bookings/?device_instance=' + deviceId.value);
    const data = await response.json();
    console.log('Fetch events Success:', data);

    currentEvents.value = data.map((booking: Booking) => ({
      title: booking.title,
      start: booking.datetime_start,
      end: booking.datetime_end,
      allDay: false,
      extendedProps: {
        description: booking.description,
      },
    }));
    console.log("currentEvents:", currentEvents.value);
  } catch (error) {
    console.error('Error:', error);
  }
}

    return {
      ...toRefs(
        reactive({
          fullCalendar,
          deviceName,
          deviceId,
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
