## labelDIY.py
### Usage
```
py labelDIY.py --dst <Output directory> --src <Input directories>
```
### Comments
1. .csv file format    
Input files must have the format of "First row: Time, Voltage".  
![img_1](https://user-images.githubusercontent.com/20588061/109459601-77e94900-7aa2-11eb-93a7-16ad24b2d34d.png)  
Output files will have the format of "First row: Time, Voltage, Label".  
![img_2](https://user-images.githubusercontent.com/20588061/109459610-7c156680-7aa2-11eb-991d-0285a7962de5.png)  
2. Input directory and output directory must be different in order to prevent overwrite.  
3. Multiples input directories supported.  
