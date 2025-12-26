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
        
        # Define required sheets (removed malpractice logs)
        sheets_config = {
            # Mechanical Engineering (NDT)
            "NDT_Quiz01": ["timestamp", "student_name", "register_number", "score", "total_questions", "answers_json", "questions_json"],
            # CSE (Compiler Design)
            "CSE_Quiz01": ["timestamp", "student_name", "register_number", "score", "total_questions", "answers_json", "questions_json"]
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
    """Displays department selection interface."""
    st.set_page_config(page_title=APP_TITLE, layout="centered", page_icon="📚")
    
    with st.spinner("🔄 Connecting to database..."):
        connection_status = initialize_spreadsheet()
    
    if connection_status:
        st.success("✅ Connected to database successfully!", icon="✅")
    else:
        st.error("❌ Failed to connect to database. Please check your configuration.", icon="🚨")
        st.stop()
    
    st.title(f"📚 {APP_TITLE}")
    st.markdown("---")
    
    st.subheader("👨‍🎓 Select Your Department")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔧 Mechanical Engineering\n(NDT - Non-Destructive Testing)", use_container_width=True, type="primary"):
            st.session_state.selected_department = "Mechanical Engineering"
            st.session_state.course_name = "NDT - Non-Destructive Testing"
            st.session_state.page = "student_selection"
            st.rerun()
    
    with col2:
        if st.button("💻 Computer Science\n(20CS012 - Compiler Design)", use_container_width=True, type="primary"):
            st.session_state.selected_department = "Computer Science"
            st.session_state.course_name = "20CS012 - Principles of Compiler Design"
            st.session_state.page = "student_selection"
            st.rerun()

def render_student_selection_page():
    """Displays student selection interface."""
    st.set_page_config(page_title="Student Information", layout="centered", page_icon="📝")
    
    st.title("📝 Student Information")
    st.markdown(f"**Department:** {st.session_state.selected_department}")
    st.markdown(f"**Course:** {st.session_state.course_name}")
    
    if st.button("← Back to Department Selection", key="back_dept"):
        st.session_state.page = "department_selection"
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
    
    # Select appropriate question bank
    if st.session_state.selected_department == "Mechanical Engineering":
        question_bank = NDT_QUESTION_BANK
    else:
        question_bank = CSE_QUESTION_BANK
    
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
        st.title(f"{st.session_state.course_name}")
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
        # Determine sheet name based on department
        if st.session_state.selected_department == "Mechanical Engineering":
            sheet_name = "NDT_Quiz01"
        else:
            sheet_name = "CSE_Quiz01"
        
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
        
        department = st.selectbox("Select Department:", ["Mechanical Engineering (NDT)", "Computer Science (Compiler Design)"])
        
        if department == "Mechanical Engineering (NDT)":
            sheet_name = "NDT_Quiz01"
            dept_label = "Mechanical Engineering"
        else:
            sheet_name = "CSE_Quiz01"
            dept_label = "Computer Science"
        
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
        
        dept_qb = st.selectbox("Select Department:", ["Mechanical Engineering (NDT)", "Computer Science (Compiler Design)"], key="qb_dept")
        
        if dept_qb == "Mechanical Engineering (NDT)":
            selected_bank = NDT_QUESTION_BANK
            dept_name = "NDT"
        else:
            selected_bank = CSE_QUESTION_BANK
            dept_name = "Compiler Design"
        
        st.info(f"Total Questions: {len(selected_bank)}")
        
        # For NDT, show CO distribution
        if dept_name == "NDT":
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