<template>
  <div id="globe">
    <div id="chart"></div>
    <div id="time-log">{{ currentTime }}</div>
    <div id="zoom-controls">
      <button @click="zoomIn">+</button>
      <button @click="zoomOut">-</button>
    </div>
  </div>
</template>

<script>
import * as THREE from "three";
import Globe from "globe.gl";

export default {
  name: "GlobeAirplane3D",
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
    selectedPlaneId(newId) {
      this.recenterOnSelectedPlane(newId);
    },
    planeData: {
      handler(newData) {
        if (this.world) {
          newData = newData.map((elem) => {
            elem.direction = 90;
            return elem;
          });
          console.log(newData)
          this.world.objectsData(newData);

          if (this.isCameraLocked && this.selectedPlaneId) {
            this.recenterOnSelectedPlane(this.selectedPlaneId);
          }
        }
      },
      deep: true,
    },
  },
  data() {
    return {
      EARTH_RADIUS_KM: 6371,
      SAT_SIZE: 100,
      TIME_STEP: 3 * 1000,
      currentTime: new Date().toString(),
      world: null,
      isCameraLocked: true,
      currentAltitude: 1.5,
    };
  },
  mounted() {
    this.initGlobe();
  },
  methods: {
    async initGlobe() {
      this.world = Globe()(this.$el.querySelector("#chart"))
          .globeImageUrl("//unpkg.com/three-globe/example/img/earth-blue-marble.jpg")
          .objectLat("lat")
          .objectLng("lng")
          .objectAltitude("alt")
          .objectFacesSurface(false)
          .objectLabel("id")
          .width(1000)
          .height(800);

      setTimeout(() => this.world.pointOfView({ altitude: this.currentAltitude }));

      const createPlaneIcon = (lat, lng, direction) => {

        const globeRadius = this.world.getGlobeRadius();
        const scaleFactor = (this.SAT_SIZE * globeRadius) / this.EARTH_RADIUS_KM;

        const bodyGeometry = new THREE.CylinderGeometry(
            0.3 * scaleFactor,
            0.3 * scaleFactor,
            2 * scaleFactor,
            8
        );
        const bodyMaterial = new THREE.MeshLambertMaterial({
          color: "red",
          transparent: false,
        });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.rotation.x = Math.PI / 2;

        const wingShape = new THREE.Shape();
        wingShape.moveTo(-1.5 * scaleFactor, 0);
        wingShape.lineTo(1.5 * scaleFactor, 0);
        wingShape.lineTo(0.8 * scaleFactor, 0.5 * scaleFactor);
        wingShape.lineTo(-0.8 * scaleFactor, 0.5 * scaleFactor);
        wingShape.lineTo(-1.5 * scaleFactor, 0);
        const wingGeometry = new THREE.ShapeGeometry(wingShape);
        const wingMaterial = new THREE.MeshLambertMaterial({
          color: "red",
          side: THREE.DoubleSide,
        });
        const wings = new THREE.Mesh(wingGeometry, wingMaterial);
        wings.rotation.x = Math.PI / 2;
        wings.position.set(0, 0, 0.5 * scaleFactor);

        const aileronShape = new THREE.Shape();
        aileronShape.moveTo(-0.6 * scaleFactor, 0);
        aileronShape.lineTo(0.6 * scaleFactor, 0);
        aileronShape.lineTo(0.4 * scaleFactor, 0.2 * scaleFactor);
        aileronShape.lineTo(-0.4 * scaleFactor, 0.2 * scaleFactor);
        aileronShape.lineTo(-0.6 * scaleFactor, 0);
        const aileronGeometry = new THREE.ShapeGeometry(aileronShape);
        const aileron = new THREE.Mesh(aileronGeometry, wingMaterial);
        aileron.rotation.x = Math.PI / 2;
        aileron.position.set(0, 0, -0.8 * scaleFactor);

        const noseGeometry = new THREE.ConeGeometry(
            0.3 * scaleFactor,
            0.7 * scaleFactor,
            8
        );
        const noseMaterial = new THREE.MeshLambertMaterial({
          color: "red",
        });
        const nose = new THREE.Mesh(noseGeometry, noseMaterial);
        nose.rotation.x = Math.PI / 2;
        nose.position.set(0, 0, 1.35 * scaleFactor);

        const tailShape = new THREE.Shape();
        tailShape.moveTo(0, 0);
        tailShape.lineTo(0.5 * scaleFactor, 1 * scaleFactor);
        tailShape.lineTo(-0.5 * scaleFactor, 0);
        tailShape.lineTo(0, 0);
        const tailGeometry = new THREE.ShapeGeometry(tailShape);
        const tailMaterial = new THREE.MeshLambertMaterial({
          color: "red",
          side: THREE.DoubleSide,
        });
        const tail = new THREE.Mesh(tailGeometry, tailMaterial);
        tail.rotation.y = Math.PI / 2;
        tail.position.set(0, 0, -0.8 * scaleFactor);

        const planeGroup = new THREE.Group();
        planeGroup.add(body);
        planeGroup.add(wings);
        planeGroup.add(aileron);
        planeGroup.add(nose);
        planeGroup.add(tail);

        const position = new THREE.Vector3().setFromSphericalCoords(
            globeRadius,
            THREE.MathUtils.degToRad(90 - lat),
            THREE.MathUtils.degToRad(lng)
        );

        const up = new THREE.Vector3().copy(position).normalize();

        const quaternion = new THREE.Quaternion().setFromUnitVectors(
            new THREE.Vector3(0, 1, 0),
            up
        );

        planeGroup.quaternion.copy(quaternion);

        const directionRad = THREE.MathUtils.degToRad(direction);

        const rotationQuaternion = new THREE.Quaternion().setFromAxisAngle(
            new THREE.Vector3(0, 1, 0), // Rotation autour de l'axe Y
            directionRad
        );

        planeGroup.quaternion.multiply(rotationQuaternion);

        return planeGroup;
      };



      this.world.objectThreeObject(({ lat, lng, direction }) =>
          createPlaneIcon(lat, lng, direction)
      );

      this.world.objectsData(this.planeData);

      this.world.controls().addEventListener("start", () => {
        this.isCameraLocked = false;
      });

      this.world.controls().addEventListener("end", () => {
        setTimeout(() => {
          this.isCameraLocked = true;
        }, 5000);
      });
    },
    recenterOnSelectedPlane(planeId) {
      const plane = this.planeData.find((p) => p.id === planeId);
      if (plane && this.world) {
        this.world.pointOfView(
            { lat: plane.lat, lng: plane.lng, altitude: this.currentAltitude },
            30
        );
      }
    },
    zoomIn() {
      this.currentAltitude = Math.max(0.1, this.currentAltitude - 0.1);
      this.world.pointOfView({ altitude: this.currentAltitude });
    },
    zoomOut() {
      this.currentAltitude += 0.1;
      this.world.pointOfView({ altitude: this.currentAltitude });
    },
  },
};
</script>


<style>
body {
  margin: 0;
}

#globe {
  position: relative;
  width: 1000px;
}

#chart {
  z-index: 0;
}

#time-log {
  position: absolute;
  z-index: 1;
  top: 1px;
  font-size: medium;
  font-family: sans-serif;
  padding: 0.5em;
  border-radius: 3px;
  color: lavender;
}

#zoom-controls {
  position: absolute;
  bottom: 10px;
  right: 10px;
  display: flex;
  flex-direction: column;
  gap: 5px;
}

#zoom-controls button {
  background-color: #555;
  color: white;
  border: none;
  border-radius: 3px;
  padding: 8px 10px;
  cursor: pointer;
  font-size: 18px;
  font-weight: bold;
}

#zoom-controls button:hover {
  background-color: #777;
}
</style>

