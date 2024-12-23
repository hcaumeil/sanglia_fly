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
      this.eventSource = new EventSource(`http://localhost:8080/api/events`);

      this.eventSource.addEventListener("message", (event) => {
        const data = JSON.parse(event.data);
        const existingObject = this.planeData.find((obj) => obj.id === data.id);

        if (existingObject) {
          existingObject.lat = data.lat;
          existingObject.lng = data.long;
          existingObject.alt = this.normalizeAltitude(data.alt);
          existingObject.realAlt = data.alt
        } else {
          this.planeData.push({
            id: data.id,
            lat: data.lat,
            lng: data.long,
            alt: this.normalizeAltitude(data.alt),
            realAlt: data.alt
          });
        }

        this.planeData = [...this.planeData];
      });
    },
    normalizeAltitude(alt, altMin = 0, altMax = 20000) {
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

