from picamera2 import Picamera2
import cv2
import threading
import time
from api import facial_expression
from servo import servo_control_slow

# 初始化摄像头
picam2 = Picamera2()
config = picam2.create_video_configuration(
    main={"format": "RGB888", "size": (640, 480)}
)
picam2.configure(config)
picam2.start()

# 设置全画幅
full_crop = picam2.camera_properties["ScalerCropMaximum"]
picam2.set_controls({"ScalerCrop": full_crop})

# 共享变量：保存最新的一帧
latest_frame = None
frame_lock = threading.Lock()

def recognize_loop():
    global latest_frame
    while True:
        time.sleep(1)  
        with frame_lock:
            if latest_frame is not None:
                frame_to_process = latest_frame.copy()  # 深拷贝防止变化
            else:
                continue

        save_path = "latest.jpg"   # 也可以加时间戳，不同名字
        cv2.imwrite(save_path, frame_to_process)
        emotion,err = facial_expression(save_path)
        if err != None:
            print(err)
            continue

        if emotion == 'happy':
            print(f"facial_expression is happy")
            servo_control_slow()
        else:
            print(f"facial_expression is not happy")


# 开一个后台线程
recognize_thread = threading.Thread(target=recognize_loop, daemon=True)
recognize_thread.start()


# 主循环：采集、显示
while True:
    frame = picam2.capture_array()
    with frame_lock:
        latest_frame = frame
    cv2.imshow("Full FOV Video", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
