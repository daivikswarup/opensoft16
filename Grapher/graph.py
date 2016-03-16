from curve import curve
import numpy as np 
import cv2
from SimpleCV import *
from pytesseract import image_to_string
from PIL import Image as IMAGE
#from matplotlib import pyplot as plt
#import matplotlib.pyplot as plt
import re
import time
from sklearn.cluster import KMeans
import threading



class graph(threading.Thread):
    def __init__(self,document,pageno,x2,x4,y2,y4,imagename,crop_image):
        threading.Thread.__init__(self)
        # reference to the document
        self.document = document

        # page in which the graph is present
        self.pageno = pageno
        self.graphID=0
        #coordinates
        self.x2 = x2
        self.x4 = x4
        self.y2 = y2
        self.y4 = y4

        #scale
        self.dx = 1                         #get it by calling findGradient(marking_imageurl) method
        self.dy = 1                         #get it by calling findGradient(marking_imageurl) method

        #marking
        self.minx = 0                       #get it by calling findMarkings(marking_imageurl)method twice.  
        self.maxx = self.x2-self.x4                       #one time each for x and y axes
        self.miny = 0                       #not working for bad quality images. 
        self.maxy = self.y2-self.y4                       #markings on image must be sharp and clear enough.

        # storing whether graph attributes are found or not
        self.isLog = False
        self.istextbox = False
        self.isxlabel = False
        self.isylabel = False
        self.isxmarkings = False
        self.isymarkings = False
        self.isxgradient = False
        self.isygradient = False
        self.isgraph = True
        #poll
        self.pollDistance = 0

        #curve point data for
        self.curveList = []
        
        self.xlabel = None                  #get it by calling findLabel(label_imageurl) method twice.
        self.ylabel = None                  #one time each for x and y axes.
        self.description = None             #even description can be obtained by the same method.

        self.graphboundX=None
        self.graphboundY=None
        self.image=imagename
        self.rectangle=crop_image
        self.nummarkX=0
        self.nummarkY=0


        self.textBoxImages=[]

    def run(self):
        self.process()

    def process(self):
        print "ok"
        self.findLabel()
        if self.isgraph==False:
            pass
        else:
            self.findLabelText()
            #self.findGradient()
            self.findMarkings()
            if self.istextbox==False:
                self.findonlycolors()
            else:
                self.findCrop()
                self.findColorNnumOfPlots()
        print self.istextbox       
        print "the curvelist is: "
        for i in self.curveList:
            print i.color , i.name

        self.fillData()        
        #g.fillData()
    
    # to find x axis label and values
    def findxaxis_width(self,x1,y1,x2,y2):
        im=self.image

        y_temp=y1
        y_array=[]
        alternate_flag=1
        while(len(y_array)<3):
            x_temp=x1
            
            a=np.array([200,200,200])
            flag=1
            while(x_temp<x2-1):
                # print "x_temp=%d y_temp=%d x2=%d"%(x_temp,y_temp,x2)
                #print (im[y_temp,x_temp].tolist())
                if( (im[y_temp,x_temp+1].tolist() < [200,200,200]or im[y_temp,x_temp+1].tolist()<[200,200,200])):
                    #print "failed"
                    flag=0
                    break
                x_temp=x_temp+1
                # print "out of loop flag=%d"%(flag)
                # print x_temp,y_temp
            if(flag==1 and alternate_flag==1):
                y_array.append(y_temp)
                alternate_flag=0
            elif(flag==0):
                alternate_flag=1
            y_temp+=1
        if len(y_array)==3:    
            self.graphboundY=y_array[2]   
        return y_array

    def findyaxis_width(self,x4,y4,x1,y1):
        im=self.image
        digit_pixel_size=(self.x2-x1)*9/236
        marking_pixel_distance=(self.x2-x1)*10/488
        #print digit_pixel_size,marking_pixel_distance
        x_temp=x4
        x_array=[]
        count =0
        alternate_flag=1
        while(x_temp>=0 and count<3):
            y_temp=y4
            flag=1
            while(y_temp<y1-1):
                if((im[y_temp,x_temp].tolist()<[200,200,200] or im[y_temp+1,x_temp].tolist()<[200,200,200])):
                    flag=0
                    break
                y_temp+=1
            if(flag==1 and alternate_flag==1):
                if(count==0):
                    #print "count 0"
                    #print x4-x_temp,marking_pixel_distance
                    if(x4-x_temp>marking_pixel_distance):
                        return -1
                if(count==2):
                    #print "count 2"
                    #print x_array[1],x_temp
                    #print x_array[1]-x_temp,digit_pixel_size
                    if(x_array[1]-x_temp>digit_pixel_size):
                        x_array.append(x_temp)
                        count+=1
                    else:
                        x_array[1]=x_temp
                else:
                    #print "count 1/0"
                    #print count
                    x_array.append(x_temp)  
                    count+=1    
                alternate_flag=0
            elif(flag==0):
                alternate_flag=1
            x_temp-=1
        print x_array
        if len(x_array)==3:
            self.graphboundX=x_array[2]

        return x_array
        



    def findLabel(self):        
        x1=self.x4
        y1=self.y2

        img=self.image
        #print self.x2,self.x4,self.y2,self.y4
        y=self.findxaxis_width(x1,y1,self.x2,self.y2)
        #print y

        iterator=0
        y_array_len=len(y)
        if(y_array_len==2):
            y.insert(2,y[1]+100)
            y_array_len+=1
            #print y
        print 'len of y1 %d' % (y_array_len)

        while iterator<y_array_len-1:
            #print "iterator"+str(iterator)
            cropped = img[y[iterator] :y[iterator+1] ,x1:self.x2]
            s =  'images/temp_x' +str(iterator+1)+'.png' 
            cv2.imwrite(s , cropped)
            iterator+=1

        x=self.findyaxis_width(self.x4,self.y4,x1,y1)
        print x

        if(x!=-1):
            x_array_len=len(x)
            if(x_array_len==2):
                x.insert(x_array_len,0)
                x_array_len+=1
                #print x
            iterator=x_array_len-1
            print 'len of x1 %d' % (x_array_len)

            i=0
            while iterator>0:
                if(iterator==2 and x_array_len==4):
                    cropped = img[self.y4:y1, x[iterator]: x[iterator-2]]
                    iterator=1
                else:
                    cropped = img[self.y4:y1, x[iterator]: x[iterator-1]]

                s =  'images/temp_y'+str(i+1)+'.png'
                if i==1:
                    print "markings fig found" 
                cv2.imwrite(s , cropped)
                iterator-=1
                i+=1
        else:
            self.isgraph=False
            print 'not a graph'


    #OCR for text labels and description of the graph. Call this method once for each of the three values.
    def findLabelText(self):
        for i in range(0,2):
            flag=0
            if i==0:
                try:                  
                    img = Image("images/temp_x2.png",0)
                except  IOError:
                    continue    
            else:
                try:
                    img = Image("images/temp_y1.png",0)
                except IOError:
                    continue
            #rotate image for y axis label
            if img.width<img.height:
                img = img.rotate(-90,fixed = False)
                flag=1
            if img.height<50 :
                #print "ok"
                img = img.resize(img.width*2,img.height*4)
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize()
                img_bin = img_bin.dilate(2)
                img_bin = img_bin.erode(1)

            else:    
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize()


            
            
            img_bin.save("images/temp.png")

            img = cv2.imread("images/temp.png") 
            dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) 
            

            try:
                label = image_to_string(IMAGE.fromarray(dst),lang='eng')    #OCR on image
                
                if i==0:
                    self.xlabel = label
                    self.isxlabel=True
                    print label
                else:
                    self.ylabel = label
                    self.isylabel=True    
                    print label

            except:
                if i==0:
                    self.xlabel = None
                    
                else:
                    self.ylabel = None    
                    
            


    #OCR for markings on x and y axes.Returns min & max value of the markings on an axis in that order.It also finds and stores gradient values
    def findMarkings(self):
        for i in range(0,2):        
            if i==0:
                try:                  
                    img = Image("images/temp_x1.png",0)
                except  IOError:
                    continue    
            else:
                try:
                    img = Image("images/temp_y2.png",0)
                except IOError:
                    continue
            """
            if i==0:
                try:
                    num_marking = int(img.width/self.dx+1)
                except ZeroDivisionError:
                    continue
            else:
                try:
                    num_marking = int(img.height/self.dy+1)       
                except ZeroDivisionError:
                    continue      
                    """
            resize=1       
            if img.width<40:
                #print "ok"
                resize=3
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize()
                img_bin = img_bin.resize(img.width*resize,img.height*resize)
                #img_bin = img_bin.dilate(2)
                #img_bin = img_bin.erode(1)
                
            
            else:
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize()

            resize=1
            if img.height<50:
                #print "ok"
                resize=3
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize()
                img_bin = img_bin.resize(img.width*resize,img.height*resize)
                #img_bin = img_bin.dilate(2)
                #img_bin = img_bin.erode(1)


            else:
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize() 

            img_bin.save("images/temp.png")

            imge = cv2.imread("images/temp.png") 
            

            gray = cv2.cvtColor(imge,cv2.COLOR_BGR2GRAY) # grayscale
            _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
            dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
            contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
            height = np.size(imge, 0)
            width = np.size(imge, 1)

            index =1
            rect_dim=[]
            xvalues=[]
            yvalues=[]
            marking=[]
            #finding markings by running OCR on individual numbers by cropping them
            for contour in contours:
                # get rectangle bounding contour
                [x,y,w,h] = cv2.boundingRect(contour)

                # discard areas that are too large
                if h>0.9*height and w>0.9*width:
                   continue
                
                # discard areas that are too small
                if h<height*0.02 or w<width*0.02:
                    continue
                
                # draw rectangle around contour on original image
                cv2.rectangle(imge,(x,y),(x+w,y+h),(255,0,255),2)

                cropped = imge[y :y+h-1 , x : x+w-1]
                print y,y+h,x,x+w
                
                cv2.imwrite("images/crop_temp.png" , cropped)
                #image = cropped
                image = cv2.imread("images/crop_temp.png")

                dst = cv2.fastNlMeansDenoisingColored(image,None,10,10,7,21) 
                number = image_to_string(IMAGE.fromarray(dst),lang='eng')
                xvalues.append(x+w/2)
                yvalues.append(y+h/2)  
                marking.append(number)
                
            cv2.imwrite("images/contoured.jpg", imge) 
               
            li=[]
            #converting markings, which can be converted into float, to float     
            for j in range(0,len(marking)):
                if re.match("^\d+\.?\d+$", marking[j]) is not None:   
                    marking[j]=float(marking[j])  
                    li.append(j)
                if len(li)==3:
                    break
            print li
            print xvalues
            print yvalues
            print marking
            #finding x gradient
            if i==0 and len(li)==3:
                self.dx=(marking[li[0]]-marking[li[1]])*resize/(xvalues[li[0]]-xvalues[li[1]])
                print "xgrad is "+str(self.dx)
                self.isxgradient=True
            #x gradient can't be found    
            elif i==0 and len(li)<3:
                self.isxgradient=False
            #finding y gradient    
            if i==1 and len(li)==3:
                self.dy=(marking[li[0]]-marking[li[1]])*resize/(yvalues[li[0]]-yvalues[li[1]])
                print "ygrad is "+str(self.dy)
                self.isygradient=True
            #y gradient can't be found     
            elif i==1 and len(li)<3:
                self.isygradient=False
            #markings can't be found                
            if len(li)<3 and i==0:
                self.isxmarkings=False
                continue
            if len(li)<3 and i==1:
                self.isymarkings=False
            #finding if graph is log or not         
            try:            
                if (marking[li[0]]/marking[li[1]])**(li[0]*1.0/li[1]) == (marking[li[1]]/marking[li[2]])**(li[1]*1.0/li[2]):
                    self.isLog=True
            except:
                if i==0:
                    self.isxmarkings=False
                else:
                    self.isymarkings=False    

            try:
                if (marking[li[0]]-marking[li[1]])/(li[0]-li[1]) == (marking[li[1]]-marking[li[2]])/(li[1]-li[2]):
                    self.isLog=False
            except:
                if i==0:
                    self.isxmarkings=False
                else:
                    self.isymarkings=False    

            else:
                self.isLog=False


            #finding common difference for non log graphs and thereby appending required missing terms into markings list
            if self.isLog==False:
                try:    
                    cd = (marking[li[0]]-marking[li[1]])/(li[0]-li[1])
                    print cd
                    for j in range(0,len(marking)):
                        marking[j]=marking[li[0]]+cd*(j-li[0])
                except:
                    print "Common difference can't be found"
                    if i==0:
                        self.isxmarkings=False
                    else:
                        self.isymarkings=False    
                    continue
                
                # write original image with added contours to disk  
                
                #marking = sorted(marking,reverse=True)
                
            #finding common difference for log graphs and thereby appending required missing terms into markings list
            if self.isLog==True:
                try:
                    cd = (marking[li[0]]/marking[li[1]])**(li[0]*1.0/li[1])
                    print cd
                    for j in range(1,len(marking)):
                        marking[j]=marking[li[0]]*(cd**(j-li[0])) 
                except:
                    print "Common difference can't be found"
                    if i==0:
                        self.isxmarkings=False
                    else:
                        self.isymarkings=False 
                    continue


            marking=sorted(marking)                
            print marking



            mark_len = len(marking) 
            #returning min and max markings       
            if i==0 :
                self.isxmarkings=True
                self.minx=marking[0]
                self.maxx=marking[mark_len-1]
                self.nummarkX=len(marking)
                print "minx and maxx are:"+str(self.minx)+"  "+str(self.maxx)            
            else:
                self.isymarkings=True
                self.miny=marking[0]
                self.maxy=marking[mark_len-1]
                self.nummarkY=len(marking)
                print "miny and maxy are:"+str(self.miny)+"  "+str(self.maxy)


            if i==0 and self.isxmarkings==False:
                marking=xvalues
                self.nummarkX=len(marking)

            if i==1 and self.isymarkings==False:
                marking=yvalues
                self.nummarkY=len(marking)

    #def findGradient(self):









    #this function not used in the procedure
    #returns number of pixels between two markings on an axis. Call this method once for each axis.
    def findPixelDensity(self):
        for i in range(0,2):
            if i==0:
                try:
                    img = Image("images/temp_x1.png",0)
                except IOError:
                    continue
            else:
                try:
                    img = Image("images/temp_y2.png",0)    
                except IOError:
                    continue
                    
            img_inv = img.invert()
            img_inv.scale(100,100)
            img_bin = img_inv.binarize()

            resize=1
            if img_bin.width<100:
                resize = 1
                img_bin = img_bin.resize(img.width*4,img.height*resize)
            flag=0
            if img_bin.width<img_bin.height:
                flag = 1 
                img_bin = img_bin.rotate(-90,fixed = False)

            img_bin.save("images/temp.png")

            img = cv2.imread("images/temp.png")
            
            img = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) 


            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) # grayscale
            _,thresh = cv2.threshold(gray,150,255,cv2.THRESH_BINARY_INV) # threshold
            kernel = cv2.getStructuringElement(cv2.MORPH_CROSS,(2,2))
            dilated = cv2.dilate(thresh,kernel,iterations = 13) # dilate
            contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE) # get contours
            height = np.size(img, 0)
            width = np.size(img, 1)

            index =1
            rect_dim=[]
            for contour in contours:
                # get rectangle bounding contour
                [x,y,w,h] = cv2.boundingRect(contour)
                y=y+h
                rect = [x,y,w,h]
                
                # discard areas that are too large
                if h>0.9*height and w>0.9*width:
                   continue
                
                # discard areas that are too small
                if h<height*0.02 or w<width*0.02:
                    continue
                #print rect
                cv2.rectangle(img,(x,y),(x+w,y-h),(255,0,255),2)
                rect_dim.append(x+w/2.0) 
            cv2.imwrite("images/contoured.png", img)     

            rect_dim.sort(reverse=True)
            pix_diff=[]
            #print len(rect_dim)
            #print rect_dim
            for i in range(0,len(rect_dim)-1):
                pix_diff.append(rect_dim[i]-rect_dim[i+1])
            print pix_diff 
            pix_diff.sort(reverse=True)
                               
            try:
                print sum(pix_diff)/len(pix_diff)
            except:
                pass

            try:    
                print sum(pix_diff[:-1])/len(pix_diff[:-1])
            except:
                pass
            
            try:
                if abs(sum(pix_diff)/len(pix_diff)-sum(pix_diff[:-1])/len(pix_diff[:-1]))>3:
                    pix_diff.remove(pix_diff[-1])

            except:
                pass


            try:    
                pix_avg=sum(pix_diff)/(len(pix_diff)*1.0)

            except:
                continue

            pix_avg = pix_avg/resize



            if i==0:
                pix_avgx=pix_avg
                print "pix_avgx="+str(pix_avgx)
                self.dx = pix_avgx
                self.isxgradient=True
            else:
                pix_avgy=pix_avg    
                print "pix_avgy="+str(pix_avgy)  
                self.dy = pix_avgy
                self.isygradient=True 
   


    #crops of the extra part at the top of the text box image returned so as to facilitate 
    def findCrop(self):
        if self.istextbox==True:
            for i in range(len(self.textBoxImages)):
                cv2.imwrite("images/temp_textbox.png",self.textBoxImages[i])
                img=IMAGE.open("images/temp_textbox.png")
                # img = cv2.imread("temp_textbox.png")
                # w=np.size(img, 0)
                # h=np.size(img, 1)
                w,h=img.size
                print'img size w=%d h=%d i=%d' %(w,h,i)
                im = img.load()
                y_temp=0
                while(y_temp<h):
                    x_temp=0
                    while(x_temp<w-1):
                        #print y_temp,x_temp,h,w
                        #print im[x_temp,y_temp]
                        if((im[x_temp,y_temp]<(200,200,200) or im[x_temp+1,y_temp]<(200,200,200))):
                            try:
                                img=cv2.imread("images/temp_textbox.png")
                            except:
                                continue
                            cropped = img[y_temp-1:h,0:w]
                            s =  'images/onlylabel_'+str(i+1)+'.png' 
                            cv2.imwrite(s , cropped)
                            return y_temp
                        x_temp+=1 
                    y_temp+=1   
                    print "als x_temp=%d y_temp=%d"%(x_temp,y_temp)

        else:
            pass



    #Returns all the labels and the corresponding colors in HSV of plots in graph in a curve datastructure.
    def findColorNnumOfPlots(self):
        if self.istextbox==True:
            for i in range(len(self.textBoxImages)):
                #flag=0
                s='images/temp_textbox.png'
                try:
                    img = Image(s,0)

                except:
                    continue     
                img_inv = img.invert()
                img_inv.scale(100,100)
                img_bin = img_inv.binarize()
                
                #elif flag!=1:
                img_bin.save("images/rot_1.png")

                img = cv2.imread("images/rot_1.png") 
                dst = cv2.fastNlMeansDenoisingColored(img,None,10,10,7,21) 
                
                graphs = image_to_string(IMAGE.fromarray(dst),lang='eng')
                graphs = graphs.replace("\n",">%$ ")                               #formatting the string to get the list 
                graphs = graphs.split(">%$ ")                                      #of plots plotted in given graphs                               
                print "the plots in graph are"
                print graphs
                graphNamesList=graphs
                n=len(graphs)                                                      #number of plots in given graph
                img = Image(s,0)
                img = img.resize(img.width*3,img.height*3)                         #resizing the image to make it big enough for cropping
                #print height
                #img = img.crop(15,15,img.width,img.height)                   #removing the edges of the given graph description image
                try:
                    height = (img.height)*1.0/n
                except ZeroDivisionError:
                    continue
                width = img.width 
                graphList=[]
                start = 0
                for i in range(0,n):                                               #cropping the image so as to get a single plot description 
                    cropImg = img.crop(0, start, width, height)                   #in one image
                    graphList.append(cropImg)
                    start+=height
                
                graphList1 = graphList    
               
                
                graphColor = []
                for i in graphList:                                                #finding colors of plots of all the images cropped above
                    i.save("images/temp.png")    
                    #raw_input()
                    imge = cv2.imread("images/temp.png",1)
                    kernel = np.ones((5,5),np.uint8)
                    #imge = cv2.erode(imge,kernel,iterations=3)
                    cv2.imwrite("aman.jpg",imge)
                    imge = cv2.fastNlMeansDenoisingColored(imge,None,10,10,7,21) 
                    imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
                
                    imge = imge.reshape((imge.shape[0] * imge.shape[1], 3))
                    n_clusters = 3                                                 #number of clusters in kmeans clustering
                    clt = KMeans(n_clusters = 3)
                    clt.fit(imge)
                    hist = centroid_histogram(clt)
                    bar,color = plot_colors(hist, n_clusters, clt.cluster_centers_)
                  
                    
                    print color
                    if color[0]>240 and color[1]>240 and color[2]>240:             
                        color = [10.00, 10.00, 10.00]
                    
                    #color = list(rgb2hsv(color[0],color[1],color[2]))
                    
                    graphColor.append(color)                                    
                    
                    
                for i in range(0,len(graphColor)):
                    c = curve(graphColor[i],graphNamesList[i])
                    
                     
                    self.curveList.append(c)
                
                print graphNamesList
                print graphColor
                print self.curveList

        else:
            pass


    def findonlycolors(self):
        graphColor = []
        midpoint=(self.x2+self.x4)/2
        cropped = self.rectangle[self.y4:self.x2, midpoint-50:midpoint+50]
        cv2.imwrite("images/colors.jpg" , cropped)
        imge = cv2.imread("images/colors.jpg",1)
        #imge = cv2.fastNlMeansDenoisingColored(imge,None,10,10,7,21) 
        #imge = cv2.cvtColor(imge, cv2.COLOR_BGR2RGB)
        

        imge = imge.reshape((imge.shape[0] * imge.shape[1], 3))
        n_clusters = 3                                                 #number of clusters in kmeans clustering
        clt = KMeans(n_clusters = 8)
        clt.fit(imge)
        hist = centroid_histogram(clt)
        bar,color = plot_colors_only(hist, n_clusters, clt.cluster_centers_)   #returns all the colors present in the given image "colors.jpg"
        # bar = cv2.cvtColor(bar,cv2.COLOR_GRAY2RGB) 
         # show our color bart
        # plt.figure()
        # plt.axis()
        # plt.imshow(bar)
        # plt.show()


        # color = list(rgb2hsv(color[0],color[1],color[2]))
        #color[1] = color[1]                                      #increasing the picture saturation and value of the image
        #color[2] = color[2]                                       #which got reduced due to processing
        #color = hsv2rgb(color[0],color[1],color[2])     
        print color                                               #list of colors of all the plots in the graph image
        print "len=%d"%(len(color))
        for var in range(0,len(color)):
            # if color[var][0]>240 and color[var][1]>240 and color[var][2]>240:
            #     color[var][0] = 10.00
            #     color[var][1] = 10.00
            #     color[var][2] = 10.00
            c = curve(color[var],"curve"+str(var))
            self.curveList.append(c)
            print color[var]







    #gets all the x values and corresponding y values of each plot in the graph and stores in curve object's attributes
    def fillData(self):
        #table=np.zeros((len(self.curveList),self.y2-self.y4,2))
        for i in self.curveList:
            if i.color[0]>240 and i.color[1]>240 and i.color[2]>240:
                self.curveList.remove(i)

        last = np.zeros(len(self.curveList))
        current = np.zeros(len(self.curveList))
        mean = np.zeros(len(self.curveList))
        samples = np.zeros(len(self.curveList))

        print "entered fill data"
        print len(self.curveList)
        print self.minx
        print self.dx
        for i in range(self.x4+1,self.x2-1):
            #print "found x coord " +str(i)
            for k in range(0,len(self.curveList)):
                current[k]=-1
            for j in range(self.y4+1,self.y2-1):
                #print j
                for k in range(0,len(self.curveList)):
                    #print self.image[j,i]
                    ar=np.array(self.curveList[k].color)
                    ar0=ar+30
                    ar1=ar-30
                    if self.image[j,i][0]<ar0[0] and self.image[j,i][2]<ar0[2] and self.image[j,i][1]<ar0[1] and self.image[j,i][0]>ar1[0] and self.image[j,i][2]>ar1[2] and self.image[j,i][1]>ar1[1]:
                        #replace image list with appropriatre  object
                        #if i< self.x4+1 +50 or last[k]== 0 or (self.maxy-(j-1-self.y4)*self.dy>=mean[k]-(self.maxy-self.miny)/20 and self.maxy-(j-1-self.y4)*self.dy<=mean[k]+(self.maxy-self.miny)/20) : #table[k,last[k]][1] last y value in the table

                        if last[k]== 0 or (self.maxy-(j-1-self.y4)*self.dy>=self.curveList[k].y[int(last[k])-self.x4-1]-(self.maxy-self.miny)/15 and self.maxy-(j-1-self.y4)*self.dy<self.curveList[k].y[int(last[k])-self.x4-1]+(self.maxy-self.miny)/15) : #table[k,last[k]][1] last y value in the table
                            current[k] = j
                            # if k ==2:
                            #     print "red @" + str(j)
                            #     print last[2]
                            
            #print current[2]
            for p in range(0,len(self.curveList)):
                if current[p]>=0:
                    
                    self.curveList[p].x.append((i-self.x4-1)*self.dx+self.minx)
                    self.curveList[p].y.append(self.maxy-(current[p]-self.y4)*self.dy)
                    last[p]=i
                    mean[k] = (mean[p]*samples[p]+ ((i-self.x4-1)*self.dx+self.minx))/(samples[p]+1)
                    samples[k]= samples[k]+1
                    # else:
                    #     self.curveList[k].x.append(self.minx+(i-self.x4-1)*self.dx)
                    #     self.curveList[k].y.append(self.maxy/math.exp(self.dy))
                    #     #table[k,i]=[self.minx+i*self.dx,self.miny+math.exp(self.dy)]
                    #     last[k]= i
                else:
                    self.curveList[p].x.append((i-self.x4-1)*self.dx+self.minx)
                    self.curveList[p].y.append("not found")            
            
        for k in range(0,len(self.curveList)):
            for i in range(self.x4+1,self.x2-1):
                try:
                    print str(self.curveList[k].x[i-self.x4-1]) +" , "+ str(self.curveList[k].y[i-self.x4-1]) 
                except:
                    pass
        
  
   
def centroid_histogram(clt):   
    numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)                   # grab the number of different clusters and create a histogram
    (hist, _) = np.histogram(clt.labels_, bins = numLabels)                     # based on the number of pixels assigned to each cluster
  
    hist = hist.astype("float")                                                 # normalize the histogram, such that it sums to one
    hist /= hist.sum()
 
    return hist                                                                 # return the histogram


def plot_colors(hist, n_clusters, centroids):
    bar = np.zeros((50, 300, 3), dtype = "uint8")                               # initialize the bar chart representing the relative frequency
    startX = 0                                                                  # of each of the colors
    
 
    i = 0                                                                       # loop over the percentage of each cluster and the color of
    mini = 300                                                                  # each cluster
    colval = 0
    for (percent, color) in zip(hist, centroids):
        endX = startX + (percent * 300)                                         # plot the relative percentage of each cluster
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        
        flag=0
        
        temp=endX-startX     
        if temp<mini and ((color[0]-color[1])>3 or (color[1]-color[0])>3 or (color[2]-color[1])>3 or (color[1]-color[2])>3 or (color[2]-color[0])>3 or (color[0]-color[2])>3):
            mini = temp
            flag=1
            colval = i    
        i=i+1
         

    color_req = centroids[colval]
    return bar,color_req
    

def plot_colors_only(hist, n_clusters, centroids):
    bar = np.zeros((50, 300, 3), dtype = "uint8")                               # initialize the bar chart representing the relative frequency
    startX = 0                                                                  # of each of the colors
    
 
    i = 0                                                                       # loop over the percentage of each cluster and the color of
    mini = 300                                                                  # each cluster
    colval = 0
    allcolors = []
    for (percent, color) in zip(hist, centroids):
        # print "color:"
        # print color
        allcolors.append(color)
        endX = startX + (percent * 300)                                         # plot the relative percentage of each cluster
        cv2.rectangle(bar, (int(startX), 0), (int(endX), 50),
            color.astype("uint8").tolist(), -1)
        
        flag=0
        """
        if color[0]>240 and color[1]>240 and color[2]>240:
             i=i+1
             startX = endX
             continue
             """
        temp=endX-startX     
        if temp<mini and ((color[0]-color[1])>3 or (color[1]-color[0])>3 or (color[2]-color[1])>3 or (color[1]-color[2])>3 or (color[2]-color[0])>3 or (color[0]-color[2])>3):
            mini = temp
            flag=1
            colval = i    
        i=i+1
        startX = endX 
        """
        if flag==1 and color[0]>240 and color[1]>240 and color[2]>240:
             i=i+1
             startX = endX
             continue
             """      
            #color_req = color
        #startX = endX
    # return the bar chart
    print colval
    color_req = centroids[colval]
    return bar,allcolors









def rgb2hsv(r, g, b):
    r, g, b = r/255.0, g/255.0, b/255.0
    mx = max(r, g, b)
    mn = min(r, g, b)
    df = mx-mn
    if mx == mn:
        h = 0
    elif mx == r:
        h = (60 * ((g-b)/df) + 360) % 360
    elif mx == g:
        h = (60 * ((b-r)/df) + 120) % 360
    elif mx == b:
        h = (60 * ((r-g)/df) + 240) % 360
    if mx == 0:
        s = 0
    else:
        s = df/mx
    v = mx
    return h, s, v
    
    
    
def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return r, g, b    
    

