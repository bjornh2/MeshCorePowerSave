#!/usr/bin/python3

# Adds PlatformIO post-processing to merge all the ESP flash images into a single image.

import os
import types

Import("env")

# On Windows, custom framework-arduinoespressif32 packages have a ~102-char path
# ("C:\Users\...\.platformio\packages\framework-arduinoespressif32@src-...") repeated
# across 310+ SDK include dirs, pushing the cc1plus.exe command line (~45,000 chars)
# past the Windows 32,767-char CreateProcess limit ("CreateProcess: No such file or directory").
# Creating a junction inside .pio/fw shortens each path by ~95 chars (~30,000 chars saved).
if os.name == "nt":
    import _winapi

    def _shorten_fw_cpppath(target_env):
        cpppath = target_env.get("CPPPATH", [])
        if not cpppath:
            return
        pio_dir = os.path.join(target_env.subst("$PROJECT_DIR"), ".pio")
        fw_link = os.path.join(pio_dir, "fw")
        new_cpppath = []
        changed = False
        for p in cpppath:
            p_str = target_env.subst(str(p))
            norm_p = os.path.normpath(p_str)
            lower_p = norm_p.lower()
            idx_fw = lower_p.find("framework-arduinoespressif32")
            if idx_fw != -1:
                sep_idx = norm_p.find(os.sep, idx_fw)
                if sep_idx != -1:
                    fw_target = norm_p[:sep_idx]
                    suffix = norm_p[sep_idx:]
                    if not os.path.exists(fw_link):
                        if os.path.lexists(fw_link):
                            try:
                                os.rmdir(fw_link)
                            except OSError:
                                pass
                        os.makedirs(pio_dir, exist_ok=True)
                        try:
                            _winapi.CreateJunction(fw_target, fw_link)
                        except OSError:
                            pass
                    if os.path.exists(fw_link):
                        new_cpppath.append(fw_link + suffix)
                        changed = True
                        continue
            new_cpppath.append(p)
        if changed:
            target_env.Replace(CPPPATH=new_cpppath)

    _orig_clone = env.Clone

    def _patched_clone(self, *args, **kwargs):
        _shorten_fw_cpppath(self)
        cloned = _orig_clone(*args, **kwargs)
        _shorten_fw_cpppath(cloned)
        return cloned

    env.Clone = types.MethodType(_patched_clone, env)

board_config = env.BoardConfig()
firmware_bin = "${BUILD_DIR}/${PROGNAME}.bin"
merged_bin = os.environ.get("MERGED_BIN_PATH", "${BUILD_DIR}/${PROGNAME}-merged.bin")


def merge_bin_action(source, target, env):
    flash_images = [
        *env.Flatten(env.get("FLASH_EXTRA_IMAGES", [])),
        "$ESP32_APP_OFFSET",
        source[0].get_abspath(),
    ]
    merge_cmd = " ".join(
        [
            '"$PYTHONEXE"',
            '"$OBJCOPY"',
            "--chip",
            board_config.get("build.mcu", "esp32"),
            "merge_bin",
            "-o",
            merged_bin,
            "--flash_mode",
            board_config.get("build.flash_mode", "dio"),
            "--flash_freq",
            "${__get_board_f_flash(__env__)}",
            "--flash_size",
            board_config.get("upload.flash_size", "4MB"),
            *flash_images,
        ]
    )
    env.Execute(merge_cmd)


env.AddCustomTarget(
    name="mergebin",
    dependencies=firmware_bin,
    actions=merge_bin_action,
    title="Merge binary",
    description="Build combined image",
    always_build=True,
)