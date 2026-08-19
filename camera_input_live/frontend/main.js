// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  // Only run the render code the first time the component is loaded.
  if (!window.rendered) {
    const {height, width, debounce, showControls, startLabel, stopLabel, switchLabel} = event.detail.args

    if (showControls) {
      Streamlit.setFrameHeight(45)
    }

    if (isNaN(height)) {
      height = width / (4/3);
    }

    let video = document.getElementById('video');
    let canvas = document.getElementById('canvas');
    let button = document.getElementById('button');
    let switchButton = document.getElementById('switchButton');

    let stopped = false;
    // "environment" = camara trasera (por defecto), "user" = camara frontal
    let facingMode = "environment";

    video.setAttribute('width', width);
    video.setAttribute('height', height);
    canvas.setAttribute('width', width);
    canvas.setAttribute('height', height);

    function takepicture() {
      if (stopped) {
        return;
      }
      let context = canvas.getContext('2d');
      canvas.width = width;
      canvas.height = height;
      context.drawImage(video, 0, 0, width, height);

      var data = canvas.toDataURL('image/png');
      sendValue(data);
    }

    function stopStream() {
      if (video.srcObject) {
        video.srcObject.getTracks().forEach(function(track) {
          track.stop();
        });
        video.srcObject = null;
      }
    }

    function startVideo() {
      stopStream();
      navigator.mediaDevices.getUserMedia({ video: { facingMode: { ideal: facingMode } } })
        .then(function(stream) {
          video.srcObject = stream;
          video.play();
        })
        .catch(function(err) {
          console.log("An error occurred: " + err);
          // Si falla la camara solicitada (por ejemplo no hay trasera),
          // intenta con cualquier camara disponible.
          navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
              video.srcObject = stream;
              video.play();
            })
            .catch(function(err2) {
              console.log("No se pudo acceder a ninguna camara: " + err2);
            });
        });
    }

    function stopVideo() {
      video.pause();
      stopStream();
      stopped = true;
    }

    function toggleVideo() {
      if (stopped) {
        startVideo();
        stopped = false;
      } else {
        stopVideo();
        stopped = true;
      }
      button.textContent = stopped ? startLabel : stopLabel;
    }

    function switchCamera() {
      facingMode = (facingMode === "environment") ? "user" : "environment";
      switchButton.textContent = (facingMode === "environment") ? switchLabel + " (trasera)" : switchLabel + " (frontal)";
      if (!stopped) {
        startVideo();
      }
    }

    startVideo();

    button.addEventListener('click', toggleVideo);
    button.textContent = stopped ? startLabel : stopLabel;

    switchButton.addEventListener('click', switchCamera);
    switchButton.textContent = switchLabel + " (frontal)";

    takepicture();
    setInterval(takepicture, debounce);
    window.rendered = true
  }
}

// Render the component whenever python send a "render event"
Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
// Tell Streamlit that the component is ready to receive events
Streamlit.setComponentReady()
// Don't actually need to display anything, so set the height to 0
Streamlit.setFrameHeight(0)