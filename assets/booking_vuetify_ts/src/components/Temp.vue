<template>
  <!-- <v-container>
      <v-row>
        <v-col cols="12" md="6">
          <v-menu
            v-model="menu"
            :close-on-content-click="false"
            transition="scale-transition"
            offset-y
            max-width="290px"
            min-width="290px"
          >
            <template v-slot:activator="{ props }">
              <v-text-field
                v-model="selectedDate"
                label="Select a date"
                prepend-icon="mdi-calendar"
                readonly
                v-bind="props"
              ></v-text-field>
            </template>
            <v-date-picker v-model="selectedDate" @accept="menu = false" @click="console.log(selectedDate instanceof Date)"></v-date-picker> -->
  <!-- </v-menu>
        </v-col>
      </v-row>
    </v-container> -->
  <v-text-field
    v-model="dateTime"
    :active="dialog"
    :focused="dialog"
    label="Picker in dialog"
    prepend-icon="mdi-clock-time-four-outline"
    readonly
  >
    <v-dialog v-model="dialog" activator="parent" width="auto">
      <v-date-picker v-if="dp" v-model="date" @update:model-value="dp=false;tp=true"></v-date-picker>
      <v-time-picker v-if="tp" v-model="time" @update:model-value="tp=false;dialog=false;"></v-time-picker>
    </v-dialog>
  </v-text-field>
</template>

<script lang="ts">
import { VTimePicker } from "vuetify/labs/VTimePicker";

export default {
  components: {
    VTimePicker,
  },
  data() {
    return {
      dialog: false,
      dp: false,
      tp: false,
      dateTime: new Date(),
      date: new Date(),
      time: '',
    };
  },
  watch: {
    dialog(val) {
      this.dp = val;
    },
    time(val) {
      this.addTimeToDateTime();
      console.log(typeof(val));
    },
  },
  methods:{
    addTimeToDateTime(){
      if(this.date && this.time){
      const [hours, minutes] = this.time.split(':').map(Number);
      this.date.setHours(hours);
      this.date.setMinutes(minutes);
      }
      this.dateTime = this.date;
    }
  }
};
</script>

<style scoped>
/* Add any custom styles here if necessary */
</style>
