<template>
  <div style="color: white; height: 1vh; margin: 2em">
    <v-card
        class="mx-auto"
        width="700"
        color="primary"
    >
      <div class="content-container">
        <div class="text-container">
          <v-card-title>
            <div class="title">
              <span class="font-weight-black">Sanglia fly</span>
            </div>
          </v-card-title>
          <v-card-subtitle>
            <div class="subtitle">
              <span class="font-weight-black">Welcome</span>
            </div>
          </v-card-subtitle>

          <v-card-text>
            Explorez les vols d'avions en temps réel grâce à notre outil interactif.<br>
            Que vous préfériez une vue immersive en 3D ou une carte détaillée en 2D, suivez facilement le trajet des avions dans le monde entier.
            Visualisez leurs trajectoires, altitudes et positions actualisées en direct.<br> <br>
            Avec une interface intuitive, sélectionnez un avion pour le suivre de près et plongez dans l'expérience du suivi aérien comme jamais auparavant.

            Préparez-vous à prendre votre envol avec Sanglia Fly !
          </v-card-text>
        </div>

        <div class="image-container">
          <v-img
              src="/public/logo.png"
              height="100%"
              class="logo-image"
          />
        </div>
      </div>
      <v-card-actions>
        <v-btn
            color="orange-lighten-2"
            text="SUIVRE UN AVION"
            @click="show = !show"
        ></v-btn>
        <v-spacer></v-spacer>
      </v-card-actions>

      <v-expand-transition v-if="show">
        <div>
          <v-divider></v-divider>
          <v-autocomplete
              label="Sélectionne l'avion que tu veux suivre"
              :items="planeData.flatMap((plane) => plane.id).concat(['aucun'])"
              v-model="localSelectedPlaneId"
          ></v-autocomplete>
          <table v-if="selectedPlaneId != null && selectedPlaneId !== 'aucun'">
            <caption>
              <h2>Informations du vol en temps réel</h2>
            </caption>
            <thead>
            <tr>
              <th scope="col">Coordonnées</th>
            </tr>
            </thead>
            <tbody>
              <tr>
                <td>
                  <div style="display: flex; flex-direction: row; justify-content: space-evenly">
                    <span>Latitude: {{ parseFloat(planeData.filter((elem) => elem.id === selectedPlaneId)[0].lat.toFixed(2)) }}° </span>
                    <span>Longitude: {{ parseFloat(planeData.filter((elem) => elem.id === selectedPlaneId)[0].lng.toFixed(2)) }}° </span>
                    <span>Altitude: {{ parseFloat(planeData.filter((elem) => elem.id === selectedPlaneId)[0].realAlt.toFixed(2)) }}m </span>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
          <table v-if="selectedPlaneId != null && selectedPlaneId !== 'aucun'">
            <thead>
            <tr>
              <th scope="col">Vitesse</th>
              <th scope="col">Type</th>
            </tr>
            </thead>
            <tbody>
            <tr>
              <td width="50%">{{planeData.filter((elem) => elem.id === selectedPlaneId)[0].speed}}km/h</td>
              <td>{{planeData.filter((elem) => elem.id === selectedPlaneId)[0].type}}</td>
            </tr>
            </tbody>
          </table>
        </div>
      </v-expand-transition>
    </v-card>
  </div>
</template>


<script>
export default {
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
  data() {
    return {
      localSelectedPlaneId: this.selectedPlaneId,
      show: false,
    };
  },
  watch: {
    selectedPlaneId(newId) {
      this.localSelectedPlaneId = newId;
    },
    localSelectedPlaneId(newId) {
      this.$emit("update:selectedPlaneId", newId);
    },
  },
};
</script>

<style scoped>
.content-container {
  display: flex;
  flex-direction: row;
}

.text-container {
  width: 70%;
  padding-right: 20px;
}

.logo-image {
  width: 300px;
  height: auto;
  margin-left: -50px;
  margin-top: -50px;
}

.title {
  font-size: xxx-large;
}

.subtitle {
  font-size: xx-large;
}

table {
  width: 80%;
  margin: 1em auto;
}

th {
  padding-top: 1em;
  font-weight: bold;
}

tr {
  text-align: center;
}
</style>

