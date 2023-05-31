<template>
  <div class="w-full">
    <!-- 2.0 UI-->
    <!-- Top Row-->
    <div class="flex flex-row content-center justify-center mt-6">
      <!-- Logo-->
      <div class="basis-1/12 justify-center items-center" style="display: flex; justify-content: center">
        <div class="">
          <a role="button" tabindex="0" href="https://codebyedge.co.uk" class="a a-link">
            <img src="./logo.svg" alt="logo" srcset="" width="100" />
          </a>
        </div>
      </div>
      <!-- Talk to Us-->
      <div class="basis-6/12 flex items-center" style="display: flex; justify-content: center">
        <button class="bg-gray-100 hover:bg-gray-200 cbe-btn-text-green cbe-btn-text-font py-2 px-12 rounded-none h-3/4" @click="$parent.modalVisible = true">
          <div class="flex flex-row content-center justify-start gap-x-2">
            <div class="basis-1/4">
              <img class="cbe-btn-svg-fill" src="./chat.svg" alt="chat" srcset="" width="24" />
            </div>
            <div class="basis-3/4">
              <p>Talk to Us</p>
            </div>
          </div>
        </button>
      </div>
      <!-- Buy Now -->
      <div class="basis-5/12 flex pr-1" style="display: flex; justify-content: end">
        <!-- not full width container-->
        <div class="basis-3/12"></div>
        <div class="basis-9/12 flex justify-center">
          <button v-if="!$parent.working" :class="`${$parent.buyButtonDisabled ? 'bg-slate-500' : 'cbe-bg-green hover:bg-teal-700'} w-full py-8 px-4 rounded-lg justify-self-end text-2xl font-extrabold text-white`" :disabled="$parent.buyButtonDisabled" @click="$parent.addToCart">
            <div class="flex justify-between px-8" style="display: flex; justify-content: space-between">
              <p class="cbe-font-comorant">£{{ $parent.total() }}</p>
              <p class="cbe-font-comorant-garamond">Buy Now</p>
            </div>
          </button>
          <button v-if="$parent.working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6" disabled></button>
        </div>
      </div>
    </div>
    <div class="flex flex-row content-center justify-center">
      <!-- Logo Empty-->
      <div class="basis-1/12" style="display: flex; justify-content: center"></div>
      <!-- 3D Container-->
      <div class="basis-6/12" style="display: flex; justify-content: center">
        <!-- 3D Class-->
        <!-- Models-->
        <div class="cbe-canvas mt-12">
          <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer" :alpha="true">
            <Camera :position="{ z: 0 }" ref="camera" />
            <Scene ref="scene" background="white">
              <GltfModel v-for="(glb, index) in $parent.glbArray" :key="index" :src="`/static/src/glb/ring_mayfair_` + glb + `.glb`" @load="onReady" :position="{ x: index * 0, y: index * 0, z: index * 1.5 - 2 }" :rotation="{ x: 0, y: 0, z: 0 }" />
            </Scene>
            <EffectComposer>
              <RenderPass />
              <UnrealBloomPass :strength="0.18" />
            </EffectComposer>
          </Renderer>
        </div>
      </div>
      <!-- Options-->
      <div class="basis-5/12 flex pr-1 py-4" style="display: flex; justify-content: center">
        <div class="basis-3/12"></div>
        <!-- Options Column-->
        <div class="basis-9/12 flex flex-col">
          <!-- First Row-->
          <div class="flex flex-row" style="display: flex; justify-content: center">
            <!-- Message -->
            <div class="basis-4/12 pr-1">
              <button :class="`${$parent.optionActive == 'message' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-6 w-full rounded-none`" @click="$parent.rowUpdate('message')">
                <div class="flex flex-row content-center justify-center gap-x-2">
                  <div class="basis-3/4">
                    <p class="font-bold">Message</p>
                  </div>
                </div>
              </button>
            </div>
            <div class="basis-4/12 pr-1">
              <button :class="`${$parent.optionActive == 'metal' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-4 w-full rounded-none`" @click="$parent.rowUpdate('metal')">
                <div class="flex flex-row content-center justify-center gap-x-2">
                  <div class="basis-3/4 flex flex-col">
                    <p class="italic text-xs">Select</p>
                    <p class="font-bold">Metal</p>
                  </div>
                </div>
              </button>
            </div>
            <div class="basis-4/12">
              <button :class="`${$parent.optionActive == 'size' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-4 w-full rounded-none`" @click="$parent.rowUpdate('size')">
                <div class="flex flex-row content-center justify-center gap-x-2">
                  <div class="basis-3/4 flex flex-col">
                    <p class="italic text-xs">Select</p>
                    <p class="font-bold">Size</p>
                  </div>
                </div>
              </button>
            </div>
          </div>
          <!-- End First Row-->
          <!-- Second Row-->
          <div class="flex flex-row mt-4" style="display: flex; justify-content: center">
            <!-- Amanti (Simple) Input-->
            <div v-show="$parent.optionActive == 'message'" :class="`basis-11/12`">
              <div class="message__inputs">
                <div class="message__input-container">
                  <div class="morse-code" id="morseContainer"></div>
                  <div class="message__input cbe-font-mono" :contenteditable="$parent.editableAmanti" @input="updateMorse" id="messageInput" :onkeypress="$parent.amantiValidateInput" :style="{ 'font-size': $parent.fontSize + 'rem !important', 'letter-spacing': $parent.lineSpacing + 'rem' }"></div>
                  <div class="message__placeholder message__placeholder--visible cbe-font cbe-message-placeholder-fix mt-1">{{ $parent.placeholder }}</div>
                </div>
              </div>
              <div v-if="$parent.isRendering" class="col-span-3 align-middle grid grid-cols-3 content-center">
                <div></div>
                <div class="flex justify-center"><img class="text-center align-middle" src="./Infinity-1s-197px.gif" /></div>
                <div></div>
              </div>
              <div v-if="!$parent.isRendering" class="col-span-3 align-middle">
                <p class="text-center text-stone-500 cbe-font-label mt-1 text-sm">Zoom: Mouse Wheel, Rotate: Left Mouse Button, Pan: Right Mouse Button</p>
              </div>
              <div></div>
            </div>
            <!-- Select Metal-->
            <div v-show="$parent.optionActive == 'metal'" :class="`flex flex-col basis-12/12 w-full`" style="display: flex; justify-content: center">
              <div class="mb-1" v-for="option in $parent.obj.options" :key="option">
                <button :class="`${$parent.isActiveFinish(option.text) ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} py-6  rounded-none w-full py-8 px-10 rounded-lg justify-self-end`" :disabled="$parent.isActiveFinish(option.text)" @click="updateFinish(option.text)">
                  <div class="flex justify-between px-8" style="display: flex; justify-content: space-between">
                    <p class="cbe-btn-text-font text-sm font-medium">{{ option.text }}</p>
                    <p class="text-sm text-gray-500">{{ $parent.metalDiff(option.text) }}</p>
                  </div>
                </button>
              </div>
              <div class="cbe-font cbe-btn-text-green italic mt-4 mb-12">
                <p class="mb-4 font-semibold">Looking for another metal?</p>
                <p class="mb-4 font-semibold">Contact Us</p>
                <p class="mb-1 font-semibold">Call us on +44 20 3883 1388</p>
                <p class="mb-1 font-semibold">Monday to Friday - 10 AM - 5:30 PM</p>
                <p class="mb-1 font-semibold">Email</p>
                <a class="mb-1 font-semibold" href="mailto:hello@codebyedge.com">hello@codebyedge.com</a>
              </div>
              <div class="cbe-font italic cbe-btn-text-green py-2">
                <p class="leading-6 font-semibold">Our precious metals and gemstones are all sourced in accordance with the Responsible Jewellery Council Code of Conduct</p>
              </div>
            </div>
            <!-- Select Size-->
            <div v-show="$parent.optionActive == 'size'" :class="`flex flex-col basis-12/12 w-full`" style="display: flex; justify-content: center">
              <div class="flex flex-row mb-1" v-for="sizeRow in $parent.sizesObj()" :key="sizeRow" style="display: flex; justify-content: start">
                <div class="basis-4/12 pr-1" v-for="size in sizeRow" :key="size">
                  <button :class="`${$parent.isActiveSize(size) ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} bg-gray-100 cbe-btn-text-green cbe-bnt-text-font py-6 w-full rounded-none`" @click="$parent.activeSizeUpdate(size)">
                    {{ size }}
                  </button>
                </div>
              </div>
              <div class="cbe-font cbe-btn-text-green italic mt-4 mb-12">
                <p class="mb-4 font-semibold">Do you need help with sizing?</p>
                <p class="mb-4 font-semibold">Contact Us</p>
                <p class="mb-1 font-semibold">Call us on +44 20 3883 1388</p>
                <p class="mb-1 font-semibold">Monday to Friday - 10 AM - 5:30 PM</p>
                <p class="mb-1 font-semibold">Email</p>
                <a class="mb-1 font-semibold" href="mailto:hello@codebyedge.com">hello@codebyedge.com</a>
              </div>
            </div>
          </div>
          <!-- End Second Row-->
        </div>
        <!-- End Options Column-->
      </div>
    </div>
  </div>
</template>

<script>
import { sRGBEncoding, ACESFilmicToneMapping, CubeTextureLoader, EquirectangularReflectionMapping, MeshStandardMaterial, MeshPhysicalMaterial, SpotLight, TextureLoader } from "three";
import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";
export default {
  data() {
    return {
      metalName : "02 - Default",
    };
  },
  methods: {
    onReady(e) {
      let thisComponent = this;
      thisComponent.$refs.scene.scene.visible = false;
      thisComponent.$parent.isRendering = true;
      //console.log(thisComponent.$refs.scene.scene.visible);
      let children = e.scene.children[0].children;
      let goldName = thisComponent.metalName;
      let gemName = "03 - Default";
      const gold = new MeshPhysicalMaterial({
        color: thisComponent.$parent.activeFinish,
        metalness: 0.98,
        roughness: 0.0001,
        clearcoat: 1,
        clearcoatRoughness: 0.0001,
        name: goldName,
      });
      // Diamond
      const loader = new CubeTextureLoader();
      const texturePaths = ["/static/src/glb/obj/nx.png", "/static/src/glb/obj/ny.png", "/static/src/glb/obj/nz.png", "/static/src/glb/obj/px.png", "/static/src/glb/obj/py.png", "/static/src/glb/obj/pz.png"];
      const cubeTexturePromise = new Promise((resolve, reject) => {
        const cubeTexture = loader.load(texturePaths, resolve, undefined, reject);
      });
      const primaryTexturePromise = new Promise((resolve, reject) => {
        const primaryTexture = new TextureLoader().load("/static/src/glb/diamond/diamond_1.jpg", resolve, undefined, reject);
      });
      const secondaryTexturePromise = new Promise((resolve, reject) => {
        const secondaryTexture = new TextureLoader().load("/static/src/glb/diamond/diamond_2.png", resolve, undefined, reject);
      });
      const tertiaryTexturePromise = new Promise((resolve, reject) => {
        const tertiaryTexture = new TextureLoader().load("/static/src/glb/diamond/diamond_3.jpg", resolve, undefined, reject);
      });
      const tertiaryTextureInvertPromise = new Promise((resolve, reject) => {
        const tertiaryTextureInvert = new TextureLoader().load("/static/src/glb/diamond/diamond_3_i.jpg", resolve, undefined, reject);
      });
      const quadTexturePromise = new Promise((resolve, reject) => {
        const quadTexture = new TextureLoader().load("/static/src/glb/diamond/diamond_4.png", resolve, undefined, reject);
      });
      const tertiaryTextureRoundPromise = new Promise((resolve, reject) => {
        const tertiaryTextureRound = new TextureLoader().load("/static/src/glb/diamond/diamond_3.jpg", resolve, undefined, reject);
      });
      Promise.all([cubeTexturePromise, primaryTexturePromise, secondaryTexturePromise, tertiaryTexturePromise, tertiaryTextureInvertPromise, quadTexturePromise, tertiaryTextureRoundPromise])
        .then((textures) => {
          const [cubeTexture, primaryTexture, secondaryTexture, tertiaryTexture, tertiaryTextureInvert, quadTexture, tertiaryTextureRound] = textures;
          const gemRound = new MeshPhysicalMaterial({
            color: 0xffffff,
            map: tertiaryTextureRound,
            clearcoat: 0.64,
            clearcoatRoughness: 0,
            metalness: 0.64,
            //metalnessMap: quadTexture,
            roughness: 0,
            ior: 2.1,
            //transmission: 0.33,
            //transmissionMap: secondaryTexture,
            envMap: cubeTexture,
            envMapIntensity: 2,
            name: "gemRound",
          });
          let tx1Round = 0.64;
          let ty1Round = 0.64;
          let tx2Round = 0.2;
          let ty2Round = 0.2;
          let tx3Round = 0.1;
          let ty3Round = 0.1;
          gemRound.map.repeat.set(tx1Round, ty1Round);
          //gemRound.metalnessMap.repeat.set(tx2Round, ty2Round);
          //gemRound.transmissionMap.repeat.set(tx3Round, ty3Round);
          const gemFlat = new MeshPhysicalMaterial({
            color: 0xeeeeee,
            map: tertiaryTexture,
            clearcoat: 0.84,
            clearcoatRoughness: 0,
            metalness: 0.64,
            metalnessMap: tertiaryTextureInvert,
            roughness: 0,
            ior: 2.1,
            specularIntensity: 0.99,
            //specularColor: 0xffffff,
            specularColorMap: quadTexture,
            transmission: 0.33,
            //transmissionMap: tertiaryTextureInvert,
            thickness: 0.5,
            bumpMap: tertiaryTexture,
            bumpScale: 0.0001,
            envMap: cubeTexture,
            envMapIntensity: 2,
            name: "gemFlat",
          });
          let tx1Flat = 0.25;
          let ty1Flat = 0.25;
          let tx2Flat = 0.1;
          let ty2Flat = 0.1;
          gemFlat.map.repeat.set(tx1Flat, ty1Flat);
          gemFlat.metalnessMap.repeat.set(tx1Flat, ty1Flat);
          gemFlat.specularColorMap.repeat.set(tx2Flat, ty2Flat);
          //gemFlat.transmissionMap.repeat.set(tx4Flat, ty4Flat);
          gemFlat.bumpMap.repeat.set(tx1Flat, ty1Flat);
          // Assignment
          children.forEach((child) => {
            if (child.material) {
              if (child.material.name == thisComponent.metalName) {
                child.material = gold;
              }
              if (child.material.name == "03 - Default") {
                child.material = gemRound;
              }
              // diamond
              if (child.userData.name.includes("03 - Default")) {
                child.material = gemRound;
              }
              if (child.userData.name.includes("princess") || child.userData.name.includes("Princess")) {
                child.material = gemFlat;
              }
            }
          });
          thisComponent.$nextTick(() => {
            thisComponent.$refs.scene.scene.visible = true;
            thisComponent.$parent.isRendering = false;
          });
        })
        .catch((error) => {
          console.error("Error loading textures:", error);
        });
    },
    updateFinish(finish) {
      //let finish = e.target.value;
      let newPrices = this.$parent.obj.options.filter((option) => {
        return option.text == finish;
      });
      newPrices = newPrices[0].letters;
      this.$parent.prices = newPrices;
      this.$parent.activeFinish = this.$parent.finishes[finish];
      let thisComponent = this;
      let scene = this.$refs.scene.scene;
      scene.children.forEach((element) => {
        if (element.children.length != 0) {
          element.children.forEach((obj) => {
            obj.children.forEach((mesh) => {
              if (mesh.material != null) {
                if (mesh.material.name == thisComponent.metalName) {
                  mesh.material = new MeshStandardMaterial({
                    color: thisComponent.$parent.activeFinish,
                    metalness: 1,
                    roughness: 0.05,
                    name: thisComponent.metalName,
                  });
                  mesh.updateMatrix();
                }
              }
            });
          });
        }
      });
    },
    updateMorse(e) {
      this.$parent.editableAmanti = false;
      this.$parent.placeholder = null;
      let morseContainer = document.getElementById("morseContainer");
      morseContainer.innerHTML = null;
      this.$parent.message = document.getElementById("messageInput").innerHTML;
      if (this.$parent.message === "") {
        this.$parent.placeholder = "Please enter your message";
      } else {
        this.$parent.placeholder = null;
      }
      // morse function
      let messageArray = this.$parent.message.split("");
      this.$parent.messageArray = messageArray;
      let equiv = null;
      let insertion = null;
      let morseClass = null;
      let morseHeight = null;
      let thisComponent = this;
      thisComponent.$parent.glbArray = [];
      thisComponent.$forceUpdate();
      thisComponent.$nextTick(() => {
        messageArray.forEach((element) => {
          // find dict equiv
          thisComponent.$parent.glbArray.push(element.toUpperCase());
          equiv = this.$parent.morseDict[element.toLowerCase()];
          // if not null
          if (equiv) {
            let insertion = `<div class="morse-code__letter">`;
            equiv = equiv.split("");
            equiv.forEach((chara) => {
              if (chara == ".") {
                morseClass = "morse-code--dot";
                morseHeight = "6px";
              } else {
                morseClass = "morse-code--dash";
                morseHeight = "16px";
              }
              insertion += `<div class="${morseClass}" style="height: ${morseHeight}"></div>`;
            });
            insertion += `</div>`;
            morseContainer.innerHTML += insertion;
          }
        });
        thisComponent.$parent.editableAmanti = true;
        thisComponent.$nextTick(() => {
          // wait before you give it focus back
          setTimeout(function () {
            document.getElementById("messageInput").focus();
          }, 250);
        });
        //let cam = this.$refs.camera.camera;
        let orbitCtrl = this.$refs.renderer.three.cameraCtrl;
        window.orbitCtrl = orbitCtrl;
        // init cam pos
        let length = this.$parent.messageArray.length;
        let cx = -7.5;
        let cy = 5.125;
        let cz = 3.25;
        let tx = -0.85;
        let ty = -1;
        let tz = -0.5;
        // 0.5923475164113253 -0.3367853915585729 5.603194531924488
        // set both camera pos and target as per length of messge
        orbitCtrl.object.position.set(cx + (length - 1) * 0.45, cy + (length - 1) * 0.5, cz - (length - 1) * 0.5);
        orbitCtrl.target.set(tx + (length - 1) * 0.5, ty + (length - 1) * 0.1, tz + (length - 1) * 0.5);

        thisComponent.$nextTick(() => {
          // if desktop no change
          if (window.innerWidth <= 600) {
            // if mobile reduce font size and letter spacing to tally with dots
            thisComponent.$parent.fontSize = 2 - thisComponent.$parent.messageArray.length * 0.064;
            thisComponent.$parent.lineSpacing = 1.4 - thisComponent.$parent.messageArray.length * 0.075;
          } else {
            thisComponent.$parent.fontSize = 2;
            thisComponent.$parent.lineSpacing = 1.4;
          }
        });
        /*
          let length = this.messageArray.length;
          let x = 2;
          let y = length * 0.32;
          orbitCtrl.target.set(x, 0, 0);
          orbitCtrl.target0.set(x,0, 0);
          console.log(orbitCtrl)
          */
        //cam.lookAt(new THREE.Vector3(5, 1, 0));
      });
    },
  },
  mounted() {
    this.$nextTick(() => {
      //console.log(thisComponent.key);
      let thisComponent = this;
      let renderer = thisComponent.$refs.renderer.renderer;
      let scene = thisComponent.$refs.scene.scene;
      let camera = thisComponent.$refs.camera.camera;
      thisComponent.$refs.renderer.three.cameraCtrl.autoRotate = true;
      /*console.log(thisComponent.$refs.renderer.three.cameraCtrl.autoRotate);*/
      //console.log(scene);
      renderer.outputEncoding = sRGBEncoding;
      renderer.toneMapping = ACESFilmicToneMapping;
      renderer.toneMappingExposure = 0.82;
      //let envmap = new RGBELoader().setPath("/static/src/obj/").load("studio_small_08_1k.hdr", function (texture) {
      let envmap = new RGBELoader().setPath("/static/src/glb/").load("brown_photostudio_02_1k_b.hdr", function (texture) {
        texture.mapping = EquirectangularReflectionMapping;
        scene.environment = texture;
        //scene.background = texture;
      });
      const spotLight = new SpotLight(0xffffff);
      spotLight.position.set(10, 10, 20);
      spotLight.castShadow = true;
      spotLight.shadow.mapSize.width = 1024;
      spotLight.shadow.mapSize.height = 1024;
      spotLight.shadow.camera.near = 500;
      spotLight.shadow.camera.far = 4000;
      spotLight.shadow.camera.fov = 30;
      scene.add(spotLight);
    });
  },
};
</script>

<style></style>
