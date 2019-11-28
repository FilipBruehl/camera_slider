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

        self.name, self.addr = Camera.available_cameras[index]
        self.camera = gp.Camera()

        port_info_list = gp.PortInfoList()
        port_info_list.load()
        idx = port_info_list.lookup_path(self.addr)
        self.camera.set_port_info(port_info_list[idx])
        self.camera.init()

        config = self.camera.get_config()
        capture_target = config.get_child_by_name('capturetarget')
        choice = capture_target.get_choice(1)
        capture_target.set_value(choice)
        self.camera.set_config(config)
        print("Camera initialized")
        # self.list_config()

        # self.get_battery()
        # self.get_focal()
        # self.get_shutter_speed()
        # self.get_iso()
        # self.get_autofocus()
        # self.get_image_quality()

    def take_picture(self):
        file_path = self.camera.capture(gp.GP_CAPTURE_IMAGE)
        file = self.camera.file_get_info(file_path.folder, file_path.name)
        print(file_path.folder, file_path.name, file.file.width, file.file.height, file.file.type)
        return file_path

    def get_information(self):
        return {
            'name': self.name,
            'battery': self.get_battery(),
            'focal': self.get_focal(),
            'shutter': self.get_shutter_speed(),
            'iso': self.get_iso(),
            'focus': self.get_autofocus(),
            'quality': self.get_image_quality()
        }

    def list_config(self):
        config = self.camera.list_config()
        for con in config:
            print(con)

    def get_shutter_speed(self):
        config = self.camera.get_config()
        shutter_speed = config.get_child_by_name('shutterspeed2')
        shutter_speed = shutter_speed.get_value()
        return shutter_speed

    def get_battery(self):
        config = self.camera.get_config()
        battery = config.get_child_by_name('batterylevel')
        battery = battery.get_value()
        return battery

    def get_focal(self):
        config = self.camera.get_config()
        focal = config.get_child_by_name('f-number')    # apertureatminfocallength, apertureatmaxfocallength
        focal = focal.get_value()
        return focal

    def get_autofocus(self):
        config = self.camera.get_config()
        fm = config.get_child_by_name('focusmode')
        fm = fm.get_value()
        return fm

    def get_image_quality(self):
        config = self.camera.get_config()
        qual = config.get_child_by_name('imagequality')
        qual = qual.get_value()
        return qual

    def get_iso(self):
        config = self.camera.get_config()
        iso = config.get_child_by_name('iso')
        iso = iso.get_value()
        return iso
