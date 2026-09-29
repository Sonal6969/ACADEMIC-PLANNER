# Academic Scheduler (Study Planner) 🎓

A sleek, dark-mode desktop application built with Python to help students track academic tasks, assignments, and deadlines. Designed specifically with native macOS integrations for alerts and sounds.

## 🌟 Features
* **Modern UI:** Built using `customtkinter` for a beautiful, responsive dark-mode interface.
* **Task Management:** Easily Add, Edit, and Delete academic tasks.
* **Smart Organization:** Track tasks alongside your current Academic Year and Semester.
* **Color-Coded Statuses:** Visually distinguishes between Pending, Urgent, Today, and Missed tasks.
* **Native macOS Notifications:** Runs a background checker to deliver Apple system notifications (banners) and native system sounds (`afplay`) when tasks become Urgent, are due Today, or get Missed.
* **Local Storage:** Saves all user data and tasks locally using JSON formatting so you never lose your progress.

## 📋 Prerequisites
Because this app utilizes native macOS terminal commands for sounds and banners, it is designed to run on **macOS**. 

You will need:
* Python 3.10 or newer (Installed via python.org or Homebrew, *not* the macOS default system Python)
* `customtkinter` library

## ⚙️ Installation

1. Clone this repository to your local machine:
   ```bash
   git clone [https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git](https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git)
