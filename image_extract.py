#requires ghosht script
import subprocess

pdf_path = "a.pdf"
Extraction = subprocess.call("gs -sDEVICE=pngalpha -o file-%03d.png -sDEVICE=pngalpha -r144 " +pdf_path,shell=True)
print 
