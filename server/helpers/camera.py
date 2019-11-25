import gphoto2 as gp
import subprocess, os, signal


def kill_gphoto_process():
    p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
    out, error = p.communicate()

    for line in out.splitlines():
        if b'gvfsd-gphoto2' in line:
            pid = int(line.split(None, 1)[0])
            os.kill(pid, signal.SIGKILL)


def init_camera(camera):
    kill_gphoto_process()

    name, addr = camera
    camera = gp.Camera()

    port_info_list = gp.PortInfoList()
    port_info_list.load()
    idx = port_info_list.lookup_path(addr)
    camera.set_port_info(port_info_list[idx])
    camera.init()

    config = camera.get_config()
    capture_target = config.get_child_by_name('capturetarget')
    choice = capture_target.get_choice(1)
    capture_target.set_value(choice)
    camera.set_config(config)
    print("Camera initialized")
    return camera


def take_picture(camera):
    file_path = camera.capture(gp.GP_CAPTURE_IMAGE)
    file = camera.file_get_info(file_path.folder, file_path.name)
    print(file_path.folder, file_path.name, file.file.width, file.file.height, file.file.type)
    return file_path
