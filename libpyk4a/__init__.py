from pathlib import Path
import os
import sys
def _add_dll_directory(path: Path):
    from ctypes import c_wchar_p, windll  # type: ignore
    from ctypes.wintypes import DWORD

    AddDllDirectory = windll.kernel32.AddDllDirectory
    AddDllDirectory.restype = DWORD
    AddDllDirectory.argtypes = [c_wchar_p]
    AddDllDirectory(str(path))


def kinect():
    if sys.platform != "win32":
        return
    env_path = os.getenv("KINECT_LIBS", None)
    if env_path:
        candidate = Path(env_path)
        dll = candidate / "k4a.dll"
        if dll.exists():
            _add_dll_directory(candidate)
            return
    # autodetecting
    program_files = Path("C:\\Program Files\\")
    for dir in sorted(program_files.glob("Azure Kinect SDK v*"), reverse=True):
        candidate = dir / "sdk" / "windows-desktop" / "amd64" / "release" / "bin"
        dll = candidate / "k4a.dll"
        if dll.exists():
            _add_dll_directory(candidate)
            return
    return
kinect()
import k4a_module

from .calibration import Calibration, CalibrationType
from .capture import PyK4ACapture
from .config import (
    FPS,
    ColorControlCommand,
    ColorControlMode,
    ColorResolution,
    Config,
    DepthMode,
    ImageFormat,
    WiredSyncMode,
)
from .errors import K4AException, K4ATimeoutException
from .playback import PyK4APlayback, SeekOrigin
from .pyk4a import ColorControlCapabilities, PyK4A
from .record import PyK4ARecord
from .transformation import (
    color_image_to_depth_camera,
    depth_image_to_color_camera,
    depth_image_to_color_camera_custom,
    depth_image_to_point_cloud,
)


def connected_device_count() -> int:
    return k4a_module.device_get_installed_count()


__all__ = (
    "Calibration",
    "CalibrationType",
    "FPS",
    "ColorControlCommand",
    "ColorControlMode",
    "ImageFormat",
    "ColorResolution",
    "Config",
    "DepthMode",
    "WiredSyncMode",
    "K4AException",
    "K4ATimeoutException",
    "PyK4A",
    "PyK4ACapture",
    "PyK4APlayback",
    "SeekOrigin",
    "ColorControlCapabilities",
    "color_image_to_depth_camera",
    "depth_image_to_point_cloud",
    "depth_image_to_color_camera",
    "depth_image_to_color_camera_custom",
    "PyK4ARecord",
    "connected_device_count",
)
