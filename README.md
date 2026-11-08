# ISN S4 Project - VOYAGE VOYAGE

## Description
This project allows users to plan a complete train trip and create optimized itineraries to visit places once at the destination. The visiting order is defined to minimize the walking distance between successive locations.

The user enters:
- a departure city and an arrival city (in France),
- a departure date and time, as well as a return date and time,
- the categories of places they wish to visit (Museums, Parks, Monuments, Gastronomy),
- and the accommodation of their choice.

The algorithm first queries the SNCF API to suggest the best train routes. Then, it generates a daily itinerary whose starting and ending point is the hotel provided by the user. Each day includes a maximum of 3 places to visit, ordered to minimize distances using a nearest neighbor algorithm.

Places and hotels are selected using OpenStreetMap data via the osmnx library, guaranteeing real coordinates.

## Getting Started

### Installation:
Simply download the zip folder and extract it.
The application requires a few libraries. To install all necessary dependencies, simply run the following command in your terminal:

```bash
pip install customtkinter tkintermapview requests pandas osmnx Pillow
```

### Running the application
In the project folder, simply run `python main.py` and everything should work normally.

## Compatibility
This application works on Linux. However, please note that CustomTkinter has certain technical limitations on this environment.
Although the logic and features remain intact, this may cause:
- Variations in the visual rendering of component corner radii (corner_radius).
- A different font than expected.
- A less accurate aesthetic appearance than on Windows or macOS.

```bash
python main.py
```

## Latency and potential bugs:
Latency or bugs may occur, especially on the hotel search and activity search pages.
In case of minor bugs or latency exceeding one minute, it may be necessary and recommended to Restart Kernel (En) or Redemarrer le noyau (Fr). To do this, go to the Consoles section in Spyder.

## Instructions:

### Configuration Window
- The user inputs the departure and arrival city - (IMPORTANT: due to the use of the SNCF API, these must be French cities served by the network).
- The user also inputs the dates and times, and checks the desired categories.
- Once all steps are completed, to move to the next step, the user clicks "Rechercher Itinéraires".

### Train Window:
- In this window, the user sees the top 5 routes found. The shortest route is highlighted.
- The user must select an outbound and return journey, then validate.

### Map Window (Accommodation):
- Accommodations will be suggested in a grid format. Due to osmnx limitations, some minor accommodations may not be present.
- The user clicks "Réserver" under the hotel of their choice to proceed.

### Activity Selection Window:
- The user can check the activities they actually want to do. A counter limits the selection to 3 activities per day on site (calculated based on train dates).
- Once the selection is complete, they click "Planifier mes journées".

### Planning Window:
- The optimized itinerary is displayed day by day.
- If the order is not suitable, the user can click the "⇄ Échanger" button between two different activities to manually modify the schedule.
- To conclude, they click "Générer le Carnet".

### Roadbook Window:
- The program displays the final interactive map with numbered markers and a text summary on the right, including estimated walking times between each step.

## Authors
- Boënnec Gaël (75%)
- Alduy Mathis (10%)
- Diop Mame Diarra (5%)
- Vernay Frecon Leila (5%)
- Delgado Carrero Renata (5%)
