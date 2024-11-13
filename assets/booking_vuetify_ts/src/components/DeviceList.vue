<template>
  <h1>Devices</h1>
  <v-row class="cards">
    <v-col
      cols="12"
      md="4"
      v-for="device in devices"
      :key="device.deviceinstance_id"
    >
      <v-card
        :title="device.name"
        :to="{
          path: '/calendar',
          query: {
            deviceName: device.name,
            deviceId: device.deviceinstance_id,
          },
        }"
      ></v-card>
    </v-col>
  </v-row>
</template>

<script lang="ts" setup>
interface Device {
  name: string;
  deviceinstance_id: string;
}
const props = defineProps<{
  devices: Array<Device>;
}>();

// console.log(props.devices);
</script>
