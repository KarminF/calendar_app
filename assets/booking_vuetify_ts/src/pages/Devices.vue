<template>
  <NavBar />
  <DeviceList :devices="devices" />
</template>

<script lang="ts" setup>
import { ref } from 'vue';
interface Device {
  name: string;
  deviceinstance_id: string;
}
const devices = ref<Device[]>([]);

fetch('http://127.0.0.1:8000/api/devices/')
      .then(response => response.json())
      .then(data => {
        devices.value = data;
      })
      .catch(error => {
        console.error('Error:', error);
      });

</script>
