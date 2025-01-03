<template>
  <div id="view">
    <div class="map">
      <GlobeAirplane3D
          :planeData="planeData"
          :selectedPlaneId="selectedPlaneId"
          v-if="dim === 3"
      />
      <Map
          :planeData="planeData"
          :selectedPlaneId="selectedPlaneId"
          v-if="dim === 2" />
      <div class="switch">
        <div class="switch-container">
          <span :class="{ active: dim === 2 }">2D</span>
          <v-switch
              inset
              hide-details
              v-model="is3D"
              @change="dim = is3D ? 3 : 2"
          ></v-switch>
          <span :class="{ active: dim === 3 }">3D</span>
        </div>
      </div>
    </div>
    <Form
        :planeData="planeData"
        :selectedPlaneId="selectedPlaneId"
        @update:selectedPlaneId="selectedPlaneId = $event"
    />
  </div>
</template>

<script>
import GlobeAirplane3D from "./Globe.vue";
import Form from "@/components/Form.vue";
import Map from "@/components/Map.vue";

export default {
  name: "ViewInterface",
  components: {
    Map,
    Form,
    GlobeAirplane3D,
  },
  data() {
    return {
      planeData: [],
      selectedPlaneId: null,
      eventSource: null,
      dim: 2,
    };
  },
  mounted() {
    this.startEventSource();
  },
  beforeDestroy() {
    if (this.eventSource) {
      this.eventSource.close();
    }
  },
  methods: {
    startEventSource() {
      let api_url = import.meta.env.VITE_API_URL
      if (api_url === undefined) {
        api_url = "http://localhost:8080"
      }
      this.eventSource = new EventSource(api_url+`/live/`);

      this.eventSource.addEventListener("message", (event) => {
        const data = JSON.parse(event.data);
        const existingObject = this.planeData.find((obj) => obj.id === data.origin);

        if (existingObject) {
          existingObject.lat = data.latitude;
          existingObject.lng = data.longitude;
          existingObject.alt = this.normalizeAltitude(data.altitude);
          existingObject.realAlt = data.altitude;
          existingObject.speed = data.speed;
          existingObject.type = data.type;
          existingObject.orientation = data.orientation;
        } else {
          this.planeData.push({
            id: data.origin,
            lat: data.latitude,
            lng: data.longitude,
            alt: this.normalizeAltitude(data.altitude),
            realAlt: data.altitude,
            speed: data.speed,
            type: data.type,
            orientation: data.orientation
          });
        }

        this.planeData = [...this.planeData];
      });
    },
    normalizeAltitude(alt, altMin = 0, altMax = 200000) {
      return Math.min(Math.max((alt - altMin) / (altMax - altMin), 0), 1);
    },
    onPlaneSelected(id) {
      this.selectedPlaneId = id;
    },
  },
  computed: {
    is3D: {
      get() {
        return this.dim === 3;
      },
      set(value) {
        this.dim = value ? 3 : 2;
      },
    },
  },

};
</script>

<style scoped>
#view {
  position: absolute;
  width: 100vw;
  display: flex;
  flex-direction: row;
  justify-content: space-between;
  color: white;
}
.map {
  width: 40%;
}
Form {
  width: 40%;
}

.switch {
  display: flex;
  flex-direction: row;
  align-content: center;
  justify-content: center;
  width: 1000px;
  margin-top: 20px;
}

.switch-container {
  display: flex;
  align-items: center;
  justify-content: space-around;
  background-color: #333;
  border-radius: 20px;
  padding: 10px 20px;
  width: 200px;
}

.switch-container span {
  font-size: 16px;
  font-weight: bold;
  color: white;
}

.switch-container span.active {
  color: #ffcc00;
}
</style>

