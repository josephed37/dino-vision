# 🦖 Dino Vision

**Dino Vision** is a classic side-scrolling dinosaur game, similar to the one found in the Chrome browser, built from scratch with **Python** and **Pygame**.

The project's ultimate goal is to move beyond traditional keyboard controls and implement **real-time gesture control** using computer vision.

![Dino Vision Screenshot](assets/dino.png)

---

## ✅ Current Features (Phase 1 Complete)

The game is currently in a fully playable and polished state with keyboard controls. It includes:

- **Complete Game Loop**  
  A robust loop that handles player input, game state changes (playing, game over), and restarting.

- **Animated Player Character**  
  A fully animated dinosaur with separate animations for running, jumping, and dying.

- **Dynamic Obstacles**  
  Randomly spawning obstacle sprites that challenge the player.

- **Scrolling Environment**  
  A multi-layered, parallax background and seamless tiled ground create an illusion of depth and movement.

- **Progressive Difficulty**  
  The game’s speed gradually increases over time for added challenge.

- **Time-Based Physics**  
  All movement and animations are delta time-driven, ensuring smooth performance regardless of frame rate.

- **Scoring System**  
  Includes a real-time score display and a persistent high-score system saved to a file.

---

## 🔭 Project Roadmap (What's Next)

The next major phase of this project is to integrate computer vision for a unique control scheme:

### Phase 2: OpenCV Gesture Control

- **Webcam Integration**  
  Capture a live video feed from the user's webcam.

- **Hand Tracking**  
  Use libraries like **OpenCV** and **MediaPipe** to identify the position and landmarks of the user's hand in real time.

- **Gesture Recognition**  
  Recognize specific gestures (e.g., open palm, raised finger) to trigger the "jump" command.

- **Control Integration**  
  Replace the spacebar input with recognized gestures for completely hands-free dino control.

---

## 🚀 How to Run the Project

1. **Clone the Repository**  

   ```bash
   git clone git@github.com:josephed37/dino-vision.git
   cd dino-vision
   ```

2. **Set Up a Virtual Environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Game**

   ```bash
   python3 main.py
   ```
