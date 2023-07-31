# WhatsApp Chat Analyzer

## Demo
![WhatsApp Chat Analyzer](whatsapp-demo.gif)

WhatsApp Chat Analyzer is a Python-based web application built using Streamlit that allows you to analyze and visualize the content of a WhatsApp chat. With this app, you can gain insights into chat statistics, user activity, message timelines, word usage, and more.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [How to Use](#how-to-use)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Features

- Extracts and processes chat data from a WhatsApp chat export file.
- Provides statistics such as total messages, total words, and most active users.
- Displays monthly and daily timelines of message flow.
- Generates word clouds and shows the most common words used in the chat.
- Visualizes user activity with activity maps and heatmaps.

## Getting Started

### Prerequisites

- Python 3.7 or higher
- Conda or virtual environment (optional but recommended)

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/whatsapp-chat-analyzer.git
cd whatsapp-chat-analyzer
```

2. (Optional) Set up a virtual environment (recommended):

```bash
# Using Conda
conda create --name whatsapp-analyzer python=3.8
conda activate whatsapp-analyzer

# Using virtualenv
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

3. Install the required packages:

```bash
pip install streamlit pandas matplotlib seaborn wordcloud
```

## How to Use

1. Export your WhatsApp chat history:
   - Open the WhatsApp chat you want to analyze.
   - Tap the three dots menu (⋮) and select "More."
   - Choose "Export chat" and select "Without media" or "Include media" based on your preference.
   - Send the chat export to yourself via email or save it to a location accessible on your computer.

2. Run the Streamlit app:

```bash
streamlit run whatsapp_analyzer.py
```

3. In the app's sidebar, upload the exported WhatsApp chat file.

4. Select the user you want to analyze from the drop-down menu or choose "Overall" for an overall analysis.

5. Click on the "Show Analysis" button to view the various visualizations and statistics.

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, feel free to create a pull request or submit an issue.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- The app uses Streamlit (https://streamlit.io/) to create the web interface.
- Thanks to the developers of pandas, matplotlib, seaborn, and wordcloud for the excellent Python libraries used in this project.

---
Created by [Shahbaz Khan](https://github.com/Shahbazkhan555)
```
