import cv2


def preprocess_video(video_path):
    """Read a video and preprocess sampled frames for model inference."""
    video_capture = None

    try:
        video_capture = cv2.VideoCapture(video_path)

        if not video_capture.isOpened():
            return None

        processed_frames = []
        frame_index = 0

        while True:
            success, frame = video_capture.read()
            if not success:
                break

            # Sample one frame every 30 frames to reduce processing overhead.
            if frame_index % 30 == 0:
                resized_frame = cv2.resize(frame, (224, 224))
                rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                processed_frames.append(rgb_frame)

            frame_index += 1

        return processed_frames
    except (cv2.error, OSError, TypeError):
        return None
    finally:
        if video_capture is not None:
            video_capture.release()
