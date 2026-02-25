# ndt_quiz_app.py - NDT Quiz System for Mechanical & CSE Departments

import streamlit as st
import json
import random
import datetime
import pandas as pd
from io import BytesIO
import time

# --- Third-party libraries ---
import gspread
from streamlit_autorefresh import st_autorefresh

# --- PDF Generation Libraries ---
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER

# =====================================================================================
# --- 📝 CONFIGURATION & CONSTANTS ---
# =====================================================================================
APP_TITLE = "Department Quiz System"
QUESTIONS_PER_QUIZ = 20
QUIZ_DURATION_MINUTES = 5
QUIZ_DURATION_SECONDS = QUIZ_DURATION_MINUTES * 60
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

# =====================================================================================
# --- 🎓 STUDENT ROLL DATA ---
# =====================================================================================

MECHANICAL_STUDENTS = [
    {"roll": "2403713811421001", "reg": "2403713811421001", "name": "ARJUN K"},
    {"roll": "2403713811421002", "reg": "2403713811421002", "name": "ASHWIN S"},
    {"roll": "2403713811421003", "reg": "2403713811421003", "name": "DEV ANANTH R"},
    {"roll": "2403713811421004", "reg": "2403713811421004", "name": "DHANWANTH R"},
    {"roll": "2403713811421005", "reg": "2403713811421005", "name": "GIRITHARAN N"},
    {"roll": "2403713811421006", "reg": "2403713811421006", "name": "HARISH KUMAR S P"},
    {"roll": "2403713811421007", "reg": "2403713811421007", "name": "KALAISELVAN S"},
    {"roll": "2403713811421008", "reg": "2403713811421008", "name": "KAMALESHWARAN P"},
    {"roll": "2403713811421009", "reg": "2403713811421009", "name": "MADHAN KUMAR S"},
    {"roll": "2403713811421010", "reg": "2403713811421010", "name": "MADHESH G A"},
    {"roll": "2403713811421011", "reg": "2403713811421011", "name": "MAGESHWARAN M"},
    {"roll": "2403713811421012", "reg": "2403713811421012", "name": "MARI SELVAM P"},
    {"roll": "2403713811421013", "reg": "2403713811421013", "name": "NAVANEETHAN B"},
    {"roll": "2403713811421014", "reg": "2403713811421014", "name": "PRANAV R"},
    {"roll": "2403713811421015", "reg": "2403713811421015", "name": "PRANAVAN S"},
    {"roll": "2403713811421016", "reg": "2403713811421016", "name": "RATHIEESH M"},
    {"roll": "2403713811422017", "reg": "2403713811422017", "name": "SENBAGAPRIYA S"},
    {"roll": "2403713811421018", "reg": "2403713811421018", "name": "SIVA HARRIS S"},
    {"roll": "2403713811421019", "reg": "2403713811421019", "name": "YOKESH S"},
    {"roll": "2403713811421301", "reg": "2403713811421301", "name": "HARINATH S"},
    {"roll": "2403713811421302", "reg": "2403713811421302", "name": "KABILL K"},
    {"roll": "2403713811421303", "reg": "2403713811421303", "name": "KATHIROLI S"},
    {"roll": "2403713811421304", "reg": "2403713811421304", "name": "KISHORE R"},
    {"roll": "2403713811421305", "reg": "2403713811421305", "name": "NAVEEN J"},
    {"roll": "2403713811421306", "reg": "2403713811421306", "name": "NISHANTH R M"},
    {"roll": "2403713811421307", "reg": "2403713811421307", "name": "PRASANNA T"},
    {"roll": "2403713811421308", "reg": "2403713811421308", "name": "RAMESH V"},
    {"roll": "2403713811421309", "reg": "2403713811421309", "name": "SABARISH P"},
    {"roll": "2403713811421310", "reg": "2403713811421310", "name": "SAI SARAN S C"},
    {"roll": "2403713811421311", "reg": "2403713811421311", "name": "SIVABALAN J"}
]

CSE_STUDENTS = [
    {"roll": "7138230206", "reg": "71382302061", "name": "JEESHA S"},
    {"roll": "7138230206", "reg": "71382302062", "name": "JEEVA BHARATHI M"},
    {"roll": "7138230206", "reg": "71382302063", "name": "JEEVAPRIYADHARSHAN S"},
    {"roll": "7138230206", "reg": "71382302064", "name": "JISHA J"},
    {"roll": "7138230206", "reg": "71382302065", "name": "JOELSUMAN A"},
    {"roll": "7138230206", "reg": "71382302066", "name": "JOHN SAMUEL R"},
    {"roll": "7138230206", "reg": "71382302067", "name": "KALAIVANAN K"},
    {"roll": "7138230206", "reg": "71382302068", "name": "KANAGARAJ G"},
    {"roll": "7138230206", "reg": "71382302069", "name": "KANAGAVEL M"},
    {"roll": "7138230207", "reg": "71382302070", "name": "KARSHNA B"},
    {"roll": "7138230207", "reg": "71382302071", "name": "KARTHICK S"},
    {"roll": "7138230207", "reg": "71382302072", "name": "KARTHIKA P"},
    {"roll": "7138230207", "reg": "71382302073", "name": "KAVIN VEL SELVARAJ"},
    {"roll": "7138230207", "reg": "71382302074", "name": "KAVIYA SREE R"},
    {"roll": "7138230207", "reg": "71382302075", "name": "KAVYA S"},
    {"roll": "7138230207", "reg": "71382302076", "name": "KIRISH R"},
    {"roll": "7138230207", "reg": "71382302077", "name": "KIRUBANITHI P"},
    {"roll": "7138230207", "reg": "71382302078", "name": "KIRUTHIGA SREE S V"},
    {"roll": "7138230207", "reg": "71382302079", "name": "KOHARANI J"},
    {"roll": "7138230208", "reg": "71382302080", "name": "KOWSALYA R"},
    {"roll": "7138230208", "reg": "71382302081", "name": "KOWSALYA S"},
    {"roll": "7138230208", "reg": "71382302082", "name": "KOWSHIK BALAJIE G S"},
    {"roll": "7138230208", "reg": "71382302083", "name": "KRISHNAKANTH M"},
    {"roll": "7138230208", "reg": "71382302084", "name": "LAKSHMANAN M"},
    {"roll": "7138230208", "reg": "71382302085", "name": "LEENASRI J"},
    {"roll": "7138230208", "reg": "71382302086", "name": "LOGADHARINISH V"},
    {"roll": "7138230208", "reg": "71382302087", "name": "MADHAVAN R"},
    {"roll": "7138230208", "reg": "71382302088", "name": "MADHUJITH B"},
    {"roll": "7138230208", "reg": "71382302089", "name": "MAHALAKSHMI R"},
    {"roll": "7138230209", "reg": "71382302090", "name": "MALAVIKHA A"},
    {"roll": "7138230209", "reg": "71382302091", "name": "MANOJ KUMAR N"},
    {"roll": "7138230209", "reg": "71382302092", "name": "MATHAN K"},
    {"roll": "7138230209", "reg": "71382302093", "name": "MITHUN SHRI K M"},
    {"roll": "7138230209", "reg": "71382302094", "name": "MOHAMED ARSATH A"},
    {"roll": "7138230209", "reg": "71382302095", "name": "MOHAMED IMRAN M"},
    {"roll": "7138230209", "reg": "71382302096", "name": "MOHAMMED FAZAL P M"},
    {"roll": "7138230209", "reg": "71382302097", "name": "MOHAMMED SAIFULLAH M"},
    {"roll": "7138230209", "reg": "71382302098", "name": "MOKITHA W"},
    {"roll": "7138230209", "reg": "71382302099", "name": "MONISHA A"},
    {"roll": "7138230210", "reg": "71382302100", "name": "MONISHA K"},
    {"roll": "7138230210", "reg": "71382302101", "name": "MONISHA S"},
    {"roll": "7138230210", "reg": "71382302102", "name": "MONISHKUMAR R"},
    {"roll": "7138230210", "reg": "71382302103", "name": "MUGIL K"},
    {"roll": "7138230210", "reg": "71382302104", "name": "NANDA KISHORE M"},
    {"roll": "7138230210", "reg": "71382302105", "name": "NANDHA GOPAL M"},
    {"roll": "7138230210", "reg": "71382302106", "name": "NANDHINI B"},
    {"roll": "7138230210", "reg": "71382302107", "name": "NAVEENA M"},
    {"roll": "7138230210", "reg": "71382302108", "name": "NITHIN R"},
    {"roll": "7138230210", "reg": "71382302109", "name": "NITHISH KUMAR S"},
    {"roll": "7138230211", "reg": "71382302110", "name": "NITHISH M S"},
    {"roll": "7138230211", "reg": "71382302111", "name": "NITHYASHREE R"},
    {"roll": "7138230211", "reg": "71382302112", "name": "PADMA SARAN D"},
    {"roll": "7138230211", "reg": "71382302113", "name": "PERUMAL G"},
    {"roll": "7138230211", "reg": "71382302114", "name": "PIYUSH N S"},
    {"roll": "7138230211", "reg": "71382302115", "name": "POOJA M"},
    {"roll": "7138230211", "reg": "71382302116", "name": "POOVIZHI THANGAM V"},
    {"roll": "7138230211", "reg": "71382302117", "name": "PRASANNA V"},
    {"roll": "7138230211", "reg": "71382302118", "name": "PRASANTH M S"},
    {"roll": "7138230211", "reg": "71382302119", "name": "PREETHI S R"},
    {"roll": "7138230212", "reg": "71382302120", "name": "PREM KISHORE K"}
]

# =====================================================================================
# --- 🧠 NDT QUESTION BANK (MECHANICAL ENGINEERING) ---
# =====================================================================================

# Course Outcomes mapping:
# CO1: Visual inspection techniques
# CO2: Penetrant testing
# CO3: Thermographic and Eddy current testing
# CO4: Ultrasonic and Acoustic Emission
# CO5: Radiographic testing

NDT_QUESTION_BANK = [
    # CO1: Visual Inspection (Questions 1-15)
    {"id": 1, "question": "What is the primary advantage of Non-Destructive Testing (NDT)?", 
     "options": ["Low cost", "Early detection of defects before failure", "No skilled operators needed", "Faster than destructive testing"],
     "correct": 1, "co": "CO1"},
    
    {"id": 2, "question": "Which of the following is NOT a limitation of NDT?", 
     "options": ["Requires skilled operators", "High initial equipment cost", "Destroys the component", "Each method has specific material limitations"],
     "correct": 2, "co": "CO1"},
    
    {"id": 3, "question": "The human eye is most sensitive to which wavelength of light?", 
     "options": ["Red light (7000 A)", "Yellow-green light (5560 A)", "Blue light (4500 A)", "Ultraviolet light (3000 A)"],
     "correct": 1, "co": "CO1"},
    
    {"id": 4, "question": "What is the recommended lighting level for visual inspection?", 
     "options": ["200-400 lux", "500-700 lux", "800-1000 lux", "1200-1500 lux"],
     "correct": 2, "co": "CO1"},
    
    {"id": 5, "question": "For direct visual testing, the eye should be within what distance from the surface?", 
     "options": ["12 inches (300 mm)", "25 inches (610 mm)", "36 inches (900 mm)", "48 inches (1200 mm)"],
     "correct": 1, "co": "CO1"},
    
    {"id": 6, "question": "What is the minimum viewing angle required for direct visual testing?", 
     "options": ["15 degrees", "30 degrees", "45 degrees", "60 degrees"],
     "correct": 1, "co": "CO1"},
    
    {"id": 7, "question": "Which optical aid is used for inspecting the inside of narrow tubes or bores?", 
     "options": ["Microscope", "Telescope", "Borescope", "Periscope"],
     "correct": 2, "co": "CO1"},
    
    {"id": 8, "question": "The magnification (M) of a simple magnifier is calculated using which formula?", 
     "options": ["M = f/10", "M = 10/f", "M = 10 × f", "M = f²/10"],
     "correct": 1, "co": "CO1"},
    
    {"id": 9, "question": "What is the practical upper limit of magnifying power for a simple microscope?", 
     "options": ["5x", "10x", "20x", "50x"],
     "correct": 1, "co": "CO1"},
    
    {"id": 10, "question": "Which device provides flexibility to inspect around corners and through passages with directional changes?", 
     "options": ["Rigid borescope", "Endoscope", "Flexible fiber-optic borescope (Flexiscope)", "Telescope"],
     "correct": 2, "co": "CO1"},
    
    {"id": 11, "question": "What technology replaced tube-type cameras in modern endoscopes?", 
     "options": ["CCD (Charge-Coupled Device)", "LED sensors", "Photomultiplier tubes", "Infrared sensors"],
     "correct": 0, "co": "CO1"},
    
    {"id": 12, "question": "Endoscopes keep objects in focus from approximately what distance to infinity?", 
     "options": ["1 mm", "4 mm", "10 mm", "25 mm"],
     "correct": 1, "co": "CO1"},
    
    {"id": 13, "question": "What is holography primarily used for in NDT?", 
     "options": ["Measuring thickness", "Obtaining accurate three-dimensional images", "Detecting internal flaws", "Measuring hardness"],
     "correct": 1, "co": "CO1"},
    
    {"id": 14, "question": "The continuous working period for a human inspector should be limited to how many hours?", 
     "options": ["1 hour", "2 hours", "4 hours", "8 hours"],
     "correct": 1, "co": "CO1"},
    
    {"id": 15, "question": "Which defect CANNOT be detected by unaided visual inspection?", 
     "options": ["Surface cracks", "Subsurface voids", "Surface porosity", "Misalignment"],
     "correct": 1, "co": "CO1"},
    
    # CO2: Penetrant Testing (Questions 16-25)
    {"id": 16, "question": "Liquid Penetrant Testing is used primarily to detect:", 
     "options": ["Internal defects", "Surface-breaking defects", "Subsurface defects", "Thickness variations"],
     "correct": 1, "co": "CO2"},
    
    {"id": 17, "question": "What is the key property of a penetrant liquid?", 
     "options": ["High viscosity", "Low surface tension for capillary action", "High surface tension", "High density"],
     "correct": 1, "co": "CO2"},
    
    {"id": 18, "question": "Which type of penetrant provides the highest sensitivity?", 
     "options": ["Water-washable", "Post-emulsifiable", "Solvent-removable", "All have equal sensitivity"],
     "correct": 1, "co": "CO2"},
    
    {"id": 19, "question": "The dwell time in penetrant testing refers to:", 
     "options": ["Time for cleaning", "Time penetrant remains on surface", "Time for developer application", "Time for inspection"],
     "correct": 1, "co": "CO2"},
    
    {"id": 20, "question": "What is the purpose of the developer in penetrant testing?", 
     "options": ["Clean the surface", "Draw penetrant out of defects", "Remove excess penetrant", "Provide illumination"],
     "correct": 1, "co": "CO2"},
    
    {"id": 21, "question": "Fluorescent penetrants are viewed under:", 
     "options": ["White light", "Ultraviolet (UV) light", "Infrared light", "Laser light"],
     "correct": 1, "co": "CO2"},
    
    {"id": 22, "question": "Which material is NOT suitable for liquid penetrant testing?", 
     "options": ["Aluminum", "Steel", "Porous materials like wood", "Titanium"],
     "correct": 2, "co": "CO2"},
    
    {"id": 23, "question": "Pre-cleaning before penetrant testing is important to:", 
     "options": ["Improve surface finish", "Remove contaminants that may block defects", "Increase penetrant visibility", "Reduce testing time"],
     "correct": 1, "co": "CO2"},
    
    {"id": 24, "question": "The typical dwell time for penetrant application is:", 
     "options": ["1-2 minutes", "5-30 minutes", "1-2 hours", "24 hours"],
     "correct": 1, "co": "CO2"},
    
    {"id": 25, "question": "Color contrast penetrant testing uses which color combination?", 
     "options": ["Red penetrant on white developer background", "Blue penetrant on yellow background", "Green penetrant on red background", "Black penetrant on white background"],
     "correct": 0, "co": "CO2"},
    
    # CO3: Thermographic and Eddy Current Testing (Questions 26-35)
    {"id": 26, "question": "Thermography detects defects based on:", 
     "options": ["Acoustic emissions", "Temperature differences", "Magnetic properties", "Electrical resistance"],
     "correct": 1, "co": "CO3"},
    
    {"id": 27, "question": "Which type of radiation is detected in infrared thermography?", 
     "options": ["Visible light", "Ultraviolet radiation", "Infrared radiation", "X-rays"],
     "correct": 2, "co": "CO3"},
    
    {"id": 28, "question": "Thermographic testing is classified as:", 
     "options": ["Contact method", "Non-contact method", "Destructive method", "Semi-destructive method"],
     "correct": 1, "co": "CO3"},
    
    {"id": 29, "question": "Active thermography involves:", 
     "options": ["Natural heat from component", "External heat source applied to component", "Ambient temperature measurement", "No heat source required"],
     "correct": 1, "co": "CO3"},
    
    {"id": 30, "question": "Eddy current testing is based on the principle of:", 
     "options": ["Piezoelectric effect", "Electromagnetic induction", "Photoelectric effect", "Hall effect"],
     "correct": 1, "co": "CO3"},
    
    {"id": 31, "question": "Eddy current testing can only be used for:", 
     "options": ["Non-conductive materials", "Conductive materials", "Magnetic materials only", "Any material"],
     "correct": 1, "co": "CO3"},
    
    {"id": 32, "question": "The depth of penetration in eddy current testing depends on:", 
     "options": ["Material thickness only", "Frequency of alternating current", "Surface finish", "Ambient temperature"],
     "correct": 1, "co": "CO3"},
    
    {"id": 33, "question": "Higher frequencies in eddy current testing provide:", 
     "options": ["Greater penetration depth", "Better surface defect detection", "Better subsurface detection", "No difference"],
     "correct": 1, "co": "CO3"},
    
    {"id": 34, "question": "Eddy current testing can detect:", 
     "options": ["Only surface cracks", "Only subsurface defects", "Both surface and near-surface defects", "Internal defects only"],
     "correct": 2, "co": "CO3"},
    
    {"id": 35, "question": "The main advantage of thermography is:", 
     "options": ["High resolution", "Large area inspection in single scan", "Low cost", "No operator skill required"],
     "correct": 1, "co": "CO3"},
    
    # CO4: Ultrasonic and Acoustic Emission (Questions 36-50)
    {"id": 36, "question": "Ultrasonic testing uses sound waves with frequencies:", 
     "options": ["Below 20 Hz", "20 Hz to 20 kHz", "Above 20 kHz", "1-10 MHz"],
     "correct": 2, "co": "CO4"},
    
    {"id": 37, "question": "The typical frequency range for ultrasonic NDT is:", 
     "options": ["100-500 Hz", "1-5 kHz", "0.5-25 MHz", "50-100 MHz"],
     "correct": 2, "co": "CO4"},
    
    {"id": 38, "question": "Ultrasonic testing requires a coupling medium to:", 
     "options": ["Cool the transducer", "Transmit sound waves from transducer to material", "Clean the surface", "Provide electrical insulation"],
     "correct": 1, "co": "CO4"},
    
    {"id": 39, "question": "Which ultrasonic wave mode travels along the surface?", 
     "options": ["Longitudinal wave", "Shear wave", "Surface (Rayleigh) wave", "Lamb wave"],
     "correct": 2, "co": "CO4"},
    
    {"id": 40, "question": "The piezoelectric effect is used in ultrasonic testing to:", 
     "options": ["Generate heat", "Convert electrical energy to mechanical vibrations", "Measure temperature", "Detect magnetic fields"],
     "correct": 1, "co": "CO4"},
    
    {"id": 41, "question": "A-scan presentation in ultrasonic testing displays:", 
     "options": ["Cross-sectional view", "3D image", "Amplitude vs. time", "Color-coded map"],
     "correct": 2, "co": "CO4"},
    
    {"id": 42, "question": "The main limitation of ultrasonic testing is:", 
     "options": ["Cannot detect internal defects", "Requires access to only one surface", "Requires skilled operator and surface preparation", "Cannot be automated"],
     "correct": 2, "co": "CO4"},
    
    {"id": 43, "question": "Acoustic Emission testing monitors:", 
     "options": ["Externally applied sound", "Stress waves generated by material under stress", "Ambient noise", "Electromagnetic radiation"],
     "correct": 1, "co": "CO4"},
    
    {"id": 44, "question": "Acoustic Emission testing is unique because it:", 
     "options": ["Uses X-rays", "Detects active/growing defects in real-time", "Requires vacuum", "Works only on metals"],
     "correct": 1, "co": "CO4"},
    
    {"id": 45, "question": "Common coupling media for ultrasonic testing include:", 
     "options": ["Air only", "Water, oil, or gel", "Sand", "Mercury"],
     "correct": 1, "co": "CO4"},
    
    {"id": 46, "question": "The velocity of ultrasonic waves depends on:", 
     "options": ["Surface finish", "Material properties (density and elastic modulus)", "Ambient temperature only", "Operator skill"],
     "correct": 1, "co": "CO4"},
    
    {"id": 47, "question": "Angle beam ultrasonic testing is used primarily for:", 
     "options": ["Thickness measurement", "Detecting laminar defects and weld inspection", "Surface finish evaluation", "Temperature measurement"],
     "correct": 1, "co": "CO4"},
    
    {"id": 48, "question": "Acoustic Emission sensors detect:", 
     "options": ["Temperature changes", "High-frequency elastic waves", "Magnetic field variations", "Light emissions"],
     "correct": 1, "co": "CO4"},
    
    {"id": 49, "question": "Which factor does NOT affect ultrasonic wave propagation?", 
     "options": ["Material grain structure", "Material density", "Color of the material", "Material elasticity"],
     "correct": 2, "co": "CO4"},
    
    {"id": 50, "question": "Time-of-flight in ultrasonic testing is used to determine:", 
     "options": ["Material hardness", "Defect depth/location", "Surface roughness", "Material composition"],
     "correct": 1, "co": "CO4"},
    
    # CO5: Radiographic Testing (Questions 51-65)
    {"id": 51, "question": "Radiographic testing uses which type of radiation?", 
     "options": ["Visible light", "Infrared radiation", "X-rays and Gamma rays", "Microwaves"],
     "correct": 2, "co": "CO5"},
    
    {"id": 52, "question": "The main safety concern with radiographic testing is:", 
     "options": ["Noise pollution", "Radiation exposure hazards", "Chemical contamination", "Heat generation"],
     "correct": 1, "co": "CO5"},
    
    {"id": 53, "question": "Film density in radiography refers to:", 
     "options": ["Film thickness", "Degree of film darkening", "Film weight", "Film clarity"],
     "correct": 1, "co": "CO5"},
    
    {"id": 54, "question": "Which isotope is commonly used as a gamma ray source in radiography?", 
     "options": ["Carbon-14", "Iridium-192", "Hydrogen-3", "Oxygen-16"],
     "correct": 1, "co": "CO5"},
    
    {"id": 55, "question": "Radiographic testing can detect:", 
     "options": ["Only surface defects", "Only subsurface defects", "Internal volumetric defects", "Only cracks"],
     "correct": 2, "co": "CO5"},
    
    {"id": 56, "question": "Image Quality Indicators (IQI) or penetrameters are used to:", 
     "options": ["Measure radiation intensity", "Assess radiographic image quality and sensitivity", "Protect the film", "Generate radiation"],
     "correct": 1, "co": "CO5"},
    
    {"id": 57, "question": "Which provides better portability: X-ray or Gamma ray sources?", 
     "options": ["X-ray sources", "Gamma ray sources", "Both are equally portable", "Neither is portable"],
     "correct": 1, "co": "CO5"},
    
    {"id": 58, "question": "Digital radiography offers advantages including:", 
     "options": ["Lower cost than film", "Immediate image viewing and image processing capabilities", "No radiation required", "Can detect surface defects only"],
     "correct": 1, "co": "CO5"},
    
    {"id": 59, "question": "Computed Tomography (CT) in NDT provides:", 
     "options": ["2D images only", "3D volumetric images", "Surface images only", "Temperature maps"],
     "correct": 1, "co": "CO5"},
    
    {"id": 60, "question": "The contrast in a radiographic image depends on:", 
     "options": ["Film color", "Differences in material density and thickness", "Ambient lighting", "Operator experience"],
     "correct": 1, "co": "CO5"},
    
    {"id": 61, "question": "Radiographic testing requires access to:", 
     "options": ["One side of the component", "Both sides of the component", "No physical access needed", "Only edges"],
     "correct": 1, "co": "CO5"},
    
    {"id": 62, "question": "The inverse square law in radiography states that radiation intensity:", 
     "options": ["Increases with distance", "Decreases with square of distance", "Remains constant", "Increases with square of distance"],
     "correct": 1, "co": "CO5"},
    
    {"id": 63, "question": "Real-time radiography (fluoroscopy) allows:", 
     "options": ["Only static images", "Dynamic viewing during inspection", "Only surface inspection", "No image capture"],
     "correct": 1, "co": "CO5"},
    
    {"id": 64, "question": "Which material is commonly used for radiation shielding?", 
     "options": ["Aluminum", "Lead", "Copper", "Plastic"],
     "correct": 1, "co": "CO5"},
    
    {"id": 65, "question": "The main disadvantage of radiographic testing is:", 
     "options": ["Cannot detect internal defects", "Radiation safety concerns and high equipment cost", "Only works on metals", "Requires contact with surface"],
     "correct": 1, "co": "CO5"},
]

# =====================================================================================
# --- 🧠 CSE QUESTION BANK (20CS012 - PRINCIPLES OF COMPILER DESIGN) ---
# =====================================================================================

CSE_QUESTION_BANK = [
    {"id": 1, "question": "What is the primary role of a lexical analyzer in a compiler?", 
     "options": ["To generate object code", "To break the source program into tokens and pass them to the syntax analyzer", "To optimize the intermediate code", "To perform semantic analysis"],
     "correct": 1},
    
    {"id": 2, "question": "Which of the following is NOT a typical function of a lexical analyzer?", 
     "options": ["Removing white spaces and comments", "Recognizing identifiers and keywords", "Type checking of variables", "Generating symbol table entries"],
     "correct": 2},
    
    {"id": 3, "question": "What does a token represent in lexical analysis?", 
     "options": ["A sequence of characters with collective meaning", "A single character in the source code", "An error message", "A memory location"],
     "correct": 0},
    
    {"id": 4, "question": "Which buffering technique is commonly used in lexical analyzers to efficiently handle input?", 
     "options": ["Single buffer", "Two-buffer scheme with sentinels", "Circular buffer only", "No buffering is needed"],
     "correct": 1},
    
    {"id": 5, "question": "What type of lexical error occurs when an identifier name is too long?", 
     "options": ["Syntax error", "Semantic error", "Exceeding length of token", "Type mismatch error"],
     "correct": 2},
    
    {"id": 6, "question": "Regular expressions are used in lexical analysis to:", 
     "options": ["Specify the structure of programming language constructs", "Describe patterns for tokens", "Generate parse trees", "Optimize code"],
     "correct": 1},
    
    {"id": 7, "question": "Which of the following regular expression operators has the highest precedence?", 
     "options": ["Union (|)", "Concatenation (.)", "Kleene closure (*)", "All have equal precedence"],
     "correct": 2},
    
    {"id": 8, "question": "In the process of converting a regular expression to DFA, which intermediate step is typically used?", 
     "options": ["Context-free grammar", "Non-deterministic Finite Automaton (NFA)", "Push-down automaton", "Turing machine"],
     "correct": 1},
    
    {"id": 9, "question": "What is the purpose of DFA minimization?", 
     "options": ["To increase the number of states", "To reduce the number of states while preserving language recognition", "To convert DFA to NFA", "To handle errors"],
     "correct": 1},
    
    {"id": 10, "question": "LEX is:", 
     "options": ["A parser generator tool", "A compiler optimization tool", "A lexical analyzer generator tool", "An assembler"],
     "correct": 2},
    
    {"id": 11, "question": "Why is a lexical analyzer needed as a separate phase in compilation?", 
     "options": ["To improve compiler modularity and efficiency", "Because it's mandatory by compiler standards", "To increase compilation time", "To make the compiler more complex"],
     "correct": 0},
    
    {"id": 12, "question": "Which of the following is an example of a lexical error?", 
     "options": ["Missing semicolon", "Unmatched string delimiter", "Undeclared variable", "Type mismatch in assignment"],
     "correct": 1},
    
    {"id": 13, "question": "What happens when a lexical analyzer encounters an illegal character?", 
     "options": ["It ignores the character", "It reports a lexical error", "It converts it to a legal character", "It stops compilation immediately without reporting"],
     "correct": 1},
    
    {"id": 14, "question": "The sentinel approach in input buffering is used to:", 
     "options": ["Mark the end of the buffer to reduce the number of tests per character read", "Encrypt the input", "Store error messages", "Compress the input data"],
     "correct": 0},
    
    {"id": 15, "question": "Which regular expression represents one or more digits?", 
     "options": ["[0-9]*", "[0-9]+", "[0-9]?", "[0-9]"],
     "correct": 1},
    
    {"id": 16, "question": "Thompson's construction algorithm is used for:", 
     "options": ["Converting regular expression to NFA", "Converting NFA to DFA", "Minimizing DFA", "Parsing context-free grammars"],
     "correct": 0},
    
    {"id": 17, "question": "The subset construction method is used for:", 
     "options": ["Converting regular expression to NFA", "Converting NFA to DFA", "Minimizing DFA", "Generating lexical analyzers"],
     "correct": 1},
    
    {"id": 18, "question": "In DFA minimization, states are partitioned based on:", 
     "options": ["Number of incoming transitions", "Distinguishability with respect to accepting states", "Alphabetical order", "Random selection"],
     "correct": 1},
    
    {"id": 19, "question": "In LEX specification, the auxiliary declarations section is enclosed in:", 
     "options": ["{ }", "%{ %}", "[ ]", "( )"],
     "correct": 1},
    
    {"id": 20, "question": "Which pattern in LEX matches any single character except newline?", 
     "options": [".", "*", "+", "?"],
     "correct": 0},
    
    {"id": 21, "question": "The lexical analyzer interfaces with which compiler phase?", 
     "options": ["Code generator", "Syntax analyzer (parser)", "Semantic analyzer only", "Code optimizer"],
     "correct": 1},
    
    {"id": 22, "question": "Lookahead is sometimes required in lexical analysis to:", 
     "options": ["Speed up the scanning process", "Determine where one token ends and another begins", "Reduce memory usage", "Eliminate all errors"],
     "correct": 1},
    
    {"id": 23, "question": "What type of error is detected when a comment is not properly closed?", 
     "options": ["Syntactic error", "Semantic error", "Lexical error", "Runtime error"],
     "correct": 2},
    
    {"id": 24, "question": "The purpose of using two buffers in input buffering is to:", 
     "options": ["Store twice as much data", "Allow reloading one buffer while scanning the other", "Improve error detection", "Reduce memory requirements"],
     "correct": 1},
    
    {"id": 25, "question": "Which regular expression represents an identifier that starts with a letter followed by any number of letters or digits?", 
     "options": ["[a-zA-Z][0-9]*", "[a-zA-Z][a-zA-Z0-9]*", "[0-9][a-zA-Z]*", "[a-zA-Z]+[0-9]+"],
     "correct": 1},
    
    {"id": 26, "question": "An epsilon (ε) transition in an NFA:", 
     "options": ["Requires reading an input symbol", "Allows state transition without consuming input", "Indicates an error", "Is not allowed in NFA"],
     "correct": 1},
    
    {"id": 27, "question": "After converting an NFA to DFA using subset construction, the resulting DFA may have:", 
     "options": ["Fewer states than the NFA", "The same number of states as the NFA", "More states than the NFA", "Exponentially more states (in worst case)"],
     "correct": 3},
    
    {"id": 28, "question": "The algorithm for DFA minimization partitions states into equivalence classes based on:", 
     "options": ["State numbers", "Transition functions and finality", "Input symbols only", "Random grouping"],
     "correct": 1},
    
    {"id": 29, "question": "In a LEX program, the translation rules section contains:", 
     "options": ["Regular expressions only", "C code only", "Pattern-action pairs", "Symbol table definitions"],
     "correct": 2},
    
    {"id": 30, "question": "The output of LEX is:",
     "options": ["A DFA table", "A C program implementing the lexical analyzer (lex.yy.c)", "An executable file", "A parse tree"],
     "correct": 1},
]

# =====================================================================================
# --- 🧠 NDT QUESTION BANK - QUIZ 02 (Thermography & Eddy Current Testing) ---
# =====================================================================================

NDT_QUIZ02_QUESTION_BANK = [
    {"id": 1, "question": "What is Thermography in the context of NDT?",
     "options": ["A method that uses sound waves to detect defects", "An NDT method that detects defects by measuring temperature variations on the surface of a component", "A technique that uses magnetic fields to identify cracks", "A method that uses X-rays to image internal defects"],
     "correct": 1, "co": "CO3"},
    {"id": 2, "question": "Which of the following best describes Active Thermography?",
     "options": ["The component is inspected using its natural heat emission without any external energy input", "An external energy source is applied to the component to induce thermal contrast for defect detection", "The component is cooled below ambient temperature for inspection", "Infrared cameras are used without any stimulation of the component"],
     "correct": 1, "co": "CO3"},
    {"id": 3, "question": "Which of the following best describes Passive Thermography?",
     "options": ["External heat is applied to the component before inspection", "The component's natural heat emission during operation is monitored to detect anomalies", "The component is submerged in liquid for thermal imaging", "UV light is used to stimulate thermal emission from the component"],
     "correct": 1, "co": "CO3"},
    {"id": 4, "question": "Liquid Crystal Thermography works on the principle that:",
     "options": ["Liquid crystals emit infrared radiation proportional to defect depth", "Liquid crystals change colour in response to temperature variations, revealing thermal patterns", "Liquid crystals conduct electricity differently over defects", "Liquid crystals fluoresce under ultraviolet light near crack regions"],
     "correct": 1, "co": "CO3"},
    {"id": 5, "question": "Which of the following is an advantage of Liquid Crystal Thermography?",
     "options": ["It can detect very deep subsurface defects up to several centimetres", "It provides a full-field, real-time colour map of surface temperature distribution", "It does not require any surface preparation", "It works on all metallic and non-metallic materials without calibration"],
     "correct": 1, "co": "CO3"},
    {"id": 6, "question": "Which of the following is a limitation of Liquid Crystal Thermography?",
     "options": ["It cannot measure temperature at all", "It has a narrow operating temperature range and requires direct contact with the surface", "It requires radioactive isotopes for activation", "It can only be used on ferromagnetic materials"],
     "correct": 1, "co": "CO3"},
    {"id": 7, "question": "Infrared Thermography detects defects by measuring:",
     "options": ["The electrical resistance across the component surface", "Infrared radiation emitted from the component surface, which varies with subsurface defects", "The magnetic field strength at the component surface", "The acoustic emission from propagating cracks"],
     "correct": 1, "co": "CO3"},
    {"id": 8, "question": "The electromagnetic spectrum region used in Infrared Thermography is:",
     "options": ["Ultraviolet region", "Infrared region (wavelengths between 0.75 μm and 1000 μm)", "X-ray region", "Visible light region only"],
     "correct": 1, "co": "CO3"},
    {"id": 9, "question": "Which of the following is a type of IR detector used in Infrared Thermography?",
     "options": ["Piezoelectric transducer", "Photon detector and thermal detector", "Geiger-Muller tube", "Scintillation counter"],
     "correct": 1, "co": "CO3"},
    {"id": 10, "question": "In Infrared Thermography, a defect appears as a ______ spot on the thermal image compared to the surrounding area.",
     "options": ["Same temperature", "Hot or cold spot depending on the nature and location of the defect", "Always a cold spot", "Always a hot spot"],
     "correct": 1, "co": "CO3"},
    {"id": 11, "question": "Which of the following is an application of Infrared Thermography in NDT?",
     "options": ["Detecting surface cracks in aluminium using penetrant liquids", "Detecting delaminations in composites, heat loss in buildings, and electrical hotspots in circuits", "Measuring the hardness of metallic surfaces", "Identifying grain boundaries in metals using magnetic fields"],
     "correct": 1, "co": "CO3"},
    {"id": 12, "question": "Which of the following is an inspection method used in Active Thermography?",
     "options": ["Passive emission monitoring", "Pulsed thermography, lock-in thermography, and vibrothermography", "Continuous wave ultrasonic stimulation only", "Magnetic pulse heating"],
     "correct": 1, "co": "CO3"},
    {"id": 13, "question": "What instrumentation is primarily used to capture thermal images in Infrared Thermography?",
     "options": ["Ultrasonic flaw detector", "Infrared camera (thermographic camera)", "Magnetic yoke with Hall effect sensor", "X-ray film and developer"],
     "correct": 1, "co": "CO3"},
    {"id": 14, "question": "Which of the following is an advantage of Infrared Thermography as an NDT method?",
     "options": ["It requires physical contact with the component for accurate results", "It is a non-contact, full-field inspection method capable of scanning large areas quickly", "It can detect only metallic defects", "It requires the component to be ferromagnetic"],
     "correct": 1, "co": "CO3"},
    {"id": 15, "question": "In thermography, emissivity refers to:",
     "options": ["The ability of a material to conduct electricity", "The efficiency of a surface in emitting infrared radiation compared to a perfect blackbody", "The temperature gradient across a defect", "The reflectivity of a surface to ultrasonic waves"],
     "correct": 1, "co": "CO3"},
    {"id": 16, "question": "What is the basic principle of Eddy Current Testing (ECT)?",
     "options": ["A penetrant liquid is drawn into surface defects by capillary action", "A changing magnetic field induces eddy currents in a conductive material, and defects alter these currents, which is detected by the probe", "Ultrasonic pulses are reflected from internal discontinuities", "Magnetic particles are attracted to flux leakage points at defects"],
     "correct": 1, "co": "CO3"},
    {"id": 17, "question": "Eddy currents are induced in a conductive material when:",
     "options": ["A static magnetic field is applied to the surface", "An alternating magnetic field from a coil is brought near the electrically conductive material", "Ultrasonic waves pass through the material", "The material is heated above its Curie temperature"],
     "correct": 1, "co": "CO3"},
    {"id": 18, "question": "Which of the following materials can be tested using Eddy Current Testing?",
     "options": ["Non-conductive materials like wood and ceramics", "Electrically conductive materials such as metals and alloys", "Only ferromagnetic materials", "Only non-ferrous metals like aluminium and copper"],
     "correct": 1, "co": "CO3"},
    {"id": 19, "question": "In Eddy Current Testing, the presence of a defect is detected by observing:",
     "options": ["A change in the colour of the component surface", "A change in the impedance of the test coil caused by the altered eddy current flow", "A temperature rise at the defect location", "Reflection of magnetic particles at the crack boundary"],
     "correct": 1, "co": "CO3"},
    {"id": 20, "question": "The depth to which eddy currents penetrate into a material is called:",
     "options": ["Wavelength", "Standard depth of penetration or skin depth", "Attenuation depth", "Diffraction depth"],
     "correct": 1, "co": "CO3"},
    {"id": 21, "question": "How does the test frequency affect the depth of penetration in Eddy Current Testing?",
     "options": ["Higher frequency increases the depth of penetration", "Lower frequency increases the depth of penetration into the material", "Frequency has no effect on penetration depth", "Higher frequency is always used for subsurface defect detection"],
     "correct": 1, "co": "CO3"},
    {"id": 22, "question": "Which of the following is an element of an Eddy Current Testing system?",
     "options": ["Penetrant applicator and developer spray", "Test coil (probe), AC power source, impedance measuring instrument, and display unit", "Magnetic yoke and fluorescent particles", "X-ray tube, film, and darkroom processing equipment"],
     "correct": 1, "co": "CO3"},
    {"id": 23, "question": "Which type of Eddy Current probe is commonly used for detecting surface cracks in flat components?",
     "options": ["Encircling coil", "Surface (pancake) probe", "Internal bobbin coil", "Differential through-transmission coil"],
     "correct": 1, "co": "CO3"},
    {"id": 24, "question": "An encircling coil in Eddy Current Testing is used for:",
     "options": ["Inspecting flat plate surfaces for corrosion", "Inspecting cylindrical components like tubes, rods, and bars as they pass through the coil", "Detecting deep subsurface defects in thick sections", "Measuring the surface roughness of components"],
     "correct": 1, "co": "CO3"},
    {"id": 25, "question": "Which of the following properties of a material can be measured using Eddy Current Testing?",
     "options": ["Tensile strength and hardness only", "Electrical conductivity, magnetic permeability, coating thickness, and detection of cracks", "Grain size and fracture toughness", "Melting point and thermal conductivity only"],
     "correct": 1, "co": "CO3"},
    {"id": 26, "question": "Which of the following is an application of Eddy Current Testing?",
     "options": ["Detecting internal porosity in castings using sound waves", "Inspection of heat exchanger tubes, aircraft fuselage skin, and detection of cracks in conductive components", "Measuring wall thickness of non-conductive polymer pipes", "Detecting surface cracks in ceramics using penetrant liquids"],
     "correct": 1, "co": "CO3"},
    {"id": 27, "question": "Which of the following is a limitation of Eddy Current Testing?",
     "options": ["It cannot detect surface cracks", "It is limited to electrically conductive materials and has limited depth of penetration", "It requires the component to be submerged in water during inspection", "It can only be performed at elevated temperatures"],
     "correct": 1, "co": "CO3"},
    {"id": 28, "question": "In Eddy Current Testing, the 'lift-off effect' refers to:",
     "options": ["The increase in eddy current penetration as the probe is lifted from the surface", "The change in probe impedance caused by variations in the distance between the probe and the test surface", "The reduction in magnetic field strength due to component geometry", "The signal noise generated by surface roughness of the component"],
     "correct": 1, "co": "CO3"},
    {"id": 29, "question": "Which of the following is a key advantage of Eddy Current Testing over Magnetic Particle Testing?",
     "options": ["ECT can test ferromagnetic materials only", "ECT can be applied to all electrically conductive materials including non-ferromagnetic metals, and requires no contact or surface preparation", "ECT always provides greater depth of penetration than MPT", "ECT does not require any instrumentation or calibration"],
     "correct": 1, "co": "CO3"},
    {"id": 30, "question": "A case study application of Eddy Current Testing in the aviation industry involves:",
     "options": ["Using penetrant liquids to detect cracks in composite panels", "Detecting fatigue cracks around fastener holes in aluminium aircraft structures during maintenance inspections", "Using gamma rays to image internal defects in engine components", "Applying magnetic particles to detect cracks in titanium landing gear components"],
     "correct": 1, "co": "CO3"},
]

# =====================================================================================
# --- 🧠 NDT QUESTION BANK - QUIZ 03 (Evaluate & Interpret UT & AE Results) ---
# CO4: Ability to evaluate and interpret the results obtained in the
#       Ultrasonic inspection and Acoustic Emission technique.
# =====================================================================================

NDT_QUIZ03_QUESTION_BANK = [
    {"id": 1, "question": "In an A-scan display, what does a high-amplitude indication appearing before the back-wall echo signify?",
     "options": ["A surface coating artifact", "A subsurface discontinuity whose depth is proportional to the signal's time position", "A calibration error in the system", "Proper beam coupling with the material"],
     "correct": 1, "co": "CO4"},
    {"id": 2, "question": "The 6 dB drop method for defect sizing defines the defect edge at the probe position where the peak signal drops to:",
     "options": ["25% of maximum amplitude", "10% of maximum amplitude", "50% of maximum amplitude", "75% of maximum amplitude"],
     "correct": 2, "co": "CO4"},
    {"id": 3, "question": "A Distance-Amplitude Correction (DAC) curve in ultrasonic testing is constructed using:",
     "options": ["Side-drilled holes at various depths in a calibration block", "Flat-bottom holes all at the same depth", "Surface notches of varying widths", "Back-wall echoes from increasing material thicknesses"],
     "correct": 0, "co": "CO4"},
    {"id": 4, "question": "In ultrasonic testing, when the back-wall echo completely disappears while a flaw indication is present, this most likely indicates:",
     "options": ["A small rounded pore that scatters the beam in all directions", "Loss of acoustic coupling between the transducer and material surface", "A large planar defect that blocks the entire ultrasonic beam from reaching the back wall", "Excessive surface roughness causing beam scattering"],
     "correct": 2, "co": "CO4"},
    {"id": 5, "question": "In a B-scan ultrasonic display, the axes represent:",
     "options": ["Signal amplitude vs. signal frequency", "Probe scan position (horizontal) vs. reflector depth (vertical)", "Defect length (horizontal) vs. defect width (vertical)", "Time of flight vs. beam angle"],
     "correct": 1, "co": "CO4"},
    {"id": 6, "question": "A C-scan ultrasonic display provides:",
     "options": ["Signal amplitude vs. time at a single fixed point", "A depth cross-section along the scan direction", "A plan (top) view showing the lateral extent and distribution of defects at a selected gate depth", "A three-dimensional volumetric reconstruction of the test piece"],
     "correct": 2, "co": "CO4"},
    {"id": 7, "question": "The 'dead zone' in pulse-echo ultrasonic testing is the region where:",
     "options": ["The sound beam diverges and sensitivity decreases beyond the far field", "Shallow defects cannot be detected because the initial transmitted pulse obscures early echoes", "Acoustic emission signals cannot be received by the sensor", "The back-wall reflection is fully absorbed by the material"],
     "correct": 1, "co": "CO4"},
    {"id": 8, "question": "In the 20 dB drop sizing method, the probe edges of a defect are defined where the signal amplitude drops to what percentage of the maximum?",
     "options": ["50%", "25%", "5%", "10%"],
     "correct": 3, "co": "CO4"},
    {"id": 9, "question": "The IIW (International Institute of Welding) V1 calibration block is primarily used for:",
     "options": ["Measuring the chemical composition of the test material", "Time base (distance) calibration and sensitivity setting of the ultrasonic instrument", "Setting the threshold for acoustic emission monitoring", "Determining the hardness of weld joints"],
     "correct": 1, "co": "CO4"},
    {"id": 10, "question": "In Acoustic Emission (AE) testing, 'ring-down counts' (threshold crossings) are used to:",
     "options": ["Locate the AE source position in three dimensions", "Measure the temperature at the defect location", "Quantify the intensity of AE signals by counting the number of times the signal exceeds the threshold", "Determine the dominant frequency of the AE waveform"],
     "correct": 2, "co": "CO4"},
    {"id": 11, "question": "The Kaiser Effect in AE testing describes the phenomenon that:",
     "options": ["AE activity increases proportionally with applied load at all stress levels", "AE signal amplitude is directly proportional to crack opening displacement", "No significant AE emissions occur upon reloading until the previously applied maximum stress level is exceeded", "AE sensors detect emissions only above a minimum threshold material thickness"],
     "correct": 2, "co": "CO4"},
    {"id": 12, "question": "A Felicity Ratio (FR) less than 1.0 in AE testing indicates:",
     "options": ["The material is in perfect condition with no prior damage", "AE emissions occur below the previously applied maximum load, signifying damage accumulation or active defects", "The AE sensors are not properly coupled to the structure", "The test frequency is too high for the material being tested"],
     "correct": 1, "co": "CO4"},
    {"id": 13, "question": "In AE source location using the time-of-arrival (TOA) method with two sensors on a linear structure, the source position is determined by:",
     "options": ["The ratio of amplitudes received at each sensor", "The difference in arrival times of the AE wave at the two sensors multiplied by the wave velocity", "The frequency content of signals at the closer sensor", "The total signal energy received at both sensors combined"],
     "correct": 1, "co": "CO4"},
    {"id": 14, "question": "Which AE parameter is MOST directly related to the energy released by a fracture event?",
     "options": ["Rise time of the AE waveform", "Duration of the AE signal (in microseconds)", "Signal energy (proportional to the integral of the squared voltage over time)", "Peak amplitude (in dB) of the AE signal"],
     "correct": 2, "co": "CO4"},
    {"id": 15, "question": "When evaluating ultrasonic weld inspection results, a 'non-relevant indication' is best defined as:",
     "options": ["Any signal exceeding the 20% DAC evaluation level", "A signal from a real internal defect of critical dimensions", "A signal caused by geometric reflectors such as weld root or cap geometry rather than actual defects", "Any signal observed during scanning that falls below the noise floor"],
     "correct": 2, "co": "CO4"},
    {"id": 16, "question": "In the TOFD (Time of Flight Diffraction) technique, defect depth is calculated from:",
     "options": ["The amplitude of the diffracted signals from defect tips", "The time delay between the lateral wave and the diffracted tip echo, combined with the probe separation geometry", "The frequency shift of the back-wall echo over the defect", "The reduction in back-wall echo amplitude above the defect region"],
     "correct": 1, "co": "CO4"},
    {"id": 17, "question": "In a Phased Array Ultrasonic Testing (PAUT) S-scan image, a defect is characterised by:",
     "options": ["Only the largest amplitude indication across all angles", "Its angular position, depth location, lateral extent, and orientation relative to the weld geometry", "The colour of the indication on the display screen only", "The dominant frequency component at that scan angle"],
     "correct": 1, "co": "CO4"},
    {"id": 18, "question": "The 'near field' (Fresnel zone) of an ultrasonic transducer presents evaluation challenges because:",
     "options": ["Sound travels faster in the near field region", "The beam is fully diverged in the near field with minimum on-axis sensitivity", "Unpredictable pressure fluctuations make amplitude-based defect sizing unreliable in this zone", "Temperature effects are amplified in the near field region"],
     "correct": 2, "co": "CO4"},
    {"id": 19, "question": "In AE testing of a pressure vessel during a hydrostatic test, AE activity that continues during the pressure hold period at constant pressure is interpreted as:",
     "options": ["Normal thermal expansion noise from pressurization", "Evidence of active crack growth or structural instability under sustained load", "Friction noise from test equipment attachments to the vessel", "Signal from the coupling agent between sensors and the vessel wall"],
     "correct": 1, "co": "CO4"},
    {"id": 20, "question": "'Location clustering' of AE events concentrated in a small region during AE monitoring indicates:",
     "options": ["Sensors placed too close together causing signal overlap interference", "Random background noise distributed across the structure", "Normal elastic material behaviour during initial loading", "A localised active defect or area of stress concentration that warrants further investigation"],
     "correct": 3, "co": "CO4"},
    {"id": 21, "question": "During ultrasonic weld inspection with angle-beam probes, a 'dynamic response' (signal that changes significantly as the probe is moved) is typically associated with:",
     "options": ["A planar specular reflector aligned perfectly perpendicular to the beam axis", "A volumetric defect like porosity that scatters the beam from multiple positions", "A geometric indication from the weld root region", "A calibration reference side-drilled hole signal"],
     "correct": 1, "co": "CO4"},
    {"id": 22, "question": "During ultrasonic corrosion mapping, areas with measured wall thickness below the minimum retirement thickness require:",
     "options": ["Recalibration of the instrument and retest only", "A repeat inspection with a different coupling medium", "Immediate rejection or a formal fitness-for-service assessment", "Increasing the ultrasonic frequency for better measurement accuracy"],
     "correct": 2, "co": "CO4"},
    {"id": 23, "question": "In AE waveform analysis, a high-frequency, short-duration, fast rise-time signal is typically associated with:",
     "options": ["Large-scale plastic deformation or matrix cracking in composites", "Brittle fracture or rapid crack propagation events", "Slow corrosion processes occurring over a large surface area", "Environmental electromagnetic interference from nearby equipment"],
     "correct": 1, "co": "CO4"},
    {"id": 24, "question": "The signal-to-noise ratio (SNR) is critical in ultrasonic evaluation because:",
     "options": ["A low SNR increases the velocity of sound measurement accuracy", "A high SNR ensures that genuine defect signals can be reliably distinguished from material grain noise and background scatter", "The SNR directly determines the depth of the dead zone in the test material", "A low SNR indicates the inspected material contains no defects"],
     "correct": 1, "co": "CO4"},
    {"id": 25, "question": "In AE data interpretation, a decreasing 'b-value' (from amplitude distribution analysis) indicates:",
     "options": ["Stable microcracking activity with no change in damage state", "Improvement in material structural integrity during the test", "Transition from distributed microcracking to dominant macrocrack formation and growth", "Reduction in background noise levels during monitoring"],
     "correct": 2, "co": "CO4"},
    {"id": 26, "question": "During straight-beam UT inspection, a gradual decrease in back-wall echo amplitude across a scan area without discrete flaw indications most likely indicates:",
     "options": ["A discrete planar crack parallel to the inspection surface", "Gradual wall thinning, internal corrosion, or increased material attenuation in that region", "A broken transducer element causing inconsistent performance", "Air entrapment within the coupling gel applied to the surface"],
     "correct": 1, "co": "CO4"},
    {"id": 27, "question": "In AE testing of carbon fibre reinforced polymer (CFRP) composites, fibre breakage is characterised by:",
     "options": ["Low amplitude, long duration signals from matrix cracking only", "Low frequency, high energy signals representing large delaminations", "High amplitude, short rise-time signals indicating sudden energy release", "Very low amplitude signals consistently below the AE detection threshold"],
     "correct": 2, "co": "CO4"},
    {"id": 28, "question": "An AE monitoring system shows increased activity during cyclic loading but negligible AE during static hold periods. This behaviour most likely suggests:",
     "options": ["An active through-crack that is continuously growing under all loading conditions", "Fretting or rubbing of crack faces during load cycling rather than genuine active crack propagation", "Complete sensor malfunction that only occurs during the hold period", "That complete structural failure is imminent within a few load cycles"],
     "correct": 1, "co": "CO4"},
    {"id": 29, "question": "When evaluating UT results using the DAC curve, an indication with amplitude between 20% DAC and 100% DAC should be:",
     "options": ["Immediately rejected as a critical defect requiring weld repair", "Recorded, characterised, and evaluated for acceptance or rejection according to the applicable code", "Ignored completely as it is below the 100% DAC rejection level", "Re-inspected only using a lower frequency transducer"],
     "correct": 1, "co": "CO4"},
    {"id": 30, "question": "In TOFD data evaluation, a parabolic arc-shaped signal in the TOFD image typically represents:",
     "options": ["A planar defect lying parallel to the scanning surface", "A small point-like volumetric reflector such as a pore or small inclusion", "Correct instrument calibration giving expected signal geometry", "A delamination between two material layers in a composite"],
     "correct": 1, "co": "CO4"},
]

# =====================================================================================
# --- 🧠 CSE QUESTION BANK - QUIZ 02 (Syntax Analysis & Parsing) ---
# =====================================================================================

CSE_QUIZ02_QUESTION_BANK = [
    {"id": 1, "question": "What is the primary role of a parser in compiler design?",
     "options": ["To convert source code into machine code", "To perform lexical analysis and tokenization", "To check the syntactic structure and build a parse tree", "To optimize the intermediate code"],
     "correct": 2},
    {"id": 2, "question": "Which of the following is NOT a characteristic of Context Free Grammars (CFG)?",
     "options": ["CFGs can represent nested structures", "Every production has exactly one non-terminal on the left side", "CFGs can describe all programming language constructs", "CFGs are more powerful than regular grammars"],
     "correct": 2},
    {"id": 3, "question": "In Top-Down Parsing, the parse tree is constructed:",
     "options": ["From leaves to root", "From root to leaves", "In random order", "Only for left-recursive grammars"],
     "correct": 1},
    {"id": 4, "question": "What is the main limitation of Recursive Descent Parser?",
     "options": ["Cannot handle any grammar", "Cannot handle left recursion and requires backtracking for some grammars", "Only works for LR grammars", "Requires too much memory"],
     "correct": 1},
    {"id": 5, "question": "A Predictive Parser is:",
     "options": ["A bottom-up parser without backtracking", "A top-down parser without backtracking", "An LR parser with lookahead", "A parser that predicts errors"],
     "correct": 1},
    {"id": 6, "question": "In LL(1), the '1' represents:",
     "options": ["One production rule", "One non-terminal", "One symbol lookahead", "One pass compilation"],
     "correct": 2},
    {"id": 7, "question": "Which parsing technique is used in Bottom-Up Parsing?",
     "options": ["Leftmost derivation", "Rightmost derivation in reverse", "Random derivation", "No derivation needed"],
     "correct": 1},
    {"id": 8, "question": "In Shift-Reduce Parser, a 'reduce' action:",
     "options": ["Reduces the input string length", "Replaces the handle at the top of stack with a non-terminal", "Shifts symbols to the stack", "Reduces the number of states"],
     "correct": 1},
    {"id": 9, "question": "An LR(0) item is:",
     "options": ["A production with zero terminals", "A production with a dot indicating parsing position", "A grammar with zero ambiguity", "A state with zero conflicts"],
     "correct": 1},
    {"id": 10, "question": "YACC stands for:",
     "options": ["Yet Another Compiler Constructor", "Yet Another Code Compiler", "Yet Another Compiler-Compiler", "Yet Another Context Checker"],
     "correct": 2},
    {"id": 11, "question": "Which of the following conflicts can occur in LL(1) parsing?",
     "options": ["Shift-Reduce conflict", "Reduce-Reduce conflict", "FIRST-FIRST and FIRST-FOLLOW conflicts", "Both Shift-Reduce and Reduce-Reduce"],
     "correct": 2},
    {"id": 12, "question": "The handle in bottom-up parsing is:",
     "options": ["The leftmost non-terminal", "A substring matching the right side of a production", "The lookahead symbol", "The start symbol"],
     "correct": 1},
    {"id": 13, "question": "SLR parser stands for:",
     "options": ["Simple Left-Right parser", "Simple LR parser", "Systematic Left Recursive parser", "Simple Lookahead Recursive parser"],
     "correct": 1},
    {"id": 14, "question": "What is the main difference between SLR and Canonical LR(1) parsers?",
     "options": ["SLR uses FOLLOW sets, LR(1) uses specific lookaheads", "SLR is bottom-up, LR(1) is top-down", "SLR is more powerful than LR(1)", "There is no difference between them"],
     "correct": 0},
    {"id": 15, "question": "LALR parser is created by:",
     "options": ["Merging LR(0) items with same core", "Merging LR(1) items with same core", "Simplifying LL(1) parser tables", "Combining SLR and LR parsers"],
     "correct": 1},
    {"id": 16, "question": "In Operator Precedence Parsing, we compare:",
     "options": ["Non-terminals with terminals", "Precedence of operators", "Stack depth", "Number of productions"],
     "correct": 1},
    {"id": 17, "question": "Which grammar can be parsed by Recursive Descent Parser without modification?",
     "options": ["Left-recursive grammar", "Ambiguous grammar", "LL(1) grammar without left recursion", "Any context-free grammar"],
     "correct": 2},
    {"id": 18, "question": "Panic mode error recovery in syntax analysis involves:",
     "options": ["Stopping compilation immediately on first error", "Skipping tokens until a synchronizing token is found", "Inserting missing tokens automatically", "Correcting all errors automatically"],
     "correct": 1},
    {"id": 19, "question": "The FIRST set of a non-terminal contains:",
     "options": ["All non-terminals that can appear first", "All terminals that can appear first in derivations from that non-terminal", "The first production rule only", "Only terminal symbols from the first production"],
     "correct": 1},
    {"id": 20, "question": "In an LR parser, the ACTION table determines:",
     "options": ["Which production to reduce using only", "Whether to shift or reduce and which state to go to", "Only the shift operations allowed", "The next input symbol to read"],
     "correct": 1},
    {"id": 21, "question": "Which of the following is a viable prefix in LR parsing?",
     "options": ["Any prefix of the input string", "A prefix of a right-sentential form up to the handle", "The first symbol of the input string", "Any substring of any production"],
     "correct": 1},
    {"id": 22, "question": "The FOLLOW set of a non-terminal A includes:",
     "options": ["Terminals that can immediately follow A in some derivation", "All terminals in the grammar", "Non-terminals that follow A", "Only the end marker $"],
     "correct": 0},
    {"id": 23, "question": "What problem does LALR solve compared to Canonical LR(1)?",
     "options": ["Reduces the number of states significantly", "Eliminates all conflicts", "Makes parsing faster", "Handles more grammars than LR(1)"],
     "correct": 0},
    {"id": 24, "question": "In a Shift-Reduce parser, what indicates successful parsing?",
     "options": ["Empty input buffer only", "Stack contains only the start symbol and input buffer is empty", "No conflicts in parsing table", "All productions have been used"],
     "correct": 1},
    {"id": 25, "question": "Left recursion in grammar causes problems for:",
     "options": ["Bottom-up parsers", "LR parsers", "Top-down parsers", "Operator precedence parsers"],
     "correct": 2},
    {"id": 26, "question": "An augmented grammar is created by:",
     "options": ["Adding a new start symbol S' and production S' → S", "Removing left recursion from the grammar", "Eliminating all ambiguity from the grammar", "Adding error productions for recovery"],
     "correct": 0},
    {"id": 27, "question": "Which parser generator tool is commonly used for bottom-up parsing?",
     "options": ["LEX", "YACC", "FLEX", "ANTLR (primarily top-down)"],
     "correct": 1},
    {"id": 28, "question": "Phrase-level error recovery in syntax analysis:",
     "options": ["Replaces or inserts tokens locally to allow parsing to continue", "Only detects errors without recovery", "Requires complete recompilation", "Uses semantic information for recovery"],
     "correct": 0},
    {"id": 29, "question": "The closure operation in LR(0) item construction:",
     "options": ["Closes the input file after parsing", "Adds all items derivable from non-terminals after the dot", "Removes duplicate items from the state", "Finalizes the state transitions"],
     "correct": 1},
    {"id": 30, "question": "The predictive parsing (LL(1)) table is constructed using:",
     "options": ["Only FIRST sets", "Only FOLLOW sets", "Both FIRST and FOLLOW sets", "Neither FIRST nor FOLLOW sets"],
     "correct": 2},
    {"id": 31, "question": "Which conflict can occur in SLR parsing but is resolved in Canonical LR(1)?",
     "options": ["Shift-Shift conflict", "Ambiguity conflict", "Reduce-Reduce conflict due to imprecise lookaheads", "Syntax errors in the grammar"],
     "correct": 2},
    {"id": 32, "question": "In operator precedence parsing, the relation '<' between two operators means:",
     "options": ["Equal precedence between the operators", "Left operand has lower precedence (right operator should be evaluated first)", "Right operand has lower precedence", "No precedence relation exists between them"],
     "correct": 1},
    {"id": 33, "question": "The GOTO function in LR parsing:",
     "options": ["Determines the next state after a reduction or shift action", "Transfers control to the error handler", "Jumps to a specific grammar production", "Exits the parser on completion"],
     "correct": 0},
    {"id": 34, "question": "Which parsing method is most powerful in terms of grammar coverage?",
     "options": ["LL(1)", "SLR", "Canonical LR(1)", "Operator Precedence"],
     "correct": 2},
    {"id": 35, "question": "Error productions in a grammar are used for:",
     "options": ["Generating error messages only", "Continuing parsing after detecting common predictable errors", "Creating syntax errors intentionally", "Optimizing the parser performance"],
     "correct": 1},
    {"id": 36, "question": "What does the dot (.) represent in an LR(0) item [A → α.β]?",
     "options": ["The end of the production", "The current parsing position separating what has been seen from what is expected", "A terminal symbol in the grammar", "An error point in the parse"],
     "correct": 1},
    {"id": 37, "question": "The main advantage of LL(1) parsers is:",
     "options": ["They can handle all context-free grammars", "They are simple to implement and highly efficient", "They require no grammar transformation at all", "They use less memory than all LR parsers"],
     "correct": 1},
    {"id": 38, "question": "In YACC, productions are specified using:",
     "options": ["Regular expressions", "BNF-like notation with embedded semantic actions", "State transition diagrams", "Finite automata specifications"],
     "correct": 1},
    {"id": 39, "question": "The kernel items in an LR state are:",
     "options": ["All items present in the state", "The initial item S' → .S and all items with the dot not at the leftmost position", "Items with the dot at the rightmost position (reduce items)", "Items derived from epsilon productions only"],
     "correct": 1},
    {"id": 40, "question": "Global error recovery in syntax analysis involves:",
     "options": ["Finding the minimum cost correction to the entire input string", "Local token manipulation at the error point", "Ignoring all errors found during parsing", "Stopping at the very first error encountered"],
     "correct": 0},
]

# =====================================================================================
# --- 🧠 CSE QUESTION BANK - QUIZ 03 (SDT, Intermediate Code & Type Systems) ---
# =====================================================================================

CSE_QUIZ03_QUESTION_BANK = [
    {"id": 1, "question": "What is Syntax Directed Definition (SDD)?",
     "options": ["A method to generate machine code directly", "A formalism that associates attributes and semantic rules with grammar productions", "A technique for lexical analysis and tokenization", "A parsing strategy for handling ambiguous grammars"],
     "correct": 1},
    {"id": 2, "question": "Which of the following is a type of attribute in Syntax Directed Definitions?",
     "options": ["Inherited and Synthesized", "Static and Dynamic", "Local and Global", "Terminal and Non-terminal"],
     "correct": 0},
    {"id": 3, "question": "In Three-Address Code, each instruction has at most:",
     "options": ["One operand", "Two operands", "Three operands", "Four operands"],
     "correct": 2},
    {"id": 4, "question": "Which of the following is a valid Three-Address Code representation of a = b + c * d?",
     "options": ["a = b + c * d", "t1 = c * d; t2 = b + t1; a = t2", "PUSH b; ADD c; POP a", "MOV a, b"],
     "correct": 1},
    {"id": 5, "question": "Type Conversions in a type system are of which two kinds?",
     "options": ["Implicit and Explicit", "Static and Dynamic", "Forward and Backward", "Narrow and Broad"],
     "correct": 0},
    {"id": 6, "question": "Which intermediate code form uses a record with four fields: operator, arg1, arg2, and result?",
     "options": ["Triples", "Indirect Triples", "Quadruples", "Postfix notation"],
     "correct": 2},
    {"id": 7, "question": "In a Type System, what is the purpose of Type Equivalence?",
     "options": ["To convert one type to another type automatically", "To determine if two type expressions represent the same type", "To allocate memory for variables of each type", "To check syntax errors in declarations"],
     "correct": 1},
    {"id": 8, "question": "What is the evaluation order of attributes in an SDD called?",
     "options": ["Parse Order", "Derivation Order", "Evaluation Order or Dependency Order", "Reduction Order"],
     "correct": 2},
    {"id": 9, "question": "Which of the following is NOT a type of Three-Address Code statement?",
     "options": ["Assignment: x = y op z", "Unconditional jump: goto L", "Push and Pop stack operations", "Conditional jump: if x goto L"],
     "correct": 2},
    {"id": 10, "question": "A simple type checker verifies that:",
     "options": ["The program compiles without syntax errors", "Each operation receives operands of the correct and compatible types", "All variables are initialized before use at runtime", "The code is optimized for performance"],
     "correct": 1},
    {"id": 11, "question": "Syntax Directed Translation (SDT) extends CFG by:",
     "options": ["Adding regular expressions to productions", "Attaching program fragments called semantic actions to grammar productions", "Removing ambiguity from context-free grammars", "Adding lookahead symbols to each grammar rule"],
     "correct": 1},
    {"id": 12, "question": "Which notation is used for representing expressions in Three-Address Code without parentheses?",
     "options": ["Infix notation", "Prefix notation", "Postfix notation", "Mixed notation"],
     "correct": 2},
    {"id": 13, "question": "In Syntax Directed Definitions, a synthesized attribute gets its value from:",
     "options": ["The parent node in the parse tree", "The children nodes in the parse tree", "The sibling nodes of the current node", "An external symbol table lookup"],
     "correct": 1},
    {"id": 14, "question": "Which of the following correctly describes an Inherited Attribute?",
     "options": ["Its value is computed from the children of the current node", "Its value is computed from the parent or sibling nodes in the parse tree", "It is always associated with a terminal symbol", "It is defined only for the start symbol of the grammar"],
     "correct": 1},
    {"id": 15, "question": "Type Expressions are used to:",
     "options": ["Represent the structure and kind of data types in a programming language", "Perform arithmetic computations on type values", "Generate assembly language instructions", "Allocate stack frames for function calls"],
     "correct": 0},
    {"id": 16, "question": "In a Three-Address Code using Triples, the result of each operation is referred to by:",
     "options": ["A named temporary variable", "The position (index) of the triple in the triple list", "A hardware register name", "A physical memory address"],
     "correct": 1},
    {"id": 17, "question": "Which of the following is an intermediate code representation that resembles an Abstract Syntax Tree?",
     "options": ["Three-address code", "Quadruples", "DAG (Directed Acyclic Graph)", "Postfix code"],
     "correct": 2},
    {"id": 18, "question": "Declarations in a block-structured language are used to:",
     "options": ["Generate machine code directly", "Determine the type and storage layout of identifiers", "Parse tokens from the source code", "Optimize loops in the program"],
     "correct": 1},
    {"id": 19, "question": "Which of the following represents structural equivalence of types?",
     "options": ["Two types are equivalent if they have the same name", "Two types are equivalent if they have the same structure regardless of name", "Two types are equivalent only if they are both integers", "Two types are never considered equivalent"],
     "correct": 1},
    {"id": 20, "question": "Intermediate Code Generation is placed between which two phases in a compiler?",
     "options": ["Lexical Analysis and Syntax Analysis", "Semantic Analysis (or Syntax Analysis) and Code Optimization", "Code Optimization and Code Generation", "Semantic Analysis and Lexical Analysis"],
     "correct": 1},
    {"id": 21, "question": "What is the main advantage of using intermediate code in a compiler?",
     "options": ["It directly executes on the hardware without further translation", "It makes the compiler machine-independent and retargetable to multiple architectures", "It eliminates the need for lexical analysis", "It automatically removes all syntax errors"],
     "correct": 1},
    {"id": 22, "question": "A Type System in a programming language is a collection of:",
     "options": ["Parsing rules for the grammar", "Rules that assign types to constructs and check for type errors", "Code optimization techniques", "Memory allocation strategies"],
     "correct": 1},
    {"id": 23, "question": "Widening type conversion refers to:",
     "options": ["Converting a larger type to a smaller type (e.g., double to int)", "Converting a smaller type to a larger compatible type without data loss (e.g., int to double)", "Casting between completely unrelated types", "Converting string values to integer values"],
     "correct": 1},
    {"id": 24, "question": "In an S-attributed SDD, all attributes are:",
     "options": ["Inherited", "Synthesized", "Both inherited and synthesized equally", "Derived from the root node only"],
     "correct": 1},
    {"id": 25, "question": "Which of the following is true about L-attributed SDDs?",
     "options": ["They can only have synthesized attributes", "They allow inherited attributes that depend only on left siblings or the parent node", "They are only used in bottom-up parsers", "They do not support semantic actions in productions"],
     "correct": 1},
    {"id": 26, "question": "The Three-Address Code instruction for an unconditional jump is written as:",
     "options": ["if x goto L", "goto L", "jump x", "branch L if true"],
     "correct": 1},
    {"id": 27, "question": "Name equivalence of types means:",
     "options": ["Two types are the same only if they are declared with the exact same name", "Two types are the same if they have the same structure", "All primitive types are automatically equivalent", "Types are compared dynamically at runtime"],
     "correct": 0},
    {"id": 28, "question": "Which data structure is typically used to implement a simple type checker?",
     "options": ["Stack", "Queue", "Symbol Table", "Priority Queue"],
     "correct": 2},
    {"id": 29, "question": "Backpatching in intermediate code generation is a technique used to:",
     "options": ["Optimize loop structures in the generated code", "Fill in jump target addresses that are unknown at the time of code generation", "Allocate registers efficiently during code generation", "Remove redundant assignment statements"],
     "correct": 1},
    {"id": 30, "question": "In Three-Address Code, a conditional jump instruction looks like:",
     "options": ["goto L", "if x relop y goto L", "jump if true", "branch x to L"],
     "correct": 1},
]

# =====================================================================================
# --- ☁️ GOOGLE SHEETS HELPER FUNCTIONS ---
# =====================================================================================

def get_gspread_client():
    """Connects to Google Sheets using credentials from Streamlit secrets."""
    try:
        return gspread.service_account_from_dict(st.secrets["gcp_service_account"])
    except Exception as e:
        st.error(f"❌ Failed to connect to Google Sheets: {e}")
        return None

def initialize_spreadsheet():
    """Initializes the spreadsheet with required sheets and headers."""
    try:
        client = get_gspread_client()
        if not client:
            return False
        
        spreadsheet = client.open_by_url(st.secrets["google_sheets"]["spreadsheet_url"])
        
        # Define required sheets for all quizzes
        headers = ["timestamp", "student_name", "register_number", "score", "total_questions", "answers_json", "questions_json"]
        sheets_config = {
            "NDT_Quiz01": headers, "NDT_Quiz02": headers, "NDT_Quiz03": headers,
            "CSE_Quiz01": headers, "CSE_Quiz02": headers, "CSE_Quiz03": headers,
        }
        
        existing_sheets = [ws.title for ws in spreadsheet.worksheets()]
        
        for sheet_name, headers in sheets_config.items():
            if sheet_name not in existing_sheets:
                worksheet = spreadsheet.add_worksheet(title=sheet_name, rows=1000, cols=len(headers))
                worksheet.append_row(headers)
            else:
                worksheet = spreadsheet.worksheet(sheet_name)
                existing_headers = worksheet.row_values(1)
                if not existing_headers or existing_headers != headers:
                    worksheet.clear()
                    worksheet.append_row(headers)
        
        return True
    except Exception as e:
        st.error(f"❌ Error initializing spreadsheet: {e}")
        return False

def save_to_gsheet(sheet_name, data_dict):
    """Saves a dictionary of data as a new row in the specified Google Sheet."""
    try:
        client = get_gspread_client()
        if not client:
            return False
        
        spreadsheet = client.open_by_url(st.secrets["google_sheets"]["spreadsheet_url"])
        ws = spreadsheet.worksheet(sheet_name)
        header = ws.row_values(1)
        row_to_insert = [data_dict.get(key, "N/A") for key in header]
        ws.append_row(row_to_insert, value_input_option='USER_ENTERED')
        return True
    except Exception as e:
        st.error(f"❌ Could not write to Google Sheets: {e}")
        return False

def get_sheet_data(sheet_name):
    """Retrieves all data from a specified sheet."""
    try:
        client = get_gspread_client()
        if not client:
            return None
        
        spreadsheet = client.open_by_url(st.secrets["google_sheets"]["spreadsheet_url"])
        ws = spreadsheet.worksheet(sheet_name)
        return pd.DataFrame(ws.get_all_records())
    except Exception as e:
        st.error(f"❌ Error reading from sheet {sheet_name}: {e}")
        return None

# =====================================================================================
# --- 📄 PDF GENERATION FUNCTIONS ---
# =====================================================================================

def create_results_pdf(session_data):
    """Generates a detailed PDF report for a single student."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['h1'], alignment=TA_CENTER, fontSize=18, textColor=colors.HexColor('#1f4788'))
    story.append(Paragraph(f"{session_data.get('department', 'Quiz')} - Performance Report", title_style))
    story.append(Spacer(1, 0.25 * inch))
    
    student_info = [
        ['Student Name:', session_data.get('student_name', 'N/A')],
        ['Register Number:', session_data.get('register_number', 'N/A')],
        ['Department:', session_data.get('department', 'N/A')],
        ['Date & Time:', session_data.get('timestamp', 'N/A')],
        ['Score:', f"<b>{session_data.get('score', '0')} / {session_data.get('total_questions', 20)}</b>"],
        ['Percentage:', f"<b>{(session_data.get('score', 0) / session_data.get('total_questions', 20) * 100):.2f}%</b>"]
    ]
    
    info_table = Table(student_info, colWidths=[1.5 * inch, 4.5 * inch])
    info_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.4 * inch))
    
    story.append(Paragraph("Detailed Answer Sheet", styles['h3']))
    story.append(Spacer(1, 0.2 * inch))
    
    results_data = [['Q#', 'Your Answer', 'Correct Answer', 'Result']]
    questions = session_data.get('questions', [])
    answers = session_data.get('answers', [])
    
    for i, q in enumerate(questions):
        user_answer_idx = answers[i]
        user_answer_text = q['options'][user_answer_idx] if user_answer_idx is not None else "Not Answered"
        correct_answer_text = q['options'][q['correct']]
        result = "✓ Correct" if user_answer_idx == q['correct'] else "✗ Wrong"
        
        results_data.append([
            str(i + 1),
            Paragraph(user_answer_text, styles['Normal']),
            Paragraph(correct_answer_text, styles['Normal']),
            result
        ])
    
    results_table = Table(results_data, colWidths=[0.4*inch, 2.4*inch, 2.4*inch, 0.8*inch])
    results_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1f4788')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('ALIGN', (1, 1), (2, -1), 'LEFT'),
        ('FONTSIZE', (0, 1), (-1, -1), 9),
    ]))
    
    for i, row in enumerate(results_data[1:], start=1):
        if row[-1] == "✓ Correct":
            results_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightgreen)]))
        else:
            results_table.setStyle(TableStyle([('BACKGROUND', (0, i), (-1, i), colors.lightpink)]))
    
    story.append(results_table)
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

def create_question_bank_pdf(department, question_bank):
    """Generates a PDF of the question bank."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=0.5*inch, bottomMargin=0.5*inch)
    styles = getSampleStyleSheet()
    story = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['h1'], alignment=TA_CENTER, fontSize=18)
    story.append(Paragraph(f"{department} - Question Bank", title_style))
    story.append(Spacer(1, 0.3 * inch))
    
    for idx, q in enumerate(question_bank, 1):
        q_text = f"<b>Q{idx}. {q['question']}</b>"
        if 'co' in q:
            q_text += f" [{q['co']}]"
        story.append(Paragraph(q_text, styles['Normal']))
        story.append(Spacer(1, 0.1 * inch))
        
        for opt_idx, option in enumerate(q['options']):
            opt_letter = chr(97 + opt_idx)
            opt_text = f"{opt_letter}) {option}"
            if opt_idx == q['correct']:
                opt_text = f"<b><font color='green'>{opt_text} ✓</font></b>"
            story.append(Paragraph(opt_text, styles['Normal']))
        
        story.append(Spacer(1, 0.2 * inch))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()

# =====================================================================================
# --- 🖥️ UI RENDERING FUNCTIONS ---
# =====================================================================================

def render_department_selection_page():
    """Step 1 — Choose department."""
    st.set_page_config(page_title=APP_TITLE, layout="centered", page_icon="📚")

    with st.spinner("🔄 Connecting to database..."):
        connection_status = initialize_spreadsheet()

    if connection_status:
        st.success("✅ Connected to database successfully!")
    else:
        st.error("❌ Failed to connect to database. Please check your configuration.")
        st.stop()

    st.title(f"📚 {APP_TITLE}")
    st.markdown("---")
    st.subheader("👨‍🎓 Step 1 — Select Your Department")
    st.markdown("")

    col1, col2 = st.columns(2)

    with col1:
        if st.button(
            "🔧 Mechanical Engineering\n(NDT — Non-Destructive Testing)",
            use_container_width=True, type="primary", key="dept_mech"
        ):
            st.session_state.selected_department = "Mechanical Engineering"
            st.session_state.course_name = "NDT - Non-Destructive Testing"
            st.session_state.page = "quiz_selection"
            st.rerun()

    with col2:
        if st.button(
            "💻 Computer Science\n(20CS012 — Compiler Design)",
            use_container_width=True, type="primary", key="dept_cse"
        ):
            st.session_state.selected_department = "Computer Science"
            st.session_state.course_name = "20CS012 - Principles of Compiler Design"
            st.session_state.page = "quiz_selection"
            st.rerun()


def render_quiz_selection_page():
    """Step 2 — Choose which quiz (1, 2 or 3) to attempt."""
    st.set_page_config(page_title="Select Quiz", layout="centered", page_icon="📋")

    dept = st.session_state.selected_department
    course = st.session_state.course_name

    st.title("📋 Step 2 — Select Quiz")
    st.markdown(f"**Department:** {dept}")
    st.markdown(f"**Course:** {course}")

    if st.button("← Back to Department Selection", key="back_to_dept"):
        st.session_state.page = "department_selection"
        st.rerun()

    st.markdown("---")
    st.subheader("Choose a Quiz to Attempt")
    st.markdown("")

    if dept == "Mechanical Engineering":
        quizzes = [
            ("Quiz 01", "Quiz 1", "Visual Inspection & Penetrant Testing",
             "CO1 & CO2 · 20 random questions from a bank of 65"),
            ("Quiz 02", "Quiz 2", "Thermography & Eddy Current Testing",
             "CO3 · 20 random questions from a bank of 30"),
            ("Quiz 03", "Quiz 3", "Evaluate & Interpret UT & AE Results",
             "CO4 · 20 random questions from a bank of 30"),
        ]
    else:
        quizzes = [
            ("Quiz 01", "Quiz 1", "Lexical Analysis & Finite Automata",
             "20 random questions from a bank of 30"),
            ("Quiz 02", "Quiz 2", "Syntax Analysis & Parsing Techniques",
             "20 random questions from a bank of 40"),
            ("Quiz 03", "Quiz 3", "SDT, Intermediate Code & Type Systems",
             "20 random questions from a bank of 30"),
        ]

    for quiz_key, quiz_label, topic, detail in quizzes:
        col_info, col_btn = st.columns([3, 1])
        with col_info:
            st.markdown(f"**{quiz_label} — {topic}**")
            st.caption(detail)
        with col_btn:
            if st.button(
                f"Start {quiz_label}",
                key=f"pick_{quiz_key}",
                use_container_width=True,
                type="primary"
            ):
                st.session_state.selected_quiz = quiz_key
                st.session_state.page = "student_selection"
                st.rerun()
        st.markdown("---")


def render_student_selection_page():
    """Step 3 — Identify the student."""
    st.set_page_config(page_title="Student Information", layout="centered", page_icon="📝")

    st.title("📝 Step 3 — Student Information")
    st.markdown(f"**Department:** {st.session_state.selected_department}")
    st.markdown(f"**Course:** {st.session_state.course_name}")
    quiz_key = st.session_state.get("selected_quiz", "Quiz 01")
    st.markdown(f"**Quiz:** {quiz_key.replace('0', '')} ")

    if st.button("← Back to Quiz Selection", key="back_dept"):
        st.session_state.page = "quiz_selection"
        st.rerun()
    
    st.markdown("---")
    if st.session_state.selected_department == "Mechanical Engineering":
        students = MECHANICAL_STUDENTS
    else:
        students = CSE_STUDENTS
    
    st.subheader("Select Your Details")
    
    # Create dropdown options
    student_options = ["-- Select from list --"] + [f"{s['name']} ({s['reg']})" for s in students] + ["-- Enter manually --"]
    
    selected_option = st.selectbox("Choose your name:", student_options)
    
    if selected_option == "-- Enter manually --":
        with st.form("manual_entry_form"):
            st.info("📝 Enter your details manually")
            student_name = st.text_input("Full Name *", placeholder="Enter your full name")
            register_number = st.text_input("Register Number *", placeholder="Enter your register number")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Start Quiz", type="primary", use_container_width=True)
            with col2:
                back = st.form_submit_button("← Cancel", use_container_width=True)
            
            if back:
                st.rerun()
            
            if submitted:
                if not all([student_name.strip(), register_number.strip()]):
                    st.error("❌ Please fill in all required fields marked with *")
                else:
                    proceed_to_quiz(student_name.strip(), register_number.strip())
    
    elif selected_option != "-- Select from list --":
        # Extract student info from selected option
        selected_student = None
        for s in students:
            if f"{s['name']} ({s['reg']})" == selected_option:
                selected_student = s
                break
        
        if selected_student:
            st.success(f"✅ Selected: {selected_student['name']}")
            st.info(f"Register Number: {selected_student['reg']}")
            
            if st.button("Start Quiz", type="primary", use_container_width=True):
                proceed_to_quiz(selected_student['name'], selected_student['reg'])

def proceed_to_quiz(name, reg_no):
    """Initialize quiz session."""
    st.session_state.student_name = name
    st.session_state.register_number = reg_no
    st.session_state.quiz_started = True
    st.session_state.start_time = time.time()

    dept = st.session_state.selected_department
    quiz = st.session_state.get("selected_quiz", "Quiz 01")

    # Map department + quiz number → question bank and sheet name
    bank_map = {
        ("Mechanical Engineering", "Quiz 01"): (NDT_QUESTION_BANK,       "NDT_Quiz01"),
        ("Mechanical Engineering", "Quiz 02"): (NDT_QUIZ02_QUESTION_BANK, "NDT_Quiz02"),
        ("Mechanical Engineering", "Quiz 03"): (NDT_QUIZ03_QUESTION_BANK, "NDT_Quiz03"),
        ("Computer Science",       "Quiz 01"): (CSE_QUESTION_BANK,        "CSE_Quiz01"),
        ("Computer Science",       "Quiz 02"): (CSE_QUIZ02_QUESTION_BANK, "CSE_Quiz02"),
        ("Computer Science",       "Quiz 03"): (CSE_QUIZ03_QUESTION_BANK, "CSE_Quiz03"),
    }
    question_bank, sheet_name = bank_map.get((dept, quiz), (NDT_QUESTION_BANK, "NDT_Quiz01"))

    st.session_state.quiz_sheet_name = sheet_name
    st.session_state.questions = random.sample(question_bank, min(QUESTIONS_PER_QUIZ, len(question_bank)))
    st.session_state.answers = [None] * len(st.session_state.questions)
    st.session_state.current_question_index = 0
    st.session_state.page = "quiz"
    st.rerun()

def render_quiz_page():
    """Displays the main quiz interface with timer and questions."""
    st.set_page_config(page_title="Quiz in Progress", layout="centered", page_icon="✍️")

    # Auto-refresh for timer
    st_autorefresh(interval=1000, limit=None, key="quiz_timer")
    elapsed_time = time.time() - st.session_state.start_time
    remaining_time = QUIZ_DURATION_SECONDS - elapsed_time
    
    if remaining_time <= 0:
        st.toast("⏳ Time's up! Auto-submitting your quiz...", icon="⏰")
        time.sleep(2)
        st.session_state.quiz_submitted = True
        st.session_state.page = "results"
        st.rerun()
        return

    col1, col2 = st.columns([3, 1])
    with col1:
        quiz_label = st.session_state.get("selected_quiz", "Quiz 01")
        st.title(f"{st.session_state.course_name} | {quiz_label}")
    with col2:
        mins, secs = divmod(int(remaining_time), 60)
        timer_color = "🟢" if remaining_time > 120 else "🟡" if remaining_time > 60 else "🔴"
        st.metric(f"{timer_color} Time Left", f"{mins:02d}:{secs:02d}")

    progress = (st.session_state.current_question_index + 1) / len(st.session_state.questions)
    st.progress(progress)
    
    q_index = st.session_state.current_question_index
    question_data = st.session_state.questions[q_index]
    
    st.markdown(f"### Question {q_index + 1} of {len(st.session_state.questions)}")
    
    # Show CO mapping for NDT questions
    if 'co' in question_data:
        st.caption(f"Course Outcome: {question_data['co']}")
    
    st.markdown(f"**{question_data['question']}**")
    st.markdown("")
    
    saved_answer_index = st.session_state.answers[q_index]
    
    if saved_answer_index is not None:
        default_index = saved_answer_index
    else:
        default_index = 0
    
    user_choice_label = st.radio(
        "Select your answer:",
        options=question_data['options'],
        index=default_index,
        key=f"q_{q_index}_{st.session_state.start_time}"
    )
    
    st.session_state.answers[q_index] = question_data['options'].index(user_choice_label)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        if st.button("⬅️ Previous", use_container_width=True, disabled=(q_index == 0)):
            st.session_state.current_question_index -= 1
            st.rerun()
    
    with col2:
        st.markdown(f"<center>Question {q_index + 1}/{len(st.session_state.questions)}</center>", unsafe_allow_html=True)
    
    with col3:
        if q_index < len(st.session_state.questions) - 1:
            if st.button("Next ➡️", use_container_width=True):
                st.session_state.current_question_index += 1
                st.rerun()
        else:
            if st.button("✅ Submit Quiz", type="primary", use_container_width=True):
                st.session_state.quiz_submitted = True
                st.session_state.page = "results"
                st.rerun()
    
    st.markdown("---")
    st.markdown("**Question Overview:**")
    answered = sum(1 for ans in st.session_state.answers if ans is not None)
    st.info(f"Answered: {answered} / {len(st.session_state.questions)}")

def render_results_page():
    """Displays final results and allows PDF download."""
    st.set_page_config(page_title="Quiz Results", layout="centered", page_icon="🎉")
    
    score = sum(1 for i, q in enumerate(st.session_state.questions) 
                if st.session_state.answers[i] is not None and st.session_state.answers[i] == q['correct'])
    
    total_questions = len(st.session_state.questions)
    percentage = (score / total_questions) * 100
    
    st.balloons()
    st.title("🎉 Quiz Submitted Successfully!")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Score", f"{score}/{total_questions}")
    with col2:
        st.metric("Percentage", f"{percentage:.1f}%")
    with col3:
        grade = "Excellent" if percentage >= 80 else "Good" if percentage >= 60 else "Pass" if percentage >= 40 else "Needs Improvement"
        st.metric("Grade", grade)
    
    # Only save once - check if already saved
    if not st.session_state.get('submission_saved', False):
        sheet_name = st.session_state.get("quiz_sheet_name", "NDT_Quiz01")

        submission_data = {
            "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "student_name": st.session_state.student_name,
            "register_number": st.session_state.register_number,
            "score": score,
            "total_questions": total_questions,
            "answers_json": json.dumps(st.session_state.answers),
            "questions_json": json.dumps([{"question": q["question"], "options": q["options"], "correct": q["correct"], "co": q.get("co", "N/A")} for q in st.session_state.questions])
        }
        
        # Save to Google Sheets
        save_success = save_to_gsheet(sheet_name, submission_data)
        
        if save_success:
            st.success("✅ Your results have been saved successfully!", icon="💾")
            # Mark as saved to prevent duplicate submissions
            st.session_state.submission_saved = True
        else:
            st.warning("⚠️ Could not save results to database. Please contact administrator.")
    else:
        # Already saved - just show confirmation
        st.info("✅ Your results have already been recorded in the database.", icon="💾")
    
    st.markdown("---")
    st.subheader("📄 Download Your Report")
    
    pdf_data = {
        'department': st.session_state.selected_department,
        'course_name': st.session_state.course_name,
        'student_name': st.session_state.student_name,
        'register_number': st.session_state.register_number,
        'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'score': score,
        'total_questions': total_questions,
        'questions': st.session_state.questions,
        'answers': st.session_state.answers
    }
    
    pdf_bytes = create_results_pdf(pdf_data)
    st.download_button(
        label="📥 Download Performance Report (PDF)",
        data=pdf_bytes,
        file_name=f"{st.session_state.register_number}_Report.pdf",
        mime="application/pdf",
        use_container_width=True
    )
    
    st.markdown("---")
    if st.button("🔄 Take Another Quiz", use_container_width=True):
        # Clear all session state for new quiz
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def render_admin_panel():
    """Displays admin panel in sidebar."""
    st.sidebar.markdown("---")
    st.sidebar.title("🔐 Admin Access")
    
    with st.sidebar.form("admin_login"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        login = st.form_submit_button("Login")
    
    if login:
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.admin_authenticated = True
            st.session_state.page = "admin_dashboard"
            st.rerun()
        else:
            st.sidebar.error("❌ Invalid credentials")

def render_admin_dashboard():
    """Displays the full admin dashboard."""
    st.set_page_config(page_title="Admin Dashboard", layout="wide", page_icon="👨‍💼")
    
    st.title("👨‍💼 Admin Dashboard")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([6, 1, 1])
    with col3:
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.admin_authenticated = False
            st.session_state.page = "department_selection"
            st.rerun()
    
    tab1, tab2 = st.tabs(["📊 Quiz Results", "📚 Question Banks"])
    
    with tab1:
        st.subheader("Quiz Results")
        
        quiz_choices = {
            "NDT - Quiz 01 (Visual & Penetrant)":        ("NDT_Quiz01", "Mechanical Engineering"),
            "NDT - Quiz 02 (Thermography & Eddy Current)": ("NDT_Quiz02", "Mechanical Engineering"),
            "NDT - Quiz 03 (Evaluate UT & AE Results)":  ("NDT_Quiz03", "Mechanical Engineering"),
            "CSE - Quiz 01 (Lexical Analysis)":          ("CSE_Quiz01", "Computer Science"),
            "CSE - Quiz 02 (Syntax Analysis)":           ("CSE_Quiz02", "Computer Science"),
            "CSE - Quiz 03 (Intermediate Code & Types)": ("CSE_Quiz03", "Computer Science"),
        }
        department = st.selectbox("Select Quiz:", list(quiz_choices.keys()))
        sheet_name, dept_label = quiz_choices[department]
        
        if st.button("🔄 Refresh Data"):
            st.cache_data.clear()
        
        with st.spinner("Loading data..."):
            df = get_sheet_data(sheet_name)
        
        if df is not None and not df.empty:
            st.metric("Total Submissions", len(df))
            
            col1, col2, col3 = st.columns(3)
            with col1:
                avg_score = df['score'].mean()
                st.metric("Average Score", f"{avg_score:.2f}")
            with col2:
                max_score = df['score'].max()
                st.metric("Highest Score", f"{max_score}")
            with col3:
                min_score = df['score'].min()
                st.metric("Lowest Score", f"{min_score}")
            
            st.markdown("### Recent Submissions")
            display_df = df[['timestamp', 'student_name', 'register_number', 'score', 'total_questions']].copy()
            display_df['percentage'] = (display_df['score'] / display_df['total_questions'] * 100).round(2)
            st.dataframe(display_df, use_container_width=True)
            
            csv_bytes = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download All Results (CSV)",
                data=csv_bytes,
                file_name=f"{sheet_name}_results.csv",
                mime="text/csv",
                use_container_width=True
            )
            
            st.markdown("### Individual Student Reports")
            student_names = df['student_name'].tolist()
            selected_student = st.selectbox("Select Student:", student_names)
            
            if st.button("📄 Download Student Report (PDF)"):
                student_record = df[df['student_name'] == selected_student].iloc[0]
                
                pdf_data = {
                    'department': dept_label,
                    'course_name': "NDT" if dept_label == "Mechanical Engineering" else "Compiler Design",
                    'student_name': student_record['student_name'],
                    'register_number': student_record['register_number'],
                    'timestamp': student_record['timestamp'],
                    'score': student_record['score'],
                    'total_questions': student_record['total_questions'],
                    'questions': json.loads(student_record['questions_json']),
                    'answers': json.loads(student_record['answers_json'])
                }
                
                pdf_bytes = create_results_pdf(pdf_data)
                st.download_button(
                    label=f"📥 Download {selected_student}'s Report",
                    data=pdf_bytes,
                    file_name=f"{student_record['register_number']}_Report.pdf",
                    mime="application/pdf",
                    use_container_width=True
                )
        else:
            st.info("No submissions found for this department.")
    
    with tab2:
        st.subheader("Question Banks")
        
        qb_choices = {
            "NDT - Quiz 01 (Visual & Penetrant)":           (NDT_QUESTION_BANK,        "NDT_Quiz01"),
            "NDT - Quiz 02 (Thermography & Eddy Current)":  (NDT_QUIZ02_QUESTION_BANK, "NDT_Quiz02"),
            "NDT - Quiz 03 (Evaluate UT & AE Results)":     (NDT_QUIZ03_QUESTION_BANK, "NDT_Quiz03"),
            "CSE - Quiz 01 (Lexical Analysis)":             (CSE_QUESTION_BANK,        "CSE_Quiz01"),
            "CSE - Quiz 02 (Syntax Analysis)":              (CSE_QUIZ02_QUESTION_BANK, "CSE_Quiz02"),
            "CSE - Quiz 03 (Intermediate Code & Types)":    (CSE_QUIZ03_QUESTION_BANK, "CSE_Quiz03"),
        }
        dept_qb = st.selectbox("Select Quiz:", list(qb_choices.keys()), key="qb_dept")
        selected_bank, dept_name = qb_choices[dept_qb]
        
        st.info(f"Total Questions: {len(selected_bank)}")
        
        # For NDT quizzes, show CO distribution
        if dept_name.startswith("NDT"):
            co_counts = {}
            for q in selected_bank:
                co = q.get('co', 'N/A')
                co_counts[co] = co_counts.get(co, 0) + 1
            
            st.markdown("### Course Outcome Distribution")
            co_df = pd.DataFrame(list(co_counts.items()), columns=['Course Outcome', 'Number of Questions'])
            st.dataframe(co_df, use_container_width=True)
        
        with st.expander("View Questions"):
            for idx, q in enumerate(selected_bank, 1):
                q_text = f"**Q{idx}. {q['question']}**"
                if 'co' in q:
                    q_text += f" [{q['co']}]"
                st.markdown(q_text)
                for opt_idx, option in enumerate(q['options']):
                    marker = "✅" if opt_idx == q['correct'] else ""
                    st.markdown(f"   {chr(97 + opt_idx)}) {option} {marker}")
                st.markdown("---")
        
        # Download Question Bank Section
        st.markdown("### 📥 Download Question Bank")
        
        col1, col2 = st.columns([3, 1])
        with col1:
            st.info(f"Click the button to generate and download the {dept_name} question bank as PDF")
        with col2:
            if st.button("Generate PDF", type="primary", use_container_width=True):
                with st.spinner("Generating PDF..."):
                    pdf_bytes = create_question_bank_pdf(dept_name, selected_bank)
                    st.session_state.qb_pdf_generated = True
                    st.session_state.qb_pdf_bytes = pdf_bytes
                    st.session_state.qb_pdf_filename = f"{dept_name.replace(' ', '_')}_QuestionBank.pdf"
        
        # Show download button if PDF was generated
        if st.session_state.get('qb_pdf_generated', False):
            st.download_button(
                label=f"⬇️ Download {dept_name} Question Bank PDF",
                data=st.session_state.qb_pdf_bytes,
                file_name=st.session_state.qb_pdf_filename,
                mime="application/pdf",
                use_container_width=True
            )
            st.success(f"✅ PDF generated successfully! Click above to download.")

# =====================================================================================
# --- 🚀 MAIN APPLICATION ROUTER ---
# =====================================================================================

def main():
    """Main function to control the app's page flow."""
    
    if 'page' not in st.session_state:
        st.session_state.page = "department_selection"
    
    if 'admin_authenticated' not in st.session_state:
        st.session_state.admin_authenticated = False
    
    if st.session_state.admin_authenticated and st.session_state.page == "admin_dashboard":
        render_admin_dashboard()
    elif st.session_state.page == "department_selection":
        render_department_selection_page()
        if not st.session_state.admin_authenticated:
            render_admin_panel()
    elif st.session_state.page == "quiz_selection":
        render_quiz_selection_page()
        if not st.session_state.admin_authenticated:
            render_admin_panel()
    elif st.session_state.page == "student_selection":
        render_student_selection_page()
        if not st.session_state.admin_authenticated:
            render_admin_panel()
    elif st.session_state.page == "quiz":
        render_quiz_page()
    elif st.session_state.page == "results":
        render_results_page()
    else:
        st.session_state.page = "department_selection"
        st.rerun()

if __name__ == "__main__":
    main()