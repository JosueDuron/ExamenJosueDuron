import base64
from io import BytesIO
from pathlib import Path
from typing import Optional

import streamlit.components.v1 as components

# Componente local basado en streamlit-camera-input-live (blackary),
# modificado para soportar cambio entre camara frontal y trasera,
# usando la camara trasera por defecto (util para celulares).
frontend_dir = (Path(__file__).parent / "frontend").absolute()
_component_func = components.declare_component(
    "camera_input_live", path=str(frontend_dir)
)


def camera_input_live(
    debounce: int = 300,
    height: int = 530,
    width: int = 704,
    key: Optional[str] = None,
    show_controls: bool = True,
    start_label: str = "Detener",
    stop_label: str = "Reanudar",
    switch_label: str = "Cambiar camara",
) -> Optional[BytesIO]:
    """Version en vivo de st.camera_input, con boton para cambiar entre
    camara trasera (por defecto) y frontal. Util en celulares."""
    b64_data: Optional[str] = _component_func(
        height=height,
        width=width,
        debounce=debounce,
        showControls=show_controls,
        startLabel=start_label,
        stopLabel=stop_label,
        switchLabel=switch_label,
        key=key,
    )

    if b64_data is None:
        return None

    raw_data = b64_data.split(",")[1]  # Strip the data: type prefix

    component_value = BytesIO(base64.b64decode(raw_data))

    return component_value