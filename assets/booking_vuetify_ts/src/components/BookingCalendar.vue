<template>
  <h3 style="text-align: center">Booking Calendar for: {{ deviceName }}</h3>
  <v-divider></v-divider>

  <AddEventDialog
    :event="currentEvent"
    :isOpen="addEventDialog"
    @submit="submitAddEvent"
    @close="
      addEventDialog = false;
      clearCurrentEvent();
    "
  />

  <EventDetailDialog
    :event="currentEvent"
    :isOpen="eventDetailDialog"
    @edit="
      editEventDialog = true;
      eventDetailDialog = false;
    "
    @delete="
      deleteEvent();
      eventDetailDialog = false;
    "
    @close="
      eventDetailDialog = false;
      clearCurrentEvent();
    "
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
import { defineComponent, ref, reactive, toRefs, onMounted } from "vue";
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

export default defineComponent({
  props: {
    deviceName: {
      type: String,
      required: true,
    },
  },
  components: {
    FullCalendar,
  },
  setup(props) {
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
      titleFormat: {
        year: "numeric",
        month: "numeric",
        day: "numeric",
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
      clearCurrentEvent();
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
      currentEvent.start = selectInfo.start;
      currentEvent.end = selectInfo.end ? selectInfo.end : selectInfo.start;
      currentEvent.startStr = dateStrToReadable(selectInfo.startStr);
      currentEvent.endStr = dateStrToReadable(selectInfo.endStr);
      currentEvent.allDay = selectInfo.allDay;
      addEventDialog.value = true;
    }

    function handleEventClick(clickInfo: any): void {
      console.log("clickInfo", clickInfo);
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
