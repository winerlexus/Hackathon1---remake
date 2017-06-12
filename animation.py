from sprites import *
from os import path
from setting import *
dir = path.dirname(__file__)
img_dir = path.join(dir, "png")
class LoadSprite_Animation:
    def __init__(self,object,file_png,file_xml,direction,scale = 1):
        self.object = object
        self.scale = scale
        self.direction = direction
        self.spritesheet = pg.image.load(path.join(img_dir,file_png)).convert()
        self.list = []
        self.tree = ET.parse(path.join(img_dir,file_xml))
        self.root = self.tree.getroot()
        self.last_update = 0
        self.current_frame = 0
        self.frame = 0

    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        # image = pg.transform.scale(image,(width*2,height*2))
        return image
    def extract(self, patten):
        self.list = []
        i = 0
        prog = re.compile(str(patten))
        for child in self.root:
            a = prog.fullmatch(child.attrib['name'])
            if a is not None:
                x = (
                int(child.attrib['x']), int(child.attrib['y']), int(child.attrib['width']), int(child.attrib['height']))
                self.list.append(x)
        return self.list


    def load_images(self, last_action):
        last_action = self.object.dictionary.get(self.object.last_action)
        self.status = self.extract(last_action)
        self.status_l = []
        self.status_r = []
        for i in self.status:
            if self.direction == "left":
                self.status_l.append(self.get_image(*i))
                self.status_r.append(pg.transform.flip(self.get_image(*i),True,False))
            else :
                self.status_r.append(self.get_image(*i))
                self.status_l.append(pg.transform.flip(self.get_image(*i), True, False))
    def animate(self):
        if len(self.status) == 0:
            self.status = [(0,0,0,0)]
        now = pg.time.get_ticks()
        total_time = 1000
        if now - self.last_update > total_time/len(self.status):
            self.last_update = now
            if self.object.last_direction == 'left':
                self.current_frame = (self.current_frame +1) % len(self.status_l)
                self.object.image = self.status_l[self.current_frame]
                self.object.image = pg.transform.scale(self.object.image,(
                                (self.object.image.get_width()//self.scale,self.object.image.get_height()//self.scale)))

            if self.object.last_direction == "right":
                self.current_frame = (self.current_frame + 1) % len(self.status_r)
                self.object.image = self.status_r[self.current_frame]
                self.object.image = pg.transform.scale(self.object.image,(
                                (self.object.image.get_width() // self.scale, self.object.image.get_height() // self.scale)))

    def update(self):
        self.load_images(self.object.last_action)
        self.animate()


class LoadSprite_Animation_simple: #images' origin direction is left
    def __init__(self,object,file_png,file_xml,patten,direction):
        self.object = object
        self.patten = patten
        self.direction = direction
        self.spritesheet = pg.image.load(path.join(img_dir,file_png)).convert()
        self.list = []
        self.tree = ET.parse(path.join(img_dir,file_xml))
        self.root = self.tree.getroot()
        self.last_update = 0
        self.current_frame = 0
    def get_image(self,x,y,width,height):
        image = pg.Surface((width,height))
        image.blit(self.spritesheet,(0,0),(x,y,width,height))
        # image = pg.transform.scale(image,(width*2,height*2))
        return image
    def extract(self, patten):
        self.list = []
        i = 0
        prog = re.compile(str(patten))
        for child in self.root:
            a = prog.fullmatch(child.attrib['name'])
            if a is not None:
                x = (
                int(child.attrib['x']), int(child.attrib['y']), int(child.attrib['width']), int(child.attrib['height']))
                self.list.append(x)
        return self.list

    def load_images(self,patten):
        self.status = self.extract(patten)
        self.status_l = []
        self.status_r = []
        for i in self.status:
            if self.direction == "left":
                self.status_l.append(self.get_image(*i))
                self.status_r.append(pg.transform.flip(self.get_image(*i),True,False))
            else :
                self.status_r.append(self.get_image(*i))
                self.status_l.append(pg.transform.flip(self.get_image(*i), True, False))
    def animate(self):
        now = pg.time.get_ticks()
        total_time = 700
        if now - self.last_update > total_time/len(self.status):
            self.last_update = now
            if self.object.last_direction == 'left':
                self.current_frame = (self.current_frame +1) % len(self.status_l)
                self.object.image = self.status_l[self.current_frame]
            elif self.object.last_direction == "right":
                self.current_frame = (self.current_frame + 1) % len(self.status_r)
                self.object.image = self.status_r[self.current_frame]

    def update(self):
        self.load_images(self.patten)
        self.animate()

