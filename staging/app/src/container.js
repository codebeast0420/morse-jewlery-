      /*
      // Environment Map Cubic
      const loader = new THREE.CubeTextureLoader();
      // Define the six texture file paths
      const texturePaths = ["/static/src/glb/obj/nx.png", "/static/src/glb/obj/ny.png", "/static/src/glb/obj/nz.png", "/static/src/glb/obj/px.png", "/static/src/glb/obj/py.png", "/static/src/glb/obj/pz.png"];
      // Load the six textures
      const cubeTexture = loader.load(texturePaths);
      // Diamond Textures
      const primaryTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_1.jpg");
      const secondaryTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_2.png");
      const tertiaryTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_3.jpg");
      const tertiaryTextureInvert = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_3_i.jpg");
      const quadTexture = new THREE.TextureLoader().load("/static/src/glb/diamond/diamond_4.png");



      // Diamond Attempts
      /*
      let texture = await thisComponent.loadTexture("/static/src/glb/diamond-square-small.jpg");
      const gem = new THREE.MeshPhysicalMaterial({
        map: texture,
      });
      */
      /*
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
        name: gemName,
      });
      */
      // Good checker, faces are mapped
      /*
      let gem = new THREE.MeshBasicMaterial({
        onBeforeCompile: (shader) => {
          shader.fragmentShader = `${shader.fragmentShader}`.replace(
            `vec4 diffuseColor = vec4( diffuse, opacity );`,
            `
      	float chCount = 7.;
        float checker = (1. / chCount);
        float actualCheckers = 1. - checker;
        float halfChecker = checker * 0.5;
      	vec2 bUv = (vUv * actualCheckers) - halfChecker;
      	vec2 cUv = fract((bUv) * (chCount * 0.5)) - 0.5;
        float checkerVal = clamp(step(cUv.x * cUv.y, 0.), 0.5, 1.);
      	vec3 col = vec3(checkerVal);
      	vec4 diffuseColor = vec4( col, opacity );
      `
          );
          //console.log(shader.fragmentShader);
        },
      });
      gem.defines = { USE_UV: "" };
      const texture = new THREE.TextureLoader().load("/static/src/glb/diamond-square-small.jpg");
      const gem = new THREE.MeshPhysicalMaterial({
        color: 0x002211,
        clearcoat: 0,
        clearcoatRoughness: 0,
        ior: 2.1,
        reflectivity: 1,
        metalness: 1,
        roughness: 0,
        specularIntensity: 0.94,
        specularColor: 0xffeeaa,
        transmission: 0.7,
        name: gemName,
        envMap: texture,
      });
      gem.envMap.repeat.set(0.2, 0.2);

      const texture = new THREE.TextureLoader().load("/static/src/glb/diamond-square-small.jpg");
      const guiOptions = {
        refractionIndex: 1.5,
        color: "#FFFFFF",
        dispersion: 0.1,
        roughness: 0.9,
        animation: true,
        geometry: "icosahedron",
      };
      const backSideMaterial = new THREE.ShaderMaterial({
        vertexShader: `
        varying vec3 vWorldNormal;
        void main() {
          vWorldNormal = (modelMatrix * vec4(normal, 0.0)).xyz;
          vWorldNormal = -normalize(vec3(-vWorldNormal.x, vWorldNormal.yz));
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }`,
        fragmentShader: `
        varying vec3 vWorldNormal;
        void main() {
          gl_FragColor.rgb = vWorldNormal;
        }`,
        side: THREE.BackSide,
      });
      const renderTarget = new THREE.WebGLRenderTarget(600, 600, {
        type: THREE.HalfFloatType,
      });
      const gem = new THREE.ShaderMaterial({
        uniforms: {
          //resolution: new THREE.Uniform(new THREE.Vector2(600, 600).multiplyScalar(window.devicePixelRatio)),
          resolution: { value: new THREE.Vector2( 512, 512 ) },
          backNormals: new THREE.Uniform(texture),
          envMap: new THREE.Uniform(texture),
          refractionIndex: new THREE.Uniform(guiOptions.refractionIndex),
          color: new THREE.Uniform(new THREE.Color(guiOptions.color)),
          dispersion: new THREE.Uniform(guiOptions.dispersion),
          roughness: new THREE.Uniform(guiOptions.roughness),
        },
        vertexShader: `
        varying vec3 vWorldCameraDir;
        varying vec3 vWorldNormal;
        varying vec3 vViewNormal;
        void main() {
          vec4 worldPosition = modelMatrix * vec4( position, 1.0);
          vWorldCameraDir = worldPosition.xyz - cameraPosition;
          vWorldCameraDir = normalize(vec3(-vWorldCameraDir.x, vWorldCameraDir.yz));
          vWorldNormal = (modelMatrix * vec4(normal, 0.0)).xyz;
          vWorldNormal = normalize(vec3(-vWorldNormal.x, vWorldNormal.yz));
          vViewNormal = normalize( modelViewMatrix * vec4(normal, 0.0)).xyz;
          gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
        }`,
        fragmentShader: `
        #define REF_WAVELENGTH 579.0
        #define RED_WAVELENGTH 650.0
        #define GREEN_WAVELENGTH 525.0
        #define BLUE_WAVELENGTH 440.0
        uniform vec2 resolution;
        uniform sampler2D backNormals;
        uniform samplerCube envMap;
        uniform float refractionIndex;
        uniform vec3 color;
        uniform float dispersion;
        uniform float roughness;
        varying vec3 vWorldCameraDir;
        varying vec3 vWorldNormal;
        varying vec3 vViewNormal;
        vec4 refractLight(float wavelength, vec3 backFaceNormal) {
          float index = 1.0 / mix(refractionIndex, refractionIndex * REF_WAVELENGTH / wavelength, dispersion);
          vec3 dir = vWorldCameraDir;
          dir = refract(dir, vWorldNormal, index);
          dir = refract(dir, backFaceNormal, index);
          return textureCube(envMap, dir);
        }
        vec3 fresnelSchlick(float cosTheta, vec3 F0)
        {
          return F0 + (1.0 - F0) * pow(1.0 + cosTheta, 5.0);
        }
        void main() {
          vec3 backFaceNormal = texture2D(backNormals, gl_FragCoord.xy / resolution).rgb;
          float r = refractLight(RED_WAVELENGTH, backFaceNormal).r;
          float g = refractLight(GREEN_WAVELENGTH, backFaceNormal).g;
          float b = refractLight(BLUE_WAVELENGTH, backFaceNormal).b;
          vec3 fresnel = fresnelSchlick(dot(vec3(0.0,0.0,-1.0), vViewNormal), vec3(0.04));
          vec3 reflectedColor = textureCube(envMap, reflect(vWorldCameraDir, vWorldNormal)).rgb * saturate((1.0 - roughness) + fresnel);
          gl_FragColor.rgb = vec3(r,g,b) * color + reflectedColor;
        }`,
      });
      */

      /*
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
        name: gemName,
      });
      */
      /*
      const gem = new THREE.MeshPhysicalMaterial({
        color: 0xffffff,
        map: primaryTexture,
        clearcoat: 0.64,
        clearcoatRoughness: 0,
        metalness: 0.33,
        metalnessMap: quadTexture,
        roughness: 0,
        ior: 2.1,
        transmission: 0.33,
        transmissionMap: secondaryTexture,
        //thickness: 1,
        //reflectivityMap: secondaryTexture,
        //specularIntensity: 0.99,
        //specularColor: 0xffffff,
        //specularColorMap: primaryTexture,
        //clearcoat: 1,
        //clearcoatRoughness: 0.1,
        //reflectivity: 1,
        //specularIntensity: 0.99,
        //specularColor: 0xffffff,
        //specularColorMap: primaryTexture,
        //metalness: 1,
        //ior: 2.47,
        //thickness: 1,
        //ior: 2.47,
        //reflectivity: 1,
        //reflectivityMap: texture,
        //metalness: 1,
        //metalnessMap: texture,
        //roughness: 0,
        //specularIntensity: 0.89,
        //specularColor: 0xffffff,
        //specularColorMap: texture,
        //transmission: 0.3,
        //transmissionMap: texture,
        //thickness: 1,
        //thicknessMap: texture,
        //envMap: cubeTexture,
        //envMapIntensity: 1.6,
        name: gemName,
      });
      let tx1 = 0.4;
      let ty1 = 0.4;
      let tx2 = 0.01;
      let ty2 = 0.01;
      let tx4 = 0.2;
      let ty4 = 0.2;
      gem.map.repeat.set(tx1, ty1);
      gem.transmissionMap.repeat.set(tx4, ty4);
      //gem.metalnessMap.repeat.set(tx, ty);
      //gem.specularColorMap.repeat.set(tx, ty);
      //gem.reflectivityMap.repeat.set(tx, ty);
      //gem.transmissionMap.repeat.set(tx, ty);
      //gem.thicknessMap.repeat.set(tx, ty);
      //gem.metalnessMap.repeat.set(tx, ty);
      //gem.reflectivityMap.repeat.set(tx, ty);
      */
      // Finish Diamond Attempts
      /*
      children.forEach((child) => {
        // has material?
        // amanti
        if (thisComponent.key == "amanti") {
          if (child.material) {
            if (child.material.name == "Metal.001") {
              child.material = gold;
            }
            if (child.material.name == "Material #0.001" || child.material.name == "03 - Default.001") {
              child.material = gem;
            }
          }
        }
        // mayfair
        if (thisComponent.key == "mayfair") {
          if (child.material.name == "02 - Default") {
            child.material = gold;
          }
          if (child.material.name == "03 - Default") {
            child.material = gem;
          }
        }
      });
      */