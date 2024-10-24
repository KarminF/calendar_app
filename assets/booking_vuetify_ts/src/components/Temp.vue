<template>
    <v-container>
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
            <v-date-picker v-model="selectedDate" @accept="menu = false" @click="console.log(selectedDate instanceof Date)"></v-date-picker>
          </v-menu>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  export default {
    data() {
      return {
        menu: false,
        selectedDate: null,
      }
    },
  }
  </script>
  
  <style scoped>
  /* Add any custom styles here if necessary */
  </style>
  