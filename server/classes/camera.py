import gphoto2 as gp
import subprocess, os, signal


class Camera:
    available_cameras = None

    @staticmethod
    def kill_gphoto_process():
        p = subprocess.Popen(['ps', '-A'], stdout=subprocess.PIPE)
        out, error = p.communicate()

        for line in out.splitlines():
            if b'gvfsd-gphoto2' in line:
                pid = int(line.split(None, 1)[0])
                os.kill(pid, signal.SIGKILL)

    @staticmethod
    def get_available_cameras():
        if hasattr(gp, 'gp_camera_autodetect'):
            Camera.available_cameras = gp.check_result(gp.gp_camera_autodetect())
        return Camera.available_cameras

    def __init__(self, index):
        self.index = index
        Camera.kill_gphoto_process()

        name, addr = Camera.available_cameras[index]
        self.camera = gp.Camera()

        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(addr)
        self.camera.set_port_info(port_info_list[idx])
        self.camera.init()

        config = self.camera.get_config()
        capture_target = config.get_child_by_name('capturetarget')
        choice = capture_target.get_choice(1)
        capture_target.set_value(choice)
        self.camera.set_config(config)
        print("Camera initialized")

    def take_picture(self):
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        file = self.camera.file_get_info(file_path.folder, file_path.name)
        print(file_path.folder, file_path.name, file.file.width, file.file.height, file.file.type)
        return file_path
