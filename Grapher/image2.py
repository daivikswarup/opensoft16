#requires ghosht script
import subprocess

pdf_path = "a.pdf"
Extraction = subprocess.call("gs -sDEVICE=jpeg -dQUIET  -o file-%03d.jpg -r144 " +pdf_path,shell=True)
