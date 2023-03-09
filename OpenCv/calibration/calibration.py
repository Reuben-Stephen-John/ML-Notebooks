import numpy as np
import cv2 as cv
import glob

chessboardSize=(9,6)
frameSize=(1280,720)

# termination criteria
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((chessboardSize[0]*chessboardSize[1],3), np.float32)
objp[:,:2] = np.mgrid[0:chessboardSize[0],0:chessboardSize[1]].T.reshape(-1,2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob("C:\Reuben's Code's\ML-Notebooks\OpenCv\calibration\dataset\*.jpg")
for fname in images:
    print(fname)
    img = cv.imread(fname)
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv.findChessboardCorners(gray, chessboardSize,None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        objpoints.append(objp)

        corners2 = cv.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)

        # Draw and display the corners
        cv.drawChessboardCorners(img, chessboardSize, corners2,ret)
        cv.imshow('img',img)
        cv.waitKey(100)

cv.destroyAllWindows()

ret, mtx, dist, rvecs, tvecs = cv.calibrateCamera(objpoints, imgpoints, frameSize,None,None)

print( "Camera Calibrated: ",ret)
print("\nCamera Matrix: \n", mtx)
print("\nDistortion Parameters:\n", dist)
print("\nRotation Vectors: \n", rvecs)
print("\nTrans1ation Vectors:\n", tvecs)

### UNDISTORTION #####

img = cv.imread("C:\Reuben's Code's\ML-Notebooks\OpenCv\calibration\dataset\WIN_20230228_22_15_39_Pro.jpg")
h,  w = img.shape[:2]
newcameramtx, roi=cv.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))

# undistort
dst = cv.undistort(img, mtx, dist, None, newcameramtx)
#crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite("C:\Reuben's Code's\ML-Notebooks\OpenCv\calibration\dataset\calibresult1.png",dst)

# undistort with remapping
mapx,mapy = cv.initUndistortRectifyMap(mtx,dist,None,newcameramtx,(w,h),5)
dst = cv.remap(img,mapx,mapy,cv.INTER_LINEAR)
#crop the image
x,y,w,h = roi
dst = dst[y:y+h, x:x+w]
cv.imwrite("C:\Reuben's Code's\ML-Notebooks\OpenCv\calibration\dataset\calibresult2.png",dst) 

#reporjection error
mean_error = 0
for i in range(len(objpoints)):
    imgpoints2, _ = cv.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
    error = cv.norm(imgpoints[i],imgpoints2, cv.NORM_L2)/len(imgpoints2)
    mean_error += error

print( "total error: ", mean_error/len(objpoints))
print("\n")