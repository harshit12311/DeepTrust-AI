import cv2


def preprocess_video(video_path):
    """
    Read a video and return sampled RGB frames.
    No resizing or preprocessing is done here.
    """

    video_capture = None

    try:
        video_capture = cv2.VideoCapture(video_path)

        if not video_capture.isOpened():
            return None

        frames = []
        frame_index = 0

        while True:
            success, frame = video_capture.read()

            if not success:
                break

            # Sample one frame every 30 frames
            if frame_index % 30 == 0:
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                frames.append(rgb_frame)

            frame_index += 1

        return frames

    except (cv2.error, OSError, TypeError):
        return None

    finally:
        if video_capture is not None:
            video_capture.release()