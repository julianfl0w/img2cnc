# img2cnc
 Convert an image to CNC GCODE  
## Usage
```
pip install opencv-python  
pip install numpy  
# all sizes in inches
python img2cnc.py --width 10 --height 12 --image Lenna.png --headsize 0.1 --headsperpixel 2 --colors 5
```

## Output Images
![image](https://user-images.githubusercontent.com/8158655/184055867-c03187c0-f32a-4726-80dd-754b9ac71717.png)  
  
## Sample Output GCODE
```
        PUT INITIALIZATION GCODE HERE
            GOTO X=0.0, Y=0.0, Z=1;
    GOTO X=1.0, Y=0.0, Z=1;
    GOTO X=0.0, Y=0.1, Z=1;
    GOTO X=1.0, Y=0.1, Z=1;
    GOTO X=0.0, Y=0.2, Z=1;
    GOTO X=1.0, Y=0.2, Z=1;
    GOTO X=0.0, Y=0.30000000000000004, Z=1;
    GOTO X=1.0, Y=0.30000000000000004, Z=1;
    GOTO X=0.0, Y=0.4, Z=1;
    GOTO X=1.0, Y=0.4, Z=1;
    GOTO X=0.0, Y=0.5, Z=1;
    GOTO X=1.0, Y=0.5, Z=1;
    GOTO X=0.0, Y=0.6000000000000001, Z=1;
    GOTO X=1.0, Y=0.6000000000000001, Z=1;
    GOTO X=0.0, Y=0.7000000000000001, Z=1;
    GOTO X=1.0, Y=0.7000000000000001, Z=1;
```
