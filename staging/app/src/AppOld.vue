<template>
    <div class="w-full">
      <div class="w-full" v-if="desktop">
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
            <button class="bg-gray-100 hover:bg-gray-200 cbe-btn-text-green cbe-btn-text-font py-2 px-12 rounded-none h-3/4" @click="modalVisible = true">
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
              <button v-if="!working" :class="`${buyButtonDisabled ? 'bg-slate-500' : 'cbe-bg-green hover:bg-teal-700'} w-full py-8 px-4 rounded-lg justify-self-end text-2xl font-extrabold text-white`" :disabled="buyButtonDisabled" @click="addToCart">
                <div class="flex justify-between px-8" style="display: flex; justify-content: space-between">
                  <p class="cbe-font-comorant">£{{ total() }}</p>
                  <p class="cbe-font-comorant-garamond">Buy Now</p>
                </div>
              </button>
              <button v-if="working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6" disabled></button>
            </div>
          </div>
        </div>
        <!-- End Top Row-->
        <!-- 2.0 UI End-->
        <!-- 2ndary Row-->
        <div class="flex flex-row content-center justify-center">
          <!-- Logo Empty-->
          <div class="basis-1/12" style="display: flex; justify-content: center"></div>
          <!-- 3D Container-->
          <div class="basis-6/12" style="display: flex; justify-content: center">
            <!-- 3D Amanti (Simple) Class-->
            <!-- Amanti Rings-->
            <div v-if="key == 'amanti'">
              <div class="cbe-canvas mt-12">
                <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer" :alpha="true">
                  <Camera :position="{ z: 0 }" ref="camera" />
                  <Scene ref="scene" background="white">
                    <GltfModel v-for="(glb, index) in glbArray" :key="index" :src="`/static/src/glb/ring_` + glb + `.glb`" @load="onReady" :position="{ x: index * 0, y: index * 0, z: index * 1.5 - 2 }" :rotation="{ x: 0, y: 0, z: 0 }" />
                  </Scene>
                  <EffectComposer>
                    <RenderPass />
                    <UnrealBloomPass :strength="0.18" />
                  </EffectComposer>
                </Renderer>
              </div>
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
                  <button :class="`${optionActive == 'message' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-6 w-full rounded-none`" @click="rowUpdate('message')">
                    <div class="flex flex-row content-center justify-center gap-x-2">
                      <div class="basis-3/4">
                        <p class="font-bold">Message</p>
                      </div>
                    </div>
                  </button>
                </div>
                <div class="basis-4/12 pr-1">
                  <button :class="`${optionActive == 'metal' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-4 w-full rounded-none`" @click="rowUpdate('metal')">
                    <div class="flex flex-row content-center justify-center gap-x-2">
                      <div class="basis-3/4 flex flex-col">
                        <p class="italic text-xs">Select</p>
                        <p class="font-bold">Metal</p>
                      </div>
                    </div>
                  </button>
                </div>
                <div class="basis-4/12">
                  <button :class="`${optionActive == 'size' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-4 w-full rounded-none`" @click="rowUpdate('size')">
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
                <div v-show="optionActive == 'message'" :class="`basis-11/12`" v-if="classes.amanti.includes(key) && key != 'aquafiore-bracelet' && key != 'aquafiore-pendant'">
                  <div class="message__inputs">
                    <div class="message__input-container">
                      <div class="morse-code" id="morseContainer"></div>
                      <div class="message__input cbe-font-mono" :contenteditable="editableAmanti" @input="amantiUpdateMorse" id="messageInput" :onkeypress="amantiValidateInput" :style="{ 'font-size': fontSize + 'rem !important', 'letter-spacing': lineSpacing + 'rem' }"></div>
                      <div class="message__placeholder message__placeholder--visible cbe-font cbe-message-placeholder-fix mt-1">{{ placeholder }}</div>
                    </div>
                  </div>
                  <div v-if="isRendering" class="col-span-3 align-middle grid grid-cols-3 content-center">
                    <div></div>
                    <div class="flex justify-center"><img class="text-center align-middle" src="./Infinity-1s-197px.gif" /></div>
                    <div></div>
                  </div>
                  <div v-if="!isRendering" class="col-span-3 align-middle">
                    <p class="text-center text-stone-500 cbe-font-label mt-1 text-sm">Zoom: Mouse Wheel, Rotate: Left Mouse Button, Pan: Right Mouse Button</p>
                  </div>
                  <div></div>
                </div>
                <!-- Select Metal-->
                <div v-show="optionActive == 'metal'" v-if="key == 'amanti'" :class="`flex flex-col basis-12/12 w-full`" style="display: flex; justify-content: center">
                  <div class="mb-1" v-for="option in obj.options" :key="option">
                    <button :class="`${isActiveFinish(option.text) ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} py-6  rounded-none w-full py-8 px-10 rounded-lg justify-self-end`" :disabled="isActiveFinish(option.text)" @click="amantiUpdateFinish(option.text)">
                      <div class="flex justify-between px-8" style="display: flex; justify-content: space-between">
                        <p class="cbe-btn-text-font text-sm font-medium">{{ option.text }}</p>
                        <p class="text-sm text-gray-500">{{ metalDiff(option.text) }}</p>
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
                <div v-show="optionActive == 'size'" v-if="key == 'amanti'" :class="`flex flex-col basis-12/12 w-full`" style="display: flex; justify-content: center">
                  <div class="flex flex-row mb-1" v-for="sizeRow in sizesObj()" :key="sizeRow" style="display: flex; justify-content: start">
                    <div class="basis-4/12 pr-1" v-for="size in sizeRow" :key="size">
                      <button :class="`${isActiveSize(size) ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} bg-gray-100 hover:bg-gray-200 cbe-btn-text-green cbe-bnt-text-font py-6 w-full rounded-none`" @click="activeSizeUpdate(size)">
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
        <div v-if="classes.amanti.includes(key) && key != 'aquafiore-bracelet' && key != 'aquafiore-pendant'" class="grid grid-cols-5"></div>
        <!-- End Amanti Input -->
        <!-- Aquafiore Bracelet Input-->
        <div v-if="key == 'aquafiore-bracelet'" class="grid grid-cols-5 mt-1">
          <div></div>
          <div class="message__inputs col-span-3">
            <div class="message__input-container">
              <div class="morse-code" id="morseContainer"></div>
              <div class="message__input cbe-font-mono cbe-font-black cbe-spacing" contenteditable="true" @input="aquaBraceletUpdateMorse" id="messageInput" :onkeypress="amantiValidateInput"></div>
              <div class="message__placeholder message__placeholder--visible cbe-font">{{ placeholder }}</div>
            </div>
          </div>
          <div></div>
        </div>
        <div v-if="key == 'aquafiore-bracelet'" class="grid grid-cols-5">
          <div></div>
          <div class="col-span-3 align-middle">
            <p class="text-center text-stone-500 cbe-font-label">The character limit for the {{ key }} class is {{ obj.limit }} characters</p>
          </div>
          <div></div>
        </div>
        <!-- End Aquafiore Bracelet Input -->
        <!-- Aquafiore Pendant Input-->
        <div v-if="key == 'aquafiore-pendant'" class="grid grid-cols-5 mt-1">
          <div></div>
          <div class="message__inputs col-span-3">
            <div class="message__input-container">
              <div class="morse-code" id="morseContainer"></div>
              <div class="message__input cbe-font-mono cbe-font-black cbe-spacing" contenteditable="true" @input="aquaPendantUpdateMorse" id="messageInput" :onkeypress="amantiValidateInput"></div>
              <div class="message__placeholder message__placeholder--visible cbe-font">{{ placeholder }}</div>
            </div>
          </div>
          <div></div>
        </div>
        <div v-if="key == 'aquafiore-pendant'" class="grid grid-cols-5">
          <div></div>
          <div class="col-span-3 align-middle">
            <p class="text-center text-stone-500 cbe-font-label">The character limit for the {{ key }} class is {{ obj.limit }} characters</p>
          </div>
          <div></div>
        </div>
        <!-- End Aquafiore Pendant Input -->
        <!-- Earrings Input-->
        <div v-if="classes.earring.includes(key)" class="grid grid-cols-9 mt-1">
          <div></div>
          <div class="message__inputs col-span-3 sm:col-span-3">
            <div class="message__input-container">
              <div class="morse-code" id="morseContainerLeft"></div>
              <div class="message__input cbe-font-mono cbe-font-black cbe-spacing" contenteditable="true" @input="earringsUpdateMorse" id="messageInputLeft" :onkeypress="earringsValidateInputLeft"></div>
              <div class="message__placeholder message__placeholder--visible cbe-font">{{ placeholderLeft }}</div>
            </div>
          </div>
          <div></div>
          <div class="message__inputs col-span-3">
            <div class="message__input-container">
              <div class="morse-code" id="morseContainerRight"></div>
              <div class="message__input cbe-font-mono cbe-font-black cbe-spacing" contenteditable="true" @input="earringsUpdateMorse" id="messageInputRight" :onkeypress="earringsValidateInputRight"></div>
              <div class="message__placeholder message__placeholder--visible cbe-font">{{ placeholderRight }}</div>
            </div>
          </div>
          <div></div>
        </div>
        <div v-if="classes.earring.includes(key)" class="grid grid-cols-5 mt-3">
          <div></div>
          <div class="col-span-3 align-middle">
            <p class="text-center text-stone-500 cbe-font-label">The character limit for the {{ key }} class is {{ obj.limit }} characters</p>
          </div>
          <div></div>
        </div>
        <!-- End Earrings Input-->
        <!-- Necklace Input-->
        <div v-if="classes.necklace.includes(key)" class="grid grid-cols-5 mt-1">
          <div></div>
          <div class="message__inputs col-span-3">
            <div class="message__input-container">
              <div class="morse-code" id="morseContainer"></div>
              <div class="message__input cbe-font-mono cbe-font-black cbe-spacing" contenteditable="true" @input="necklaceUpdateMorse" id="messageInput" :onkeypress="necklaceValidateInput"></div>
              <div class="message__placeholder message__placeholder--visible cbe-font">{{ placeholder }}</div>
            </div>
          </div>
          <div></div>
        </div>
        <div v-if="classes.necklace.includes(key)" class="grid grid-cols-5">
          <div></div>
          <div class="col-span-3 align-middle">
            <!--<p class="text-center text-stone-500 cbe-font-label">The character limit for the {{ key }} class is {{ obj.limit }} characters</p>-->
            <p class="text-center text-stone-500 cbe-font-label">The stones limit for the {{ key }} class is 15 stones</p>
            <p v-if="debug" class="text-center text-red cbe-font-label">{{ debug }}</p>
          </div>
          <div></div>
        </div>
        <!-- End Necklace Input -->
        <!--######################################### END INPUT ##################################################################-->
        <!--##################################################################3D#####################################################################################-->
        <!-- Mayfair Rings-->
        <div v-if="key == 'mayfair'" class="flex justify-center">
          <div></div>
          <div class="cbe-canvas">
            <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer">
              <Camera :position="{ z: 0 }" ref="camera" />
              <Scene ref="scene" background="white">
                <GltfModel v-for="(glb, index) in glbArray" :key="index" :src="`/static/src/glb/ring_mayfair_` + glb + `.glb`" @load="onReady" :position="{ x: index * 0, y: index * 0, z: index * 0.65 - 4 }" :rotation="{ x: 0, y: 0, z: 0 }" />
              </Scene>
              <EffectComposer>
                <RenderPass />
                <UnrealBloomPass :strength="0.18" />
              </EffectComposer>
            </Renderer>
          </div>
          <div></div>
        </div>
        <!-- Aquafiore Bracelets-->
        <div v-if="key == 'aquafiore-bracelet'" class="flex justify-center">
          <div></div>
          <div class="cbe-canvas">
            <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer">
              <Camera :position="{ z: 10 }" ref="camera" />
              <Scene ref="scene" background="white">
                <!--
              <Box ref="box" :rotation="{ y: Math.PI / 4, z: Math.PI / 4 }">
                <LambertMaterial />
              </Box>
            -->
                <!-- Big chain-->
                <GltfModel v-if="glbArray.length != 0" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx, y: 0, z: 0 }" :rotation="{ x: 0, y: 0, z: 0 }" />
                <!-- 9 smaller chains -->
                <GltfModel v-if="glbArray.length != 0" v-for="i in 9" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + 0.015 + i * 0.055, y: 0, z: 0 }" :rotation="smallChainRotationFirstNine(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
                <!-- Big chain-->
                <GltfModel v-if="glbArray.length != 0" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + 0.582, y: 0, z: 0 }" :rotation="{ x: 0, y: 0, z: 0 }" />
                <!-- 31 smaller chains -->
                <GltfModel v-if="glbArray.length != 0" v-for="i in 30" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + 0.6 + i * 0.055, y: 0, z: 0 }" :rotation="smallChainRotationFirstNine(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
                <!-- First Hex-->
                <GltfModel v-if="glbArray.length != 0" :src="`/static/src/glb/aquafiore_bracelet/export/hex_b.glb`" @load="aquaBraceletHexOnReady" :position="{ x: braceletx + 2.665, y: 0, z: 0 }" :rotation="{ x: 0, y: 0, z: 0 }" :scale="{ x: 0.45, y: 0.45, z: 0.45 }" />
                <!-- Prefix 7 smaller chains -->
                <GltfModel v-if="glbArray.length != 0" v-for="i in 7" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + 3.02 + i * 0.055, y: 0, z: 0 }" :rotation="smallChainRotationSeven(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
                <!-- Middle Component -->
                <GltfModel v-if="glbArray.length != 0" v-for="(comp, index) in braceletArray" :key="index" :src="comp.src" @load="aquaBraceletMiddleOnReady" :position="comp.position" :rotation="comp.rotation" :scale="comp.scale" />
                <!-- Suffix 7 smaller chains -->
                <GltfModel v-if="glbArray.length != 0" v-for="i in 7" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + braceletMiddleEnd - 0.28 + i * 0.055, y: 0, z: 0 }" :rotation="smallChainRotationSeven(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
                <!-- Last Hex-->
                <GltfModel v-if="glbArray.length != 0" :src="`/static/src/glb/aquafiore_bracelet/export/hex_b.glb`" @load="aquaBraceletHexOnReady" :position="{ x: braceletx + braceletMiddleEnd + 0.52, y: 0, z: 0 }" :rotation="{ x: 0, y: 0, z: 0 }" :scale="{ x: 0.45, y: 0.45, z: 0.45 }" />
                <!-- Last 60 smaller chains -->
                <GltfModel v-if="glbArray.length != 0" v-for="i in 61" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + braceletMiddleEnd + 0.87 + i * 0.055, y: 0, z: 0 }" :rotation="smallChainRotationSeven(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
                <!-- Clasp -->
                <GltfModel v-if="glbArray.length != 0" :src="`/static/src/glb/aquafiore_bracelet/export/clasp_b.glb`" @load="aquaBraceletClaspOnReady" :position="{ x: braceletx + braceletMiddleEnd + 4.47, y: 0, z: -0.028 }" :rotation="{ x: 0, y: 0, z: 0 }" :scale="{ x: 0.28, y: 0.28, z: 0.28 }" />
                <!-- End Middle Component-->
                <!-- Morse Groups (jewel/chain pairs) -->
                <!--
              <Group v-if="glbArray.length != 0" v-for="(signal, index) in braceletMorseArray" :key="index">
                 A jewel for each index
                <GltfModel v-if="glbArray.length != 0" :src="`/static/src/glb/aquafiore_bracelet/export/${signal}_b.glb`" @load="aquaBraceletJewelOnReady" :position="{ x: braceletx + braceletJewelsOffset + index * braceletJewelsOffset * 0.25, y: 0, z: 0 }" :rotation="{ x: 0, y: 0, z: 0 }" :scale="{ x: 0.45, y: 0.45, z: 0.45 }" />
                 A 5 chain if not first or last jewel
                <GltfModel v-if="glbArray.length != 0" v-for="i in 5" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + braceletJewelsOffset + braceletChainOffset(signal) + index * braceletJewelsOffset * 0.2765 + i * 0.055, y: 0, z: 0 }" :rotation="smallChainRotationSeven(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
              </Group>
              End Morse Group-->
  
                <!-- Jewels-->
                <!-- n-1 smaller chains group between jewels-->
                <!--
              <Group v-if="glbArray.length != 0" v-for="groupIndex in braceletMorseArray.length - 1" :key="groupIndex">
                <GltfModel v-if="glbArray.length != 0" v-for="i in 5" :key="i" :src="`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`" @load="aquaBraceletChainOnReady" :position="{ x: braceletx + 3.02 + (groupIndex * 1.5)+(i * 0.055), y: 0, z: 0 }" :rotation="smallChainRotationSeven(i)" :scale="{ x: 0.6, y: 0.6, z: 0.6 }" />
              </Group>
              <GltfModel v-for="(glb, index) in glbArray" :key="index" :src="`/static/src/glb/aquafiore_bracelet/export/clasp_b.glb`" @load="aquaBraceletClaspOnReady" :position="{ x: braceletx+1, y: 0, z: 0 }" :rotation="{ x: 0, y: 0, z: 0 }" :scale="{x: 0.5, y: 0.5, z: 0.5}" />
              --></Scene>
            </Renderer>
          </div>
          <div></div>
        </div>
        <!-- End Aquafiore Bracelets-->
        <!-- Aquafiore Pendant -->
        <div v-if="key == 'aquafiore-pendant'" class="flex justify-center">
          <div></div>
          <div class="cbe-canvas">
            <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer">
              <Camera :position="{ z: 10 }" ref="camera" />
              <Scene ref="scene" background="white">
                <GltfModel v-if="glbArray.length != 0" v-for="(comp, index) in pendantArray" :key="index" @load="aquaPendantLoad($event, comp)" :src="comp.src" :position="comp.position" :rotation="comp.rotation" :scale="comp.scale" />
              </Scene>
            </Renderer>
          </div>
          <div></div>
        </div>
        <!-- End Aquafiore Pendant -->
        <!-- Aquafiore Earrings -->
        <div v-if="key == 'aquafiore-earrings'" class="flex justify-center">
          <div></div>
          <div class="cbe-canvas">
            <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer">
              <Camera :position="{ z: 10 }" ref="camera" />
              <Scene ref="scene" background="white">
                <GltfModel v-for="(comp, index) in earringArray" :key="index" @load="aquaEarringsLoad($event, comp)" :src="comp.src" :position="comp.position" :rotation="comp.rotation" :scale="comp.scale" />
              </Scene>
            </Renderer>
          </div>
          <div></div>
        </div>
        <!-- End Aquafiore Earrings -->
        <!-- Aquafiore Earrings -->
        <div v-if="key == 'aquafiore-necklace'" class="flex justify-center">
          <div></div>
          <div class="cbe-canvas">
            <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer">
              <Camera :position="{ z: 15 }" ref="camera" />
              <Scene ref="scene" background="white">
                <GltfModel v-for="(comp, index) in necklaceArray" :key="index" @load="necklaceLoad($event, comp)" :src="comp.src" :position="comp.position" :rotation="comp.rotation" :scale="comp.scale" />
              </Scene>
            </Renderer>
          </div>
          <div></div>
        </div>
        <!-- End Aquafiore Earrings -->
        <!-- ########################################## END 3D ######################################################################################-->
        <!-- #########################################Finish##################################################################### -->
        <!-- Amanti Finish-->
  
        <!-- End Amanti Finish-->
        <!-- Mayfair Finish-->
        <div v-if="key == 'mayfair'" class="flex justify-center mt-4 sm:mt-4 lg:mt-6">
          <div class="w-3/5 sm:w-3/5 lg:w-1/2">
            <label for="finishes" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white cbe-font-select-label text-center lg:text-center">Select Finish</label>
            <div class="flex justify-center">
              <select id="finishes" @change="mayfairUpdateFinish" class="cbe-select justify-center">
                <option v-for="option in obj.options">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <!-- End Mayfair Finish-->
        <!-- Aquafiore Bracelet Finish-->
        <div v-if="key == 'aquafiore-bracelet'" class="flex justify-center mt-4 sm:mt-4 lg:mt-6">
          <div class="w-3/5 sm:w-3/5 lg:w-1/2">
            <label for="finishes" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white cbe-font-select-label text-center lg:text-center">Select Finish</label>
            <div class="flex justify-center">
              <select id="finishes" @change="aquabraceletUpdateFinish" class="cbe-select justify-center">
                <option v-for="option in obj.options">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <!-- End Aquafiore Bracelet Finish-->
        <!-- Aquafiore Pendant Finish-->
        <div v-if="key == 'aquafiore-pendant'" class="flex justify-center mt-4 sm:mt-4 lg:mt-6">
          <div class="w-3/5 sm:w-3/5 lg:w-1/2">
            <label for="finishes" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white cbe-font-select-label text-center lg:text-center">Select Finish</label>
            <div class="flex justify-center">
              <select id="finishes" @change="aquapendantUpdateFinish" class="cbe-select justify-center">
                <option v-for="option in obj.options">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <!-- End Aquafiore Pendant Finish-->
        <!-- Aquafiore Earrings Finish-->
        <div v-if="key == 'aquafiore-earrings'" class="flex justify-center mt-4 sm:mt-4 lg:mt-6">
          <div class="w-3/5 sm:w-3/5 lg:w-1/2">
            <label for="finishes" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white cbe-font-select-label text-center lg:text-center">Select Finish</label>
            <div class="flex justify-center">
              <select id="finishes" @change="aquaearringUpdateFinish" class="cbe-select justify-center">
                <option v-for="option in obj.options">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <!-- End Aquafiore Earrings Finish-->
        <!-- Aquafiore Necklace Finish-->
        <div v-if="key == 'aquafiore-necklace'" class="flex justify-center mt-4 sm:mt-4 lg:mt-6">
          <div class="w-3/5 sm:w-3/5 lg:w-1/2">
            <label for="finishes" class="block mb-2 text-sm font-medium text-gray-900 dark:text-white cbe-font-select-label text-center lg:text-center">Select Finish</label>
            <div class="flex justify-center">
              <select id="finishes" @change="necklaceUpdateFinish" class="cbe-select justify-center">
                <option v-for="option in obj.options">
                  {{ option.text }}
                </option>
              </select>
            </div>
          </div>
        </div>
        <!-- End Aquafiore Earrings Finish-->
        <!-- ########################################End Finish#####################################################################-->
        <!-- ########################################Invoice Table#####################################################################-->
        <!-- Amanti And Earring Table-->
        <!--
      <div v-if="classes.amanti.includes(key) || classes.earring.includes(key)" class="flex justify-center mt-4 sm:mt-4 lg:mt-8">
        <div class="flex justify-center w-5/6 sm:w-5/6 lg:w-5/6">
          <table class="cbe-table">
            <thead class="cbe-table-head text-base sm:text-base">
              <tr>
                <th scope="col" class="px-4 py-3">Letter</th>
                <th scope="col" class="px-4 sm:px-4 lg:px-14 py-3">Morse Code</th>
                <th scope="col" class="px-4 py-3">Price</th>
              </tr>
            </thead>
            <tbody class="cbe-td">
              <tr v-for="char in messageArray" class="cbe-td">
                <td scope="row" class="cbe-td">{{ char }}</td>
                <td scope="row" class="cbe-td text-xl tracking-wider">{{ morseDict[char.toLowerCase()] }}</td>
                <td class="cbe-td">{{ "£" + " " + prices[char.toUpperCase()] }}</td>
              </tr>
            </tbody>
            <tfoot>
              <tr class="font-semibold text-left text-gray-900">
                <th scope="row" class="px-4 py-3 text-base text-left">Total</th>
                <td class="px-6 py-3"></td>
                <td class="px-4 py-3 text-left">{{ "£" + " " + total() }}</td>
              </tr>
            </tfoot>
          </table>
        </div>
      </div>
    -->
        <!-- End Amanti And Earring Table-->
        <!-- Aquafiore Necklace  Table-->
        <div v-if="classes.necklace.includes(key)" class="flex justify-center mt-4 sm:mt-4 lg:mt-8">
          <div class="flex justify-center w-5/6 sm:w-5/6 lg:w-5/6">
            <table class="cbe-table">
              <thead class="cbe-table-head text-base sm:text-base">
                <tr>
                  <th scope="col" class="px-4 py-3">Item</th>
                  <th scope="col" class="px-4 sm:px-4 lg:px-14 py-3">Morse Code</th>
                  <th scope="col" class="px-4 py-3">Price</th>
                </tr>
              </thead>
              <tbody v-if="messageArray.length != 0" class="cbe-td">
                <tr class="cbe-td">
                  <td scope="row" class="cbe-td">Necklace</td>
                  <td scope="row" class="cbe-td text-xl tracking-wider"></td>
                  <td class="cbe-td">{{ "£ " + necklacePrices.basic }}</td>
                </tr>
                <tr v-for="char in messageArray" class="cbe-td">
                  <td scope="row" class="cbe-td">{{ char }}</td>
                  <td scope="row" class="cbe-td text-xl tracking-wider">{{ morseDict[char.toLowerCase()] }}</td>
                  <td class="cbe-td">{{ "£ " + necklaceStonePrice(char) }}</td>
                </tr>
                <tr v-for="(spacer, index) in spacers" :key="index" class="cbe-td">
                  <td scope="row" class="cbe-td">Spacer {{ index + 1 }}</td>
                  <td scope="row" class="cbe-td text-xl tracking-wider"></td>
                  <td class="cbe-td">{{ "£ " + necklacePrices.spacer }}</td>
                </tr>
                <tr v-for="(hexagon, index) in hexagons" :key="index" class="cbe-td">
                  <td scope="row" class="cbe-td">Hexagon {{ index + 1 }}</td>
                  <td scope="row" class="cbe-td text-xl tracking-wider"></td>
                  <td class="cbe-td">{{ "£ " + necklacePrices.hexagon }}</td>
                </tr>
              </tbody>
              <tfoot>
                <tr class="font-semibold text-left text-gray-900 dark:text-white">
                  <th scope="row" class="px-4 py-3 text-base text-left">Total</th>
                  <td class="px-6 py-3"></td>
                  <td class="px-4 py-3 text-left">{{ messageArray.length == 0 ? "£  0" : `£  ` + necklaceTotal() }}</td>
                </tr>
              </tfoot>
            </table>
          </div>
        </div>
        <!-- End Aquafiore Necklace Table-->
        <!-- ##################################################################End Invoice Table#############################################################-->
        <!-- Add to Cart-->
        <!--
      <div class="flex justify-center mt-2 sm:mt-2 lg:mt-4">
        <form class="grid justify-center" onsubmit="return false;">
          <button v-if="submittable && cartable" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6 px-4" :disabled="working" @click="addToCart">Add to Cart</button>
          <div class="flex justify-center">
            <button v-if="working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6" disabled></button>
          </div>
        </form>
      </div>
    -->
        <!-- End Add to Cart-->
        <!-- Email Collection-->
        <!--
      <div class="flex justify-center mt-4 sm:mt-4 lg:mt-8">
        <div class="cbe-footer-text">
          <p class="cbe-footer-text">Get Quote & 3D Rendering</p>
        </div>
      </div>
      <div class="flex justify-center mt-2 sm:mt-2 lg:mt-4">
        <form class="grid justify-center" onsubmit="return false;">
          <input :class="inputClass" type="email" placeholder="Enter your email" v-model="email" />
          <hr />
          <span v-if="isInvalid" class="flex items-center font-medium tracking-wide text-red-500 text-xs mt-1 ml-1">Invalid Email!</span>
          <button v-if="submittable && key != 'aquafiore-necklace'" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6" :disabled="working" @click="submit">Submit</button>
          <button v-if="submittable && key == 'aquafiore-necklace'" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6" :disabled="working" @click="necklaceSubmit">Submit</button>
          <div class="flex justify-center">
            <button v-if="working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6" disabled></button>
          </div>
        </form>
      </div>
    -->
        <!-- End Email Collection-->
        <!-- Empty Low-->
        <div class="mt-4 sm:mt-4 lg:mt-8"></div>
        <!-- Email Modal-->
        <div id="emailModal" :class="`${modalVisible ? '' : 'hidden'} fixed z-10 inset-0 overflow-y-auto`">
          <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
            <div class="fixed inset-0 transition-opacity">
              <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <!-- Modal content -->
            <div class="fixed top-0 py-20 inline-block align-bottom bg-white rounded-lg text-center overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <button type="button" class="fixed top-5 right-5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="defaultModal" @click="modalVisible = false">
                  <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
                <div class="flex items-center justify-center">
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-center w-full">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 cbe-font text-xl text-teal-950">Talk to Us</h3>
                    <div class="mt-4">
                      <form class="grid justify-center" onsubmit="return false;">
                        <label class="cbe-font font-medium text-lg text-teal-950 text-left py-2">Email</label>
                        <input :class="inputClassEmail" type="email" placeholder="Enter your email" v-model="email" />
                        <hr />
                        <span v-if="isInvalidEmail" class="flex items-center font-medium tracking-wide text-red-500 text-xs mt-1 ml-1">Invalid Email!</span>
                        <label class="cbe-font font-medium text-lg text-teal-950 text-left py-2">Message</label>
                        <textarea :class="inputClassEmailMessage" type="email" placeholder="Enter your message" v-model="emailMessage" rows="20" id="emailMessage"></textarea>
                        <span v-if="isInvalidEmailMessage" class="flex items-center font-medium tracking-wide text-red-500 text-xs mt-1 ml-1">Invalid Message!</span>
                        <button v-if="key != 'aquafiore-necklace'" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6" :disabled="working" @click="submit">Send</button>
                        <button v-if="submittable && key == 'aquafiore-necklace'" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6" :disabled="working" @click="necklaceSubmit">Submit</button>
                        <div class="flex justify-center">
                          <button v-if="working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6" disabled></button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- End Modal-->
        <!-- Email Modal-->
  
        <!-- End Email Modal-->
      </div>
      <!-- Mobile Version -->
      <div class="w-full" v-if="!desktop">
        <div class="flex flex-col content-center justify-center mt-0" style="display: flex; justify-content: center">
          <!-- Buy Now -->
          <button v-if="!working" :class="`${buyButtonDisabled ? 'bg-slate-500' : 'cbe-bg-green hover:bg-teal-700'} w-full py-8 px-4 rounded-lg justify-self-end text-2xl font-extrabold text-white`" :disabled="buyButtonDisabled" @click="addToCart">
            <div class="flex justify-between px-8" style="display: flex; justify-content: space-between">
              <p class="cbe-font-comorant">£{{ total() }}</p>
              <p class="cbe-font-comorant-garamond">Buy Now</p>
            </div>
          </button>
          <button v-if="working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6 ml-48 mb-4" disabled></button>
          <!-- Talk to Us-->
          <div class="basis-12/12 flex items-center mt-2" style="display: flex; justify-content: center">
            <button class="bg-gray-100 hover:bg-gray-200 cbe-btn-text-green cbe-btn-text-font py-4 px-12 rounded-none h-3/4" @click="emailModalVisible = true">
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
          <!-- 3D Container-->
          <div class="basis-6/12" style="display: flex; justify-content: center">
            <div v-if="key == 'amanti'">
              <div class="cbe-canvas mt-12">
                <Renderer :resize="true" :orbitCtrl="true" :antialias="true" ref="renderer" :alpha="true">
                  <Camera :position="{ z: 0 }" ref="camera" />
                  <Scene ref="scene" background="white">
                    <GltfModel v-for="(glb, index) in glbArray" :key="index" :src="`/static/src/glb/ring_` + glb + `.glb`" @load="onReady" :position="{ x: index * 0, y: index * 0, z: index * 1.5 - 2 }" :rotation="{ x: 0, y: 0, z: 0 }" />
                  </Scene>
                  <EffectComposer>
                    <RenderPass />
                    <UnrealBloomPass :strength="0.18" />
                  </EffectComposer>
                </Renderer>
              </div>
            </div>
          </div>
          <!-- Options Footer-->
          <div class="flex flex-row w-full fixed bottom-0 z-10" style="display: flex; justify-content: center">
            <!-- Message -->
            <div class="basis-4/12 pr-1">
              <button :class="`${optionActive == 'message' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-6 w-full rounded-none`" @click="rowMobileUpdate('message')">
                <div class="flex flex-row content-center justify-center gap-x-2">
                  <div class="basis-3/4">
                    <p class="font-bold">Message</p>
                  </div>
                </div>
              </button>
            </div>
            <div class="basis-4/12 pr-1">
              <button :class="`${optionActive == 'metal' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-4 w-full rounded-none`" @click="rowMobileUpdate('metal')">
                <div class="flex flex-row content-center justify-center gap-x-2">
                  <div class="basis-3/4 flex flex-col">
                    <p class="italic text-xs">Select</p>
                    <p class="font-bold">Metal</p>
                  </div>
                </div>
              </button>
            </div>
            <div class="basis-4/12">
              <button :class="`${optionActive == 'size' ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} cbe-btn-text-green cbe-btn-text-font py-4 w-full rounded-none`" @click="rowMobileUpdate('size')">
                <div class="flex flex-row content-center justify-center gap-x-2">
                  <div class="basis-3/4 flex flex-col">
                    <p class="italic text-xs">Select</p>
                    <p class="font-bold">Size</p>
                  </div>
                </div>
              </button>
            </div>
          </div>
        </div>
        <!-- Email Modal-->
        <div id="emailModalMobile" :class="`${emailModalVisible ? '' : 'hidden'} fixed z-10 inset-0 overflow-y-auto`">
          <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
            <div class="fixed inset-0 transition-opacity">
              <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <!-- Modal content -->
            <div class="fixed top-2 bottom-2 w-5/6 py-20 inline-block align-bottom bg-white rounded-lg text-center overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <button type="button" class="fixed top-5 right-5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="defaultModal" @click="emailModalVisible = false">
                  <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
                <div class="flex items-center justify-center">
                  <div class="mt-3 text-center sm:mt-0 sm:ml-4 sm:text-center w-full">
                    <h3 class="text-lg leading-6 font-medium text-gray-900 cbe-font text-xl text-teal-950">Talk to Us</h3>
                    <div class="mt-4">
                      <form class="grid justify-center" onsubmit="return false;">
                        <label class="cbe-font font-medium text-lg text-teal-950 text-left py-2">Email</label>
                        <input :class="inputClassEmail" type="email" placeholder="Enter your email" v-model="email" />
                        <hr />
                        <span v-if="isInvalidEmail" class="flex items-center font-medium tracking-wide text-red-500 text-xs mt-1 ml-1">Invalid Email!</span>
                        <label class="cbe-font font-medium text-lg text-teal-950 text-left py-2">Message</label>
                        <textarea :class="inputClassEmailMessage" type="email" placeholder="Enter your message" v-model="emailMessage" rows="20" id="emailMessage"></textarea>
                        <span v-if="isInvalidEmailMessage" class="flex items-center font-medium tracking-wide text-red-500 text-xs mt-1 ml-1">Invalid Message!</span>
                        <button v-if="key != 'aquafiore-necklace'" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6" :disabled="working" @click="submit">Send</button>
                        <button v-if="submittable && key == 'aquafiore-necklace'" type="button" class="cbe-btn mt-4 sm:mt-4 lg:mt-6" :disabled="working" @click="necklaceSubmit">Submit</button>
                        <div class="flex justify-center">
                          <button v-if="working == true" type="button" class="cbe-spinner mt-4 sm:mt-4 lg:mt-6" disabled></button>
                        </div>
                      </form>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
        <!-- Global Modal-->
        <div id="MobileModal" :class="`${mobileModalVisible ? '' : 'hidden'} fixed z-9 inset-0 overflow-y-scroll`">
          <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:p-0">
            <div class="fixed inset-0 transition-opacity">
              <div class="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <!-- Modal content -->
            <div class="fixed bottom-0 w-full inline-block bg-white rounded-lg text-center overflow-scroll shadow-xl transform transition-all">
              <div class="bg-white px-4 pt-5 pb-4 mb-28">
                <button type="button" class="fixed top-5 right-5 text-gray-400 bg-transparent hover:bg-gray-200 hover:text-gray-900 rounded-lg text-sm p-1.5 ml-auto inline-flex items-center dark:hover:bg-gray-600 dark:hover:text-white" data-modal-hide="defaultModal" @click="mobileModalClose()">
                  <svg aria-hidden="true" class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                </button>
                <div class="flex items-center justify-center">
                  <!-- Amanti (Simple) Input-->
                  <div v-show="optionActive == 'message'" :class="`basis-11/12 mt-16`" v-if="classes.amanti.includes(key) && key != 'aquafiore-bracelet' && key != 'aquafiore-pendant'">
                    <div class="message__inputs">
                      <div class="message__input-container">
                        <div class="morse-code" id="morseContainer"></div>
                        <div class="message__input cbe-font-mono" contenteditable="true" @input="amantiUpdateMorse" id="messageInput" :onkeypress="amantiValidateInput" :style="{ 'font-size': '2rem !important', 'letter-spacing': '1.14rem' }"></div>
                        <div class="message__placeholder message__placeholder--visible cbe-font cbe-message-placeholder-fix mt-1">{{ placeholder }}</div>
                      </div>
                    </div>
                    <div v-if="isRendering" class="col-span-3 align-middle grid grid-cols-3 content-center">
                      <div></div>
                      <div class="flex justify-center"><img class="text-center align-middle" src="./Infinity-1s-197px.gif" /></div>
                      <div></div>
                    </div>
                    <div v-if="!isRendering" class="col-span-3 align-middle">
                      <p class="text-center text-stone-500 cbe-font-label mt-1 text-sm">Zoom: Mouse Wheel, Rotate: Left Mouse Button, Pan: Right Mouse Button</p>
                    </div>
                    <div></div>
                  </div>
                  <!-- Select Metal-->
                  <div v-show="optionActive == 'metal'" v-if="key == 'amanti'" :class="`flex flex-col basis-12/12 w-full mt-12`" style="display: flex; justify-content: center">
                    <div class="mb-1" v-for="option in obj.options" :key="option">
                      <button :class="`${isActiveFinish(option.text) ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} py-6  rounded-none w-full py-2 px-10 rounded-lg justify-self-end`" :disabled="isActiveFinish(option.text)" @click="amantiUpdateFinish(option.text)">
                        <div class="flex justify-between px-8" style="display: flex; justify-content: space-between">
                          <p class="cbe-btn-text-font text-sm font-medium">{{ option.text }}</p>
                          <p class="text-sm text-gray-500">{{ metalDiff(option.text) }}</p>
                        </div>
                      </button>
                    </div>
                    <div class="cbe-font cbe-btn-text-green italic mt-2 mb-2">
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
                  <div v-show="optionActive == 'size'" v-if="key == 'amanti'" :class="`flex flex-col basis-12/12 w-full mt-12`" style="display: flex; justify-content: center">
                    <div class="flex flex-row mb-1" v-for="sizeRow in sizesObj()" :key="sizeRow" style="display: flex; justify-content: start">
                      <div class="basis-4/12 pr-1" v-for="size in sizeRow" :key="size">
                        <button :class="`${isActiveSize(size) ? 'cbe-bg-green-lightest' : 'bg-gray-100 hover:bg-gray-200'} bg-gray-100 hover:bg-gray-200 cbe-btn-text-green cbe-bnt-text-font py-2 w-full rounded-none text-sm`" @click="activeSizeUpdate(size)">
                          {{ size }}
                        </button>
                      </div>
                    </div>
                    <div class="cbe-font cbe-btn-text-green italic mt-2 mb-2">
                      <p class="mb-4 font-semibold">Do you need help with sizing?</p>
                      <p class="mb-4 font-semibold">Contact Us</p>
                      <p class="mb-1 font-semibold">Call us on +44 20 3883 1388</p>
                      <p class="mb-1 font-semibold">Monday to Friday - 10 AM - 5:30 PM</p>
                      <p class="mb-1 font-semibold">Email</p>
                      <a class="mb-1 font-semibold" href="mailto:hello@codebyedge.com">hello@codebyedge.com</a>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  <script>
  import db from "./db.json";
  import axios, { isCancel, AxiosError } from "axios";
  import * as THREE from "three";
  import { EffectComposer, HalftonePass, RenderPass, UnrealBloomPass } from "troisjs";
  import { RGBELoader } from "three/examples/jsm/loaders/RGBELoader.js";
  import { OrbitControls } from "three/examples/jsm/controls/OrbitControls.js";
  import { DirectionalLight, PointLight, Color } from "three";
  axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
  axios.defaults.xsrfCookieName = "csrftoken";
  export default {
    components: { EffectComposer, HalftonePass, RenderPass, UnrealBloomPass },
    computed: {
      buyButtonDisabled() {
        let r = false;
        if (this.message == null || this.message.length == 0 || this.working) {
          r = true;
        }
        return r;
      },
      braceletJewelsOffset() {
        let offset = 0;
        if (this.messageArray.length != 0) {
          let element = this.messageArray[0];
          let morse = this.morseDict[element.toLowerCase()];
          let first = morse.charAt(0);
          if (first == ".") {
            offset = 3.785;
          } else if (first == "-") {
            offset = 3.885;
          }
        }
        return offset;
      },
      cartable() {
        let cartable = ["amanti", "mayfair", "aquafiore-bracelet", "aquafiore-pendant", "aquafiore-earrings", "aquafiore-necklace"];
        return cartable.includes(this.key);
      },
      desktop() {
        let r = true;
        if (window.innerWidth <= 600) {
          r = false;
        }
        return r;
      },
      inputClassEmail() {
        if (this.isInvalidEmail == true) {
          return "cbe-font text-xl py-2  relative w-full border rounded placeholder-gray-400 focus:border-indigo-400 focus:outline-none py-2 pr-2 pl-12 border-red-500";
        } else {
          return "cbe-font text-xl py-2";
        }
      },
      inputClassEmailMessage() {
        if (this.isInvalidEmailMessage == true) {
          return "cbe-font text-xl py-2  relative w-full border rounded placeholder-gray-400 focus:border-indigo-400 focus:outline-none py-2 pr-2 pl-12 border-red-500";
        } else {
          return "cbe-font text-xl py-2";
        }
      },
      submittable() {
        let s = false;
        if (this.key == "aquafiore-earrings") {
          s = this.working == false && this.messageArrayLeft.length != 0 && this.messageArrayRight.length != 0;
        } else {
          s = this.working == false && this.messageArray.length != 0;
        }
        return s;
      },
    },
    data() {
      return {
        activeFinish: 0xf5b838,
        activeSize: null,
        braceletArray: [],
        braceletx: 0,
        braceletMorseArray: [],
        braceletMiddleEnd: 0,
        classes: {
          amanti: ["amanti", "mayfair", "aquafiore-bracelet", "aquafiore-pendant"],
          earring: ["aquafiore-earrings"],
          necklace: ["aquafiore-necklace"],
        },
        db: db,
        debug: null,
        editableAmanti: true,
        email: null,
        emailMessage: null,
        emailModalVisible: false,
        earringArray: [],
        finishes: {
          "18ct Recycled Yellow Gold": 0xf5b838,
          "18ct Recycled Rose Gold": 0xe5844b,
          "950 Platinum": 0xaaaaaa,
          "925 Silver": 0xcccccc,
        },
        fontSize: 2,
        glbArray: [],
        hexagons: [],
        isInvalidEmail: false,
        isInvalidEmailMessage: false,
        isRendering: false,
        key: null,
        lineSpacing: 1.2,
        message: "",
        messageArray: [],
        messageArrayLeft: [],
        messageArrayRight: [],
        messageLeft: "",
        messageRight: "",
        mobileModalVisible: true,
        modalVisible: false,
        morseDict: { a: ".-", b: "-...", c: "-.-.", d: "-..", e: ".", f: "..-.", g: "--.", h: "....", i: "..", j: ".---", k: "-.-", l: ".-..", m: "--", n: "-.", o: "---", p: ".--.", q: "--.-", r: ".-.", s: "...", t: "-", u: "..-", v: "...-", w: ".--", x: "-..-", y: "-.--", z: "--..", 0: "-----", 1: ".----", 2: "..---", 3: "...--", 4: "....-", 5: ".....", 6: "-....", 7: "--...", 8: "---..", 9: "----." },
        necklaceArray: [],
        necklacePrices: null,
        obj: {
          limit: null,
          chLimit: null,
          options: [],
        },
        optionActive: "message",
        pendantArray: [],
        placeholder: "Please enter your message",
        placeholderLeft: "Left",
        placeholderRight: "Right",
        prices: {},
        products: {
          amanti: 8218132152617,
          mayfair: 8236553765161,
          "aquafiore-bracelet": 8236574441769,
          "aquafiore-pendant": 8236577947945,
          "aquafiore-earrings": 8236587319593,
          "aquafiore-necklace": 8236619301161,
        },
        spacers: [],
        working: false,
      };
    },
    methods: {
      activeSizeUpdate(size) {
        this.activeSize = size;
      },
      addToCart() {
        let thisComponent = this;
        thisComponent.working = true;
        //let finish = document.getElementById("finishes").value;
        let finish;
        this.obj.options.forEach((option) => {
          if (thisComponent.finishes[option.text] == thisComponent.activeFinish) {
            finish = option.text;
          }
        });
        let variantMessage = "";
        if (thisComponent.key == "aquafiore-earrings") {
          variantMessage = "Left: " + thisComponent.messageLeft + ",Right: " + thisComponent.messageRight;
        } else {
          variantMessage = thisComponent.message;
        }
        let total = 0;
        if (thisComponent.key == "aquafiore-necklace") {
          total = thisComponent.necklaceTotal();
        } else {
          total = thisComponent.total();
        }
        let size = thisComponent.activeSize;
        axios
          .post(
            "/api/variants",
            {
              product: thisComponent.products[thisComponent.key],
            },
            {
              headers: {
                "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken").value,
              },
            }
          )
          .then(function (response) {
            thisComponent.working = false;
            let variants = response.data.product?.variants;
            let variant = "not_found";
            variants.forEach((v) => {
              if (parseInt(v.price) == parseInt(total)) {
                variant = v;
                return;
              }
            });
            if (variant == "not_found") {
              // create one
              axios
                .post("/api/variants/create", {
                  productid: thisComponent.products[thisComponent.key],
                  price: total,
                })
                .then(function (response) {
                  variant = response.data.variant;
                  window.open(`https://codebyedge.co.uk/cart/add?id=${variant.id}&quantity=1&properties[message]=${encodeURIComponent(variantMessage)}&properties[finish]=${encodeURIComponent(finish)}&properties[size]=${encodeURIComponent(size)}`, "_blank");
                  return;
                  window.open(`https://codebyedge.co.uk/cart/add?id=${variant.id}&quantity=1&properties[message]=${variantMessage}&properties[finish]=${finish}`, "_blank");
  
                  setTimeout(() => {
                    window.open(`https://codebyedge.co.uk/cart/add?id=${variant.id}&quantity=1&properties[message]=${variantMessage}&properties[finish]=${finish}`, "_blank");
                  }, 8000);
                })
                .catch(function (error) {
                  console.log(error);
                  console.log(error.response);
                });
            } else {
              // ready to redirect
              window.open(`https://codebyedge.co.uk/cart/add?id=${variant.id}&quantity=1&properties[message]=${encodeURIComponent(variantMessage)}&properties[finish]=${encodeURIComponent(finish)}&properties[size]=${encodeURIComponent(size)}`, "_blank");
            }
          })
          .catch(function (error) {
            console.log(error);
            console.log(error.response);
          });
        return;
        /*
        let productID = this.products[this.key];
        let variants = null;
        // get me all the variants of this product
  
        let total = this.total();
        "https://codebyedge.co.uk/cart/add?quantity=1&id=44820388544809"
        window.open(`https://codebyedge.co.uk/cart/add?id=${variant}&quantity=1&price=${total}`, "_blank");
        */
      },
      aquabraceletUpdateFinish(e) {
        let finish = e.target.value;
        let newPrices = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newPrices = newPrices[0].letters;
        this.prices = newPrices;
        this.activeFinish = this.finishes[e.target.value];
        let thisComponent = this;
        let scene = this.$refs.scene.scene;
        let newMat = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "chain",
        });
        // groups
        scene.children.forEach((group) => {
          // has material?
          if (group.material) {
            if (group.material.name == "chain" || group.material.name == "clasp" || group.material.name == "hexagon") {
              group.material = newMat;
              group.updateMatrix();
            }
          } else {
            // has children?
            if (group.children.length != 0) {
              // objects
              group.children.forEach((object) => {
                // has material?
                if (object.material) {
                  if (object.material.name == "chain" || object.material.name == "clasp" || object.material.name == "hexagon") {
                    object.material = newMat;
                    object.updateMatrix();
                  }
                } else {
                  // has children?
                  if (object.children.length != 0) {
                    // components
                    object.children.forEach((comp) => {
                      // has material?
                      if (comp.material) {
                        if (comp.material.name == "chain" || comp.material.name == "clasp" || comp.material.name == "hexagon") {
                          comp.material = newMat;
                          comp.updateMatrix();
                        }
                      }
                    });
                  }
                }
              });
            }
          }
        });
        /*
        scene.children.forEach((element) => {
          if (element.children.length != 0) {
            element.children.forEach((obj) => {
              obj.children.forEach((mesh) => {
                if (mesh.material != null) {
                  if (mesh.material.name == "chain") {
                    mesh.material = new THREE.MeshStandardMaterial({
                      color: thisComponent.activeFinish,
                      metalness: 1,
                      roughness: 0.05,
                      name: "chain",
                    });
                    mesh.updateMatrix();
                  }
                }
              });
            });
          }
        });
        */
      },
      aquaBraceletChainOnReady(e) {
        let thisComponent = this;
        let chain = e.scene.children[0];
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "chain",
        });
        chain.material = metal;
      },
      aquaBraceletClaspOnReady(e) {
        let thisComponent = this;
        let elements = e.scene.children[0].children;
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "clasp",
        });
        elements.forEach((element) => {
          element.material = metal;
        });
      },
      aquaBraceletHexOnReady(e) {
        let thisComponent = this;
        let elements = e.scene.children[0].children;
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "hexagon",
        });
        elements.forEach((element) => {
          element.material = metal;
        });
      },
      aquaBraceletJewelOnReady(e) {
        let thisComponent = this;
        let elements = e.scene.children[0].children;
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "chain",
        });
        const gem = new THREE.MeshPhysicalMaterial({
          color: 0x002211,
          clearcoat: 0,
          clearcoatRoughness: 0,
          ior: 2.1,
          reflectivity: 1,
          metalness: 0,
          roughness: 0,
          specularIntensity: 0.94,
          specularColor: 0xffeeaa,
          transmission: 0.7,
          name: "jewel",
        });
        elements.forEach((element) => {
          if (element.material.name == "chain") {
            element.material = metal;
          } else if (element.material.name == "jewel") {
            element.material = gem;
          }
        });
      },
      aquaBraceletMiddleOnReady(e) {
        let thisComponent = this;
        let name = e.scene.children[0].name;
        if (name == "RD" || name == "OB") {
          let elements = e.scene.children[0].children;
          const metal = new THREE.MeshStandardMaterial({
            color: thisComponent.activeFinish,
            metalness: 1,
            roughness: 0.05,
            name: "chain",
          });
          const gem = new THREE.MeshPhysicalMaterial({
            color: 0x002211,
            clearcoat: 0,
            clearcoatRoughness: 0,
            ior: 2.1,
            reflectivity: 1,
            metalness: 0,
            roughness: 0,
            specularIntensity: 0.94,
            specularColor: 0xffeeaa,
            transmission: 0.7,
            name: "jewel",
          });
          elements.forEach((element) => {
            if (element.material.name == "chain") {
              element.material = metal;
            } else if (element.material.name == "jewel") {
              element.material = gem;
            }
          });
        } else if (name == "Chain_Element_metal") {
          let chain = e.scene.children[0];
          const metal = new THREE.MeshStandardMaterial({
            color: thisComponent.activeFinish,
            metalness: 1,
            roughness: 0.05,
            name: "chain",
          });
          chain.material = metal;
        }
      },
      aquaBraceletUpdateMorse(e) {
        this.placeholder = null;
        let morseContainer = document.getElementById("morseContainer");
        morseContainer.innerHTML = null;
        this.message = document.getElementById("messageInput").innerHTML;
        if (this.message === "") {
          this.placeholder = "Please enter your message";
        } else {
          this.placeholder = null;
        }
        // morse function
        let messageArray = this.message.split("");
        this.messageArray = messageArray;
        let equiv = null;
        let insertion = null;
        let morseClass = null;
        let morseHeight = null;
        let thisComponent = this;
        thisComponent.braceletMorseArray = [];
        thisComponent.glbArray = [];
        thisComponent.$forceUpdate();
        let braceletArray = [];
        class middleComponent {
          constructor(src, position, rotation, scale) {
            this.src = src;
            this.position = position;
            this.rotation = rotation;
            this.scale = scale;
          }
        }
        let xAxis = 3.4;
        let dotX = 0.385;
        let chainX = 0.055;
        let dashX = 0.485;
        let push;
        thisComponent.$nextTick(() => {
          messageArray.forEach((element) => {
            // find dict equiv
            thisComponent.glbArray.push(element.toUpperCase());
            equiv = this.morseDict[element.toLowerCase()];
            // if not null
            if (equiv) {
              let insertion = `<div class="morse-code__letter">`;
              equiv = equiv.split("");
              equiv.forEach((chara) => {
                if (chara == ".") {
                  morseClass = "morse-code--dot";
                  morseHeight = "6px";
                  xAxis += dotX;
                  push = new middleComponent(
                    `/static/src/glb/aquafiore_bracelet/export/dot_b.glb`,
                    {
                      x: xAxis,
                      y: 0,
                      z: 0,
                    },
                    { x: 0, y: 0, z: 0 },
                    { x: 0.45, y: 0.45, z: 0.45 }
                  );
                  braceletArray.push(push);
                  xAxis += dotX;
                  // add 5 chains
                  for (let index = 0; index < 5; index++) {
                    let xRotation = index % 2 ? 1.6 : 0;
                    push = new middleComponent(
                      `/static/src/glb/aquafiore_bracelet/export/chain_b.glb`,
                      {
                        x: xAxis,
                        y: 0,
                        z: 0,
                      },
                      { x: xRotation, y: 0, z: 0 },
                      { x: 0.6, y: 0.6, z: 0.6 }
                    );
                    braceletArray.push(push);
                    if (index != 4) {
                      xAxis += chainX;
                    }
                  }
                  //thisComponent.braceletMorseArray.push("dot");
                } else {
                  //thisComponent.braceletMorseArray.push("dash");
                  morseClass = "morse-code--dash";
                  morseHeight = "16px";
                  xAxis += dashX;
                  push = new middleComponent(
                    `/static/src/glb/aquafiore_bracelet/export/dash_b.glb`,
                    {
                      x: xAxis,
                      y: 0,
                      z: 0,
                    },
                    { x: 0, y: 0, z: 0 },
                    { x: 0.45, y: 0.45, z: 0.45 }
                  );
                  braceletArray.push(push);
                  xAxis += dashX;
                  // add 5 chains
                  for (let index = 0; index < 5; index++) {
                    let xRotation = index % 2 ? 1.6 : 0;
                    push = new middleComponent(
                      `/static/src/glb/aquafiore_bracelet/export/chain_b.glb`,
                      {
                        x: xAxis,
                        y: 0,
                        z: 0,
                      },
                      { x: xRotation, y: 0, z: 0 },
                      { x: 0.6, y: 0.6, z: 0.6 }
                    );
                    braceletArray.push(push);
                    if (index != 4) {
                      xAxis += chainX;
                    }
                  }
                }
                insertion += `<div class="${morseClass}" style="height: ${morseHeight}"></div>`;
              });
              insertion += `</div>`;
              morseContainer.innerHTML += insertion;
            }
          });
          braceletArray.splice(-5);
          thisComponent.braceletArray = braceletArray;
          thisComponent.braceletMiddleEnd = xAxis;
        });
  
        //console.log(messageArray);
        //console.log(e)
      },
      aquaEarringsLoad(e, comp) {
        let thisComponent = this;
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "metal",
        });
        const gem = new THREE.MeshPhysicalMaterial({
          color: 0x002211,
          clearcoat: 0,
          clearcoatRoughness: 0,
          ior: 2.1,
          reflectivity: 1,
          metalness: 0,
          roughness: 0,
          specularIntensity: 0.94,
          specularColor: 0xffeeaa,
          transmission: 0.7,
          name: "gem",
        });
        let type = comp.type;
        if (type == "stud") {
          let elements = e.scene.children[0].children;
          elements.forEach((element) => {
            if (element.material.name == "metal" || element.material.name == "metal.003" || element.material.name == "metal.001") {
              element.material = metal;
            } else if (element.material.name == "gem") {
              element.material = gem;
            }
          });
        } else if (type == "chain") {
          let chain = e.scene.children[0];
          chain.material = metal;
        } else if (type == "gem") {
          let name = e.scene.children[0].name;
          if (name == "RD" || name == "OB") {
            let elements = e.scene.children[0].children;
            elements.forEach((element) => {
              if (element.material.name == "chain") {
                element.material = metal;
              } else if (element.material.name == "jewel") {
                element.material = gem;
              }
            });
          }
        }
        /*
        if (type == "stud") {
          let chain = e.scene.children[0];
          chain.material = metal;
        } else if (type == "gem") {
          let name = e.scene.children[0].name;
          if (name == "RD" || name == "OB") {
            let elements = e.scene.children[0].children;
            elements.forEach((element) => {
              if (element.material.name == "chain") {
                element.material = metal;
              } else if (element.material.name == "jewel") {
                element.material = gem;
              }
            });
          } else if (name == "Chain_Element_metal") {
            let chain = e.scene.children[0];
            chain.material = metal;
          }
        } else if (type == "hex") {
          let elements = e.scene.children[0].children;
          elements.forEach((element) => {
            element.material = metal;
          });
        }
        */
      },
      aquapendantUpdateFinish(e) {
        let finish = e.target.value;
        let newPrices = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newPrices = newPrices[0].letters;
        this.prices = newPrices;
        this.activeFinish = this.finishes[e.target.value];
        let thisComponent = this;
        let scene = this.$refs.scene.scene;
        let newMat = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "chain",
        });
        // groups
        scene.children.forEach((group) => {
          // has material?
          if (group.material) {
            if (group.material.name == "chain" || group.material.name == "clasp" || group.material.name == "hexagon") {
              group.material = newMat;
              group.updateMatrix();
            }
          } else {
            // has children?
            if (group.children.length != 0) {
              // objects
              group.children.forEach((object) => {
                // has material?
                if (object.material) {
                  if (object.material.name == "chain" || object.material.name == "clasp" || object.material.name == "hexagon") {
                    object.material = newMat;
                    object.updateMatrix();
                  }
                } else {
                  // has children?
                  if (object.children.length != 0) {
                    // components
                    object.children.forEach((comp) => {
                      // has material?
                      if (comp.material) {
                        if (comp.material.name == "chain" || comp.material.name == "clasp" || comp.material.name == "hexagon") {
                          comp.material = newMat;
                          comp.updateMatrix();
                        }
                      }
                    });
                  }
                }
              });
            }
          }
        });
      },
      aquaPendantLoad(e, comp) {
        let thisComponent = this;
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "chain",
        });
        const gem = new THREE.MeshPhysicalMaterial({
          color: 0x002211,
          clearcoat: 0,
          clearcoatRoughness: 0,
          ior: 2.1,
          reflectivity: 1,
          metalness: 0,
          roughness: 0,
          specularIntensity: 0.94,
          specularColor: 0xffeeaa,
          transmission: 0.7,
          name: "jewel",
        });
        let type = comp.type;
        if (type == "chain") {
          let chain = e.scene.children[0];
          chain.material = metal;
        } else if (type == "gem") {
          let name = e.scene.children[0].name;
          if (name == "RD" || name == "OB") {
            let elements = e.scene.children[0].children;
            elements.forEach((element) => {
              if (element.material.name == "chain") {
                element.material = metal;
              } else if (element.material.name == "jewel") {
                element.material = gem;
              }
            });
          } else if (name == "Chain_Element_metal") {
            let chain = e.scene.children[0];
            chain.material = metal;
          }
        } else if (type == "hex") {
          let elements = e.scene.children[0].children;
          elements.forEach((element) => {
            element.material = metal;
          });
        }
      },
      aquaPendantUpdateMorse(e) {
        this.placeholder = null;
        let morseContainer = document.getElementById("morseContainer");
        morseContainer.innerHTML = null;
        this.message = document.getElementById("messageInput").innerHTML;
        if (this.message === "") {
          this.placeholder = "Please enter your message";
        } else {
          this.placeholder = null;
        }
        // morse function
        let messageArray = this.message.split("");
        this.messageArray = messageArray;
        let equiv = null;
        let insertion = null;
        let morseClass = null;
        let morseHeight = null;
        let thisComponent = this;
        let pendantArray = [];
        thisComponent.pendantArray = [];
        thisComponent.glbArray = [];
        thisComponent.$forceUpdate();
        class glbObject {
          constructor(src, position, rotation, scale, type) {
            this.src = src;
            this.position = position;
            this.rotation = rotation;
            this.scale = scale;
            this.type = type;
          }
        }
        let originx = 0;
        let originy = 0;
        let rotationx = 1.566;
        let leftInitialRotationx = 0;
        let leftInitialRotationz = 1.95;
        let leftRotationx = 0;
        let leftRotationz = 0;
        let rightInitialRotationx = 0;
        let rightInitialRotationz = 1.2;
        let rightRotationx = 0;
        let rightRotationz = 0;
        let obj;
        thisComponent.$nextTick(() => {
          // first origin chain
          obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx, y: originy, z: 0 }, { x: rotationx, y: 0, z: 0 }, { x: 1, y: 1, z: 1 }, "chain");
          pendantArray.push(obj);
          // second, left side
          let leftOriginx = originx - 0.015;
          let leftOriginy = originy + 0.015;
          for (let index = 1; index < 150; index++) {
            leftRotationx = index % 2 ? leftInitialRotationx : rotationx;
            leftRotationz = index % 2 ? leftInitialRotationz : 0;
            obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: leftOriginx - index * 0.02, y: leftOriginy + index * 0.045, z: 0 }, { x: leftRotationx, y: 0, z: leftRotationz }, { x: 0.5, y: 0.5, z: 0.5 }, "chain");
            pendantArray.push(obj);
          }
          obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: leftOriginx - 150 * 0.02 - 0.01, y: leftOriginy + 150 * 0.045 + 0.015, z: 0 }, { x: rotationx, y: 0, z: 0 }, { x: 1, y: 1, z: 1 }, "chain");
          pendantArray.push(obj);
          // third, right side
          let rightOriginx = originx + 0.015;
          let rightOriginy = originy + 0.015;
          let hexExclude = [133, 134, 135, 136, 137, 138, 139, 140, 141];
          for (let index = 1; index < 147; index++) {
            if (!hexExclude.includes(index)) {
              rightRotationx = index % 2 ? rightInitialRotationx : rotationx;
              rightRotationz = index % 2 ? rightInitialRotationz : 0;
              obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: rightOriginx + index * 0.02, y: rightOriginy + index * 0.045, z: 0 }, { x: rightRotationx, y: 0, z: rightRotationz }, { x: 0.5, y: 0.5, z: 0.5 }, "chain");
              pendantArray.push(obj);
            }
          }
          // hexagon
          obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/hex_b.glb`, { x: rightOriginx + 137 * 0.02, y: rightOriginy + 137 * 0.045, z: 0 }, { x: rotationx, y: rightInitialRotationz, z: 0 }, { x: 0.25, y: 0.25, z: 0.25 }, "hex");
          pendantArray.push(obj);
          // clasp
          obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/clasp_b.glb`, { x: rightOriginx + 150 * 0.02 - 0.029, y: rightOriginy + 150 * 0.045 - 0.01, z: 0 }, { x: rotationx, y: rightInitialRotationz, z: 0 }, { x: 0.19, y: 0.19, z: 0.19 }, "hex");
          pendantArray.push(obj);
          // forth, two more big chains below
          obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx, y: originy - 0.09, z: 0 }, { x: rotationx, y: 0, z: rotationx }, { x: 1, y: 1, z: 1 }, "chain");
          pendantArray.push(obj);
          obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx, y: originy - 0.18, z: 0 }, { x: rotationx, y: 0, z: 0 }, { x: 1, y: 1, z: 1 }, "chain");
          pendantArray.push(obj);
          // update y to wherever chains led us
          let extraBuffer = 0.04;
          let yAxis = originy - 0.09 - 0.08 - extraBuffer;
          let dotY = 0.385;
          let chainY = 0.0475;
          let dashY = 0.485;
          let chainCompensationBuffer = 0.0075;
          messageArray.forEach((element) => {
            // find dict equiv
            thisComponent.glbArray.push(element.toUpperCase());
            equiv = this.morseDict[element.toLowerCase()];
            // if not null
            if (equiv) {
              let insertion = `<div class="morse-code__letter">`;
              //group insertions to reverse later for vertical consistency
              let insertionGroup = [];
              equiv = equiv.split("");
              equiv.forEach((chara) => {
                if (chara == ".") {
                  morseClass = "morse-code--dot";
                  morseHeight = "6px";
                  // insert dash for vertical consitency
                  yAxis -= dotY;
                  obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/dot_b.glb`, { x: originx, y: yAxis, z: 0 }, { x: rotationx, y: 0, z: 0 }, { x: 0.45, y: 0.45, z: 0.45 }, "gem");
                  pendantArray.push(obj);
                  yAxis -= dotY;
                  yAxis += chainCompensationBuffer;
                  for (let index = 0; index < 5; index++) {
                    let smallChainRotationx = index % 2 ? 1.566 : 0;
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx, y: yAxis, z: 0 }, { x: rotationx, y: 0, z: smallChainRotationx }, { x: 0.5, y: 0.5, z: 0.5 }, "chain");
                    pendantArray.push(obj);
                    if (index != 4) {
                      yAxis -= chainY;
                    }
                  }
                  yAxis += chainCompensationBuffer;
                } else {
                  morseClass = "morse-code--dash";
                  morseHeight = "16px";
                  // insert a dot for vertical consitency
                  yAxis -= dashY;
                  obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/dash_b.glb`, { x: originx, y: yAxis, z: 0 }, { x: rotationx, y: rotationx, z: 0 }, { x: 0.45, y: 0.45, z: 0.45 }, "gem");
                  pendantArray.push(obj);
                  yAxis -= dashY;
                  yAxis += chainCompensationBuffer;
                  for (let index = 0; index < 5; index++) {
                    let smallChainRotationx = index % 2 ? 1.566 : 0;
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx, y: yAxis, z: 0 }, { x: rotationx, y: 0, z: smallChainRotationx }, { x: 0.5, y: 0.5, z: 0.5 }, "chain");
                    pendantArray.push(obj);
                    if (index != 4) {
                      yAxis -= chainY;
                    }
                  }
                  yAxis += chainCompensationBuffer;
                }
                insertionGroup.push(`<div class="${morseClass}" style="height: ${morseHeight}"></div>`);
                //insertion += `<div class="${morseClass}" style="height: ${morseHeight}"></div>`;
              });
              insertionGroup.reverse();
              insertion += insertionGroup.join("");
              insertion += `</div>`;
              morseContainer.innerHTML += insertion;
            }
          });
          pendantArray.splice(-5);
          thisComponent.pendantArray = pendantArray;
        });
      },
      braceletChainOffset(signal) {
        console.log(signal);
        let offset = 0;
        if (signal == "dot") {
          offset = 0.325;
        } else if (signal == "dash") {
          offset = 0.42;
        }
        return offset;
      },
      amantiUpdateFinish(finish) {
        //let finish = e.target.value;
        let newPrices = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newPrices = newPrices[0].letters;
        this.prices = newPrices;
        this.activeFinish = this.finishes[finish];
        let thisComponent = this;
        let scene = this.$refs.scene.scene;
        scene.children.forEach((element) => {
          if (element.children.length != 0) {
            element.children.forEach((obj) => {
              obj.children.forEach((mesh) => {
                if (mesh.material != null) {
                  if (mesh.material.name == "Metal.001") {
                    mesh.material = new THREE.MeshStandardMaterial({
                      color: thisComponent.activeFinish,
                      metalness: 1,
                      roughness: 0.05,
                      name: "Metal.001",
                    });
                    mesh.updateMatrix();
                  }
                }
              });
            });
          }
        });
      },
      aquaearringUpdateFinish(e) {
        let finish = e.target.value;
        let newPrices = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newPrices = newPrices[0].letters;
        this.prices = newPrices;
        this.activeFinish = this.finishes[e.target.value];
        let thisComponent = this;
        let scene = this.$refs.scene.scene;
        let newMat = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "metal",
        });
        // groups
        scene.children.forEach((group) => {
          // has material?
          if (group.material) {
            if (group.material.name == "metal") {
              group.material = newMat;
              group.updateMatrix();
            }
          } else {
            // has children?
            if (group.children.length != 0) {
              // objects
              group.children.forEach((object) => {
                // has material?
                if (object.material) {
                  if (object.material.name == "metal") {
                    object.material = newMat;
                    object.updateMatrix();
                  }
                } else {
                  // has children?
                  if (object.children.length != 0) {
                    // components
                    object.children.forEach((comp) => {
                      // has material?
                      if (comp.material) {
                        if (comp.material.name == "metal") {
                          comp.material = newMat;
                          comp.updateMatrix();
                        }
                      }
                    });
                  }
                }
              });
            }
          }
        });
      },
      amantiUpdateMorse(e) {
        this.editableAmanti = false;
        this.placeholder = null;
        let morseContainer = document.getElementById("morseContainer");
        morseContainer.innerHTML = null;
        this.message = document.getElementById("messageInput").innerHTML;
        if (this.message === "") {
          this.placeholder = "Please enter your message";
        } else {
          this.placeholder = null;
        }
        // morse function
        let messageArray = this.message.split("");
        this.messageArray = messageArray;
        let equiv = null;
        let insertion = null;
        let morseClass = null;
        let morseHeight = null;
        let thisComponent = this;
        thisComponent.glbArray = [];
        thisComponent.$forceUpdate();
        thisComponent.$nextTick(() => {
          messageArray.forEach((element) => {
            // find dict equiv
            thisComponent.glbArray.push(element.toUpperCase());
            equiv = this.morseDict[element.toLowerCase()];
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
          thisComponent.editableAmanti = true;
          thisComponent.$nextTick(() => {
            // wait before you give it focus back
            setTimeout(function () {
              document.getElementById("messageInput").focus();
            }, 300);
            
          });
  
          // camera center of rotation fix
          // amanti
          if (this.key == "amanti") {
            //let cam = this.$refs.camera.camera;
            let orbitCtrl = this.$refs.renderer.three.cameraCtrl;
            window.orbitCtrl = orbitCtrl;
            // init cam pos
            let length = this.messageArray.length;
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
                thisComponent.fontSize = 2 - thisComponent.messageArray.length * 0.064;
                thisComponent.lineSpacing = 1.4 - thisComponent.messageArray.length * 0.075;
              } else {
                thisComponent.fontSize = 2;
                thisComponent.lineSpacing = 1.4;
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
            //cam.position.set(camy, camy, 10);
            //console.log(cam.position);
            //cam.position.set(0, 2.5, 2.5); // Set position like this
            //cam.lookAt(new THREE.Vector3(0, 0, 0));
          }
          if (thisComponent.key == "mayfair") {
            //let cam = this.$refs.camera.camera;
            let orbitCtrl = this.$refs.renderer.three.cameraCtrl;
            window.orbitCtrl = orbitCtrl;
            console.log(orbitCtrl);
            // obj at 1
            // init cam pos
            let length = this.messageArray.length;
            let cx = 8.4;
            let cy = 5.4;
            let cz = -4;
            let tx = 0.15;
            let ty = -0.64;
            let tz = -5.4;
            // set both camera pos and target as per length of messge
            orbitCtrl.object.position.set(cx - (length - 1) * 1, cy + (length - 1) * 0.33, cz + (length - 1) * 0.1);
            orbitCtrl.target.set(tx - (length - 1) * 0.1, ty + (length - 1) * 0.1, tz + (length - 1) * 0.4);
  
            thisComponent.$nextTick(() => {
              // if desktop no change
              if (window.innerWidth <= 600) {
                // if mobile reduce font size and letter spacing to tally with dots
                thisComponent.fontSize = 2 - thisComponent.messageArray.length * 0.064;
                thisComponent.lineSpacing = 1.4 - thisComponent.messageArray.length * 0.075;
              } else {
                thisComponent.fontSize = 2;
                thisComponent.lineSpacing = 1.4;
              }
            });
          }
        });
      },
      amantiValidateInput(e) {
        // disable enter bug
        if (e.which == 13) {
          return false;
        }
        let inputDiv = document.getElementById("messageInput");
        let textLength = inputDiv.innerText.length;
        let chLimit = this.obj.chLimit;
        let cond = textLength <= chLimit;
        // no funky input
        let char = e.key;
        let re = /^[a-zA-Z0-9]+$/;
        cond = cond && re.test(char);
        return cond;
      },
      earringsUpdateMorse(e) {
        this.placeholderLeft = null;
        this.placeholderRight = null;
        let morseContainerLeft = document.getElementById("morseContainerLeft");
        let morseContainerRight = document.getElementById("morseContainerRight");
        morseContainerLeft.innerHTML = null;
        morseContainerRight.innerHTML = null;
        this.messageLeft = document.getElementById("messageInputLeft").innerHTML;
        this.messageRight = document.getElementById("messageInputRight").innerHTML;
        if (this.messageLeft === "") {
          this.placeholderLeft = "Left";
        } else {
          this.placeholderLeft = null;
        }
        if (this.messageRight === "") {
          this.placeholderRight = "Right";
        } else {
          this.placeholderRight = null;
        }
        // morse function
        let messageArrayLeft = this.messageLeft.split("");
        let messageArrayRight = this.messageRight.split("");
        this.messageArrayLeft = messageArrayLeft;
        this.messageArrayRight = messageArrayRight;
        let equiv = null;
        let insertion = null;
        let morseClass = null;
        let morseHeight = null;
        let earringArray = [];
        let thisComponent = this;
        thisComponent.earringArray = [];
        thisComponent.glbArray = [];
        thisComponent.$forceUpdate();
        class glbObject {
          constructor(src, position, rotation, scale, type) {
            this.src = src;
            this.position = position;
            this.rotation = rotation;
            this.scale = scale;
            this.type = type;
          }
        }
        let originx = 0;
        let originy = 2;
        let angle = 1.566;
        let offset = 2;
        let leftYAxis = 0;
        let rightYAxis = 0;
        let studY = {
          dot: 0.9,
          dash: 1.12,
        };
        let gemY = {
          dot: 0.7,
          dash: 0.93,
        };
        let chainOffset = 0.18;
        let obj;
        let rotation;
        let equivRight;
        thisComponent.$nextTick(() => {
          // add stud for left if not empty
          if (messageArrayLeft.length != 0) {
            messageArrayLeft.forEach((element) => {
              // find dict equiv
              equiv = this.morseDict[element.toLowerCase()];
              // if not null
              if (equiv) {
                let insertion = `<div class="morse-code__letter">`;
                //group insertions to reverse later for vertical consistency
                let leftInsertionGroup = [];
                equiv = equiv.split("");
                for (let index = 0; index < equiv.length; index++) {
                  if (equiv[index] == ".") {
                    morseClass = "morse-code--dot";
                    morseHeight = "6px";
                  } else {
                    morseClass = "morse-code--dash";
                    morseHeight = "16px";
                  }
                  //insertion += `<div class="${morseClass}" style="height: ${morseHeight}"></div>`;
                  leftInsertionGroup.push(`<div class="${morseClass}" style="height: ${morseHeight}"></div>`);
                  let type = equiv[index] == "." ? "dot" : "dash";
                  // first element? add stud
                  if (index == 0) {
                    obj = new glbObject(`/static/src/glb/export/stud_${type}_b.glb`, { x: originx - offset, y: originy, z: 0 }, { x: angle, y: angle, z: 0 }, { x: 1, y: 1, z: 1 }, "stud");
                    earringArray.push(obj);
                    leftYAxis += studY[type];
                  } else {
                    // otherwise a gem and trail chains
                    leftYAxis += gemY[type];
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${type}_b.glb`, { x: originx - offset, y: originy - leftYAxis, z: 0 }, { x: angle, y: angle, z: 0 }, { x: 1, y: 1, z: 1 }, "gem");
                    earringArray.push(obj);
                    leftYAxis += gemY[type];
                    leftYAxis += chainOffset;
                  }
                  // add 5 trailing with conditions
                  let c1 = equiv.length != 1;
                  let c2 = index != equiv.length - 1;
                  if (c1 && c2) {
                    for (let j = 0; j < 5; j++) {
                      rotation = j % 2 ? angle : 0;
                      obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx - offset, y: originy - leftYAxis, z: 0 }, { x: angle, y: 0, z: rotation }, { x: 2, y: 2, z: 2 }, "chain");
                      earringArray.push(obj);
                      leftYAxis += chainOffset;
                    }
                  }
                }
                leftInsertionGroup.reverse();
                insertion += leftInsertionGroup.join("");
                insertion += `</div>`;
                morseContainerLeft.innerHTML += insertion;
              }
            });
          }
          if (messageArrayRight.length != 0) {
            messageArrayRight.forEach((element) => {
              // find dict equiv
              equivRight = this.morseDict[element.toLowerCase()];
              // if not null
              if (equivRight) {
                let insertionRight = `<div class="morse-code__letter">`;
                //group insertions to reverse later for vertical consistency
                let rightInsertionGroup = [];
                equivRight = equivRight.split("");
                for (let index = 0; index < equivRight.length; index++) {
                  if (equivRight[index] == ".") {
                    morseClass = "morse-code--dot";
                    morseHeight = "6px";
                  } else {
                    morseClass = "morse-code--dash";
                    morseHeight = "16px";
                  }
                  //insertion += `<div class="${morseClass}" style="height: ${morseHeight}"></div>`;
                  rightInsertionGroup.push(`<div class="${morseClass}" style="height: ${morseHeight}"></div>`);
                  let type = equivRight[index] == "." ? "dot" : "dash";
                  // first element? add stud
                  if (index == 0) {
                    obj = new glbObject(`/static/src/glb/export/stud_${type}_b.glb`, { x: originx + offset, y: originy, z: 0 }, { x: angle, y: angle, z: 0 }, { x: 1, y: 1, z: 1 }, "stud");
                    earringArray.push(obj);
                    //console.log(earringArray);
                    rightYAxis += studY[type];
                  } else {
                    // otherwise a gem and trail chains
                    rightYAxis += gemY[type];
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${type}_b.glb`, { x: originx + offset, y: originy - rightYAxis, z: 0 }, { x: angle, y: angle, z: 0 }, { x: 1, y: 1, z: 1 }, "gem");
                    earringArray.push(obj);
                    rightYAxis += gemY[type];
                    rightYAxis += chainOffset;
                  }
                  // add 5 trailing with conditions
                  let c1 = equivRight.length != 1;
                  let c2 = index != equivRight.length - 1;
                  if (c1 && c2) {
                    for (let j = 0; j < 5; j++) {
                      rotation = j % 2 ? angle : 0;
                      obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: originx + offset, y: originy - rightYAxis, z: 0 }, { x: angle, y: 0, z: rotation }, { x: 2, y: 2, z: 2 }, "chain");
                      earringArray.push(obj);
                      rightYAxis += chainOffset;
                    }
                  }
                }
                rightInsertionGroup.reverse();
                insertionRight += rightInsertionGroup.join("");
                insertionRight += `</div>`;
                morseContainerRight.innerHTML += insertionRight;
              }
            });
          }
          let merge = messageArrayLeft.concat(messageArrayRight);
          merge.sort();
          this.messageArray = merge;
          thisComponent.earringArray = earringArray;
        });
      },
      earringsValidateInputLeft(e) {
        let inputDivLeft = document.getElementById("messageInputLeft");
        let textLengthLeft = inputDivLeft.innerText.length;
        let chLimit = this.obj.chLimit;
        let cond = textLengthLeft <= chLimit;
        // no funky input
        let char = e.key;
        let re = /^[a-zA-Z0-9]+$/;
        cond = cond && re.test(char);
        return cond;
      },
      earringsValidateInputRight(e) {
        let inputDivRight = document.getElementById("messageInputRight");
        let textLengthRight = inputDivRight.innerText.length;
        let chLimit = this.obj.chLimit;
        let cond = textLengthRight <= chLimit;
        // no funky input
        let char = e.key;
        let re = /^[a-zA-Z0-9]+$/;
        cond = cond && re.test(char);
        return cond;
      },
      loadTexture(url) {
        const textureLoader = new THREE.TextureLoader();
        return new Promise((resolve, reject) => {
          textureLoader.load(url, resolve, undefined, reject);
        });
      },
      gem(name) {
        const diamondMaterial = new THREE.MeshPhysicalMaterial({
          color: 0xff00ff,
          clearcoat: 0,
          clearcoatRoughness: 0,
          ior: 2.1,
          reflectivity: 1,
          metalness: 0,
          roughness: 0,
          specularIntensity: 0.94,
          specularColor: 0xffeeaa,
          transmission: 0.7,
          name: name,
        });
        return diamondMaterial;
      },
      isActiveFinish(option) {
        //console.log(option)
        let activeOption = this.finishes[option];
        return activeOption == this.activeFinish;
      },
      isActiveSize(size) {
        return size == this.activeSize;
      },
      mayfairUpdateFinish(e) {
        let finish = e.target.value;
        let newPrices = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newPrices = newPrices[0].letters;
        this.prices = newPrices;
        this.activeFinish = this.finishes[e.target.value];
        let thisComponent = this;
        let scene = this.$refs.scene.scene;
        scene.children.forEach((element) => {
          if (element.children.length != 0) {
            element.children.forEach((obj) => {
              obj.children.forEach((mesh) => {
                if (mesh.material != null) {
                  if (mesh.material.name == "02 - Default") {
                    mesh.material = new THREE.MeshStandardMaterial({
                      color: thisComponent.activeFinish,
                      metalness: 1,
                      roughness: 0.05,
                      name: "02 - Default",
                    });
                    mesh.updateMatrix();
                  }
                }
              });
            });
          }
        });
      },
      metalDiff(metal) {
        let thisComponent = this;
        // is it the active Finish?
        if (thisComponent.finishes[metal] == thisComponent.activeFinish) {
          return "";
        } else {
          const data = thisComponent.db[document.getElementById("app").attributes.key.nodeValue];
          if (data) {
            let prices;
            data.options.forEach((option) => {
              if (option.text == metal) {
                prices = option;
              }
            });
            prices = prices.letters;
            let total = 0;
            thisComponent.messageArray.forEach((e) => {
              total += prices[e.toUpperCase()];
            });
            let diff = parseInt(thisComponent.total()) - parseInt(total);
            let signal = "";
            if (diff < 0) {
              signal = "+";
            }
            if (diff > 0) {
              signal = "-";
            }
            return signal + " £" + Math.abs(diff);
          } else {
            return "";
          }
        }
      },
      mobileModalClose() {
        this.mobileModalVisible = false;
        this.optionActive = null;
      },
      necklaceLoad(e, comp) {
        let thisComponent = this;
        const metal = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "metal",
        });
        const gem = new THREE.MeshPhysicalMaterial({
          color: 0x002211,
          clearcoat: 0,
          clearcoatRoughness: 0,
          ior: 2.1,
          reflectivity: 1,
          metalness: 0,
          roughness: 0,
          specularIntensity: 0.94,
          specularColor: 0xffeeaa,
          transmission: 0.7,
          name: "gem",
        });
        let type = comp.type;
        if (type == "spacer") {
          let elements = e.scene.children[0].children;
          elements.forEach((element) => {
            if (element.material.name == "metal" || element.material.name == "metal.003" || element.material.name == "metal.001") {
              element.material = metal;
            } else if (element.material.name == "gem") {
              element.material = gem;
            }
          });
        } else if (type == "chain" || type == "bigchain") {
          let chain = e.scene.children[0];
          chain.material = metal;
        } else if (type == "dot" || type == "dash") {
          let name = e.scene.children[0].name;
          if (name == "RD" || name == "OB") {
            let elements = e.scene.children[0].children;
            elements.forEach((element) => {
              if (element.material.name == "chain") {
                element.material = metal;
              } else if (element.material.name == "jewel") {
                element.material = gem;
              }
            });
          }
        } else if (type == "hex" || type == "clasp") {
          let elements = e.scene.children[0].children;
          elements.forEach((element) => {
            element.material = metal;
          });
        }
      },
      necklaceUpdateFinish(e) {
        let finish = e.target.value;
        let newOptions = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newOptions = newOptions[0];
        this.necklacePrices = newOptions;
        this.activeFinish = this.finishes[e.target.value];
        let thisComponent = this;
        console.log(thisComponent.activeFinish);
        let scene = this.$refs.scene.scene;
        let newMat = new THREE.MeshStandardMaterial({
          color: thisComponent.activeFinish,
          metalness: 1,
          roughness: 0.05,
          name: "metal",
        });
        // groups
        scene.children.forEach((group) => {
          // has material?
          if (group.material) {
            if (group.material.name == "metal") {
              group.material = newMat;
              group.updateMatrix();
            }
          } else {
            // has children?
            if (group.children.length != 0) {
              // objects
              group.children.forEach((object) => {
                // has material?
                if (object.material) {
                  if (object.material.name == "metal") {
                    object.material = newMat;
                    object.updateMatrix();
                  }
                } else {
                  // has children?
                  if (object.children.length != 0) {
                    // components
                    object.children.forEach((comp) => {
                      // has material?
                      if (comp.material) {
                        if (comp.material.name == "metal") {
                          comp.material = newMat;
                          comp.updateMatrix();
                        }
                      }
                    });
                  }
                }
              });
            }
          }
        });
      },
      necklaceUpdateMorse(e) {
        // disable input
        this.placeholder = null;
        let morseContainer = document.getElementById("morseContainer");
        morseContainer.innerHTML = null;
        this.message = document.getElementById("messageInput").innerHTML;
        if (this.message === "") {
          this.placeholder = "Please enter your message";
        } else {
          this.placeholder = null;
        }
        // morse function
        // space management for necklace
        // detect spaces in a string and remove them
        // this for total calculation and 3D
        let cleanedMessage = this.message.replace(/&nbsp;| +/g, "");
        // this is for the hidden more class
        let replacedMessage = this.message.replace(/&nbsp;| +/g, "&");
        //console.log(replacedMessage);
        let messageArray = cleanedMessage.split("");
        let replacedArray = replacedMessage.split("");
        this.messageArray = messageArray;
        let equiv = null;
        let insertion = null;
        let morseClass = null;
        let morseHeight = null;
        let thisComponent = this;
        thisComponent.glbArray = [];
        thisComponent.necklaceArray = [];
        thisComponent.$forceUpdate();
        thisComponent.$nextTick(() => {
          replacedArray.forEach((element) => {
            //console.log(element);
            // find dict equiv
            //thisComponent.glbArray.push(element.toUpperCase());
            // if not &
            if (element != "&") {
              equiv = this.morseDict[element.toLowerCase()];
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
            } else {
              let insertion = `<div class="morse-code__letter">`;
              morseClass = "morse-code--dot cbe-dot-bg-override";
              morseHeight = "6px";
              insertion += `<div class="${morseClass}" style="height: ${morseHeight}"></div>`;
              insertion += `</div>`;
              morseContainer.innerHTML += insertion;
            }
          });
          // update spacers
          thisComponent.spacers = [];
          thisComponent.hexagons = [];
          let totalSpaces = replacedMessage.split("").filter((c) => c === "&").length;
          let totalWords = totalSpaces + 1;
          let totalLetters = cleanedMessage.split("").length;
          let spacerCount = totalLetters - totalWords;
          //console.log(totalLetters, totalWords, spacerCount);
          for (let index = 0; index < spacerCount; index++) {
            thisComponent.spacers.push("spacer");
          }
          for (let index = 0; index < totalWords; index++) {
            thisComponent.hexagons.push("hexagon");
          }
          // 3D attempt B ###########################################################///////////////////////////////////////////////##############################
          // parametric coords
          let xcoords = function (i) {
            return (3 + 1.5 * Math.cos(i)) * Math.sin(i);
          };
          let ycoords = function (i) {
            return (5 + Math.cos(i)) * Math.cos(i);
          };
          // set curve center to 0,0
          let scene = this.$refs.scene.scene;
          // Create a spline curve
          //let points = [];
          let leftPoints = [];
          let rightPoints = [];
          for (let i = 19; i >= 1; i--) {
            leftPoints.push(new THREE.Vector3(xcoords((-Math.PI / 19) * i), ycoords((-Math.PI / 19) * i), 0));
          }
          for (let i = 0; i <= 18; i++) {
            rightPoints.push(new THREE.Vector3(xcoords(-Math.PI * (i / 19) - Math.PI), ycoords(-Math.PI * (i / 19) - Math.PI)));
          }
          //const spline = new THREE.CatmullRomCurve3(points);
          let leftSpline = new THREE.CatmullRomCurve3(leftPoints);
          let rightSpline = new THREE.CatmullRomCurve3(rightPoints);
          //let leftCurveGeometry = new THREE.BufferGeometry().setFromPoints(leftSpline.getPoints(40));
          //let rightCurveGeometry = new THREE.BufferGeometry().setFromPoints(rightSpline.getPoints(40));
          //let curveMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
          //let leftCurve = new THREE.Line(leftCurveGeometry, curveMaterial);
          //let rightCurve = new THREE.Line(rightCurveGeometry, curveMaterial);
          //scene.add(leftCurve);
          //scene.add(rightCurve);
          // build the whole array
          // count the stones and place them in the middle
          let necklaceObjectsArray = ["hex"];
          let morse;
          let morseKeys = {
            ".": "dot",
            "-": "dash",
          };
          // First modify replaceArray to abstract 3d Array
          for (let index = 0; index < replacedArray.length; index++) {
            // is it a space?
            if (replacedArray[index] == "&") {
              necklaceObjectsArray.push("hex");
            } else {
              // then it's a letter
              // morse it
              morse = thisComponent.morseDict[replacedArray[index].toLowerCase()];
              // if no error or something
              if (morse) {
                // explode string
                morse = morse.split("");
                morse.forEach((element) => {
                  necklaceObjectsArray.push(morseKeys[element]);
                });
                // is this the last index?
                if (index + 1 == replacedArray.length) {
                  // add final hex
                  necklaceObjectsArray.push("hex");
                } else if (replacedArray[index + 1] != "&") {
                  // is the next one not a space?
                  // add a spacer
                  necklaceObjectsArray.push("spacer");
                }
              }
            }
          }
          /// Finish build the stones part
          // split
          let objCenter;
          let leftArray;
          let rightArray;
          if (necklaceObjectsArray.length % 2 == 0) {
            objCenter = "chain";
            leftArray = necklaceObjectsArray.slice(0, necklaceObjectsArray.length / 2);
            rightArray = necklaceObjectsArray.slice(necklaceObjectsArray.length / 2);
          } else {
            // find the center
            objCenter = necklaceObjectsArray[(necklaceObjectsArray.length - 1) / 2 + 1];
            leftArray = necklaceObjectsArray.slice(0, (necklaceObjectsArray.length - 1) / 2);
            rightArray = necklaceObjectsArray.slice((necklaceObjectsArray.length - 1) / 2 + 1);
          }
  
          let bigchainScaleFactor = 0.75;
          let chainScaleFactor = 0.5;
          let claspScaleFactor = 0.135;
          let dotScaleFactor = 0.2;
          let dashScaleFactor = 0.2;
          let hexScaleFactor = 0.2;
          let spacerScaleFactor = 0.2;
          let scales = {
            bigchain: { x: bigchainScaleFactor, y: bigchainScaleFactor, z: bigchainScaleFactor },
            chain: { x: chainScaleFactor, y: chainScaleFactor, z: chainScaleFactor },
            clasp: { x: claspScaleFactor, y: claspScaleFactor, z: claspScaleFactor },
            dot: { x: dotScaleFactor, y: dotScaleFactor, z: dotScaleFactor },
            dash: { x: dashScaleFactor, y: dashScaleFactor, z: dashScaleFactor },
            hex: { x: hexScaleFactor, y: hexScaleFactor, z: hexScaleFactor },
            spacer: { x: spacerScaleFactor, y: spacerScaleFactor, z: spacerScaleFactor },
          };
          // leftSide
          let leftFinal = [];
          let rightFinal = [];
          // lengths object
          leftArray = leftArray.reverse();
          for (let index = 0; index < leftArray.length; index++) {
            if (index + 1 == leftArray.length && objCenter == "chain") {
              leftFinal.push("chainr");
              rightFinal.push("chainr");
              leftFinal.push("chain");
              rightFinal.push("chain");
            } else {
              leftFinal.push("chain");
              leftFinal.push("chainr");
              leftFinal.push("chain");
              leftFinal.push("chainr");
              leftFinal.push("chain");
              rightFinal.push("chain");
              rightFinal.push("chainr");
              rightFinal.push("chain");
              rightFinal.push("chainr");
              rightFinal.push("chain");
            }
            leftFinal.push(leftArray[index]);
            rightFinal.push(rightArray[index]);
          }
          let endchains = [];
          let endchainsRight = [];
          let lengths = {
            bigchain: 0.05,
            clasp: 0.175,
            chain: 0.035,
            chainr: 0.035,
            dot: 0.3,
            dash: 0.4,
            hex: 0.335,
            spacer: 0.18,
          };
          // calcualte length
          let leftLength = 0;
          leftFinal.forEach((e) => {
            leftLength += lengths[e];
          });
          let rightLength = 0;
          rightFinal.forEach((e) => {
            rightLength += lengths[e];
          });
  
          let leftNumber = parseInt((11 - leftLength) * 18);
          if (leftNumber % 2 != 0) {
            leftNumber += 1;
          }
          let rightNumber = parseInt((11 - rightLength) * 18);
          if (rightNumber % 2 == 0) {
            rightNumber += 1;
          }
          for (let index = 0; index < leftNumber; index++) {
            let push = index % 2 ? "chainr" : "chain";
            endchains.push(push);
          }
          for (let index = 0; index < rightNumber; index++) {
            let push = index % 2 ? "chainr" : "chain";
            endchainsRight.push(push);
          }
          endchains.push("bigchain");
          endchainsRight.push("clasp");
          leftFinal = leftFinal.concat(endchains);
          rightFinal = rightFinal.concat(endchainsRight);
          class glbObject {
            constructor(src, position, rotation, scale, type) {
              this.src = src;
              this.position = position;
              this.rotation = rotation;
              this.scale = scale;
              this.type = type;
            }
          }
          let objx;
          let finalObjectsArray = [];
          // dash: 0.6395270045548216
          // dash: 0.49573299288749695
          let splineLength = leftSpline.getLength();
          function getClosestT(spline, point, step = 0.001) {
            let closestT = 0;
            let closestDistance = Infinity;
            for (let t = 0; t <= 1; t += step) {
              const currentPosition = spline.getPointAt(t);
              const distance = currentPosition.distanceTo(point);
              if (distance < closestDistance) {
                closestDistance = distance;
                closestT = t;
              }
            }
            return closestT;
          }
          // Function to get the next position along the spline with the desired distance from the starting point
          function getNextPosition(spline, startPoint, distance, step = 0.001) {
            let currentPosition = startPoint.clone();
            let currentT = getClosestT(spline, startPoint, step);
            while (currentPosition.distanceTo(startPoint) < distance && currentT <= 1) {
              currentT += step;
              currentPosition = spline.getPointAt(currentT);
            }
            return currentPosition;
          }
          let pos = leftSpline.getPointAt(0);
          objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${objCenter}_b.glb`, pos, { x: 1.566, y: 0, z: 0 }, scales[objCenter], objCenter);
          finalObjectsArray.push(objx);
          //thisComponent.necklaceArray = finalObjectsArray;
          //console.log(scene);
          //return;
          pos = getNextPosition(leftSpline, pos, lengths[objCenter] / 2);
          let t;
          //leftFinal = ['dash', 'dash', 'dash'];
          for (let index = 0; index < leftFinal.length; index++) {
            if (leftFinal[index] == "chainr") {
              pos = getNextPosition(leftSpline, pos, lengths["chain"] / 2);
            } else {
              pos = getNextPosition(leftSpline, pos, lengths[leftFinal[index]] / 2);
            }
            t = getClosestT(leftSpline, pos);
            const tangent = leftSpline.getTangentAt(t);
            const modelForward = new THREE.Vector3(0, 0, 1);
            const quaternion = new THREE.Quaternion();
            quaternion.setFromUnitVectors(modelForward, tangent);
            const eulerRotation = new THREE.Euler();
            eulerRotation.setFromQuaternion(quaternion);
            if (leftFinal[index] == "chainr") {
              objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, pos, { x: 1.566, y: -eulerRotation.y, z: 1.566 }, scales["chain"], "chain");
            } else {
              if (leftFinal[index] == "bigchain") {
                objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, pos, { x: 1.566, y: -eulerRotation.y + 1.566, z: 0 }, scales[leftFinal[index]], leftFinal[index]);
              } else {
                objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${leftFinal[index]}_b.glb`, pos, { x: 1.566, y: -eulerRotation.y + 1.566, z: 0 }, scales[leftFinal[index]], leftFinal[index]);
              }
            }
            finalObjectsArray.push(objx);
            if (leftFinal[index] == "chainr") {
              pos = getNextPosition(leftSpline, pos, lengths["chain"] / 2);
            } else {
              pos = getNextPosition(leftSpline, pos, lengths[leftFinal[index]] / 2);
            }
          }
          // Right Side
          let posRight = rightSpline.getPointAt(0);
          posRight = getNextPosition(rightSpline, posRight, lengths[objCenter] / 2);
          let tRight;
          for (let index = 0; index < rightFinal.length; index++) {
            if (rightFinal[index] == "chainr") {
              posRight = getNextPosition(rightSpline, posRight, lengths["chain"] / 2);
            } else if (rightFinal[index] == "clasp") {
              posRight = getNextPosition(rightSpline, posRight, lengths[rightFinal[index]] / 2);
              posRight.x -= 0.015;
            } else {
              posRight = getNextPosition(rightSpline, posRight, lengths[rightFinal[index]] / 2);
            }
            tRight = getClosestT(rightSpline, posRight);
            const tangentRight = rightSpline.getTangentAt(tRight);
            const modelForwardRight = new THREE.Vector3(0, 0, 1);
            const quaternionRight = new THREE.Quaternion();
            quaternionRight.setFromUnitVectors(modelForwardRight, tangentRight);
            const eulerRotationRight = new THREE.Euler();
            eulerRotationRight.setFromQuaternion(quaternionRight);
            if (rightFinal[index] == "chainr") {
              objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, posRight, { x: 1.566, y: -eulerRotationRight.y, z: 1.566 }, scales["chain"], "chain");
            } else {
              if (rightFinal[index] == "bigchain") {
                objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, posRight, { x: 1.566, y: -eulerRotationRight.y + 1.566, z: 0 }, scales[rightFinal[index]], rightFinal[index]);
              } else {
                objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${rightFinal[index]}_b.glb`, posRight, { x: 1.566, y: -eulerRotationRight.y + 1.566, z: 0 }, scales[rightFinal[index]], rightFinal[index]);
              }
            }
            finalObjectsArray.push(objx);
            if (rightFinal[index] == "chainr") {
              posRight = getNextPosition(rightSpline, posRight, lengths["chain"] / 2);
            } else {
              posRight = getNextPosition(rightSpline, posRight, lengths[rightFinal[index]] / 2);
            }
          }
          //12.246585034288717
          //console.log(scene);
          /*
          endchains.forEach(c => {
            tx = leftSpline.getUtoTmapping(currentArcLength/splineLength);
            //tx = currentPos / splineLength;
            objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, leftSpline.getPointAt(tx), { x: 1.566, y: 0, z: 0 }, scales['chain'], 'chain');
            finalObjectsArray.push(objx);
            currentArcLength += 2*lengths['chain'];
          })
          */
          /*
          for (let i = 0; i < leftFinal.length; i++) {
            tx = currentPos / splineLength;
            objx = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${leftFinal[i]}_b.glb`, leftSpline.getPoint(tx), { x: 1.566, y: 0, z: 0 }, scales[leftFinal[i]], leftFinal[i]);
            finalObjectsArray.push(objx);
            currentPos += 0.1;
  
          }*/
          thisComponent.necklaceArray = finalObjectsArray;
          thisComponent.$nextTick(() => {
            console.log(scene);
          });
  
          return;
  
          // Create a geometry to visualize the spline
          //const curveGeometry = new THREE.BufferGeometry().setFromPoints(spline.getPoints(50));
          //const curveMaterial = new THREE.LineBasicMaterial({ color: 0xff0000 });
          //const curve = new THREE.Line(curveGeometry, curveMaterial);
          //scene.add(curve);
          /*
          let nArray = [];
          // Position objects along the spline curve and align their rotation
          const upV = new THREE.Vector3(0, 1, 0); // Assuming Y-axis is up
          const fV = new THREE.Vector3();
          let oblx;
          let currentLengthx = 0;
          let tx;
          let ro;
          let tangenx;
  
  
          let totalLengthx = 3;
          for (let k = 0; k < 30; k++) {
            tx = currentLengthx / totalLengthx;
            oblx = new glbObject("/static/src/glb/aquafiore_bracelet/export/dash_b.glb", spline.getPoint(tx), { x: 1.566, y: 0, z: 0 }, scales["dot"], "dot");
            nArray.push(oblx);
            currentLengthx += 0.05;
          }
          thisComponent.necklaceArray = nArray;
          return;
          // Create random-sized spheres and calculate their total length
          const numObjects = 10;
          const sizes = [];
          const totalLength = numObjects * 0.1; // Start with a base sphere size of 0.1
  
          for (let i = 0; i < numObjects; i++) {
            const size = 0.1 + Math.random() * 0.15; // Random size between 0.1 and 0.25
            sizes.push(size);
          }
  
          // Position objects along the spline curve and align their rotation
          const upVector = new THREE.Vector3(0, 1, 0); // Assuming Y-axis is up
          const forwardVector = new THREE.Vector3();
  
          let currentLength = 0;
  
          for (let i = 0; i < numObjects; i++) {
            const sphereGeometry = new THREE.SphereGeometry(sizes[i], 32, 32);
            const sphereMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
            const sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);
  
            // Calculate the position based on the total length and current length
            const t = currentLength / totalLength;
            const position = spline.getPoint(t);
            sphere.position.copy(position);
  
            // Compute the forward direction by using the tangent vector
            const tangent = spline.getTangent(t);
            forwardVector.copy(tangent).normalize();
  
            // Align the object's rotation with the forward direction
            sphere.quaternion.setFromUnitVectors(upVector, forwardVector);
            console.log(sphere);
  
            scene.add(sphere);
  
            // Update current length for the next object
            currentLength += sizes[i] * 2; // Multiply by 2 since diameter = radius * 2
          }
  
          return;
          // 3D Work (additional loop cost wise is ok instead of tinkering with working morse characters)###################################################
          // array of necklace abstract elements
          let necklaceObjectsArray = ["hex"];
          // array to hold actual glb elements
          let necklaceArray = [];
          // parametric coords
          let xcoord = function (i) {
            return (3 + 1.5 * Math.cos(i)) * Math.sin(i);
          };
          let ycoord = function (i) {
            return (5 + Math.cos(i)) * Math.cos(i);
          };
          // set curve center to 0,0
          let originx = xcoord(Math.PI);
          let originy = ycoord(Math.PI);
          let morse;
          let morseKeys = {
            ".": "dot",
            "-": "dash",
          };
          // First modify replaceArray to abstract 3d Array
          for (let index = 0; index < replacedArray.length; index++) {
            // is it a space?
            if (replacedArray[index] == "&") {
              necklaceObjectsArray.push("hex");
            } else {
              // then it's a letter
              // morse it
              morse = thisComponent.morseDict[replacedArray[index].toLowerCase()];
              // if no error or something
              if (morse) {
                // explode string
                morse = morse.split("");
                morse.forEach((element) => {
                  necklaceObjectsArray.push(morseKeys[element]);
                });
                // is this the last index?
                if (index + 1 == replacedArray.length) {
                  // add final hex
                  necklaceObjectsArray.push("hex");
                } else if (replacedArray[index + 1] != "&") {
                  // is the next one not a space?
                  // add a spacer
                  necklaceObjectsArray.push("spacer");
                }
              }
            }
          }
          // find the array center
          //console.log(necklaceObjectsArray);
          //console.log(necklaceObjectsArray.length);
          let objCenter;
          let leftArray;
          let rightArray;
          if (necklaceObjectsArray.length % 2 == 0) {
            objCenter = "chain";
            leftArray = necklaceObjectsArray.slice(0, necklaceObjectsArray.length / 2);
            rightArray = necklaceObjectsArray.slice(necklaceObjectsArray.length / 2);
          } else {
            // find the center
            objCenter = necklaceObjectsArray[(necklaceObjectsArray.length - 1) / 2 + 1];
            leftArray = necklaceObjectsArray.slice(0, (necklaceObjectsArray.length - 1) / 2);
            rightArray = necklaceObjectsArray.slice((necklaceObjectsArray.length - 1) / 2 + 1);
          }
          // reverse Left Array to go backwards in 3d
          leftArray = leftArray.reverse();
          //console.log(objCenter);
          //console.log(leftArray);
          //console.log(rightArray);
  
          let t = -Math.PI;
          let b = -Math.PI;
          let obl;
          let obr;
          let xR;
          let yR;
          let zR;
          let offsets = {
            chain: 0,
            dash: 0.12,
            dot: 0.05,
            hex: 0.1,
            spacer: 0.05,
          };
          let ys = {
            chain: 0.01,
            dash: 0.025,
            dot: 0.05,
            hex: 0.0175,
            spacer: 0.0125,
          };
          objCenter = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${objCenter}_b.glb`, { x: xcoord(t), y: ycoord(t) + ys[objCenter], z: 0 }, { x: 1.566, y: 0, z: 0 }, scales[objCenter], objCenter);
          necklaceArray.push(objCenter);
          // if center object is a chain add two chains
          if (objCenter.type == "chain") {
            for (let index = 0; index < 2; index++) {
              t += 0.03;
              b -= 0.03;
              xR = index % 2 ? 1.566 : 0;
              obl = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(t), y: ycoord(t), z: 0 }, { x: xR, y: 0, z: 0 }, scales["chain"], "chain");
              necklaceArray.push(obl);
              obr = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(b), y: ycoord(b), z: 0 }, { x: xR, y: 0, z: 0 }, scales["chain"], "chain");
              necklaceArray.push(obr);
            }
          } else {
            // offset
            t += offsets[objCenter.type];
            b -= offsets[objCenter.type];
            // add five chains
            for (let index = 0; index < 5; index++) {
              t += 0.0275;
              b -= 0.0275;
              xR = index % 2 ? 0 : 1.566;
              zR = index % 2 ? 0.1 + 0.1 * index : 0;
              obl = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(t), y: ycoord(t), z: 0 }, { x: xR, y: 0, z: -zR }, scales["chain"], "chain");
              necklaceArray.push(obl);
              obr = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(b), y: ycoord(b), z: 0 }, { x: xR, y: 0, z: +zR }, scales["chain"], "chain");
              necklaceArray.push(obr);
            }
          }
          for (let index = 0; index < leftArray.length; index++) {
            t += offsets[leftArray[index]] * (Math.abs(Math.PI / 2 - Math.abs(t)) * 0.5);
            b -= offsets[rightArray[index]];
            yR = (Math.PI + t) * 1.566 - 0.2 * index;
            obl = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${leftArray[index]}_b.glb`, { x: xcoord(t), y: ycoord(t), z: 0 }, { x: 1.566, y: -yR, z: 0 }, scales[leftArray[index]], leftArray[index]);
            necklaceArray.push(obl);
            obr = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${rightArray[index]}_b.glb`, { x: xcoord(b), y: ycoord(b), z: 0 }, { x: 1.566, y: yR, z: 0 }, scales[rightArray[index]], rightArray[index]);
            necklaceArray.push(obr);
            // push center again exponentially
            t += offsets[leftArray[index]] * (Math.abs(Math.PI / 2 - Math.abs(t)) * 0.5);
            b -= offsets[rightArray[index]];
            // add 5 chains left / right
            for (let j = 0; j < 5; j++) {
              xR = j % 2 ? 0 : 1.566;
              zR = j % 2 ? 0.1 + 0.1 * j : 0;
              obl = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(t), y: ycoord(t), z: 0 }, { x: xR, y: 0, z: -zR }, scales["chain"], "chain");
              necklaceArray.push(obl);
              obr = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(b), y: ycoord(b), z: 0 }, { x: xR, y: 0, z: zR }, scales["chain"], "chain");
              necklaceArray.push(obr);
              t += 0.0275;
              b -= 0.0275;
            }
          }
          let counter = leftArray.length;
          while (t <= -0.1) {
            t += 0.0275;
            b -= 0.0275;
            xR = counter % 2 ? 0 : 1.566;
            zR = counter % 2 ? 0.1 + 0.1 * counter : 0;
            obl = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(t), y: ycoord(t), z: 0 }, { x: 1.566, y: 0, z: 0 }, scales["chain"], "chain");
            necklaceArray.push(obl);
            obr = new glbObject("/static/src/glb/aquafiore_bracelet/export/chain_b.glb", { x: xcoord(b), y: ycoord(b), z: 0 }, { x: xR, y: 0, z: +zR }, scales["chain"], "chain");
            necklaceArray.push(obr);
          }
          thisComponent.necklaceArray = necklaceArray;
          return;
          // object to store possible previous ends from middle object
          let previousEnds = {
            chain: { x: xcoord(-Math.PI + 0.025), y: ycoord(-Math.PI), z: 0 },
            dot: { x: xcoord(-Math.PI + 0.122), y: ycoord(-Math.PI), z: 0 },
            dash: { x: xcoord(-Math.PI + 0.1525), y: ycoord(-Math.PI), z: 0 },
            hex: { x: xcoord(-Math.PI + 0.1525), y: ycoord(-Math.PI), z: 0 },
            spacer: { x: xcoord(-Math.PI + 0.1525), y: ycoord(-Math.PI), z: 0 },
          };
          let nextEnds = {
            chain: { x: xcoord(-Math.PI - 0.025), y: ycoord(-Math.PI), z: 0 },
            dot: { x: xcoord(-Math.PI - 0.122), y: ycoord(-Math.PI), z: 0 },
            dash: { x: xcoord(-Math.PI - 0.1525), y: ycoord(-Math.PI), z: 0 },
            hex: { x: xcoord(-Math.PI - 0.1525), y: ycoord(-Math.PI), z: 0 },
            spacer: { x: xcoord(-Math.PI - 0.1525), y: ycoord(-Math.PI), z: 0 },
          };
  
          // center object
          if (objCenter == "chain") {
            objCenter = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${objCenter}_b.glb`, { x: xcoord(-Math.PI), y: ycoord(-Math.PI), z: 0 }, { x: 1.566, y: 0, z: 0 }, scales[objCenter], objCenter);
            necklaceArray.push(objCenter);
          } else {
            objCenter = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${objCenter}_b.glb`, { x: xcoord(-Math.PI), y: ycoord(-Math.PI), z: 0 }, { x: 1.566, y: 0, z: 0 }, scales[objCenter], objCenter);
            necklaceArray.push(objCenter);
          }
          // left array
          let obj;
          let rotationZ;
          let chainRotationX;
          let chainRotationZ;
          let xdeltaLeft = 0;
          let ydeltaLeft = ycoord(-Math.PI);
          let elementRotationY;
          let halfCurves = {
            chain: {
              x: 0.22,
              y: 0.24,
            },
            dash: {
              x: 0.195,
              y: 0.24,
            },
            dot: {
              x: 0.22,
              y: 0.24,
            },
            hex: {
              x: 0.24,
              y: 0.24,
            },
            spacer: {
              x: 0.24,
              y: 0.24,
            },
          };
          for (let index = 0; index < leftArray.length; index++) {
            // if it is the first item in the array
            if (index == 0) {
              // if the middle element is not the set of chains we need 5 chains
              if (objCenter.type != "chain") {
                for (let j = 0; j < 5; j++) {
                  // the first chain must start at the end of the middle
                  if (j == 0) {
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, previousEnds[objCenter.type], { x: 1.566, y: 0, z: 0 }, scales["chain"], "chain");
                    necklaceArray.push(obj);
                    // RightSide
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, nextEnds[objCenter.type], { x: 1.566, y: 0, z: 0 }, scales["chain"], "chain");
                    necklaceArray.push(obj);
                  } else {
                    rotationZ = -0.4 - j * 0.05;
                    //console.log(rotationZ, ycoord(Math.PI + j / 2));
                    chainRotationX = j % 2 ? 0 : 1.566;
                    chainRotationZ = j % 2 ? rotationZ : 0;
                    //rotationj = 1.566-ycoord(Math.PI*j/2);
                    //chainRotation = j % 2 ? 0 : rotationj;
                    //console.log(chainRotation);
                    //chainRotation = 1.566;
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: xcoord(-Math.PI + (j * 0.09) / Math.PI) + previousEnds[objCenter.type].x, y: ycoord(-Math.PI + (j * 0.3) / (Math.PI + j * 0.6)), z: 0 }, { x: chainRotationX, y: 0, z: chainRotationZ }, scales["chain"], "chain");
                    necklaceArray.push(obj);
                    xdeltaLeft = xcoord(-Math.PI + (j * 0.09) / Math.PI) + previousEnds[objCenter.type].x;
                    ydeltaLeft = ycoord(-Math.PI + (j * 0.3) / (Math.PI + j * 0.6));
                    // Right side
                    obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: xcoord(-Math.PI - (j * 0.09) / Math.PI) + nextEnds[objCenter.type].x, y: ycoord(-Math.PI + (j * 0.3) / (Math.PI + j * 0.6)), z: 0 }, { x: chainRotationX, y: 0, z: -chainRotationZ }, scales["chain"], "chain");
                    necklaceArray.push(obj);
                  }
                }
              } else if (objCenter.type == "chain") {
                // if even and the center is the five chains
                // render the left and right 4 (5-1) chains
                for (let k = 0; k < 2; k++) {
                  //left
                  rotationZ = -0.4 - k * 0.05;
                  chainRotationX = k % 2 ? 1.566 : 0;
                  chainRotationZ = k % 2 ? 0 : rotationZ;
                  obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: xcoord(-Math.PI + (k * 0.09) / Math.PI) + previousEnds[objCenter.type].x, y: ycoord(-Math.PI + (k * 0.3) / (Math.PI + k * 0.6)), z: 0 }, { x: chainRotationX, y: 0, z: chainRotationZ }, scales["chain"], "chain");
                  necklaceArray.push(obj);
                  xdeltaLeft = xcoord(-Math.PI - (k * 0.09) / Math.PI)+previousEnds[objCenter.type].x;
                  ydeltaLeft = ycoord(-Math.PI + (k * 0.3) / (Math.PI + k * 0.6));
                  //right
                  obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: xcoord(-Math.PI - (k * 0.09) / Math.PI) + nextEnds[objCenter.type].x, y: ycoord(-Math.PI + (k * 0.3) / (Math.PI + k * 0.6)), z: 0 }, { x: chainRotationX, y: 0, z: -chainRotationZ }, scales["chain"], "chain");
                  necklaceArray.push(obj);
                }
              }
            }
  
            // then we start rendering
            // render element
            // left side
            // move the center half the element
            //xdeltaLeft -= halfCurves[leftArray[index]].x;
            xdeltaLeft = xcoord(-Math.PI + (index + 1) * 0.05);
            // move along the y axis
            ydeltaLeft = ycoord(-Math.PI + ((index + 1) * 1.35) / (Math.PI + (index + 1) * 0.6));
            // get rotation right
            elementRotationY = (index + 1) * -0.6;
            obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/${leftArray[index]}_b.glb`, { x: xdeltaLeft, y: ydeltaLeft, z: 0 }, { x: 1.566, y: elementRotationY, z: 0 }, scales[leftArray[index]], leftArray[index]);
            necklaceArray.push(obj);
          }
  
          // add final closing hex to abstract array
  
          /*
          for (let index = 0; index < 33; index++) {
            obj = new glbObject(`/static/src/glb/aquafiore_bracelet/export/chain_b.glb`, { x: xcoord(index / 10), y: ycoord(index / 10), z: 0 }, { x: 0, y: 0, z: 0 }, { x: 1, y: 1, z: 1 }, "chain");
            necklaceArray.push(obj);
          }
  
          thisComponent.necklaceArray = necklaceArray;
          thisComponent.$nextTick(() => {
            // enable input
          });
          */
        });
  
        //console.log(messageArray);
        //console.log(e)
      },
      necklaceValidateInput(e) {
        let inputDiv = document.getElementById("messageInput");
        let textLength = inputDiv.innerText.length;
        let chLimit = this.obj.chLimit;
        let cond = textLength <= chLimit;
        // no funky input
        let char = e.key;
        let re = /^[a-zA-Z0-9\s]+$/;
        // number of stones condition
        let thisComponent = this;
        let input = e.target.innerText;
        let stonesCount = 0;
        let characterArray = input.split("");
        let symbols;
        characterArray.forEach((character) => {
          symbols = thisComponent.morseDict[character.toUpperCase()];
          stonesCount += symbols.length;
        });
        let stonesCond = stonesCount < 15;
        //console.log(e);
        cond = cond && re.test(char) && stonesCond;
        return cond;
      },
      necklaceStonePrice(char) {
        let n = this.obj.letters[char.toUpperCase()];
        let p = this.necklacePrices.stone;
        return n * p;
      },
      necklaceSubmit() {
        var thisComponent = this;
        thisComponent.isInvalid = false;
        thisComponent.working = true;
        thisComponent.$nextTick(() => {
          // double check email
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          let isEmail = emailRegex.test(thisComponent.email);
          if (isEmail == false) {
            thisComponent.isInvalid = true;
            thisComponent.working = false;
          }
          if (this.messageArray.length != 0 && isEmail == true) {
            let body = "";
            body += "You have received a new customization request from:\n";
            body += thisComponent.email + "\n";
            body += "Details:\n";
            body += "Class: " + thisComponent.key + "\n";
            body += "Finish: " + document.getElementById("finishes").value + "\n";
            //
            body += "Message: " + thisComponent.message + "\n";
            //
            var morse = "[";
            let quote = "Basic Element: $" + thisComponent.necklacePrices.basic + "\n";
            let total = parseInt(thisComponent.necklacePrices.basic);
            thisComponent.messageArray.forEach((element) => {
              morse += thisComponent.morseDict[element.toLowerCase()] + "|";
              quote += element + ": $ " + thisComponent.necklaceStonePrice(element) + "\n";
              total += thisComponent.necklaceStonePrice(element);
            });
            var spacerC = 0;
            thisComponent.spacers.forEach((spacer) => {
              spacerC += 1;
              quote += "Spacer " + spacerC + ": $" + thisComponent.necklacePrices.spacer + "\n";
              total += thisComponent.necklacePrices.spacer;
            });
            var hexagonC = 0;
            thisComponent.hexagons.forEach((hexagon) => {
              hexagonC += 1;
              quote += "Hexagon " + hexagonC + ": $" + thisComponent.necklacePrices.hexagon + "\n";
              total += thisComponent.necklacePrices.hexagon;
            });
            body += "Morse: " + morse.slice(0, -1) + "] \n";
            body += "Quote: \n";
            body += quote;
            body += "Total: $ " + total + "\n";
            body += "Thank You,\n";
            body += "Customiser";
            thisComponent.$forceUpdate();
            axios
              .post(
                "api/email",
                {
                  //email: thisComponent.email,
                  body: body,
                },
                {
                  headers: {
                    "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken").value,
                  },
                }
              )
              .then(function (response) {
                console.log(response.data);
                window.location.href = "https://codebyedge.co.uk/pages/custom-design-thank-you";
              })
              .catch(function (error) {
                console.log(error);
                console.log(error.response);
                thisComponent.working = false;
                //alert(error);
              });
          }
          //thisComponent.working = false;
        });
      },
      necklaceTotal() {
        let b = this.necklacePrices.basic;
        // stones
        let s = 0;
        let thisComponent = this;
        this.messageArray.forEach((element) => {
          s += thisComponent.necklaceStonePrice(element);
        });
        // spacers
        let sp = 0;
        this.spacers.forEach((spacer) => {
          sp += thisComponent.necklacePrices.spacer;
        });
        // hexagons
        let h = 0;
        this.hexagons.forEach((hexagon) => {
          h += thisComponent.necklacePrices.hexagon;
        });
        return b + s + sp + h;
      },
      onReady(e) {
        let thisComponent = this;
        thisComponent.$refs.scene.scene.visible = false;
        thisComponent.isRendering = true;
        //console.log(thisComponent.$refs.scene.scene.visible);
        let children = e.scene.children[0].children;
        let goldName;
        let gemName;
        if (thisComponent.key == "amanti") {
          goldName = "Metal.001";
          gemName = "Material #0.001";
        }
        if (thisComponent.key == "mayfair") {
          goldName = "02 - Default";
          gemName = "03 - Default";
        }
        const gold = new THREE.MeshPhysicalMaterial({
          color: thisComponent.activeFinish,
          metalness: 0.98,
          roughness: 0.0001,
          clearcoat: 1,
          clearcoatRoughness: 0.0001,
          name: goldName,
        });
        // Diamond
        const loader = new THREE.CubeTextureLoader();
        const texturePaths = ["/static/src/glb/obj/nx.png", "/static/src/glb/obj/ny.png", "/static/src/glb/obj/nz.png", "/static/src/glb/obj/px.png", "/static/src/glb/obj/py.png", "/static/src/glb/obj/pz.png"];
        const cubeTexturePromise = new Promise((resolve, reject) => {
          const cubeTexture = loader.load(texturePaths, resolve, undefined, reject);
        });
        const primaryTexturePromise = new Promise((resolve, reject) => {
          const primaryTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_1.jpg", resolve, undefined, reject);
        });
        const secondaryTexturePromise = new Promise((resolve, reject) => {
          const secondaryTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_2.png", resolve, undefined, reject);
        });
        const tertiaryTexturePromise = new Promise((resolve, reject) => {
          const tertiaryTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_3.jpg", resolve, undefined, reject);
        });
        const tertiaryTextureInvertPromise = new Promise((resolve, reject) => {
          const tertiaryTextureInvert = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_3_i.jpg", resolve, undefined, reject);
        });
        const quadTexturePromise = new Promise((resolve, reject) => {
          const quadTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_4.png", resolve, undefined, reject);
        });
        const tertiaryTextureRoundPromise = new Promise((resolve, reject) => {
          const tertiaryTextureRound = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_3.jpg", resolve, undefined, reject);
        });
        Promise.all([cubeTexturePromise, primaryTexturePromise, secondaryTexturePromise, tertiaryTexturePromise, tertiaryTextureInvertPromise, quadTexturePromise, tertiaryTextureRoundPromise])
          .then((textures) => {
            const [cubeTexture, primaryTexture, secondaryTexture, tertiaryTexture, tertiaryTextureInvert, quadTexture, tertiaryTextureRound] = textures;
            const gemRound = new THREE.MeshPhysicalMaterial({
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
            const gemFlat = new THREE.MeshPhysicalMaterial({
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
              //console.log(child);
              // has material?
              // amanti
              if (thisComponent.key == "amanti") {
                if (child.material) {
                  if (child.material.name == "Metal.001") {
                    child.material = gold;
                  }
                  // diamond
                  if (child.userData.name.includes("RB")) {
                    child.material = gemRound;
                  }
                  if (child.userData.name.includes("princess") || child.userData.name.includes("Princess")) {
                    child.material = gemFlat;
                  }
                  /*
                  if (child.material.name == "Material #0.001" || child.material.name == "03 - Default.001") {
                    child.material = gem;
                  }*/
                }
              }
              // mayfair
              if (thisComponent.key == "mayfair") {
                if (child.material.name == "02 - Default") {
                  child.material = gold;
                }
                if (child.material.name == "03 - Default") {
                  child.material = gemRound;
                }
              }
            });
            thisComponent.$nextTick(() => {
              thisComponent.$refs.scene.scene.visible = true;
              thisComponent.isRendering = false;
            });
          })
          .catch((error) => {
            console.error("Error loading textures:", error);
          });
      },
      rowMobileUpdate(comp) {
        if (this.mobileModalVisible == false) {
          this.mobileModalVisible = true;
        }
        console.log(this.mobileModalVisible);
        this.$nextTick(() => {
          this.optionActive = comp;
        });
      },
      rowUpdate(comp) {
        this.optionActive = comp;
      },
      sizesObj() {
        let data = this.db[document.getElementById("app").attributes.key.nodeValue];
        if (data) {
          let sizes = data.sizes;
          let r = [];
          let mid = [];
          sizes.forEach((size, i) => {
            mid.push(size);
            if ([2, 5, 8, 11, 14].includes(i) || i == sizes.length - 1) {
              r.push(mid);
              mid = [];
            }
          });
          //console.log(r);
          return r;
        } else {
          return null;
        }
      },
      smallChainRotationFirstNine(i) {
        let bool = i % 2;
        let x = bool ? 1.6 : 0;
        return { x: x, y: 0, z: 0 };
      },
      smallChainRotationSeven(i) {
        let bool = i % 2;
        let x = bool ? 0 : 1.6;
        return { x: x, y: 0, z: 0 };
      },
      submit() {
        var thisComponent = this;
        thisComponent.isInvalidEmail = false;
        thisComponent.isInvalidEmailMessage = false;
        thisComponent.working = true;
        thisComponent.$nextTick(() => {
          // double check email
          const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
          let isEmail = emailRegex.test(thisComponent.email);
          if (isEmail == false) {
            thisComponent.isInvalidEmail = true;
            thisComponent.working = false;
          }
          if (this.emailMessage == null || this.emailMessage.length == 0 || this.emailMessage.length > 600) {
            thisComponent.isInvalidEmailMessage = true;
            thisComponent.working = false;
          }
          if (isEmail == true && thisComponent.isInvalidEmailMessage != true) {
            let body = "";
            body += "You have received a new message request from:\n";
            body += thisComponent.email + "\n";
            body += "Component: " + thisComponent.key.toUpperCase() + "\n";
            body += "Message:\n";
            body += document.getElementById("emailMessage").value + "\n";
            body += "Thank You,\n";
            body += "Customiser";
            thisComponent.$forceUpdate();
            axios
              .post(
                "api/email",
                {
                  //email: thisComponent.email,
                  body: body,
                },
                {
                  headers: {
                    "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken").value,
                  },
                }
              )
              .then(function (response) {
                //console.log(response.data);
                //window.location.href = "https://codebyedge.co.uk/pages/custom-design-thank-you";
                window.open("https://codebyedge.co.uk/pages/custom-design-thank-you", "_blank");
                // remove errors
                thisComponent.isInvalidEmail = false;
                thisComponent.isInvalidEmailMessage = false;
                thisComponent.working = false;
                thisComponent.modalVisible = false;
              })
              .catch(function (error) {
                console.log(error);
                console.log(error.response);
                thisComponent.working = false;
                //alert(error);
              });
          }
          if (this.messageArray.length != 0 && isEmail == true && 1 == 2) {
            let body = "";
            body += "You have received a new customization request from:\n";
            body += thisComponent.email + "\n";
            body += "Details:\n";
            body += "Class: " + thisComponent.key + "\n";
            if (thisComponent.key == "aquafiore-earrings") {
              body += "Word: Left: " + thisComponent.messageLeft + ", Right: " + thisComponent.messageRight + "\n";
            } else {
              body += "Word: " + thisComponent.message + "\n";
            }
            var morse = "[";
            let quote = "";
            let total = 0;
            thisComponent.messageArray.forEach((element) => {
              morse += thisComponent.morseDict[element.toLowerCase()] + "|";
              quote += element + ": $ " + thisComponent.prices[element.toUpperCase()] + "\n";
              total += thisComponent.prices[element.toUpperCase()];
            });
            body += "Morse: " + morse.slice(0, -1) + "] \n";
            body += "Finish: " + document.getElementById("finishes").value + "\n";
            body += "Quote: \n";
            body += quote;
            body += "Total: $ " + total + "\n";
            body += "Thank You,\n";
            body += "Customiser";
            thisComponent.$forceUpdate();
            axios
              .post(
                "api/email",
                {
                  //email: thisComponent.email,
                  body: body,
                },
                {
                  headers: {
                    "X-CSRFToken": document.getElementsByName("csrfmiddlewaretoken").value,
                  },
                }
              )
              .then(function (response) {
                console.log(response.data);
                window.location.href = "https://codebyedge.co.uk/pages/custom-design-thank-you";
              })
              .catch(function (error) {
                console.log(error);
                console.log(error.response);
                thisComponent.working = false;
                //alert(error);
              });
          }
          //thisComponent.working = false;
        });
      },
      total() {
        var thisComponent = this;
        let t = 0;
        thisComponent.messageArray.forEach((element) => {
          t += thisComponent.prices[element.toUpperCase()];
        });
        return t;
      },
      validateInput(e) {
        // no more than characterLimit
        if (this.key != "aquafiore-earrings") {
          let inputDiv = document.getElementById("messageInput");
          let textLength = inputDiv.innerText.length;
          let chLimit = this.obj.chLimit;
          let cond = textLength <= chLimit;
          // no funky input
          let char = e.key;
          // re for non necklace
          if (this.key != "aquafiore-necklace") {
            var re = /^[a-zA-Z0-9]+$/;
          } else {
            // re for necklace
            var re = /^[a-zA-Z0-9\s]+$/;
          }
          cond = cond && re.test(char);
          return cond;
          "return (this.innerText.length <= " + obj.chLimit + ")";
        }
      },
      updateFinish(e) {
        let updatedMaterial = new THREE.MeshPhysicalMaterial({
          color: thisComponent.activeFinish,
          metalness: 0.98,
          roughness: 0.0001,
          clearcoat: 1,
          clearcoatRoughness: 0.0001,
          name: "Metal.001",
        });
        let finish = e.target.value;
        let newPrices = this.obj.options.filter((option) => {
          return option.text == finish;
        });
        newPrices = newPrices[0].letters;
        this.prices = newPrices;
        this.activeFinish = this.finishes[e.target.value];
        let thisComponent = this;
        if (this.key == "amanti") {
          let scene = this.$refs.scene.scene;
          scene.children.forEach((element) => {
            if (element.children.length != 0) {
              element.children.forEach((obj) => {
                obj.children.forEach((mesh) => {
                  if (mesh.material != null) {
                    if (mesh.material.name == "Metal.001") {
                      mesh.material = updatedMaterial;
                      /*
                      mesh.material = new THREE.MeshStandardMaterial({
                        color: thisComponent.activeFinish,
                        metalness: 1,
                        roughness: 0.05,
                        name: "Metal.001",
                      });
                      */
                      mesh.updateMatrix();
                    }
                  }
                });
              });
            }
          });
          //console.log(scene);
        }
        if (this.key == "mayfair") {
          let scene = this.$refs.scene.scene;
          scene.children.forEach((element) => {
            if (element.children.length != 0) {
              element.children.forEach((obj) => {
                obj.children.forEach((mesh) => {
                  if (mesh.material != null) {
                    if (mesh.material.name == "02 - Default") {
                      mesh.material = new THREE.MeshStandardMaterial({
                        color: thisComponent.activeFinish,
                        metalness: 1,
                        roughness: 0.05,
                        name: "02 - Default",
                      });
                      mesh.updateMatrix();
                    }
                  }
                });
              });
            }
          });
          //console.log(scene);
        }
      },
      updateMorse(e) {
        if (this.key != "aquafiore-earrings") {
          // necklace
          this.placeholder = null;
          let morseContainer = document.getElementById("morseContainer");
          morseContainer.innerHTML = null;
          this.message = document.getElementById("messageInput").innerHTML;
          if (this.message === "") {
            this.placeholder = "Please enter your message";
          } else {
            this.placeholder = null;
          }
          // morse function
          let messageArray = this.message.split("");
          this.messageArray = messageArray;
          let equiv = null;
          let insertion = null;
          let morseClass = null;
          let morseHeight = null;
          let thisComponent = this;
          thisComponent.glbArray = [];
          thisComponent.$forceUpdate();
          thisComponent.$nextTick(() => {
            messageArray.forEach((element) => {
              // find dict equiv
              thisComponent.glbArray.push(element.toUpperCase());
              equiv = this.morseDict[element.toLowerCase()];
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
          });
  
          //console.log(messageArray);
          //console.log(e)
        }
        if (this.key == "aquafiore-earrings") {
        }
      },
    },
    mounted() {
      /*
      if (!(this.desktop)) {
        this.optionActive = null;
      };
      */
      var thisComponent = this;
      //console.log(thisComponent.db)
      let key = document.getElementById("app").attributes.key.nodeValue;
      let data = thisComponent.db[key];
      //console.log(key,data.options);
      if (data) {
        if (key != "aquafiore-necklace") {
          data.chLimit = data.limit - 1;
          thisComponent.obj = data;
          thisComponent.prices = data.options[0].letters;
          thisComponent.key = key;
          thisComponent.activeSize = data.sizes[0];
        } else if (key == "aquafiore-necklace") {
          data.chLimit = data.limit - 1;
          thisComponent.obj = data;
          thisComponent.key = key;
          thisComponent.necklacePrices = data.options[0];
        }
      } else {
        alert("Jewelry Class: " + key + ", does not exist! Redirecting to main website.");
        setTimeout(function () {
          window.location.href = "https://www.codebyedge.co.uk";
        }, 250);
      }
      // 3D work
      if (thisComponent.key == "amanti" || thisComponent.key == "mayfair") {
        this.$nextTick(() => {
          //console.log(thisComponent.key);
          let renderer = thisComponent.$refs.renderer.renderer;
          let scene = thisComponent.$refs.scene.scene;
          let camera = thisComponent.$refs.camera.camera;
          thisComponent.$refs.renderer.three.cameraCtrl.autoRotate = true;
          /*console.log(thisComponent.$refs.renderer.three.cameraCtrl.autoRotate);*/
          //console.log(scene);
          renderer.outputEncoding = THREE.sRGBEncoding;
          renderer.toneMapping = THREE.ACESFilmicToneMapping;
          renderer.toneMappingExposure = 0.82;
          //let envmap = new RGBELoader().setPath("/static/src/obj/").load("studio_small_08_1k.hdr", function (texture) {
          let envmap = new RGBELoader().setPath("/static/src/glb/").load("brown_photostudio_02_1k_b.hdr", function (texture) {
            texture.mapping = THREE.EquirectangularReflectionMapping;
            scene.environment = texture;
            //scene.background = texture;
          });
          const spotLight = new THREE.SpotLight(0xffffff);
          spotLight.position.set(10, 10, 20);
          spotLight.castShadow = true;
          spotLight.shadow.mapSize.width = 1024;
          spotLight.shadow.mapSize.height = 1024;
          spotLight.shadow.camera.near = 500;
          spotLight.shadow.camera.far = 4000;
          spotLight.shadow.camera.fov = 30;
          scene.add(spotLight);
        });
      } else if (thisComponent.key == "aquafiore-bracelet") {
        this.$nextTick(() => {
          //console.log(thisComponent.key);
          let renderer = thisComponent.$refs.renderer.renderer;
          let scene = thisComponent.$refs.scene.scene;
          let camera = thisComponent.$refs.camera.camera;
          thisComponent.$refs.renderer.three.cameraCtrl.autoRotate = true;
          /*console.log(thisComponent.$refs.renderer.three.cameraCtrl.autoRotate);*/
          //console.log(scene);
          renderer.outputEncoding = THREE.sRGBEncoding;
          renderer.toneMapping = THREE.ACESFilmicToneMapping;
          renderer.toneMappingExposure = 1;
          let envmap = new RGBELoader().setPath("/static/src/obj/").load("studio_small_08_1k.hdr", function (texture) {
            texture.mapping = THREE.EquirectangularReflectionMapping;
            scene.environment = texture;
            //scene.background = texture;
          });
          const spotLight = new THREE.SpotLight(0xffffff);
          spotLight.position.set(10, 10, 20);
          spotLight.castShadow = true;
          spotLight.shadow.mapSize.width = 1024;
          spotLight.shadow.mapSize.height = 1024;
          spotLight.shadow.camera.near = 500;
          spotLight.shadow.camera.far = 4000;
          spotLight.shadow.camera.fov = 30;
          scene.add(spotLight);
        });
      } else if (thisComponent.key == "aquafiore-pendant") {
        this.$nextTick(() => {
          //console.log(thisComponent.key);
          let renderer = thisComponent.$refs.renderer.renderer;
          let scene = thisComponent.$refs.scene.scene;
          let camera = thisComponent.$refs.camera.camera;
          thisComponent.$refs.renderer.three.cameraCtrl.autoRotate = true;
          /*console.log(thisComponent.$refs.renderer.three.cameraCtrl.autoRotate);*/
          //console.log(scene);
          renderer.outputEncoding = THREE.sRGBEncoding;
          renderer.toneMapping = THREE.ACESFilmicToneMapping;
          renderer.toneMappingExposure = 1;
          let envmap = new RGBELoader().setPath("/static/src/obj/").load("studio_small_08_1k.hdr", function (texture) {
            texture.mapping = THREE.EquirectangularReflectionMapping;
            scene.environment = texture;
            //scene.background = texture;
          });
          const spotLight = new THREE.SpotLight(0xffffff);
          spotLight.position.set(10, 10, 20);
          spotLight.castShadow = true;
          spotLight.shadow.mapSize.width = 1024;
          spotLight.shadow.mapSize.height = 1024;
          spotLight.shadow.camera.near = 500;
          spotLight.shadow.camera.far = 4000;
          spotLight.shadow.camera.fov = 30;
          scene.add(spotLight);
        });
      } else if (thisComponent.key == "aquafiore-earrings") {
        this.$nextTick(() => {
          //console.log(thisComponent.key);
          let renderer = thisComponent.$refs.renderer.renderer;
          let scene = thisComponent.$refs.scene.scene;
          let camera = thisComponent.$refs.camera.camera;
          thisComponent.$refs.renderer.three.cameraCtrl.autoRotate = true;
          /*console.log(thisComponent.$refs.renderer.three.cameraCtrl.autoRotate);*/
          //console.log(scene);
          renderer.outputEncoding = THREE.sRGBEncoding;
          renderer.toneMapping = THREE.ACESFilmicToneMapping;
          renderer.toneMappingExposure = 1;
          let envmap = new RGBELoader().setPath("/static/src/obj/").load("studio_small_08_1k.hdr", function (texture) {
            texture.mapping = THREE.EquirectangularReflectionMapping;
            scene.environment = texture;
            //scene.background = texture;
          });
          const spotLight = new THREE.SpotLight(0xffffff);
          spotLight.position.set(10, 10, 20);
          spotLight.castShadow = true;
          spotLight.shadow.mapSize.width = 1024;
          spotLight.shadow.mapSize.height = 1024;
          spotLight.shadow.camera.near = 500;
          spotLight.shadow.camera.far = 4000;
          spotLight.shadow.camera.fov = 30;
          scene.add(spotLight);
        });
      } else if (thisComponent.key == "aquafiore-necklace") {
        this.$nextTick(() => {
          //console.log(thisComponent.key);
          let renderer = thisComponent.$refs.renderer.renderer;
          let scene = thisComponent.$refs.scene.scene;
          let camera = thisComponent.$refs.camera.camera;
          thisComponent.$refs.renderer.three.cameraCtrl.autoRotate = true;
          /*console.log(thisComponent.$refs.renderer.three.cameraCtrl.autoRotate);*/
          //console.log(scene);
          renderer.outputEncoding = THREE.sRGBEncoding;
          renderer.toneMapping = THREE.ACESFilmicToneMapping;
          renderer.toneMappingExposure = 1;
          let envmap = new RGBELoader().setPath("/static/src/obj/").load("studio_small_08_1k.hdr", function (texture) {
            texture.mapping = THREE.EquirectangularReflectionMapping;
            scene.environment = texture;
            //scene.background = texture;
          });
          const spotLight = new THREE.SpotLight(0xffffff);
          spotLight.position.set(10, 10, 20);
          spotLight.castShadow = true;
          spotLight.shadow.mapSize.width = 1024;
          spotLight.shadow.mapSize.height = 1024;
          spotLight.shadow.camera.near = 500;
          spotLight.shadow.camera.far = 4000;
          spotLight.shadow.camera.fov = 30;
          scene.add(spotLight);
        });
      }
    },
  };
  </script>
  <style>
  /* Styles for mobile devices with screen width up to 600px */
  @media screen and (max-width: 600px) {
    .cbe-canvas {
      width: 300px;
      height: 600px;
    }
  }
  
  /* Styles for desktop devices with screen width over 600px */
  @media screen and (min-width: 601px) {
    .cbe-canvas {
      width: 800px;
      height: 800px;
    }
  }
  @font-face {
    font-family: "Optima nova";
    font-weight: 400;
    font-style: normal;
    font-display: swap;
    src: url("./optima.woff") format("woff2");
  }
  .cbe-bg-green {
    background: #183e3f;
  }
  .cbe-bg-green-lighter {
    background: #3c6668;
  }
  .cbe-bg-green-lightest {
    background: #d4e4e4;
  }
  .cbe-btn {
    background: #305253;
    color: #ffffff;
    padding-top: 8px;
    padding-bottom: 8px;
    /*letter-spacing: 0.1em;*/
    font-family: "Cormorant Garamond", Arial, sans-serif;
    font-style: italic;
    font-size: 20px;
  }
  .cbe-btn-svg-fill {
    filter: brightness(80%) sepia(100%) hue-rotate(30deg);
  }
  .cbe-btn-text-green {
    color: #305253;
  }
  .cbe-btn-text-font {
    font-family: "Optima nova", sans-serif;
  }
  .cbe-text-color-teal {
    color: #183e3f;
  }
  .cbe-dot-bg-override {
    background-color: unset !important;
  }
  .cbe-font {
    font-family: "Cormorant", serif !important;
    font-weight: 500 !important;
    letter-spacing: 0px !important;
    line-height: 1 !important;
  }
  .cbe-font-black {
    font-weight: 800;
  }
  .cbe-font-comorant {
    font-family: "Comorant", serif !important;
  }
  .cbe-font-comorant-garamond {
    font-family: "Cormorant Garamond", Arial, sans-serif;
  }
  .cbe-font-optima {
    font-family: "Optima nova", sans-serif !important;
  }
  .cbe-font-label {
    font-family: "Optima nova", sans-serif !important;
    letter-spacing: 0.025em !important;
    line-height: 1.4 !important;
  }
  .cbe-font-mono {
    /* font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "Courier New", monospace !important; */
    font-family: "Optima nova", sans-serif !important;
    /* font-size: 2rem !important; */
    line-height: 2 !important;
  }
  .cbe-font-select-label {
    text-transform: uppercase !important;
    letter-spacing: 0.3em !important;
    font-size: 0.8em !important;
    font-weight: 400 !important;
    font-family: "Optima nova", sans-serif !important;
    color: #305253 !important;
  }
  .cbe-footer-text {
    font-family: "Optima nova", sans-serif !important;
    color: #305253 !important;
  }
  .cbe-message-placeholder-fix {
    position: unset !important;
  }
  .cbe-select {
    background-color: inherit !important;
    color: inherit !important;
    appearance: none !important;
    padding-right: 28px !important;
    padding-top: 8px !important;
    padding-left: 8px !important;
    padding-bottom: 4px !important;
    text-indent: 0.01px !important;
    border: 1px solid !important;
    border-color: #e8e8e1 !important;
    background-image: url(https://cdn.shopify.com/s/files/1/0719/6907/9593/t/2/assets/ico-select.svg) !important;
    background-repeat: no-repeat !important;
    background-position: right 10px center !important;
    background-size: 11px !important;
    max-width: 100% !important;
    border-radius: 0 !important;
    font-family: "Optima nova", sans-serif !important;
    -webkit-font-smoothing: antialiased !important;
    -webkit-text-size-adjust: 100% !important;
    letter-spacing: 0.025em !important;
    line-height: 1.4 !important;
  }
  .cbe-spacing {
    letter-spacing: 1.6rem;
  }
  .cbe-spinner {
    padding-top: 8px;
    padding-bottom: 8px;
    content: "";
    /* display: block; */
    width: 24px;
    height: 24px;
    /*position: absolute;*/
    /* left: 50%; */
    /* top: 50%; */
    /*margin-left: -12px;*/
    /* margin-top: -12px;*/
    border-radius: 50%;
    border: 3px solid;
    border-color: #fff;
    border-color: #305253;
    border-top-color: transparent;
  
    animation: spin 1s linear infinite;
  }
  .cbe-table {
    border-spacing: 1.25px !important;
    border-width: 1px !important;
    border-color: #305253 !important;
    font-family: "Optima nova", sans-serif !important;
  }
  .cbe-table-head {
    background-color: #305253 !important;
    color: #ffffff !important;
    font-weight: 700 !important;
    text-align: left !important;
    padding: 10px 15px !important;
    letter-spacing: 0.025em !important;
    line-height: 1.4 !important;
    font-family: "Cormorant Garamond", Arial, sans-serif;
    font-size: 1.2rem;
    border: 2px !important;
    border-color: #ffffff !important;
    border-radius: 0px !important;
  }
  .cbe-td {
    border-spacing: 1.25px !important;
    border-width: 1px !important;
    border-color: #305253 !important;
    border-color: #305253 !important;
    padding: 10px 15px !important;
    font-family: "Optima nova", sans-serif !important;
  }
  @-moz-keyframes spin {
    from {
      -moz-transform: rotate(0deg);
    }
    to {
      -moz-transform: rotate(360deg);
    }
  }
  @-webkit-keyframes spin {
    from {
      -webkit-transform: rotate(0deg);
    }
    to {
      -webkit-transform: rotate(360deg);
    }
  }
  @keyframes spin {
    from {
      transform: rotate(0deg);
    }
    to {
      transform: rotate(360deg);
    }
  }
  </style>
  