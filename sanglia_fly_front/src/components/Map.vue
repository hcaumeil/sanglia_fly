<template>
  <div style="width: 100%">
    <div id="map" style="height: 800px; width: 1000px;"></div>
  </div>
</template>

<script>
import L from "leaflet";
import planeUrl from "@public/plane.png";

export default {
  name: "Map",
  props: {
    planeData: {
      type: Array,
      default: () => [],
    },
    selectedPlaneId: {
      type: String,
      default: null,
    },
  },
  watch: {
    planeData: {
      handler(newData) {
        this.updateMarkers(newData);
        if (this.selectedPlaneId && this.isCameraLocked) {
          this.followSelectedPlane();
        }
      },
      deep: true,
    },
    selectedPlaneId(newId) {
      if (this.isCameraLocked) {
        this.centerOnSelectedPlane(newId);
      }
    },
  },
  data() {
    return {
      map: null,
      markers: {},
      isCameraLocked: true,
    };
  },
  mounted() {
    this.initMap();
  },
  methods: {
    initMap() {
      this.map = L.map("map").setView([48.8566, 2.3522], 3);

      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(this.map);

      this.updateMarkers(this.planeData);

      this.map.on("movestart", () => {
        this.isCameraLocked = false;
      });

      this.map.on("moveend", () => {
        setTimeout(() => {
          this.isCameraLocked = true;
        }, 5000);
      });
    },

    updateMarkers(planeData) {
      Object.values(this.markers).forEach((marker) => this.map.removeLayer(marker));
      this.markers = {};

      planeData.forEach((plane) => {
        const icon = this.createPlaneIcon( plane.orientation -44|| -44);
        const marker = L.marker([plane.lat, plane.lng], {
          title: plane.id,
          icon,
        }).addTo(this.map);

        marker.bindPopup(`${plane.id}`);
        this.markers[plane.id] = marker;
      });
    },

    createPlaneIcon(rotation) {
      const planeIcon = L.divIcon({
        html: `
          <div style="transform: rotate(${rotation}deg);">
            <img src="`+planeUrl+`" alt="plane" style="width: 40px; height: 40px;">
          </div>
        `,
        className: "plane-icon",
        iconSize: [40, 40],
        iconAnchor: [20, 20],
      });
      return planeIcon;
    },

    centerOnSelectedPlane(planeId) {
      const selectedPlane = this.planeData.find((plane) => plane.id === planeId);
      if (selectedPlane) {
        this.map.setView([selectedPlane.lat, selectedPlane.lng], 4);
        const marker = this.markers[planeId];
        if (marker) {
          marker.openPopup();
        }
      }
    },

    followSelectedPlane() {
      const selectedPlane = this.planeData.find(
          (plane) => plane.id === this.selectedPlaneId
      );
      if (selectedPlane) {
        this.map.setView([selectedPlane.lat, selectedPlane.lng]);
      }
    },
  },
};
</script>

<style>
#map {
  border: 1px solid #ddd;
  border-radius: 8px;
  width: 100%;
}

.plane-icon img {
  transition: transform 0.2s linear;
}
</style>



