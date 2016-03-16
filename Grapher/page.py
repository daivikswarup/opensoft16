import cv2
import numpy as np
from matplotlib import pyplot as plt
from graph import graph
import threading
import wx
from Utils import ResultEvent
min_length = 0.1
max_length = 0.9
threshold = 220
delta=10
delta1 = 5
graphThresholdIntensity=1
tboxThreshhold=0.20
whlimit = 35
class Lines:
    def __init__(self):
        self.total_vertical =0
        self.vert_x = []
        self.vert_topy = []
        self.vert_bottomy = []

        self.total_horizontal =0
        self.hor_y = []
        self.hor_leftx = []
        self.hor_rightx = []
    def length(self, type, i):
        if ( type == 'v'):
            return self.vert_bottomy[i] - self.vert_topy[i]
        if (type =='h'):
            return self.hor_rightx[i]- self.hor_leftx[i]


# This class process a single page of the document
class page(threading.Thread):
    def __init__(self,document,pageno,parent):
        threading.Thread.__init__(self)
        self.parent=parent
        self.pdfImage=None
        self.graphList = []
        self.document=document
        self.pageno=pageno
        self.isgrid = False
    def process(self):
        print self.pageno
        rectangles=self.findAllRectangles()
        self.filterGraphsFromRectangles(rectangles)# populate graphList
        self.processGraphList()

    def run(self):
        self.process()
        print "Page Done"
        wx.PostEvent(self.parent, ResultEvent(5))

    def findAllRectangles(self):
        img = cv2.cvtColor(self.pdfImage,cv2.COLOR_BGR2GRAY)
        kernel = np.ones((2,2), np.uint8)
        #img = cv2.erode(img, kernel, iterations=1)
        
        width = np.size(img,1)
        heigth = np.size(img,0)

        #DP matrix 
        vert_dp = np.zeros((heigth,width), dtype=np.uint16)
        hor_dp = np.zeros((heigth,width), dtype=np.uint16)
        lines = Lines();
        for i in range(1,heigth):
            for j in range(1,width):
                if img[i][j] <= threshold :
                    vert_dp[i][j] = vert_dp[i-1][j] + 1
                    hor_dp[i][j] = hor_dp[i][j-1] + 1

                if img[i][j] > threshold:
                    if vert_dp[i-1][j] >= min_length * heigth:
                        if not (vert_dp[i-1][j-1] <= vert_dp[i-1][j] +2 and vert_dp[i-1][j-1]>= vert_dp[i-1][j] /2 ):
                            
                            k = lines.total_vertical
                            lines.vert_x.append(j)
                            lines.vert_bottomy.append(i-1)
                            lines.vert_topy.append(i - vert_dp[i-1][j] )
                            lines.total_vertical = lines.total_vertical +1 
                            #print 'added vertical line '

                    if hor_dp[i][j-1] >= min_length * heigth:
                        if not (hor_dp[i-1][j-1] <= hor_dp[i][j-1] +2 and hor_dp[i-1][j-1]>= hor_dp[i][j-1] / 2 ):
                             
                            k = lines.total_horizontal
                            lines.hor_y.append(i)
                            lines.hor_rightx.append(j-1)
                            lines.hor_leftx.append(j- hor_dp[i][j-1] )  
                            lines.total_horizontal = lines.total_horizontal +1

        
        #print lines.total_vertical
        #print lines.total_horizontal

        # Merge close lines 
        todelete=[]
        for i in range(0,lines.total_vertical):
            for j in range(i+1,lines.total_vertical):
                if((abs(lines.vert_topy[i]-lines.vert_topy[j])<=delta) and (abs(lines.vert_bottomy[i]-lines.vert_bottomy[j])<=delta) and (abs(lines.vert_x[i]-lines.vert_x[j])<=delta)):
                    todelete.append(j)
        todelete.sort(reverse=True)
        for i in todelete:
            del lines.vert_x[i]
            del lines.vert_bottomy[i]
            del lines.vert_topy[i]
            lines.total_vertical=lines.total_vertical-1
        todelete=[]
        for i in range(0,lines.total_horizontal):
            for j in range(i+1,lines.total_horizontal):
                if((abs(lines.hor_leftx[i]-lines.hor_leftx[j])<=delta) and (abs(lines.hor_rightx[i]-lines.hor_rightx[j])<=delta) and (abs(lines.hor_y[i]-lines.hor_y[j])<=delta)):
                    todelete.append(j)
        todelete.sort(reverse=True)
        for i in todelete:
            del lines.hor_y[i]
            del lines.hor_rightx[i]
            del lines.hor_leftx[i]
            lines.total_horizontal=lines.total_horizontal-1

        ########################## CHECK FOR GRID ############################
        gcount = 0;
        for i in range(1,lines.total_vertical-1):
            if (abs(lines.vert_x[i+1]-2*lines.vert_x[i] + lines.vert_x[i-1])<=delta1):
                gcount = gcount +1;

        if gcount>=4:
            self.isgrid =True

        ######################### CONSTRUCT RECTANGLES ######################
        rectangles=[]
        for i in range(0,lines.total_vertical):
            for j in range(0,lines.total_vertical):
                if(i==j):
                    continue
                if(lines.vert_x[j]<lines.vert_x[i]):
                    continue
                if((abs(lines.vert_topy[i]-lines.vert_topy[j])<=delta) and (abs(lines.vert_bottomy[i]-lines.vert_bottomy[j])<=delta)):
                    for k in range(0,lines.total_horizontal):
                        if((abs(lines.hor_y[k]-lines.vert_topy[j])<=delta) and (abs(lines.hor_y[k]-lines.vert_topy[i])<=delta) and (abs(lines.hor_rightx[k]-lines.vert_x[j])<=delta) and (abs(lines.hor_leftx[k]-lines.vert_x[i])<=delta)):
                            for l in range(0,lines.total_horizontal):
                                if(k==l):
                                    continue
                                if(lines.hor_y[l]<lines.hor_y[k]):
                                    continue
                                if((abs(lines.hor_y[l]-lines.vert_bottomy[j])<=delta) and (abs(lines.hor_y[l]-lines.vert_bottomy[i])<=delta) and (abs(lines.hor_rightx[l]-lines.vert_x[j])<=delta) and (abs(lines.hor_leftx[l]-lines.vert_x[i])<=delta)):
                                    rectangles.append(((lines.hor_y[k],lines.vert_x[i]),(lines.hor_y[l],lines.vert_x[j])))

        todelete=[]
        for i in rectangles:
            for j in rectangles:
                if(i==j):
                    continue
                if(i[0][0]<=j[0][0] and i[0][1]<=j[0][1] and i[1][0]>=j[1][0] and i[1][1]>=j[1][1]):
                    todelete.append(j)
        for i in todelete:
            try:
                rectangles.remove(i)
            except ValueError:
                pass

        #print len(rectangles)
        return rectangles

    def filterGraphsFromRectangles(self,rectangles):
        gid=0
        for r in rectangles:
            print 'page rectangle'
            print self.pageno 
            print r
            image = self.pdfImage[r[0][0]+2:r[1][0]+2, r[0][1]-2:r[1][1]-2]
            img = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
            
            graphObj=graph(self.document,self.pageno,r[1][1],r[0][1],r[1][0],r[0][0],self.pdfImage,image)
            
            ################### FINDING INTERNAL RECTANGLE #####################
        
            width = np.size(img,1)
            heigth = np.size(img,0)

            #DP matrix 
            vert_dp = np.zeros((heigth,width), dtype=np.uint16)
            hor_dp = np.zeros((heigth,width), dtype=np.uint16)
            lines = Lines();
            for i in range(1,heigth):
                for j in range(1,width):
                    if img[i][j] <= threshold :
                        vert_dp[i][j] = vert_dp[i-1][j] + 1
                        hor_dp[i][j] = hor_dp[i][j-1] + 1

                    if img[i][j] > threshold:
                        if vert_dp[i-1][j] <= max_length * heigth and vert_dp[i-1][j] >= 0.05 * heigth:
                            if not (vert_dp[i-1][j-1] <= vert_dp[i-1][j] +2 and vert_dp[i-1][j-1]>= vert_dp[i-1][j] /2 ):
                                
                                k = lines.total_vertical
                                lines.vert_x.append(j)
                                lines.vert_bottomy.append(i-1)
                                lines.vert_topy.append(i - vert_dp[i-1][j] )
                                lines.total_vertical = lines.total_vertical +1 
                                

                        if hor_dp[i][j-1] <= max_length * width and hor_dp[i][j-1] >= min_length * width:
                            if not (hor_dp[i-1][j-1] <= hor_dp[i][j-1] +2 and hor_dp[i-1][j-1]>= hor_dp[i][j-1] / 2 ):
                                 
                                k = lines.total_horizontal
                                lines.hor_y.append(i)
                                lines.hor_rightx.append(j-1)
                                lines.hor_leftx.append(j- hor_dp[i][j-1] )  
                                lines.total_horizontal = lines.total_horizontal +1

            
             
            todelete=[]
            for i in range(0,lines.total_vertical):
                for j in range(i+1,lines.total_vertical):
                    if((abs(lines.vert_topy[i]-lines.vert_topy[j])<=delta1) and (abs(lines.vert_bottomy[i]-lines.vert_bottomy[j])<=delta1) and (abs(lines.vert_x[i]-lines.vert_x[j])<=delta1)):
                        todelete.append(j)
            todelete.sort(reverse=True)
            for i in todelete:
                del lines.vert_x[i]
                del lines.vert_bottomy[i]
                del lines.vert_topy[i]
                lines.total_vertical=lines.total_vertical-1
            todelete=[]
            for i in range(0,lines.total_horizontal):
                for j in range(i+1,lines.total_horizontal):
                    if((abs(lines.hor_leftx[i]-lines.hor_leftx[j])<=delta1) and (abs(lines.hor_rightx[i]-lines.hor_rightx[j])<=delta1) and (abs(lines.hor_y[i]-lines.hor_y[j])<=delta1)):
                        todelete.append(j)
            todelete.sort(reverse=True)
            for i in todelete:
                del lines.hor_y[i]
                del lines.hor_rightx[i]
                del lines.hor_leftx[i]
                lines.total_horizontal=lines.total_horizontal-1

            
            internalrectangles=[]
            for i in range(0,lines.total_vertical):
                for j in range(0,lines.total_vertical):
                    if(i==j):
                        continue
                    if(lines.vert_x[j]<lines.vert_x[i]):
                        continue
                    if((abs(lines.vert_topy[i]-lines.vert_topy[j])<=delta1) and (abs(lines.vert_bottomy[i]-lines.vert_bottomy[j])<=delta1)):
                        for k in range(0,lines.total_horizontal):
                            if((abs(lines.hor_y[k]-lines.vert_topy[j])<=delta1) and (abs(lines.hor_y[k]-lines.vert_topy[i])<=delta1) and (abs(lines.hor_rightx[k]-lines.vert_x[j])<=delta1) and (abs(lines.hor_leftx[k]-lines.vert_x[i])<=delta1)):
                                for l in range(0,lines.total_horizontal):
                                    if(k==l):
                                        continue
                                    if(lines.hor_y[l]<lines.hor_y[k]):
                                        continue
                                    if((abs(lines.hor_y[l]-lines.vert_bottomy[j])<=delta1) and (abs(lines.hor_y[l]-lines.vert_bottomy[i])<=delta1) and (abs(lines.hor_rightx[l]-lines.vert_x[j])<=delta1) and (abs(lines.hor_leftx[l]-lines.vert_x[i])<=delta1)):
                                        internalrectangles.append(((lines.hor_y[k],lines.vert_x[i]),(lines.hor_y[l],lines.vert_x[j])))

            todelete=[]
            for i in internalrectangles:
                for j in internalrectangles:
                    if(i==j):
                        continue
                    if(i[0][0]<=j[0][0] and i[0][1]<=j[0][1] and i[1][0]>=j[1][0] and i[1][1]>=j[1][1]):
                        todelete.append(j)
            for i in todelete:
                try:
                    internalrectangles.remove(i)
                except ValueError:
                    pass
            print len(internalrectangles)
            index =0;
            for i in internalrectangles :
                if  (not ((i[0][0]<heigth/2) and i[1][0]>heigth/2 and i[0][1]<width/2 and i[1][1]>width/2)) :
                    print 'internal rectangle'
                    print self.pageno 
                    print r
                    print i
                    
                    cropped_text = image[i[0][0]:i[1][0], i[0][1]:i[1][1]]
                    graphObj.istextbox = True
                    cv2.imwrite(str(self.pageno)+'.jpg',cropped_text)
                    graphObj.textBoxImages.append(cropped_text)
                    


            if not graphObj.istextbox or self.isgrid:
        
                _,thresh = cv2.threshold(img,180,255,cv2.THRESH_BINARY_INV) # threshold
                height = np.size(img, 0)
                width = np.size(img, 1)

                kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(1,1))
                dilated = cv2.dilate(thresh,kernel,iterations = 1) # dilate

                for i in range(15):
                
                    # for each contour found, draw a rectangle around it on original image
                    contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
                    
                    for contour in contours:
                        # get rectangle bounding contour
                        [x,y,w,h] = cv2.boundingRect(contour)

                        # discard areas that are too large
                        if h>0.7*height or w>0.7*width:
                           continue
                        
                        
                        # discard areas that are too small
                        if h<0.2*height or w<0.2*width:
                            continue

                        
                        index = index +1
                        W = w
                        H = h
                        X = x
                        Y = y 
                    if index ==1 :
                        cropped_text = image[Y :Y +  H , X : X + W]
                        graphObj.istextbox = True                       
                        
                        cv2.imwrite(str(self.pageno)+'.jpg',cropped_text)
                        print 'internalrectangle'
                        print 'method2'
                        
                        break
                    kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
                    dilated = cv2.dilate(dilated,kernel,iterations = 1) # dilate
                    
                    if graphObj.istextbox:
                        graphObj.textBoxImages.append(cropped_text)
                
            graphObj.graphID=gid
            gid=gid+1
            self.graphList.append(graphObj)
                
            
    # def processGraphList(self):

    #     # f=open("log.txt","ab")
    #     # for g in self.graphList:
    #     #     g.start()

    #     # for g in self.graphList:
    #     #     g.join()
    def processGraphList(self):
        f=open("log.txt","ab")
        for g in self.graphList:
            print "ok"
            try:
                g.findLabel()
            except:
                print "Labels not found"
            if g.isgraph==False:
                print "Not a graph "
                continue
            else:
                print "Object is Graph"
                try:
                    g.findLabelText()
                except: 
                    print "Label Text were not recognised by OCR"
                #g.findGradient()
                try:
                    g.findMarkings()
                except:
                    print "Markings not detectd"
                if g.istextbox==False:
                    try:
                        g.findonlycolors()
                    except:
                        print "colors not found in text box"
                else:
                    try:
                        g.findCrop()
                        g.findColorNnumOfPlots()
                    except:
                        print "Colors Not found by method 2 "
            print g.istextbox       
            print "the curvelist is: "
            for i in g.curveList:
                print i.color , i.name

            g.fillData()

