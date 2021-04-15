import pygame, random, math
from PIL import Image, ImageFilter, ImageEnhance
pygame.init()

width=500                 #화면 가로
height=500                #화면 세로
screen = pygame.display.set_mode([width, height])
clock=pygame.time.Clock()
pygame.display.set_caption('Growth - I_Love_Python')
programIcon = pygame.image.load('icon.jfif')
pygame.display.set_icon(programIcon)

speed=3                  #이속
evap=2                   #증발속도
diff=1.7                   #확산속도
c=[0, 255, 255]         #기본색
hc=[255, 255, 255]        #하이라이트 컬러            
r=10                      #센서 반지름
rs=1                      #랜덤 강도
highlight=False            #하이라이팅 여부
count=500                 #개수
fps=360                   #fps

image_mode="RGBA"
size=(width, height)

class agent:
    def __init__(self):
        self.angle=random.randint(0, 360)
        
        self.x=random.randint(100, 200)
        self.y=random.randint(100, 200)
        '''
        self.x=width/2
        self.y=height/2
        '''
        self.x1=self.x
        self.y1=self.y

    def update(self):
        x2=self.x+math.cos(self.angle*math.pi/180)*speed
        y2=self.y+math.sin(self.angle*math.pi/180)*speed
        if x2 > width-r-1 or x2 < r+1 or y2 < r+1 or y2 > height-r-1:
            self.angle=360-self.angle+random.randint(-30, 30)
        else:
            self.x=x2
            self.y=y2
            #self.angle=random.randint(0, 360)

    def draw(self, color):
        pygame.draw.line(screen, color, [self.x, self.y], [self.x1, self.y1])
        self.x1=self.x
        self.y1=self.y

    def sense(self):
        sensed={}
        a=0
        b=0
        c=0
        if self.x>r+1 and self.x<width-r-1 and self.y>r+1 and self.y<height-r-1:
            x=int(self.x+math.ceil(math.sin(((90-(self.angle-45))%360)*math.pi/180)*r)-1)
            y=int(self.y+math.ceil(math.cos(((90-(self.angle-45))%360)*math.pi/180)*r)-1)
            for i in range(9):
                a+=sum(screen.get_at((x+i%3, y+i//3)))*random.random()
            x=int(self.x+math.ceil(math.sin(((90-self.angle)%360)*math.pi/180)*r)-1)
            y=int(self.y+math.ceil(math.cos(((90-self.angle)%360)*math.pi/180)*r-1))
            for i in range(9):
                b+=sum(screen.get_at((x+i%3, y+i//3)))*random.random()
            x=int(self.x+math.ceil(math.sin(((45-self.angle)%360)*math.pi/180)*r)-1)
            y=int(self.y+math.ceil(math.cos(((45-self.angle)%360)*math.pi/180)*r)-1)
            for i in range(9):
                c+=sum(screen.get_at((x+i%3, y+i//3)))*random.random()
            sensed[a]=-1
            sensed[b]=0
            sensed[c]=1
            self.angle+=sensed[sorted(list(sensed.keys()), reverse=True)[0]]*60+random.randint(-100, 100)/100*pow(2, rs)
        else:
            self.angle=random.randint(0, 360)

i=[]
for k in range(count):
    i.append(agent())

if highlight:
    v=agent()
    i.pop()

while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    for k in i:
        k.sense()
        k.update()
        k.draw(c)

    if highlight:
        v.sense()
        v.update()
        v.draw(hc)
    

    s = pygame.image.frombuffer(ImageEnhance.Brightness(Image.frombytes("RGBA", size, pygame.image.tostring(screen, "RGBA")).filter(ImageFilter.BoxBlur(radius=diff/10))).enhance((100-evap)/100).tobytes(), size, "RGBA")
    screen.blit(s,(0, 0))
       
    pygame.display.update()
