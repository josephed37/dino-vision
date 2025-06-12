import cv2
import threading
import mediapipe as mp
# The line "from game.components.vision import Vision" has been removed from here

class Vision:
    """
    A class to manage webcam capture and hand tracking in a separate thread.
    """
    def __init__(self):
        """Initialize webcam, MediaPipe Hands, and start the reader thread."""
        self.cap = cv2.VideoCapture(0)
        if not self.cap.isOpened():
            print("Error: Cannot open webcam.")
            self.is_running = False
            return

        self.is_running = True
        self.latest_frame = None
        self.latest_results = None
        self.lock = threading.Lock()

        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
            max_num_hands=1
        )
        self.mp_drawing = mp.solutions.drawing_utils

        self.thread = threading.Thread(target=self._reader_thread, daemon=True)
        self.thread.start()
        print("Webcam and MediaPipe Hands successfully initialized.")

    def _reader_thread(self):
        """The private method that runs in a separate thread to process frames."""
        while self.is_running:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to grab frame from webcam.")
                break
            
            frame = cv2.flip(frame, 1)

            frame.flags.writeable = False
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.hands.process(frame_rgb)
            frame.flags.writeable = True

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS
                    )
            
            with self.lock:
                self.latest_frame = frame
                self.latest_results = results
        
        self.cap.release()
        self.hands.close()
        print("Reader thread has finished and released resources.")

    def update(self):
        """Returns the most recent annotated frame and hand tracking results."""
        with self.lock:
            return self.latest_frame, self.latest_results

    def close(self):
        """Signals the reader thread to stop and waits for it to finish."""
        if self.is_running:
            self.is_running = False
            self.thread.join()
            print("Successfully joined reader thread.")
        
        cv2.destroyAllWindows()
        print("All OpenCV windows closed.")
